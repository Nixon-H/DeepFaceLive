FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04
WORKDIR /app
ARG DEBIAN_FRONTEND=noninteractive
ARG NV_VER
RUN set -e && \
    apt update && \
    apt -y install \
    libgl1-mesa-glx \
    libegl1-mesa \
    libxrandr2 \
    libxss1 \
    libxcursor1 \
    libxcomposite1 \
    libasound2 \
    libxi6 \
    libxtst6 \
    curl \
    ffmpeg \
    git \
    nano \
    gnupg2 \
    libsm6 \
    wget \
    unzip \
    libxcb-cursor0 \
    libxcb-xinerama0 \
    libxcb-icccm4 \
    libxcb-keysyms1 \
    libxcb-render0 \
    libxcb-render-util0 \
    libxcb-image0 \
    libxkbcommon-x11-0
#RUN apt -y install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6 curl ffmpeg git nano gnupg2 libsm6 wget unzip libxcb-icccm4 libxkbcommon-x11-0 libxcb-keysyms1 libxcb-icccm4 libxcb-render0 libxcb-render-util0 libxcb-image0
RUN set -e && \
    apt install --no-install-recommends -y python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python

RUN set -e && \
    git clone https://github.com/iperov/DeepFaceLive.git

#RUN python -m pip install --upgrade pip
RUN set -e && \
    python -m pip install --upgrade pip && \
    pip config set global.timeout 1200
#RUN python -m pip install onnxruntime-gpu==1.15.1 numpy==1.21.6 h5py numexpr protobuf==3.20.3 opencv-python==4.8.0.74 opencv-contrib-python==4.8.0.74 pyqt6==6.5.1 onnx==1.14.0 torch==1.13.1 torchvision==0.14.1
RUN set -e && \
    python -m pip install --default-timeout=1200 \
onnxruntime-gpu==1.15.1 \
numpy==1.21.6 \
h5py \
numexpr \
protobuf==3.20.3 \
opencv-python==4.8.0.74 \
opencv-contrib-python==4.8.0.74 \
pyqt6==6.5.1 \
onnx==1.14.0 \
torch==1.13.1 \
torchvision==0.14.1

WORKDIR /app/DeepFaceLive
COPY example.sh example.sh
COPY patches/ patches/
RUN set -e && cp patches/StreamOutput.py apps/DeepFaceLive/backend/StreamOutput.py && cp patches/QStreamOutput.py apps/DeepFaceLive/ui/QStreamOutput.py
CMD ./example.sh
