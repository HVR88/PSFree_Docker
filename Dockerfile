FROM --platform=linux/amd64 python:3.11-slim-bookworm
ARG IMAGE_VERSION
ARG IMAGE_REVISION

# Work from PSFree directory (not /app)
WORKDIR /PSFree

# Run as root
USER root

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

# Minimal OCI metadata (set at build time)
LABEL org.opencontainers.image.version="$IMAGE_VERSION" \
      org.opencontainers.image.revision="$IMAGE_REVISION"

# Default port
ENV PORT=52721
EXPOSE 52721

# Run server, honoring PORT env
CMD ["sh", "-lc", "python serve.py \"${PORT:-52721}\""]
