#ifndef INIT_H__
#define INIT_H__
#include <stdint.h>
#include "tm4c123gh6pm.h"
#include "MACROS.h"
#include "Data_Types.h"




/*void PortA_init(void);
void PortB_init(void);
void PortF_init(void);
void timer(u8 enable);
void delay(u32 count);
void delay_us(u32 us);
void delay_ms(u32 ms);*/
//
void PortA_init();
void PortB_init();
void PortF_init();

void timer(u8 enable);
void delay(u32 count);
void delay_us(u32 us);
void delay_ms(u32 ms);
void display(u8 hundreds ,u8 tens ,u8 units);
void delay_s(u32 ms);
	
#endif