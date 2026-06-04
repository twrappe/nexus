/* main.c — STM32 micro-ROS + TFLite-Micro entry point
 *
 * Target: STM32 Nucleo-F446RE (or STM32F4 Discovery)
 * RTOS:   FreeRTOS
 * Step 9 of build order.
 */
#include "main.h"
#include "microros_node.h"
#include "inference_engine.h"
#include "timing_probe.h"

/* TODO: implement main application entry point */

int main(void)
{
    /* HAL init, clock config, peripheral init */

    inference_engine_init();
    timing_probe_init();
    microros_node_start();  /* blocks — runs FreeRTOS scheduler */

    return 0;
}
