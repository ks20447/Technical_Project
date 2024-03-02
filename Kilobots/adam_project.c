#include "kilolib.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <stdbool.h>

// Info: clock ticks approx 32 times per second, or once every 30ms.
#define DETECT_RADIUS 100  // Xmm neighbourhood detection radius
#define MAX_NEIGHBORS 20  // Maximum number of detectable nighbours used to initialise arrays
#define SQUARE_LENGTH 100 // Lenght of grid squares in mm
#define TIME_FULL_TURN 10000 // Time taken in ms to do a full rotation
#define TUMBLE_RATE 20000 //

typedef enum states
{
    STATE_INIT = 0,
    STATE_RUN = 1,
    STATE_TUMBLE = 2,
    STATE_ADJUST = 3,
    STATE_TEST = -1
} state_t;

typedef enum colors
{
    NONE = 0,
    BLUE = 1,
    YELLOW = 2,
    WHITE = 3
} colors_t;

typedef enum motions
{
    STOP = 0,
    FORWARD = 1,
    LEFT = 2,
    RIGHT = 3
} motion_t;

int new_message;
int neighbor_id;
int neighbor_count;
int neighbors[MAX_NEIGHBORS];
int num_iteration;
int state;
int initialised;
long cur_light;
long prev_light;
float x_vel;
float y_vel;
float kilo_heading;
float neighbor_heading;
float neighbor_headings[MAX_NEIGHBORS];
float sum_neighbors;
uint8_t cur_distance;
uint32_t ticks_prev_x;
uint32_t ticks_prev_y;
uint32_t ticks_neighbour_reset;
uint32_t ticks_adjust;

colors_t cur_color;
colors_t prev_color;
motion_t current_motion;
message_t message;
distance_measurement_t dist;

void sample_light()
{
    int numsamples = 0;
    long average = 0;

    while (numsamples < 500)
    {
        int sample = get_ambientlight();
        if (sample != -1)
        {
            average += sample;
            numsamples++;
        }
    }

    cur_light = average / numsamples;
}

// void evaluate_color()
// {
//     int bound_low = 600, bound_high = 850;
//
//     if (cur_light >= 0 && cur_light < bound_low)
//     {
//         cur_color = BLUE;
//         set_color(RGB(0, 0, 2));
//     }
//     else if (cur_light >= bound_low && cur_light < bound_high)
//     {
//         cur_color = YELLOW;
//         set_color(RGB(2, 2, 0));
//     }
//     else if (cur_light >= bound_high)
//     {
//         cur_color = WHITE;
//         set_color(RGB(2, 2, 2));
//     }
//     else
//     {
//         cur_color = NONE;
//         set_color(RGB(0, 0, 0));
//     }
// }

void set_motion(motion_t new_motion)
{

    if (current_motion != new_motion)
    {

        current_motion = new_motion;

        if (new_motion == STOP)
        {

            set_motors(0, 0);
        }
        else if (new_motion == FORWARD)
        {

            spinup_motors();
            set_motors(kilo_straight_left, kilo_straight_right);
        }
        else if (new_motion == LEFT)
        {

            spinup_motors();
            set_motors(kilo_turn_left, 0);
        }
        else if (new_motion == RIGHT)
        {

            spinup_motors();
            set_motors(0, kilo_turn_right);
        }
    }
}

void reset_timers()
{

    ticks_neighbour_reset = kilo_ticks;
    ticks_adjust = kilo_ticks;
    ticks_prev_x = kilo_ticks;
    ticks_prev_y = kilo_ticks;
}

void set_zero(int arr[MAX_NEIGHBORS])
{
    for (int i = 0; i < MAX_NEIGHBORS; i++)
    {
        arr[i] = 0;
        neighbor_headings[i] = 0;
    }
    sum_neighbors = 0;
    neighbor_count = 0;
}

void num_neighbors(int arr[MAX_NEIGHBORS])
{

    for (int i = 0; i < MAX_NEIGHBORS; i++)
    {
        if (arr[i] != 0)
        {
            neighbor_count++;
            sum_neighbors += neighbor_headings[i];
        }
    }
}

