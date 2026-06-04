/* inference_engine.c — TFLite-Micro inference wrapper
 *
 * Wraps the INT8 quantized model for event classification.
 * Timing probes are inserted around the inference call for FM-08.
 *
 * Step 9 of build order.
 */
#include "inference_engine.h"
#include "timing_probe.h"

/* TODO: implement model loading, input tensor population, invoke, output read */

void inference_engine_init(void)
{
    /* TODO */
}

int inference_engine_run(const float *window, int window_size)
{
    /* Returns event_class integer: 0=NOMINAL, 1=ANOMALY, 2=CRITICAL_EVENT */
    /* TODO */
    return -1;
}
