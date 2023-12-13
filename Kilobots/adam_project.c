#include "kilolib.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

typedef enum {
    STOP = 0,
    FORWARD = 1,
    LEFT = 2,
    RIGHT = 3
} motion_t;

int new_message = 0;
int kilo_full_power = 100;
// Estimated time taken for one full rotation at full power
int turn_time = 10000;
int neighbour_id = 0;
int neighbors[20] = {0};
int tumble_rate = 5;
int num_iteration = 0;

motion_t current_motion = FORWARD;

message_t message;

void set_zero(int arr[20]) {
    for (int i = 0; i < 20; i++) {
        arr[i] = 0;
        }
}

int num_neighbors(int arr[20]) {
    int count = 0;

    for (int i = 0; i < 20; i++) {
        if (arr[i] != 0) {
            count++;
        }
    }
    return count;
}

void add_neighbour(int arr[20]) {

    int found = 0;

    for (int i = 0; i < 20; i++) {
        if (arr[i] == neighbour_id) {
            found = 1;
            break;
        }
    }

    if (!found) {
        for (int i = 0; i < 20; i++) {
            if (arr[i] == 0) {
                arr[i] = neighbour_id;
                break;
            }
        }
    }

}

int calculate_adjust()  {

    int my_heading = M_PI / 2;
    int neighbor_heading = M_PI;

    return (my_heading + neighbor_heading) / 2;

}

double calculate_probability() {  
    double probability = 1 - exp(-((1.0 / tumble_rate) * num_iteration));

    return probability;
}

void kilobot_tumble() {
        // Randomly choose a direction to turn
    int random_direction = rand() % 2;
    // Random amount of time to turn between 0s and 2s
    int random_tumble = 1000 + (rand() % 5001);

    if (random_direction == 0)  {
        // Sets tumble motion (Turn right)
        set_motion(RIGHT);
        // Tumble for random time
        delay(random_tumble);
    }   else    {
        // Sets tumble motion (Turn left)
        set_motion(LEFT);
        // Tumble for random time
        delay(random_tumble);
    }
}

void set_motion(motion_t new_motion) {
    if (current_motion != new_motion) {
        current_motion = new_motion;
        if (new_motion == STOP) {
            set_motors(0, 0);
        } else if (new_motion == FORWARD) {
            spinup_motors();
            set_motors(kilo_straight_left, kilo_straight_right);
        } else if (new_motion == LEFT) {
            spinup_motors();
            set_motors(kilo_turn_left, 0);
        } else if (new_motion == RIGHT) {
            spinup_motors();
            set_motors(0, kilo_turn_right);
        }
    }
}

void setup() {

    srand(time(NULL));
    delay(1000);

    // set_motion(FORWARD);
}

void loop() {
    num_iteration++;
    delay(100);

    if (new_message == 1){

        add_neighbour(neighbors);

        new_message = 0;

        // set_motion(STOP);
        // delay(500);

        

        // int adjust_angle = calculate_adjust();
        // int adjust_time = turn_time * (adjust_angle / 2*M_PI) * (kilo_turn_left / kilo_full_power);

        // if (adjust_time < 0) {
        //     set_color(RGB(0, 1, 0));
        //     adjust_time *= -1;
        //     set_motion(RIGHT);
        //     delay(adjust_time);
        // }
        // else {
        //     set_color(RGB(0, 0, 1));
        //     set_motion(LEFT);
        //     delay(adjust_time);
        // }
        }

    else  {

        set_zero(neighbors);

    }

    set_motion(FORWARD);
    delay(100);

    double probability = calculate_probability();

    double random_value = (double)rand() / RAND_MAX;  // Generate a random value between 0 and 1
    int result = (random_value < probability) ? 1 : 0;

    if (result == 1) {
        kilobot_tumble();
        num_iteration = 0;
    }

    neighbour_count();

    if (kilo_ticks % 300 == 0) {

        set_zero(neighbors);
    }


}

message_t *message_tx() {
    message.type = NORMAL;
    message.data[0] = kilo_uid;
    message.crc = message_crc(&message);
    return &message;
}

void message_rx(message_t *m, distance_measurement_t *d) {
    new_message = 1;
    neighbour_id = m->data[0];
}

void neighbour_count() {
    
    int count = num_neighbors(neighbors);

    switch (count) {
        case 0:
            set_color(RGB(1,0,0));
            break;       
        case 1:
            set_color(RGB(0,1,0));
            break;       
        case 2:
            set_color(RGB(0,0,1));
            break;        
        case 3:
            set_color(RGB(1,1,0));
            break;        
        case 4:
            set_color(RGB(0,1,1));
            break;       
        default:
            set_color(RGB(1,1,1));
            break;
    }
}

int main() {
    kilo_init();
    kilo_message_tx = message_tx;
    kilo_message_rx = message_rx;
    kilo_start(setup, loop);
    return 0;
}