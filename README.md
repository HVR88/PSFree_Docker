# PSFree_Docker

PSFree container for self-hosting and doing URL redirect

This repo is a direct fork of Nasky's repo, plus below mods:

- [PSFree from Nazky](https://github.com/Nazky/PSFree)

Nazky's repo is in turn based on the work of two other repos:

- [PSFree from Kame repo](https://github.com/kmeps4/PSFree)
- [PSFree from Al-Azif repo](https://github.com/Al-Azif/psfree-lapse)

<h1 style="color:red;text-align:center;">⚠️DON'T REPORT ERRORS FROM THIS REPO UPSTREAM⚠️</h1>

---

### Known issues

- check upstream

### Currently working firmware

PS4 9.0 - 9.6 (maybe others but I will only test on 9)

# How to run

Only one way for this repo.

Deploy with docker-compose or on Unraid.
Set up macvlan networking on its own IP
Set port to 80
Use firewall, AdGuard Home or PiHole to redirect PS's User Guide host+domain to your IP set above
Visit USER GUIDE on your PS
Enjoy.

## Locally

Not tested nor supported on my fork - look at upstream only for that.

##### Windows:

Forget about it, run a Linux server to hosty this: Unraid
