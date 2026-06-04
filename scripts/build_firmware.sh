#!/usr/bin/env bash
# build_firmware.sh — Build NEXUS STM32 firmware with TFLite-Micro
# Usage: ./scripts/build_firmware.sh
# Step 9 of build order.
set -euo pipefail

FIRMWARE_DIR="firmware"
BUILD_DIR="$FIRMWARE_DIR/build"

mkdir -p "$BUILD_DIR"

echo "Building NEXUS firmware..."
# TODO: configure for STM32CubeMX-generated Makefile or CMake
# make -C "$FIRMWARE_DIR" all
echo "TODO: build command not yet configured"
echo "Output will be written to $BUILD_DIR"