void add_neighbour(int arr[MAX_NEIGHBORS])
{

    int found = 0;

    for (int i = 0; i < MAX_NEIGHBORS; i++)
    {
        if (arr[i] == neighbor_id)
        {
            found = 1;
            break;
        }
    }

    if (!found)
    {
        for (int i = 0; i < MAX_NEIGHBORS; i++)
        {
            if (arr[i] == 0)
            {
                arr[i] = neighbor_id;
                neighbor_headings[i] = neighbor_heading;
                break;
            }
        }
    }
}

double calculate_probability()
{
    double probability = 1 - exp(-((1.0 / TUMBLE_RATE) * num_iteration));

    return probability;
}

void run()
{

    set_motion(FORWARD);
    set_color(RGB(0, 0, 0));
    delay(15);
}

void tumble()
{

    set_color(RGB(2, 0, 0));
    // Randomly choose a direction to turn
    int random_direction = rand() % 2;
    // Random amount of time to turn between 1s and 6s
    int random_tumble = 1000 + (rand() % 6001);

    if (random_direction == 0)
    {
        // Sets tumble motion (Turn right)
        set_motion(RIGHT);
        // Tumble for random time
        delay(random_tumble);

        kilo_heading -= (random_tumble / TIME_FULL_TURN) * 2 * M_PI;
    }
    else
    {
        // Sets tumble motion (Turn left)
        set_motion(LEFT);
        // Tumble for random time
        delay(random_tumble);

        kilo_heading += (random_tumble / TIME_FULL_TURN) * 2 * M_PI;
    }


    if (kilo_heading > 2 * M_PI) {
        kilo_heading -= 2 * M_PI;
    }
    else if (kilo_heading < 0)
    {
        kilo_heading += 2 * M_PI;
    }
    

}

void init()
{

    set_motion(STOP);
    set_color(RGB(1, 1, 0));
    delay(1000);

    int init_tumble = 1000 + (rand() % 6001);
    set_motion(LEFT);
    delay(init_tumble);

    set_motion(STOP);
    delay(10000 - init_tumble);

    neighbor_heading = (init_tumble / TIME_FULL_TURN) * 2 * M_PI;

    set_zero(neighbors);

    num_iteration = 0;
    new_message = 0;
    neighbor_id = 0;
    neighbor_count = 0;
    cur_light = 0;
    prev_light = 0;
    x_vel = 0;
    y_vel = 0;
    sum_neighbors = 0;

    initialised = 1;
    reset_timers();
}

void adjust()
{

    set_color(RGB(0, 2, 0));
    float new_heading = kilo_heading + sum_neighbors;
    new_heading /= neighbor_count + 1;
    new_heading *= -1;

    if (new_heading != 0)
    {
        new_heading += 2 * M_PI;
    }

    float diff_heading = kilo_heading - new_heading;
    int turn_time = (abs(diff_heading) / (2 * M_PI)) * TIME_FULL_TURN;
    turn_time += 1000;

    if (diff_heading < 0)
    {

        set_motion(LEFT);
        delay(turn_time);
    }
    else if (diff_heading > 0)
    {

        set_motion(RIGHT);
        delay(turn_time);
    }
    else 
    {

        set_motion(STOP);
        delay(turn_time);
    }

    kilo_heading = new_heading;

}

void update_state()
{

    if (initialised == 1)
    {
        state = STATE_RUN;

        if (new_message == 1)
        {
            new_message = 0;
            cur_distance = estimate_distance(&dist);

            if (cur_distance < DETECT_RADIUS)
            {
                add_neighbour(neighbors);
            }
        }
        else
        {

            set_zero(neighbors);
        }

        double probability = calculate_probability();

        double random_value = (double)rand() / RAND_MAX; // Generate a random value between 0 and 1
        int result = (random_value < probability) ? 1 : 0;

        if (result == 1)
        {
            state = STATE_TUMBLE;
            num_iteration = 0;
        }

        sum_neighbors = 0, neighbor_count = 0;
        num_neighbors(neighbors);

        if (kilo_ticks > ticks_adjust + TICKS_PER_SEC * 4 && neighbor_count > 0)
        {
            ticks_adjust = kilo_ticks;
            state = STATE_ADJUST;
            num_iteration = 0;
        }
    }
    else
    {

        state = STATE_INIT;
    }
}

