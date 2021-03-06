#include "hwlib.hpp"

extern "C" void print_int( int c ){
   hwlib::cout << c << "\n";
}

extern "C" int cave_unit1();
extern "C" int cave_unit2();
extern "C" int cave_unit3();
extern "C" int cave_unit4();
extern "C" int cave_unit5();
extern "C" int cave_unit6();
extern "C" int cave_unit7();
extern "C" int cave_unit8();
extern "C" int cave_unit9();
extern "C" int cave_unit10();
extern "C" int cave_unit11();
extern "C" int cave_unit12();
extern "C" int cave_unit13();
extern "C" int cave_unit14();
extern "C" int cave_unit15();
extern "C" int cave_unit16();
extern "C" int cave_unit17();
extern "C" int cave_unit18();
extern "C" int cave_unit19();


int main(void){

   hwlib::wait_ms(2000);
   hwlib::cout << "Program started\n";
   hwlib::cout << "Unit1: " << "odd(1) = true/1" << "\n";
   hwlib::cout << cave_unit1() << "\n\n";
   hwlib::cout << "Unit2: " << "odd(127) = true/1" << "\n";
   hwlib::cout << cave_unit2() << "\n\n";
   hwlib::cout << "Unit3: " << "odd(21) = true/1" << "\n";
   hwlib::cout << cave_unit3() << "\n\n";
   hwlib::cout << "Unit4: " << "odd(20) = false/0" << "\n";
   hwlib::cout << cave_unit4() << "\n\n";
   hwlib::cout << "Unit5: " << "even(1) = false/0" << "\n";
   hwlib::cout << cave_unit5() << "\n\n";
   hwlib::cout << "Unit6: " << "even(127) = false/0" << "\n";
   hwlib::cout << cave_unit6() << "\n\n";
   hwlib::cout << "Unit7: " << "even(21) = false/0" << "\n";
   hwlib::cout << cave_unit7() << "\n\n";
   hwlib::cout << "Unit8: " << "even(20) = true/1" << "\n";
   hwlib::cout << cave_unit8() << "\n\n";
   hwlib::cout << "Unit9: " << "even(2) = true/1" << "\n";
   hwlib::cout << cave_unit9() << "\n\n";
   hwlib::cout << "Unit10: " << "odd(0) = idk" << "\n";
   hwlib::cout << cave_unit10() << "\n\n";
   hwlib::cout << "Unit11: " << "even(0) = idk" << "\n";
   hwlib::cout << cave_unit11() << "\n\n";
   hwlib::cout << "Unit12: " << "sommig(5) = 15" << "\n";
   hwlib::cout << cave_unit12() << "\n\n";
   hwlib::cout << "Unit13: " << "sommig(1) = 1" << "\n";
   hwlib::cout << cave_unit13() << "\n\n";
   hwlib::cout << "Unit14: " << "1 + 2 = 3" << "\n";
   hwlib::cout << cave_unit14() << "\n\n";
   hwlib::cout << "Unit15: " << "1 + 127 = 128" << "\n";
   hwlib::cout << cave_unit15() << "\n\n";
   hwlib::cout << "Unit16: " << "1 - 1 = 0" << "\n";
   hwlib::cout << cave_unit16() << "\n\n";
   hwlib::cout << "Unit17: " << "1 - 2 = -1" << "\n";
   hwlib::cout << cave_unit17() << "\n\n";
   hwlib::cout << "Unit18: " << "1 * 3 = 3" << "\n";
   hwlib::cout << cave_unit18() << "\n\n";
   hwlib::cout << "Unit19: " << "3 * 3 = 9" << "\n";
   hwlib::cout << cave_unit19() << "\n\n";
   
}