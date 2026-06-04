#!/usr/bin/env bash
# start_microros_agent.sh — Start the micro-ROS agent for STM32 UART bridge
# Usage: ./scripts/start_microros_agent.sh [port] [baudrate]
# Requires micro-ROS agent built and installed (see build/ and install/).
set -euo pipefail

PORT="${1:-/dev/ttyUSB0}"
BAUD="${2:-115200}"

AGENT_BIN="$(ros2 pkg prefix micro_ros_agent)/lib/micro_ros_agent/micro_ros_agent"

if [ ! -f "$AGENT_BIN" ]; then
    echo "ERROR: micro_ros_agent binary not found — ensure the ROS2 workspace is built and sourced"
    exit 1
fi

echo "Starting micro-ROS agent on $PORT at $BAUD baud..."
"$AGENT_BIN" serial --dev "$PORT" -b "$BAUD"
