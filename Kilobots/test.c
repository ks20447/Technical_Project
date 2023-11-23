#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

int num_iteration = 0;
int tumble_rate = 20;

double calculate_probability() {  // Fixed the function declaration by adding ()
    double probability = 1 - exp(-((1.0 / tumble_rate) * num_iteration));  // Added missing () for the division

    return probability;
}

void kilobot_detect() {
    printf("Detecting neighbor messages, calculating anti-alignment, adjust trajectory \n");
}


void kilobot_run() {
    printf("Kilobot running for one time step \n");
}


void kilobot_tumble() {
    printf("Kilobot tumbles \n");
}


void loop() {

    kilobot_detect();

    kilobot_run();

    double probability = calculate_probability();

    double random_value = (double)rand() / RAND_MAX;  // Generate a random value between 0 and 1
    int result = (random_value < probability) ? 1 : 0;

    if (result == 1) {
        kilobot_tumble();
        num_iteration = 0;
    }

    num_iteration++;
}

int main() {
    srand(time(NULL));  // Seed the random number generator

    for (int i = 0; i < 10; i++) {
        loop();
    }
}

