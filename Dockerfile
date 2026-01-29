FROM --platform=linux/amd64 python:3.11-slim-bookworm

# Work from PSFree directory (not /app)
WORKDIR /PSFree

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install deps (no need for setcap if running as root)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    libcap2-bin \
 && rm -rf /var/lib/apt/lists/*

# Install runtime deps
RUN pip install --no-cache-dir rich

# Copy app into /PSFree
COPY . /PSFree

# Unraid metadata
LABEL \
  net.unraid.docker.icon="https://raw.githubusercontent.com/HVR88/PSFree_Docker/main/icon.png" \
  net.unraid.docker.port="52721" \
  net.unraid.docker.webui="http://[IP]:[PORT]/" \
  net.unraid.docker.description="PSFree local HTTP server for PS4 jailbreak" \
  org.opencontainers.image.title="PSFree" \
  org.opencontainers.image.description="PSFree local HTTP server for PS4 jailbreak" \
  org.opencontainers.image.source="https://github.com/HVR88/PSFree_Docker"


# Run as root
USER root

# Default port
ENV PORT=52721
EXPOSE 52721

# Run server, honoring PORT env
CMD ["sh", "-lc", "python serve.py \"${PORT:-52721}\""]
