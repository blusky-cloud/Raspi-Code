 1 #include <iostream>
 2 #include <wiringPi.h>
 3 #include <csignal>
 4 
 5 // global flag used to exit from the main loop
 6 bool RUNNING = true;
 7 
 8 // Blink an LED
 9 void blink_led(int led, int time) {
10     digitalWrite(led, HIGH);
11     delay(time);
12     digitalWrite(led, LOW);
13     delay(time);
14 }
15 
16 // Callback handler if CTRL-C signal is detected
17 void my_handler(int s) {
18     std::cout << "Detected CTRL-C signal no. " << s << '\n';
19     RUNNING = false;
20 }
21 
22 int main() {
23     // Register a callback function to be called if the user presses CTRL-C
24     std::signal(SIGINT, my_handler);
25 
26     // Initialize wiringPi and allow the use of BCM pin numbering
27     wiringPiSetupGpio();
28 
29     std::cout << "Controlling the GPIO pins with wiringPi\n";
30 
31     // Define the 3 pins we are going to use
32     int red = 17, yellow = 22, green = 6;
33 
34     // Setup the pins
35     pinMode(red, OUTPUT);
36     pinMode(yellow, OUTPUT);
37     pinMode(green, OUTPUT);
38 
39     int time = 1000;   // interval at which a pin is turned HIGH/LOW
40     while(RUNNING) {
41         blink_led(red, time);
42         blink_led(yellow, time);
43         blink_led(green, time);
44     }
45 
46     std::cout << "Program ended ...\n";
47 }