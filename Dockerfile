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

# Run as root
USER root

# Default port
EXPOSE 52721

# Run server, honoring PORT env
CMD ["sh", "-lc", "python serve.py \"${PORT:-52721}\""]
