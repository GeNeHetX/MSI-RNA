FROM python:3.13.1-bookworm

# Install basic utilities
RUN apt-get update
RUN apt-get install -y git sudo curl
RUN apt-get install -q -y --no-install-recommends \
        libglu1-mesa-dev \
        libgomp1 \
        libopenslide-dev \
        python3-rtree

# Add user so we don't need to run VS Code as root
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /usr/bin/bash \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# [Optional] Set the default user. Omit if you want to keep the default as root.
USER $USERNAME

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --upgrade --no-cache-dir -r requirements.txt