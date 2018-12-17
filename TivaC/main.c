#include <stdint.h>
#include <stdbool.h>
#include "tm4c123gh6pm.h"
#include "Data_Types.h"
#include "sysctl.h"
void SystemInit(){}	

void PortA_init();
void delay_us(u32 us);
void move_forward(uint32_t duration);
void move_backward(uint32_t d);
void move_right(uint32_t d);
void move_left(uint32_t d);


int main()
{

	move_forward(1000);
	move_backward(1000);
	move_right(1000);
	move_left(1000);
	
while(1)
{	
	/*
	move_forward(d);
	move_backward(d);
	move_right(d);
	move_left(d);
	*/
}

}
void PortA_init()
{
	uint32_t delay; // dummy reg
	SYSCTL_RCGCGPIO_R |= 0x01; // 0000,0001 Port A => bit 0
	delay = 1;
	//while((SYSCTL_PRGPIO_R&0x00000001)==0 ||(read_bit(SYSCTL_RCGCGPIO_R,1))==0 ){};
	GPIO_PORTA_DIR_R |= 0xF8; //1111,10XX Direction (input=0,output=1) (A3 => trig, A2 => echo)
	GPIO_PORTA_AFSEL_R = 0x00; //we didn't want to use alternative functions
	GPIO_PORTA_PCTL_R = 0x00000000; // we will use I/O
	GPIO_PORTA_DEN_R = 0xFF;
	GPIO_PORTA_AMSEL_R = 0x00;

}
void delay_us(u32 us)
{
	unsigned no_counts;
	//no_counts = (us*80) ; // no_counts = (16M hz * delay uSec) / 1 sec 
	no_counts = (us * 1000) / 62.5; // or us * clock frequency
	NVIC_ST_CTRL_R = 0;
	NVIC_ST_RELOAD_R = no_counts - 1;
	NVIC_ST_CURRENT_R = 0;
	NVIC_ST_CTRL_R = 0x5; // enable and clk source bits 0,2
	while ((read_bit(NVIC_ST_CTRL_R, 16)) == 0) {}; // wait 
													//Systic Timer is periodic so i didn't need him again after delay
	NVIC_ST_CTRL_R = 0;
}
/*
forward=>A2=1 & A3=0
backward=>A3=1 & A2=0
right=>A4=1 & A5=0
left=>A5=1 & A4=0
break=> A2=A3=A4=A5=0
*/
void move_forward(uint32_t duration)//A2=1 & A3=0
{
	PortA_init();
	clear_bit(GPIO_PORTA_DATA_R, 3);
	set_bit(GPIO_PORTA_DATA_R, 2);
	//delay duration
	delay_ms(duration);
	//clear A2
	clear_bit(GPIO_PORTA_DATA_R, 2);

}
void move_backward(uint32_t d)//A3=1 & A2=0
{
	PortA_init();
	clear_bit(GPIO_PORTA_DATA_R, 2);
	set_bit(GPIO_PORTA_DATA_R, 3);
	//delay d
	delay_ms(d);
	//clear A3
	clear_bit(GPIO_PORTA_DATA_R, 3);
}
void move_right(uint32_t d)//A4=1 & A5=0
{
	PortA_init();
	clear_bit(GPIO_PORTA_DATA_R, 5);
	set_bit(GPIO_PORTA_DATA_R, 4);
	//delay d
	delay_ms(d);
	//clear A4
	clear_bit(GPIO_PORTA_DATA_R, 4);
}
void move_left(uint32_t d)//A5=1 & A4=0
{
	PortA_init();
	clear_bit(GPIO_PORTA_DATA_R, 4);
	set_bit(GPIO_PORTA_DATA_R, 5);
	//delay d
	delay_ms(d);
	//clear A5
	clear_bit(GPIO_PORTA_DATA_R, 5);
}
