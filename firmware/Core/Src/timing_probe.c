/* timing_probe.c — GPIO timing probes for inference latency measurement (FM-08)
 *
 * PA5: inference start
 * PA6: inference end
 *
 * Connect to logic analyzer or oscilloscope for hardware latency measurement.
 * Step 9 of build order.
 */
#include "timing_probe.h"

/* TODO: implement GPIO set/clear around inference call */

void timing_probe_init(void)
{
    /* TODO: configure PA5, PA6 as GPIO output */
}

void timing_probe_start(void)
{
    /* TODO: set PA5 high */
}

void timing_probe_end(void)
{
    /* TODO: set PA5 low, set PA6 high briefly */
}
