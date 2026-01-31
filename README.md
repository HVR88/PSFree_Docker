# PSFree Web Host - Docker Deployment

A lightweight local web server for hosting the PSFree exploit with latest GoldHEN

<p align="center">
  <img src="https://raw.githubusercontent.com/HVR88/PSFree_Docker/develop/extras/icon.png" alt="PSFree Web Host" />
</p>

PSFree_Docker is based on [PSFree from Nazky](https://github.com/Nazky/PSFree) - (this repo is mainly interesting for developers)

_Normal people want the **Docker Container**_ to exploit their PS4:

> [!NOTE]
>
> ## **[espressomatic/psfree_docker](https://hub.docker.com/r/espressomatic/psfree_docker)**

### Tweaks

- _Pre-built container ready to deploy, hosted at Docker Hub and Unraid Apps_
- **Updated to latest (Jan 2026) GoldHEN 2.4b18.8**
- Multi-Architecture: amd64 and arm64 support
- _Web server drops paths/text from URL - "Just Works" on PS4_
- _Updated to allow running default http port 80_
- Automatic build action pushes container to Docker hub
- Build versioning for repo and docker container
- Docker compose with instructions and exmaple defaults
- Unraid template for manual installation and deployment to Unraid Community Apps
- Unraid Docker 'app' icon

### Currently working firmware

PS4 7.0 - 9.6

## Dev Requirements to fork this repo

You need to configure the following two secrets in your GitHub account to automatically push your build to Docker Hub

- DOCKERHUB_USERNAME (this is your normal Docker Hub login username)
- DOCKERHUB_TOKEN (you need to generater this at Docker Hub)

# Docker Container Instructions (go to Docker Hub)

Deploy with docker-compose, Portainer, Unraid, etc… Your Docker host should ideally support macvlan or IPVLAN networking

#### **Container Settings:**

1. select/set your macvlan network (br0 on Unraid)
2. set an available FIXED IP address within your lan
3. set HTTP port to 80

This allows a simple redirect without a reverse proxy

> [!NOTE]
>
> ## **[Download the complete container on Docker Hub](https://hub.docker.com/r/espressomatic/psfree_docker)**

#### **Additional Setup:**

Set the "manuals.playstation.net" domain name to point to your container's IP address

- AdGuard Home / Pi-hole: DNS rewrite → container IP
- Firewall / Router (pfSense / OPNsense / ASUS etc..): DNS Host override<br>([Host redirect on common routers](https://shorturl.at/Syx8T))

#### **On your PS4:**

Go to _Settings → User Guide_ and the exploit loads automatically → Enjoy!
