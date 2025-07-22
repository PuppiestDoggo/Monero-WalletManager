FROM debian:bookworm-slim

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*

# Create user
RUN useradd -m -s /bin/bash rpcmanager

# Switch to non-root user
USER rpcmanager

# Set working directory
WORKDIR /app

# Copy app code
COPY --chown=rpcmanager:rpcmanager . /app

# Create virtual environment and install dependencies
RUN python3 -m venv venv && \
    venv/bin/pip install --no-cache-dir --upgrade pip && \
    venv/bin/pip install --no-cache-dir -r requirements.txt

# Add venv to path so ENTRYPOINT uses it
ENV PATH="/app/venv/bin:$PATH"

# Expose port
EXPOSE 8080

# Run FastAPI with uvicorn
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