// void testing()
// {
//
//     set_motion(STOP);
//     delay(15);
//
//     prev_color = cur_color;
//     prev_light = cur_light;
//
//     if (kilo_ticks > ticks_neighbour_reset + TICKS_PER_SEC / 2)
//     {
//         ticks_neighbour_reset = kilo_ticks;
//         sample_light();
//         cur_light *= 10;
//     }
//
//     evaluate_color();
//
//     if (prev_color != NONE && cur_color != NONE)
//     {
//
//         if (cur_color != prev_color)
//         {
//             uint32_t diff_time_x = kilo_ticks - ticks_prev_x;
//             ticks_prev_x = kilo_ticks;
//
//             if ((prev_color == WHITE && cur_color == BLUE) || (prev_color == BLUE && cur_color == YELLOW) ||
//                 (prev_color == YELLOW && cur_color == WHITE))
//             {
//                 x_vel = SQUARE_LENGTH / (diff_time_x / 32);
//             }
//             else
//             {
//                 x_vel = -SQUARE_LENGTH / (diff_time_x / 32);
//             }
//         }
//         else
//         {
//             uint32_t diff_time_y = kilo_ticks - ticks_prev_y;
//             ticks_prev_y = kilo_ticks;
//             if (cur_light - prev_light > 30)
//             {
//                 y_vel = SQUARE_LENGTH / (diff_time_y / 32);
//             }
//             else if (cur_light - prev_light < -30)
//             {
//                 y_vel = -SQUARE_LENGTH / (diff_time_y / 32);
//             }
//         }
//
//         kilo_heading = atan2(y_vel, x_vel);
//
//         if (kilo_heading < 0)
//         {
//             kilo_heading += 2 * M_PI;
//         }
//     }
//
//     if (kilo_heading > 0 && kilo_heading <= (M_PI / 2))
//     {
//         set_color(RGB(2, 0, 0));
//     }
//     else if (kilo_heading > (M_PI / 2) && kilo_heading <= M_PI)
//     {
//         set_color(RGB(0, 2, 0));
//     }
//     else if (kilo_heading > M_PI && kilo_heading <= (3 * M_PI / 2))
//     {
//         set_color(RGB(0, 0, 2));
//     }
//     else if (kilo_heading > (3 * M_PI / 2) && kilo_heading <= (2 * M_PI))
//     {
//         set_color(RGB(2, 2, 2));
//     }
//     else
//     {
//         set_color(RGB(0, 0, 0));
//     }
//   
// }

void setup()
{

    srand(kilo_uid);
    state = STATE_INIT;
    initialised = 0;
    new_message = 0;
    num_iteration = 0;
    kilo_heading = 0;
    set_color(RGB(1, 1, 1));
    delay(1000);
    reset_timers();
}

void loop()
{

    num_iteration++;

    update_state();

    if (state == STATE_INIT)
    {

        init();
    }
    else if (state == STATE_RUN)
    {

        run();
    }
    else if (state == STATE_TUMBLE)
    {

        tumble();
    }
    else if (state == STATE_ADJUST)
    {

        adjust();
    }

    if (kilo_ticks > ticks_neighbour_reset + TICKS_PER_SEC * 1)
    {

        ticks_neighbour_reset = kilo_ticks;
        set_zero(neighbors);
    }
}

message_t *message_tx()
{
    message.type = NORMAL;
    message.data[0] = kilo_uid;
    message.data[1] = kilo_heading;
    message.crc = message_crc(&message);
    return &message;
}

void message_rx(message_t *m, distance_measurement_t *d)
{
    new_message = 1;
    neighbor_id = m->data[0];
    neighbor_heading = m->data[1];
    dist = *d;
}

int main()
{
    kilo_init();
    kilo_message_tx = message_tx;
    kilo_message_rx = message_rx;
    kilo_start(setup, loop);
    return 0;
}