// File name: proj.c
// System Programming Project

#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
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

void ls_file(int client_fd, int port)
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

    fprintf(fp, "<html><head><title>%s</title></head></body>", cwd);
    fprintf(fp, "<h3>");
    fprintf(fp, "System Programming & Cloud Computing Project");
    fprintf(fp, "</h3><br>");

    dirp = opendir(cwd);
    if(dirp != NULL)
    {
        fprintf(fp, "<br>Directroy Path: %s</br>", cwd);
        while((dir = readdir(dirp)) != NULL)
        {
            if(strcmp(dir->d_name, ".") == 0)   continue;
            if(strcmp(dir->d_name, "..") == 0)  continue;
            fprintf(fp, "<br>");
            fprintf(fp, "%s", dir->d_name);
            fprintf(fp, "</br>");
        }
    }

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

        time(&rawtime);
        timeinfo = localtime(&rawtime);
        time_char = asctime(timeinfo);
        time_char[strlen(time_char) - 1] = 0;

        printf("New client accessed\n");
        printf("Time: [%s]\n", time_char);
        printf("Client IP: %s, Port: %d\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));

        ls_file(client_fd, client_addr.sin_port);
        sprintf(response_header, "HTTP/1.0 200 OK\r\n"
        "Server: web server"
        "Content-length:%d\r\n"
        "Content=type:text/html\r\n\r\n", (int)strlen(response_header));
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
        time(&rawtime);
        free(response_message);
        timeinfo = localtime(&rawtime);
        time_char = asctime(timeinfo);
        time_char[strlen(time_char) - 1] = 0;
        printf("Disconnect client\n");
        printf("Time: [%s]\n", time_char);
        printf("Client IP: %s, Port: %d\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));
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