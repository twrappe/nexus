#!/usr/bin/env bash
# flash_firmware.sh — Flash NEXUS firmware to STM32 over ST-Link
# Usage: ./scripts/flash_firmware.sh [/dev/ttyUSB0]
# Step 9 of build order.
set -euo pipefail

PORT="${1:-/dev/ttyUSB0}"
BINARY="firmware/build/nexus_firmware.bin"

if [ ! -f "$BINARY" ]; then
    echo "ERROR: firmware binary not found at $BINARY — run build_firmware.sh first"
    exit 1
fi

echo "Flashing $BINARY to STM32 via ST-Link..."
# TODO: replace with actual flash command (st-flash or openocd)
# st-flash write "$BINARY" 0x08000000
echo "TODO: flash command not yet configured"
