# **PSFree Web Host - Docker Deployment**

A lightweight web server + the latest GoldHEN for PS4 firmware 7.0 - 9.6

<p align="center">
  <img src="https://raw.githubusercontent.com/HVR88/PSFree_DEV/develop/extras/icon.png" alt="PSFree Web Host" />
</p>

_PSFree_Docker is based on [PSFree from Nazky](https://github.com/Nazky/PSFree)_

### About this container

- _Pre-built & ready to deploy, hosted at Docker Hub and Unraid Apps_
- **Updated to latest (Jan 2026) GoldHEN 2.4b18.8**
- Multi-Architecture: amd64 and arm64 support
- _Web server drops paths/text from URL - "Just Works" on PS4_
- _Updated to allow running default http port 80_
- No reverse proxy needed

# Quick Start

Deploy with docker-compose, Portainer, Unraid, etc… Your Docker host should ideally support MACVLAN or IPVLAN networking

```
git clone https://github.com/HVR88/PSFree_Docker
```

#### **Edit `.env` to match your network and IP settings:**

1. Set your MACVLAN network (br0 on Unraid)
2. Set an available FIXED IP address within your LAN
3. Set HTTP port to 80
4. Run:

```bash
docker compose up -d
```

#### **Additional Setup:**

Set the "**manuals.playstation.net**" domain name to point to your container's IP address

- AdGuard Home / Pi-hole: DNS rewrite → container IP
- Firewall / Router (pfSense / OPNsense / ASUS etc..): DNS Host override<br>([Host redirect on common routers](https://shorturl.at/Syx8T))

#### **On your PS4:**

Go to _Settings → User Guide_ and the exploit loads automatically → Enjoy!

## Notes

- Default image: `espressomatic/psfree_docker:latest`
- Data volume: `./data` is mapped into `/PSFree` inside the container
- For MACVLAN mode, keep `ports:` commented out and set a LAN IP
- For bridge mode, uncomment `ports:` and remove the `networks:` section
- For bridge mode, set `HOST_PORT` in `.env` to the host-side port you want
- Project source code & build workflows: https://github.com/HVR88/PSFree_DEV
