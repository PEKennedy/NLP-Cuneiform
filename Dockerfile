# docker build -t imagename .
# docker run -p 8888:8888 --gpus all -v %cd%\..\..\:/data -w / -it imagename
# Base image
FROM tensorflow/tensorflow:2.13.0-gpu

# Install Linux development tools
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        vim \
        man-db \
        wget \
        less \
        python3-pip \
        lsb-release \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python 3.8.
RUN apt-get update && apt-get install -y \
    python3.8 \
    python3.8-dev \
    python3.8-distutils \
    python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    python3.8 -m pip install --upgrade pip

# Install python libraries
RUN pip3 --no-cache-dir install \
    tensorflow_hub \
    albumentations==1.3.1 \
    numpy==1.24.3 \
    scipy==1.10.1 \
    pandas==2.0.3 \
    scikit-learn==1.3.1 \
    matplotlib==3.7.3 \
    jupyter==1.0.0 \
    torch==2.0.1 \
    torchvision==0.15.2 \
    Pillow==10.0.1 \
    labelbox==3.52.0 \
    Pylon==0.4.4 \
    pypylon==2.3.0 \
    && \
    rm -rf /root/.cache/pip

# Exposes port 8888 for Jupyter
EXPOSE 8888

# Exposes port 80 for Matplotlib
EXPOSE 80

# Define the command to run your application
CMD ["/bin/bash"]