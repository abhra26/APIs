//#include "stddefs.h"
#include <stdint.h>
#include <stdlib.h>
#include <math.h>
#include "murax.h"
#include "queue.h"

#define QUEUE_SIZE 55
#define MAX_STRING_SIZE 128

void helpCMD(){
    println("============================ HSM CLASS HELP ============================");
    println("The HSM is a critical component of our end-to-end quantum-resilient banking."); 
    println("It provides secure key management, cryptographic acceleration,"); 
    println("and ensures that sensitive data and cryptographic keys are never exposed"); 
    println("the module. Below are the key features, usage instructions, and"); 
    println("available methods for interacting with the HSM.");
}

void CNTRL(Uart_Reg* reg, char* data){
    if (data[0] == 'h' || data[0] == 'H'){
        helpCMD();
    }

    else{
        println(data);
    }
}

void print(const char*str){
	while(*str){
		uart_write(UART,*str);
		str++;
	}
}
void println(const char*str){
	print(str);
	uart_write(UART,'\n');
}

uint32_t uart_read_uint32(Uart_Reg *reg) {
    uint32_t value = 0;
    for (uint32_t i = 0; i < 4; i++) {
        while (uart_readOccupancy(reg) == 0);
        value |= uart_read(reg) << (i * 8);
    }
    return value;
}

void delay(uint32_t loops){
	for(uint32_t i=0;i<loops;i++){
		uint32_t tmp = GPIO_A->OUTPUT;
	}
}

void main() {
    GPIO_A->OUTPUT_ENABLE = 0x0000000F;
	GPIO_A->OUTPUT = 0x00000001;
	const uint32_t nloops = 2000000;
    RequestQueue queue;
    init_queue(&queue);
    
	while(1) {
        uart_read_string(UART,&queue);
        char* data = read(UART,&queue);
        CNTRL(UART,data);
        
        
	}

}

void irqCallback(){

}
