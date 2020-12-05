// File name: proj.c
// System Programming Project

#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <time.h>
#include <stdlib.h>
#include <dirent.h>
#include <sys/stat.h>
#include <fcntl.h>


#define PORTNUM 9000
#define HTML_FILE_NAME "proj.html"

void slice_cura(char *file_name)
{
    char route[500] = "./stl";
    char result[500] = "./output/";
    char file_temp[500] = { '\0', };
    char *result_temp;

    strcpy(file_temp, file_name);
    result_temp = strtok(file_temp, "/");
    result_temp = strtok(NULL, "/");
    result_temp = strtok(NULL, "/");
    strcat(route, file_name);
    strcat(result, result_temp);
    strcat(result, ".gcode");
    execl("../CuraEngine/build/CuraEngine", " ", "slice", "-j", "./fdmprinter.def.json", "-o", result, "-l", file_name, (char *)0);
}


void slice_stl(char *req_uri, int client_fd)
{
    char file_name[300] = "./stl";
    char result_name[300] = "./output";
    char *file_buf, *temp;
    char response_header[1024] = { '\0', };
    int size_count = 0;
    FILE *fp;
    struct stat statbuf;
    pid_t pid = 1;
    

    strcat(file_name, req_uri);
    strcat(result_name, req_uri);
    strcat(result_name, ".gcode");
    if(access(file_name, F_OK | R_OK) == 0)
    {
        printf("system can access to %s\n", file_name);
        
        pid = fork();

        if(pid == 0)
        {
            close(client_fd);
            slice_cura(file_name);
        }
        else if(pid < 0)
        {
            perror("fork");
            exit(1);
        }
        else
        {
            pid_t child_pid = wait(NULL);

            if(access(result_name, F_OK | R_OK) == -1)
            {
                perror("can't access to file");
                close(client_fd);
            }
            else
            {
                fp = fopen(result_name, "r");
                stat(result_name, &statbuf);
                // fp = fopen("./output/test.txt", "r");
                // stat("./output/test.txt", &statbuf);

                temp = malloc(sizeof(char) * (500 + statbuf.st_size));

                file_buf = malloc(sizeof(char) * (statbuf.st_size + 1));

                memset(file_buf, '\0', statbuf.st_size);

                fread(file_buf, statbuf.st_size, 1, fp);

                sprintf(temp, "HTTP/1.0 200 OK\r\n"
                    "Content-type: text/plain\r\n"
                    "Server: web server\r\n"
                    "Content-length:%d\r\n"
                    "Content-Disposition: attachment; filename=\"%s\"\r\n\r\n", (int)strlen(file_buf), result_name);

                sleep(1);

                // strcat(temp, file_buf);

                // send header + text messages
                write(client_fd, temp, strlen(temp));
                write(client_fd, file_buf, strlen(file_buf));

                unlink(result_name);
                close(client_fd);
                free(file_buf);
                free(temp);   
            }
        }
    }
    else
    {
        printf("404 ERROR\n");
        temp = malloc(92 + strlen(req_uri));

        sprintf(temp, "<html><head>404 Error</head><body><h1>404 ERROR!!</h1><h2>Can't find \"%s\"</h2></body></html>", req_uri);

        sprintf(response_header, "HTTP/1.0 200 OK\r\n"
            "Server: web server\r\n"
            "Content-length:%d\r\n"
            "Content-type:text/html\r\n\r\n", (int)strlen(temp));
        
        write(client_fd, response_header, strlen(response_header));
        write(client_fd, temp, strlen(temp));

        free(temp);
        close(client_fd);
    }
}
void ls_file(int client_fd, int port, char *req_address, char *req_method)
{
    char response_header[1024] = { 0, };
    FILE *fp = fopen(HTML_FILE_NAME, "w");
    char cwd[256] = { 0, };
    DIR *dirp = NULL;
    struct dirent *dir = NULL;

    if(fp == 0)
    {
        printf("Error occured while opening file %s\n", HTML_FILE_NAME);
        exit(1);
    }

    getcwd(cwd, sizeof(cwd));
    strcat(cwd, "/stl");

    fprintf(fp, "<html><head><title>%s</title></head>", cwd);
    fprintf(fp, "<body>");
    fprintf(fp, "<h3>");
    fprintf(fp, "System Programming & Cloud Computing Project");
    fprintf(fp, "</h3>");


    dirp = opendir(cwd);
    if(dirp != NULL)
    {
        fprintf(fp, "<br>Directroy Path: %s</br>", cwd);
        fprintf(fp, "<table border=\"1\"> <tr><th>STL List</th></tr>");
        while((dir = readdir(dirp)) != NULL)
        {
            if(strcmp(dir->d_name, ".") == 0)   continue;
            if(strcmp(dir->d_name, "..") == 0)  continue;
            fprintf(fp, "<tr><th><a href=\"http://%s/%s\">", req_address, dir->d_name);
            fprintf(fp, "%s", dir->d_name);
            fprintf(fp, "</a>");
            fprintf(fp, "</th></tr>");
        }
        fprintf(fp, "</table>");
    }

    fprintf(fp, "</body>");

    fclose(fp);
}
void inet_main(int socket_fd)
{
    time_t rawtime;
    struct tm *timeinfo;
    char *time_char;
    char response_header[1024];
    char *response_message;
    char req[1024];
    char req_method[5];
    char req_address[20];
    char req_uri[50];
    char *req_temp;
    struct sockaddr_in server_addr, client_addr;
    int cli_size = sizeof(client_addr);
    int client_fd;
    int response_fd;
    int response_size;

    while(1)
    {
        if((client_fd = accept(socket_fd, (struct sockaddr *)&client_addr, &cli_size)) == -1)
        {
            printf("Error occured on accept\n");
            exit(1);
        }

        read(client_fd, req, sizeof(req));
        req_temp = strtok(req, " ");
        strcpy(req_method, req_temp);
        req_temp = strtok(NULL, " ");
        strcpy(req_uri, req_temp);
        req_temp = strtok(NULL, "\n");
        req_temp = strtok(NULL, " ");
        req_temp = strtok(NULL, "\n");
        strcpy(req_address, req_temp);
        req_temp = strtok(NULL, "\n");
        // printf("request header: %s\n", req_method);
        // printf("request address: %s\n", req_address);
        // printf("request uri: %s\n", req_uri);

        time(&rawtime);
        timeinfo = localtime(&rawtime);
        time_char = asctime(timeinfo);
        time_char[strlen(time_char) - 1] = 0;

        printf("New client accessed\n");
        printf("Time: [%s]\n", time_char);
        printf("Client IP: %s, Port: %d\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));

        if(strcmp(req_uri, "/") == 0)
        {
            printf("Client IP %s accessed to ls_file\n", inet_ntoa(client_addr.sin_addr));
            ls_file(client_fd, client_addr.sin_port, req_address, req_method);

            sprintf(response_header, "HTTP/1.0 200 OK\r\n"
                "Server: web server"
                "Content-length:%d\r\n"
                "Content-type:text/html\r\n\r\n", (int)strlen(response_header));
            response_fd = open(HTML_FILE_NAME, O_RDONLY);
            response_size = lseek(response_fd, 0, SEEK_END);
            lseek(response_fd, 0, SEEK_SET);
            response_message = malloc(response_size * sizeof(char));
            read(response_fd, response_message, response_size);
            response_message[response_size] = 0;
            close(response_fd);

            write(client_fd, response_header, strlen(response_header));
            write(client_fd, response_message, response_size);

            close(client_fd);
            free(response_message);
        }
        else if(strcmp(req_uri, "/favicon.ico") == 0)
        {
            printf("continue.....\n");
            close(client_fd);
            continue;
        }
        else if(strcmp(req_uri, "/v1/version") == 0)
        {
            response_message = malloc(30);
            
            sprintf(response_message, "{message: \"Version 1.0.0\"}");
            sprintf(response_header, "HTTP/1.0 200 OK\r\n"
            "Server: web server\r\n"
            "Content-length: %d\r\n"
            "Content-type: text/html\r\n\r\n", (int)strlen(response_message));

            write(client_fd, response_header, strlen(response_header));
            write(client_fd, response_message, strlen(response_message));

            close(client_fd);
            free(response_message);
        }
        else
        {
            slice_stl(req_uri, client_fd);
        }
        

        
        time(&rawtime);
        timeinfo = localtime(&rawtime);
        time_char = asctime(timeinfo);
        time_char[strlen(time_char) - 1] = 0;
    }
}


int main(int argc, char *argv[])
{
    int socket_fd, client_fd, sockopt;
    time_t rawtime;
    struct tm *timeinfo;
    char *time_char;
    struct sockaddr_in server_addr, client_addr;
    int cli_size = sizeof(client_addr);

    time(&rawtime);
    timeinfo = localtime(&rawtime);
    time_char = asctime(timeinfo);
    time_char[strlen(time_char) - 1] = 0;

    printf("///////////////////////////////////\n");
    printf("[%s] Server starting....\n", time_char);
    printf("///////////////////////////////////\n");

    if((socket_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        printf("Socket opening failed\n");
        exit(1);
    }

    memset((char *)&server_addr, '\0', sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORTNUM);
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);

    sockopt = 1;
    setsockopt(socket_fd, SOL_SOCKET, SO_REUSEADDR, &sockopt, sizeof(sockopt));

    if(bind(socket_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1)
    {
        printf("Error occured on binding\n");
        exit(1);
    }
    listen(socket_fd, 2);

    inet_main(socket_fd);

    return 0;
}