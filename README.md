# PSFree Web Host - Docker Deployment

This is a lightweight local web server for hosting the PSFree exploit

This repo is a fork of [PSFree from Nazky](https://github.com/Nazky/PSFree) plus tweaks (mentioned below)

This repo is intended for developers or anyone wanting to run the server bare-metal. If you are an end-user looking for the exploit you want the Docker Container itself:

> [!NOTE]
>
> ## **[Download the complete container on Docker Hub](https://hub.docker.com/r/espressomatic/psfree_docker)**

### Tweaks

- web host drops extra path and document text from URL - just hit the host and it's automatic
- updates to allow running default http port 80
- automatic build action pushes container to Docker hub
- build versioning for repo and docker container
- docker compose with instructions and exmaple defaults
- Unraid template for manual installation and deployment to Unraid Community Apps
- Unraid Docker 'app' icon

### Currently working firmware

PS4 9.0 - 9.6 (maybe others but I will only test on 9)

## Requirements for this repo

You need to configure the following two secrets to have GitHub automatically push your build to Docker Hub
-DOCKERHUB_USERNAME (this is your normal Docker Hub login username)
-DOCKERHUB_TOKEN (you need to generater this at Docker Hub)

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

Set the original "manuals.playstation.net" domain name to point to your container's IP address

- AdGuard Home / Pi-hole: DNS rewrite → container IP
- Firewall / Router (pfSense / OPNsense / ASUS etc..): DNS Host override<br>([Host redirect on common routers](https://shorturl.at/Syx8T))

#### **On your PS4:**

Go to Settings → User Guide and the exploit loads automatically → Enjoy!
