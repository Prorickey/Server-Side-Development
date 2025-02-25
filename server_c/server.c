#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8080
#define BUFFER_SIZE 1024

void handle_client(int client_socket, char *index) {
    char buffer[BUFFER_SIZE];
    read(client_socket, buffer, BUFFER_SIZE - 1);

    printf("Client Request: %s\n", buffer);

    int curs = 0;
    char *method = malloc(10*sizeof(char));

    if(method == NULL) {
        perror("Failed to allocate memory");
        exit(EXIT_FAILURE);
    }

    for(int i = 0; i < 10; i++) {
        if(buffer[i] == ' ') {
            curs = i+1;
            break;
        }
        method[i] = buffer[i];
    }

    char *route = malloc(2048*sizeof(char));

    if(route == NULL) {
        free(method);
        perror("Failed to allocate memory");
        exit(EXIT_FAILURE);
    }

    for(int i = curs; i < curs+2048; i++) {
        if(buffer[i] == ' ') {
            curs += i+1;
            break;
        }
        route[i-curs] = buffer[i];
    }

    printf("Method: %s\nRoute: %s\n", method, route);

    free(route);
    free(method);

    char response[BUFFER_SIZE + strlen(index) + 1];
    strcpy(response, "HTTP/1.1 200 OK\r\n"
                     "Content-Type: text/html\r\n"
                     "Connection: close\r\n"
                     "\r\n");

    strcat(response, index);

    write(client_socket, response, strlen(response));
    close(client_socket);
}

int main() {
    printf("Starting server...\n");

    int server_socket, client_socket;
    struct sockaddr_in server_addr, client_addr;
    socklen_t addr_len = sizeof(client_addr);

    if((server_socket = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("Socket failed");
        exit(EXIT_FAILURE);
    }

    int opt = 1;
    if (setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) == -1) {
        perror("Failed to set socket options");
        close(server_socket);
        return EXIT_FAILURE;
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    if (bind(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Bind failed");
        close(server_socket);
        exit(EXIT_FAILURE);
    }

    if (listen(server_socket, 3) < 0) {
        perror("Listen failed");
        close(server_socket);
        exit(EXIT_FAILURE);
    }

    FILE *findex;
    findex = fopen("index.html", "r");

    fseek(findex, 0L, SEEK_END);
    int sz = ftell(findex);
    fseek(findex, 0L, SEEK_SET);

    char index[sz];
    fread(index, sizeof(char), sz, findex);
    index[sz] = '\0';

    fclose(findex);

    printf("Server is listening on port %d\n", PORT);

    while (1) {
        if ((client_socket = accept(server_socket, (struct sockaddr *)&client_addr, &addr_len)) < 0) {
            perror("Accept failed");
            close(server_socket);
            exit(EXIT_FAILURE);
        }

        handle_client(client_socket, index);
    }

    return 0;
}