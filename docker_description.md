# PSFree Docker

PSFree is a lightweight local web server for hosting the PSFree exploit

<br>

#### **Currently working firmware**

PS4 9.0 - 9.6 (maybe others but I will only test on 9)

<br>

# How to run

Deploy with docker-compose, Portainer, Unraid, etc…

<br>

Your Docker host ideally supports macvlan or IPVLAN networking

#### **Container Settings:**

1. select/set your macvlan network (br0 on Unraid)
2. set an available FIXED IP address within your lan
3. set HTTP port to 80

<br>

This allows a simple redirect without a reverse proxy Set the original "manuals.playstation.net" to point to your PSFree IP

<br>

- AdGuard Home / Pi-hole: DNS rewrite → container IP
- Firewall / Router (pfSense / OPNsense / ASUS etc..): DNS Host override ([https://shorturl.at/Syx8T](https://shorturl.at/Syx8T))

<br>

Then, on PS4, open Settings → User Guide and the exploit loads automatically

<br>

Enjoy.
