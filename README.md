# DeepFaceLive Linux Docker Edition

Run **DeepFaceLive** on Linux inside a reproducible Docker container with NVIDIA GPU acceleration and virtual webcam output via `v4l2loopback`.

**Linux only.** No Windows support. No Windows instructions. This repository solely targets Linux users who want a clean, Docker-based deployment.

## Why This Exists

The upstream [DeepFaceLive](https://github.com/iperov/DeepFaceLive) project primarily targets Windows. This repository provides a **Linux-native Docker environment** that eliminates manual dependency hell while maintaining full GPU acceleration and webcam passthrough.

**Use cases:**
- Real-time face swapping in OBS Studio, Discord, Google Meet, Zoom
- Reproducible deployment without polluting the host system
- Headless processing pipelines

## Features

- NVIDIA CUDA-accelerated Docker container (CUDA 11.8)
- Physical webcam passthrough (`/dev/video*`)
- Virtual webcam output via `v4l2loopback` -> /dev/video10
- Automatic NVIDIA driver version detection
- Persistent user data volume
- Minimal host dependencies
- Fully reproducible `docker build`

## Requirements

| Component | Requirement |
|---|---|
| GPU | NVIDIA with CUDA-capable driver |
| Webcam | Any V4L2-compatible camera |
| OS | Linux x86_64 (Debian/Ubuntu/Kali/Mint/Fedora) |
| Docker | >= 24.0 with `nvidia-container-toolkit` |
| Kernel | Linux with V4L2 support |

## Quick Start

```bash
# 1. Clone
git clone <repository>
cd DeepFaceLive

# 2. Load virtual camera (once per boot)
sudo modprobe v4l2loopback \
  video_nr=10 \
  card_label="DeepFaceLive" \
  exclusive_caps=1 \
  max_buffers=2

# 3. Build & run
cd build/linux
./start.sh -c
```

With custom data folder:
```bash
./start.sh -c -d /path/to/your/data
```

## Pipeline

```
Physical Webcam  --->  DeepFaceLive  --->  FFmpeg  --->  v4l2loopback  --->  /dev/video10
                                                                              |
                                                              +---------------+---------------+
                                                            Discord  OBS  Zoom  Meet
```

## Repository Structure

```
DeepFaceLive/
├── build/
│   └── linux/
│       ├── Dockerfile              # GPU-accelerated container
│       ├── start.sh                # Container launcher
│       ├── example.sh              # Entrypoint script
│       └── README.md               # Build-specific instructions
├── patches/                        # Upstream modifications
├── userdata/                       # Persistent models & settings
├── README.md                       # This file
└── ...
```

## Script Reference

### `start.sh`

| Flag | Description |
|---|---|
| `-c` | Mount webcam devices (`/dev/video0`-`3`, `/dev/video10`) |
| `-d <path>` | Custom data folder (default: `$(pwd)/data/`) |
| `-h` | Show help |

The script automatically:
- Detects your NVIDIA driver version
- Builds the Docker image with the correct CUDA compatibility
- Passes through GPU, X11, and webcam devices
- Mounts persistent data volume

## GPU Verification

```bash
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu20.04 nvidia-smi
```

## Virtual Camera Setup

```bash
# Load once (or add to /etc/modules-load.d/v4l2loopback.conf)
sudo modprobe v4l2loopback \
  video_nr=10 \
  card_label="DeepFaceLive" \
  exclusive_caps=1 \
  max_buffers=2

# Verify
v4l2-ctl --list-devices
# Expected:
#   DeepFaceLive (platform:v4l2loopback-000):
#       /dev/video10
```

## Known Limitations

- **Linux only** -- no Windows support in this repository
- **NVIDIA GPU required** -- no AMD/Intel acceleration support
- **Webcam exclusivity** -- `/dev/video*` can only be opened by one process at a time
- **Browser compatibility** -- depends on PipeWire/V4L2 proxy configuration
- **v4l2loopback dependency** -- kernel module must be loaded before container start
- **X11 required** -- Wayland-only setups may need additional configuration

## Credits

- [DeepFaceLive](https://github.com/iperov/DeepFaceLive) -- upstream project by iperov
- build/linux contributors -- Linux Docker adaptation and testing
- NVIDIA CUDA -- GPU acceleration
- FFmpeg -- frame encoding and streaming
- Docker -- containerization
- v4l2loopback -- virtual camera device
