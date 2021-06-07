#include<xc.h>           // processor SFR definitions
#include<sys/attribs.h>  // __ISR macro
#include<stdio.h>        // lib with sprintf and sscanf

// DEVCFG0
#pragma config DEBUG = OFF // disable debugging
#pragma config JTAGEN = OFF // disable jtag
#pragma config ICESEL = ICS_PGx1 // use PGED1 and PGEC1
#pragma config PWP = OFF // disable flash write protect
#pragma config BWP = OFF // disable boot write protect
#pragma config CP = OFF // disable code protect

// DEVCFG1
#pragma config FNOSC = FRCPLL // use internal oscillator with pll
#pragma config FSOSCEN = OFF // disable secondary oscillator
#pragma config IESO = OFF // disable switching clocks
#pragma config POSCMOD = OFF // internal RC
#pragma config OSCIOFNC = OFF // disable clock output
#pragma config FPBDIV = DIV_1 // divide sysclk freq by 1 for peripheral bus clock
#pragma config FCKSM = CSDCMD // disable clock switch and FSCM
#pragma config WDTPS = PS1048576 // use largest wdt
#pragma config WINDIS = OFF // use non-window mode wdt
#pragma config FWDTEN = OFF // wdt disabled
#pragma config FWDTWINSZ = WINSZ_25 // wdt window at 25%

// DEVCFG2 - get the sysclk clock to 48MHz from the 8MHz crystal
#pragma config FPLLIDIV = DIV_2 // divide input clock to be in range 4-5MHz
#pragma config FPLLMUL = MUL_24 // multiply clock after FPLLIDIV
#pragma config FPLLODIV = DIV_2 // divide clock after FPLLMUL to get 48MHz

// DEVCFG3
#pragma config USERID = 0 // some 16bit userid, doesn't matter what
#pragma config PMDL1WAY = OFF // allow multiple reconfigurations
#pragma config IOL1WAY = OFF // allow multiple reconfigurations

// Function Prototypes
void ReadUART1(char * string, int maxLength);
void WriteUART1(const char * string);
char m[100];

int main() {

    __builtin_disable_interrupts(); // disable interrupts while initializing things

    // set the CP0 CONFIG register to indicate that kseg0 is cacheable (0x3)
    __builtin_mtc0(_CP0_CONFIG, _CP0_CONFIG_SELECT, 0xa4210583);

    // 0 data RAM access wait states
    BMXCONbits.BMXWSDRM = 0x0;

    // enable multi vector interrupts
    INTCONbits.MVEC = 0x1;

    // disable JTAG to get pins back
    DDPCONbits.JTAGEN = 0;
    
    // Use TRIS and LAT commands to just do regular digital IO
    // A4 is output
    TRISAbits.TRISA4 = 0; 
    
    // A4 is low
    LATAbits.LATA4 = 0;
    
    // B4 is input
    TRISBbits.TRISB4 = 1;
    
    // Now use the reprogrammable SFRs to communicate with UART (pins 15&16)
    U1RXRbits.U1RXR = 0b0001; // U1RX is B6 (@ pin... 15?)
    RPB7Rbits.RPB7R = 0b0001; // U1TX is B7
    
    // Insert code from NU32 startup to configure UART
    // call SFRs that will enable us to use UART (from NU32.c)
    // turn on UART1 without an interrupt
    U1MODEbits.BRGH = 0; // set baud to NU32_DESIRED_BAUD
    U1BRG = ((48000000 / 115200) / 16) - 1;
    
    // 8 bit, no parity bit, and 1 stop bit (8N1 setup)
    U1MODEbits.PDSEL = 0;
    U1MODEbits.STSEL = 0;
    
    // configure TX & RX pins as output & input pins
    U1STAbits.UTXEN = 1;
    U1STAbits.URXEN = 1;
    
    // enable the uart
    U1MODEbits.ON = 1;
    
    __builtin_enable_interrupts();

    while (1) {
        
        if (PORTBbits.RB4 == 0){
            int i;
            for (i = 0; i<4; i++){                  // run this block 4 times
                LATAINV = 0b10000;                  // toggle pin A4
                _CP0_SET_COUNT(0);                  // set sys clk to 0
                
                while(_CP0_GET_COUNT() < 0.5 * 24000000){;}  // delay 
            }
            sprintf(m, "Hello!\r\n");
            WriteUART1(m);
        }
    }
}


// Read from UART1
// block other functions until you get a '\r' or '\n'
// send the pointer to your char array and the number of elements in the array
void ReadUART1(char * message, int maxLength) { // take pointer to a char array, max # things in array
  char data = 0;
  int complete = 0, num_bytes = 0;
  // loop until you get a '\r' or '\n'
  while (!complete) {
    if (U1STAbits.URXDA) { // if data is available
      data = U1RXREG;      // read the data
      if ((data == '\n') || (data == '\r')) {
        complete = 1; // done
      } else {
        message[num_bytes] = data; // if not \r or \n put into array
        ++num_bytes;
        // roll over if the array is too small
        if (num_bytes >= maxLength) { // dont overwrite the length of buffer
          num_bytes = 0;
        }
      }
    }
  }
  // end the string
  message[num_bytes] = '\0'; // add null char at end so scanf can work on char array
}

// Write a character array using UART1
void WriteUART1(const char * string) { // take a pointer to a character array- letters generated using sprintf
  while (*string != '\0') { // the array ends in the null character 
    while (U1STAbits.UTXBF) { // wait till previous element is sent out 
      ; // wait until tx buffer isn't full (when buffer is empty we can put something else in)
    }
    U1TXREG = *string; // put in UTX register, as soon as put in register pic blinks it out using 1s and 0s tp other device
    ++string;
  }
}