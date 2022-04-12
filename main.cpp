#include "hwlib.hpp"

extern "C" void print_int( int c ){
   hwlib::cout << c << "\n";
}

extern "C" int cave_main();

int main(void){

   hwlib::wait_ms(2000);
   hwlib::cout << "Program started\n";
   hwlib::cout << cave_main();
   
}