#include "kilolib.h"
#include <stdlib.h>
#include <time.h>

#define TOO_CLOSE_DISTANCE 40

#define STOP 0
#define FORWARD 1
#define LEFT 2
#define RIGHT 3


int current_motion = STOP;
int distance;
int new_message = 0;


void setup()    
{
    // Set random to seed based on Kilobot ID
    srand(time(NULL));
}


// Function to handle motion.
void set_motion(int new_motion)
{
    // Only take an action if the motion is being changed.
    if (current_motion != new_motion)
    {
        current_motion = new_motion;
        
        if (current_motion == STOP)
        {
            set_motors(0, 0);
        }
        else if (current_motion == FORWARD)
        {
            spinup_motors();
            set_motors(kilo_straight_left, kilo_straight_right);
        }
        else if (current_motion == LEFT)
        {
            spinup_motors();
            set_motors(kilo_turn_left, 0);
        }
        else if (current_motion == RIGHT)
        {
            spinup_motors();
            set_motors(0, kilo_turn_right);
        }
    }
}


// Repeated Kilobot function
void loop()
{
    if (new_message == 1)   
    {
        new_message = 0;

        // If too close to a neighbour run forward
        if (distance < TOO_CLOSE_DISTANCE)  
        {
            // Set the LED.
            set_color(RGB(1, 1, 0));
            // Sets running motion (forward)
            set_motion(FORWARD);
            // Run for 2s
            delay(2000);
        }
        // Otherwise run normally
           else    
        {
        // Set the LED green.
        set_color(RGB(0, 1, 0));
        // Sets running motion (forward)
        set_motion(FORWARD);
        // Run for random time between 1s and 5s
        delay(1000 + (rand() % 5001));
        }
    }

    // Set the LED to White
    set_color(RGB(1, 1, 1));
    // Stop motion before tumbling
    set_motion(STOP);
    // Stop for 1s
    delay(1000);

    // Randomly choose a direction to turn
    int random_direction = rand() % 2;
    // Random amount of time to turn between 0s and 2s
    int random_tumble = 2000 + (rand() % 5001);

    if (random_direction == 0)  {
        // Set LED to Red
        set_color(RGB(1, 0, 0));
        // Sets tumble motion (Turn right)
        set_motion(RIGHT);
        // Tumble for random time
        delay(random_tumble);
    }   else    {
        // Set LED to Blue
        set_color(RGB(0, 0, 1));
        // Sets tumble motion (Turn left)
        set_motion(LEFT);
        // Tumble for random time
        delay(random_tumble);
    }

    // Set the LED to White
    set_color(RGB(1, 1, 1));
    // Stop motion before running
    set_motion(STOP);
    // Stop for 1s
    delay(1000);

}

void message_rx(message_t *m, distance_measurement_t *d)
{
    new_message = 1;
    distance = estimate_distance(d);
}


int main()
{
    kilo_init();
    kilo_message_rx = message_rx;
    kilo_start(setup, loop);

    return 0;
}
