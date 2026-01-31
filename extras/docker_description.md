# **PSFree Web Host**

A lightweight local web server for hosting the PSFree exploit with latest GoldHEN

<p align="center">
  <img src="https://raw.githubusercontent.com/HVR88/PSFree_Docker/develop/extras/icon.png" alt="PSFree Web Host" />
</p>

#### **Currently working firmware:**

PS4 7.0 - 9.6

# Details

- **Contains GoldHEN 2.4b18.8 (Jan 2026)**
- Multi-Architecture: amd64 and arm64 support
- _Web server drops paths/text from URL - "Just Works" on PS4_
- _Runs on http port 80_

# How to run

Deploy with docker-compose, Portainer, Unraid, etc… Your Docker host should ideally support MACVLAN or IPVLAN networking

#### **Container Settings:**

1. select/set your macvlan network (br0 on Unraid)
2. set an available FIXED IP address within your lan
3. set HTTP port to 80

<br>This allows a simple redirect without a reverse proxy

#### **Additional Setup:**

4. Set the "manuals.playstation.net" domain name to point to your container's IP address

- AdGuard Home / Pi-hole: DNS rewrite → container IP
- Firewall / Router (pfSense / OPNsense / ASUS etc..): DNS Host override<br>([Host redirect on common routers](https://shorturl.at/Syx8T))

#### **On your PS4:**

Go to _Settings → User Guide_ and the exploit loads automatically → Enjoy!
