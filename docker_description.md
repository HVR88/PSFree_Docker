# PSFree_Docker

PSFree is a lightweight local web server for hosting the PSFree exploit

### Currently working firmware

PS4 9.0 - 9.6 (maybe others but I will only test on 9)

# How to run

Deploy with docker-compose, Portainer, or on Unraid
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
