FROM alpine:3.20

# Install dependencies
RUN apk add --no-cache \
    git \
    ca-certificates \
    openscad

# Install Python dependencies

# Set the working directory
WORKDIR /workspace

# Default command (can be overridden)
CMD ["sh"]