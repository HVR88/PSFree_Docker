# PSFree Web Host - Docker Deployment

This is a lightweight local web server for hosting the PSFree exploit

This repo is a fork of Nasky's repo plus tweaks (mentioned below)

- [PSFree from Nazky](https://github.com/Nazky/PSFree)

Nazky's repo is in turn based on the work of two other repos:

- [PSFree from Kame repo](https://github.com/kmeps4/PSFree)
- [PSFree from Al-Azif repo](https://github.com/Al-Azif/psfree-lapse)

<h1 style="color:red;text-align:center;">⚠️ DON'T REPORT ERRORS FROM THIS REPO UPSTREAM</h1>

## And don't report exploit errors here either.

---

### Tweaks

- web host drops extra path and document text from URL - just hit the host and it's automatic
- updates to allow running default http port 80
- automatic build action pushes container to Docker hub
- build versioning for repo and docker container
- docker compose with instructions and exmaple defaults
- Unraid template for manual installation and deployment to Unraid Community Apps
- Unraid Docker 'app' icon

### Known issues

- check upstream

### Currently working firmware

PS4 9.0 - 9.6 (maybe others but I will only test on 9)

# How to run

Deploy with docker-compose or on Unraid
Your Docker host ideally supports macvlan or IPVLAN networking

Docker Settings:
• set br0 (or your macvlan) network mode
• set Fixed IP address within your lan
• set HTTP port to 80

This allows a simple redirect without a reverse proxy
Set the original "manuals.playstation.net" to point to your PSFree IP

• AdGuard Home / Pi-hole: DNS rewrite → container IP
• Firewall / Router (pfSense / OPNsense / ASUS etc..): DNS Host override (https://shorturl.at/Syx8T)

Then, on PS4, open Settings → User Guide and the exploit loads automatically

Enjoy.

## Locally

Not tested nor supported on my fork - look at upstream only for that.

##### Windows:

Forget about it, run a Linux server to hosty this: Unraid
