#include "Init.h"
//======================================================== Port A ========================================================
void PortA_init()
{
	uint32_t delay; // dummy reg
	SYSCTL_RCGCGPIO_R |= 0x01; // 0000,0001 Port A => bit 0
	delay=1;
	//while((SYSCTL_PRGPIO_R&0x00000001)==0 ||(read_bit(SYSCTL_RCGCGPIO_R,1))==0 ){};
	GPIO_PORTA_DIR_R |= 0xF8; //1111,10XX Direction (input=0,output=1) (A3 => trig, A2 => echo)
	GPIO_PORTA_AFSEL_R = 0x00; //we didn't want to use alternative functions
	GPIO_PORTA_PCTL_R = 0x00000000; // we will use I/O
	GPIO_PORTA_DEN_R = 0xFF;
	GPIO_PORTA_AMSEL_R = 0x00;

}
//======================================================== Port B ========================================================
void PortB_init()
{
	uint32_t delay; // dummy reg
	SYSCTL_RCGCGPIO_R |= 0x02; // 0000,0010 Port B => bit 1
		delay=1;
	GPIO_PORTB_DIR_R = 0xFF; //1111,1111 Direction (input=0,output=1)
	GPIO_PORTB_AFSEL_R = 0x00; //we didn't want to use alternative functions
	GPIO_PORTB_PCTL_R = 0x00000000; // we will use I/O
	GPIO_PORTB_DEN_R = 0xFF;
	GPIO_PORTB_AMSEL_R = 0x00;
}
//======================================================== Port F ========================================================
void PortF_init()
{
	uint32_t delay; // dummy reg
	SYSCTL_RCGCGPIO_R |= 0x20; // 0010,0000 Port F => bit 5
	delay=1;
	GPIO_PORTF_DIR_R=0x0E; // 0000,1110 Direction (input=0,output=1)
	GPIO_PORTF_AFSEL_R=0; // Alternate pin
	GPIO_PORTF_PUR_R=0x11; // pull-up register for two switchs (Vcc_or_GND)
	GPIO_PORTF_DEN_R =0x1F; // Digital Enable (5 bits)
	GPIO_PORTF_AMSEL_R=0; // analog
	GPIO_PORTF_LOCK_R =0x4C4F434B; // 0x4C4F434B (mask from data sheet)
	GPIO_PORTF_CR_R=0x1F;
	GPIO_PORTF_PCTL_R=0;

}
//======================================================== SysTick ========================================================
void timer(u8 enable)
{
	if(enable)
	{
		NVIC_ST_CTRL_R = 0;// clear countFlag
	  NVIC_ST_RELOAD_R = 376471-1; // 
	  NVIC_ST_CURRENT_R =0;
	  NVIC_ST_CTRL_R = 0x5; // enable and clk source bits 0,2
	}else
	{
		NVIC_ST_RELOAD_R = 0;
		NVIC_ST_CURRENT_R = 0;
		NVIC_ST_CTRL_R = 0;
	}
	
}
void delay_us(u32 us)
{
	unsigned no_counts ;
	//no_counts = (us*80) ; // no_counts = (16M hz * delay uSec) / 1 sec 
	no_counts = (us*1000)/62.5 ; // or us * clock frequency
	NVIC_ST_CTRL_R = 0;
	NVIC_ST_RELOAD_R = no_counts - 1 ;
	NVIC_ST_CURRENT_R = 0;
	NVIC_ST_CTRL_R = 0x5; // enable and clk source bits 0,2
	while((read_bit(NVIC_ST_CTRL_R,16))==0){}; // wait 
	//Systic Timer is periodic so i didn't need him again after delay
	NVIC_ST_CTRL_R = 0;
}
void delay_ms(u32 ms)
{
	unsigned no_counts ;
	no_counts = (ms*1000000)/62.5 ; // or us * clock frequency
	NVIC_ST_CTRL_R = 0;
	NVIC_ST_RELOAD_R = no_counts - 1 ;
	NVIC_ST_CURRENT_R = 0;
	NVIC_ST_CTRL_R = 0x5; // enable and clk source bits 0,2
	while((read_bit(NVIC_ST_CTRL_R,16))==0){}; // wait 
	//Systic Timer is periodic so i didn't need him again after delay
	NVIC_ST_CTRL_R = 0;
}
void delay_s(u32 s)
{
	int i;
	for(i=0;i<(100*s);i++)
	{
		delay_ms(10);
	}
}

//======================================================== 7 seg ========================================================
void display(u8 hundreds ,u8 tens ,u8 units)
{
			GPIO_PORTA_DATA_R &= 0x0F; // 0000xxxx
			GPIO_PORTA_DATA_R |= (hundreds<<4);
			GPIO_PORTB_DATA_R =0	;
			GPIO_PORTB_DATA_R |= (units<<4)+ tens;				
}

