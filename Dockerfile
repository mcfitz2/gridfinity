FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        openscad \
        git \
        ca-certificates \
        && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY builder/requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Set the working directory
WORKDIR /workspace

# Default command (can be overridden)
CMD ["bash"]