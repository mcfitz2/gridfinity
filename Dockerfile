FROM alpine:3.20

# Install dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    git \
    ca-certificates \
    openscad

# Install Python dependencies
COPY builder/requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir --break-system-packages -r /tmp/requirements.txt

# Set the working directory
WORKDIR /workspace

# Default command (can be overridden)
CMD ["sh"]