#include <stdint.h>
#include <stdlib.h>
#include <math.h>
#include "murax.h"

#define QUEUE_SIZE 55
#define MAX_STRING_SIZE 128

typedef struct{
    char buffer[MAX_STRING_SIZE];
}Request;

typedef struct{
    Request entries[QUEUE_SIZE];
    uint32_t count;
    uint32_t head;
    uint32_t tail;
    uint32_t read;
}RequestQueue;

void init_queue(RequestQueue* queue){
    queue->count = 0;
    queue->head = 0;
    queue->tail = 0;
    queue->read = 0;
}

uint32_t queue_full(RequestQueue* queue){
    return queue->count == QUEUE_SIZE;
}

void enqueue(RequestQueue* queue, char* data){
    if (queue_full(queue)){
        queue->head = (queue->head+1)%QUEUE_SIZE;
        queue->count--;
    }
    uint32_t i=0;
    
    while(1){
        if (data[i] == '\0'){
            break;
        }
        
        queue->entries[queue->tail].buffer[i] = data[i];
        i++;
        
    }
    queue->entries[queue->tail].buffer[i] = '\0';
    queue->tail = (queue->tail + 1) % QUEUE_SIZE;
    queue->count++;
}

char* read(Uart_Reg* reg,RequestQueue* queue){
    static char ch[MAX_STRING_SIZE];
    uint32_t i=0;
    while(1){
        if (queue->entries[queue->read].buffer[i] == '\0' || queue->entries[queue->read].buffer[i] == '\n'){
            break;
        }
        
        ch[i] = queue->entries[queue->read].buffer[i];
        i++;
        
        
    }
    
    ch[i] = '\0';
    queue->read = (queue->read +1) % QUEUE_SIZE;

    return ch;
    
}

void uart_read_string(Uart_Reg *reg,RequestQueue* queue) {
    char buffer[MAX_STRING_SIZE]; // Adjust buffer size as needed
    uint32_t index = 0;

    while (1) {
        while (uart_readOccupancy(reg) == 0);
        char c = uart_read(reg);

        if (c == '\r' || c == '\n') {
            break;
        }

        buffer[index++] = c;
        if (index >= MAX_STRING_SIZE) {
            break; // Prevent buffer overflow
        }
    }

    buffer[index] = '\0'; // Null-terminate the string
    enqueue(queue,buffer);

}