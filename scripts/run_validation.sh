#!/usr/bin/env bash
# run_validation.sh — Run the full NEXUS validation suite
# Usage: ./scripts/run_validation.sh [--hil] [--scenario <path>]
#
# --hil        Include STM32 hardware-in-the-loop tests (FM-02, FM-08)
# --scenario   Run a specific scenario YAML instead of the default full suite
set -euo pipefail

HIL=false
SCENARIO=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --hil) HIL=true; shift ;;
        --scenario) SCENARIO="$2"; shift 2 ;;
        *) echo "Unknown argument: $1"; exit 1 ;;
    esac
done

# Source ROS2 workspace
# shellcheck source=/dev/null
source install/setup.bash

if [ -n "$SCENARIO" ]; then
    echo "Running scenario: $SCENARIO"
    ros2 launch nexus nexus_scenario.launch.py "scenario:=$SCENARIO"
elif [ "$HIL" = true ]; then
    echo "Running full validation with STM32 HIL..."
    ros2 launch nexus nexus_hil.launch.py
else
    echo "Running host-only validation..."
    ros2 launch nexus nexus_full.launch.py
fi

echo "Running pytest suite..."
pytest tests/ -v --html=results/report.html --self-contained-html
