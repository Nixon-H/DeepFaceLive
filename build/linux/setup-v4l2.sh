#!/bin/bash
set -euo pipefail

# Reloads v4l2loopback with proper settings for DeepFaceLive virtual camera output
# Must be run with sudo on the HOST (not inside container)
# After running this, Discord/Brave/OBS can use /dev/video10 as camera

DEVICE_NR="${1:-10}"
CARD_LABEL="${2:-DeepFaceLive}"

echo "Unloading v4l2loopback..."
modprobe -r v4l2loopback 2>/dev/null || true
sleep 1

echo "Loading v4l2loopback (device=/dev/video${DEVICE_NR}, label=${CARD_LABEL})..."
modprobe v4l2loopback \
  video_nr="$DEVICE_NR" \
  card_label="$CARD_LABEL" \
  exclusive_caps=0

echo "Format will be set by the first writer (DeepFaceLive Virtual Cam)."
echo "Done. /dev/video${DEVICE_NR} ready for DeepFaceLive virtual camera output."
