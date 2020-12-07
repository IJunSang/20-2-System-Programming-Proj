FROM mjnhb2001/cura_engine:latest

WORKDIR /20-2-System-Programming-Proj

RUN mkdir project

COPY ./fdmprinter.def.json /20-2-System-Programming-Proj/project
COPY ./fdmextruder.def.json /20-2-System-Programming-Proj/project
COPY ./proj.c /20-2-System-Programming-Proj/project

WORKDIR /20-2-System-Programming-Proj/project

RUN gcc -o proj proj.c

RUN mkdir stl
RUN mkdir output

WORKDIR /20-2-System-Programming-Proj/project/stl

COPY ./stl /20-2-System-Programming-Proj/project/stl

WORKDIR /20-2-System-Programming-Proj/project

ENTRYPOINT [ "./proj" ]