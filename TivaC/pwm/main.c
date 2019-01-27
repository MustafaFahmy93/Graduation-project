#include "inc/hw_memmap.h"
#include "inc/hw_gpio.h"
#include "driverlib/gpio.h"
#include "driverlib/pin_map.h"
#include "driverlib/pwm.h"
#include "driverlib/sysctl.h"
#include "inc/hw_types.h"

void main(){

SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM1);

SysCtlPWMClockSet(SYSCTL_PWMDIV_1);

HWREG(GPIO_PORTF_BASE +GPIO_O_LOCK) = GPIO_LOCK_KEY;
HWREG(GPIO_PORTF_BASE +GPIO_O_CR)   |= 0x01;


GPIOPinConfigure(GPIO_PF0_M1PWM4);
GPIOPinConfigure(GPIO_PF1_M1PWM5);
GPIOPinConfigure(GPIO_PF2_M1PWM6);
GPIOPinConfigure(GPIO_PF3_M1PWM7);

GPIOPinTypePWM(GPIO_PORTF_BASE,GPIO_PIN_0 |GPIO_PIN_1 |GPIO_PIN_2 |GPIO_PIN_3);

PWMGenConfigure(PWM1_BASE, PWM_GEN_2, PWM_GEN_MODE_DOWN |PWM_GEN_MODE_NO_SYNC);
PWMGenConfigure(PWM1_BASE, PWM_GEN_3, PWM_GEN_MODE_DOWN |PWM_GEN_MODE_NO_SYNC);

PWMGenPeriodSet(PWM1_BASE, PWM_GEN_2, 400);
PWMGenPeriodSet(PWM1_BASE, PWM_GEN_3, 400);

PWMPulseWidthSet(PWM1_BASE, PWM_OUT_4, 300);
PWMPulseWidthSet(PWM1_BASE, PWM_OUT_5, 300);
PWMPulseWidthSet(PWM1_BASE, PWM_OUT_6, 300);
PWMPulseWidthSet(PWM1_BASE, PWM_OUT_7, 300);

PWMGenEnable(PWM1_BASE, PWM_GEN_2);
PWMGenEnable(PWM1_BASE, PWM_GEN_3);

//PWMOutputState(PWM1_BASE, (PWM_OUT_4_BIT | PWM_OUT_5_BIT | PWM_OUT_6_BIT |PWM_OUT_7_BIT  ), true);


while(1){


PWMPulseWidthSet(PWM1_BASE, PWM_OUT_4,300);
PWMPulseWidthSet(PWM1_BASE, PWM_OUT_5,300);
PWMPulseWidthSet(PWM1_BASE, PWM_OUT_6,300);
PWMPulseWidthSet(PWM1_BASE, PWM_OUT_7,300);

PWMOutputState(PWM1_BASE, (PWM_OUT_4_BIT | PWM_OUT_5_BIT | PWM_OUT_6_BIT |PWM_OUT_7_BIT  ), true);

SysCtlDelay(10000000);

PWMOutputState(PWM1_BASE, (PWM_OUT_4_BIT | PWM_OUT_5_BIT | PWM_OUT_6_BIT |PWM_OUT_7_BIT  ), false);

PWMPulseWidthSet(PWM1_BASE, PWM_OUT_4,100);
PWMPulseWidthSet(PWM1_BASE, PWM_OUT_5,100);
PWMPulseWidthSet(PWM1_BASE, PWM_OUT_6,100);
PWMPulseWidthSet(PWM1_BASE, PWM_OUT_7,100);

PWMOutputState(PWM1_BASE, (PWM_OUT_4_BIT | PWM_OUT_5_BIT | PWM_OUT_6_BIT |PWM_OUT_7_BIT  ), true);


SysCtlDelay(10000000);

PWMOutputState(PWM1_BASE, (PWM_OUT_4_BIT | PWM_OUT_5_BIT | PWM_OUT_6_BIT |PWM_OUT_7_BIT  ), false);


}
}
