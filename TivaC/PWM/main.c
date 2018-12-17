#include "stdint.h"
#include "C:\Keil\EE319Kware\inc\tm4c123gh6pm.h"
void SystemInit (){}
	
	void PortB_init()
{
	uint32_t delay; // dummy reg
	SYSCTL_RCGCGPIO_R |= 0x02; // 0000,0010 Port B => bit 1
		delay=1;
	GPIO_PORTB_DIR_R = 0xFF; //1111,1111 Direction (input=0,output=1)
	GPIO_PORTB_DEN_R = 0xFF;
	GPIO_PORTB_AMSEL_R = 0x00;
	GPIO_PORTB_AFSEL_R = 0xC0; //we want to use alternative functions
	GPIO_PORTB_PCTL_R &=~ 0x44000000; // we will use I/O
	GPIO_PORTB_PCTL_R |= 0x44000000; // we will use I/O

	SYSCTL_RCC_R=0x00100000;
	//SYSCTL_RCGC0_PWM0 = 0x00100000;
	SYSCTL_RCGCPWM_R=0x1;
	PWM0_CTL_R=0;
	PWM0_0_GENA_R=0x0000008C;
	PWM0_0_GENB_R=0x0000080C;
	PWM0_0_LOAD_R=0x0000018F;
	PWM0_0_CMPA_R=0x0000012B;
	PWM0_0_CMPB_R=0x00000063;
	PWM0_CTL_R=0x01;
	PWM0_ENABLE_R=0x00000003;
}


int main (void){
PortB_init();
	while(1)
	{
		
	}
	return 0;
}
