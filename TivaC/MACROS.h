#ifndef MACROS_H_
#define MACROS_H_

#define set_bit(reg,index) reg = reg|(1<<index)
#define clear_bit(reg,index) reg = reg &=(~(1<<index))
#define toggle_bit(reg,index) reg ^= (1<<index)
#define read_bit(reg,index)   reg>>index &1 // for check

#endif