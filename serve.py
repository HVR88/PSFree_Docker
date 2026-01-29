import sys
import socket
import os
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import json
from datetime import datetime
import hashlib
import urllib.request
import re


console = Console()


# Configuration for manifest generation
EXCLUDED_DIRS = {".venv", ".git", "noneed"}
EXCLUDED_EXTENSIONS = {
    ".yml",
    ".license",
    ".bat",
    ".txt",
    ".exe",
    ".mp4",
    ".py",
    ".bak",
    ".zip",
    ".mp3",
    ".sh",
    ".h",
    ".c",
    ".o",
    ".ld",
    ".md",
    ".d",
}
# Drop non-web files
EXCLUDED_FILES = {
    ".gitignore",
    "COPYING",
    "LICENSE",
    "MAKEFILE",
    "VERSION",
    "Dockerfile",
    "dockerfile",
}
OUTPUT_FILE = "PSFree.manifest"


def get_machine_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def is_docker():
    if os.path.exists("/.dockerenv"):
        return True
    try:
        with open("/proc/1/cgroup", "rt") as f:
            return "docker" in f.read() or "kubepods" in f.read()
    except Exception:
        return False


def get_host_ip():
    try:
        return socket.gethostbyname("host.docker.internal")
    except socket.error:
        return "Could not determine host IP"


def get_ipv4():
    if is_docker():
        ip = get_host_ip()
        if ip:
            print(f"Running inside Docker. Host IPv4: {ip}")
        else:
            print("Running inside Docker, but could not resolve host.docker.internal.")
    else:
        ip = get_machine_ip()
        print(f"Not in Docker. Machine IPv4: {ip}")
    return ip


def create_manifest():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    manifest_path = os.path.join(root_dir, OUTPUT_FILE)
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write("CACHE MANIFEST\n")
        f.write("# v1\n")
        f.write(f"# Generated on {datetime.now()}\n\n")
        f.write("CACHE:\n")

        for dirpath, dirnames, filenames in os.walk(root_dir):
            dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                relpath = os.path.relpath(filepath, root_dir)
                ext = os.path.splitext(filename)[1].lower()
                if (
                    ext in EXCLUDED_EXTENSIONS
                    or filename in EXCLUDED_FILES
                    or filename == OUTPUT_FILE
                ):
                    continue
                f.write(f"{relpath.replace(os.sep, '/')}\n")

        f.write("\nNETWORK:\n")
        f.write("*\n")


class CustomHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        # Normalize unwanted entry paths to `/` while never redirecting assets.
        path_only = self.path.split("?", 1)[0].split("#", 1)[0]

        # Always allow root.
        if path_only in ("/", "/index.html"):
            return super().do_GET()

        # Allow directories (so /folder/ serves /folder/index.html if present).
        if path_only.endswith("/"):
            return super().do_GET()

        # Allow any request that has a file extension (treat as an asset).
        _, ext = os.path.splitext(path_only)
        if ext:
            return super().do_GET()

        # Extensionless: if it doesn't map to a real file/dir, force to root.
        fs_path = self.translate_path(path_only)
        if not os.path.exists(fs_path):
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()
            return

        return super().do_GET()

    def do_HEAD(self):
        path_only = self.path.split("?", 1)[0].split("#", 1)[0]

        if path_only in ("/", "/index.html"):
            return super().do_HEAD()

        if path_only.endswith("/"):
            return super().do_HEAD()

        _, ext = os.path.splitext(path_only)
        if ext:
            return super().do_HEAD()

        fs_path = self.translate_path(path_only)
        if not os.path.exists(fs_path):
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()
            return

        return super().do_HEAD()

    def do_POST(self):
        if self.path == "/generate_manifest":
            try:
                create_manifest()
                response = {
                    "status": "success",
                    "message": f"{OUTPUT_FILE} created successfully.\nThe cache has been updated, Please refresh the page.",
                }
                self.send_response(200)
            except Exception as e:
                response = {
                    "status": "error",
                    "message": f"{str(e)}\nThis option only works on local server!\nPlease make sure your server is up.",
                }
                self.send_response(500)

            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))

        elif self.path == "/update_exploit":
            root_dir = os.path.abspath(os.path.dirname(__file__))
            files_to_update = [
                (
                    "psfree/lapse.mjs",
                    "https://raw.githubusercontent.com/Nazky/PSFree/refs/heads/main/psfree/lapse.mjs",
                ),
                (
                    "psfree/psfree.mjs",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/psfree.mjs",
                ),
                (
                    "psfree/config.mjs",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/config.mjs",
                ),
                (
                    "psfree/send.mjs",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/send.mjs",
                ),
                (
                    "psfree/kpatch/700.bin",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/kpatch/700.bin",
                ),
                (
                    "psfree/kpatch/750.bin",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/kpatch/750.bin",
                ),
                (
                    "psfree/kpatch/800.bin",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/kpatch/800.bin",
                ),
                (
                    "psfree/kpatch/850.bin",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/kpatch/850.bin",
                ),
                (
                    "psfree/kpatch/900.bin",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/kpatch/900.bin",
                ),
                (
                    "psfree/kpatch/903.bin",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/kpatch/903.bin",
                ),
                (
                    "psfree/kpatch/950.bin",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/kpatch/950.bin",
                ),
                (
                    "psfree/rop/ps4/700.mjs",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/rop/ps4/700.mjs",
                ),
                (
                    "psfree/rop/ps4/750.mjs",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/rop/ps4/750.mjs",
                ),
                (
                    "psfree/rop/ps4/800.mjs",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/rop/ps4/800.mjs",
                ),
                (
                    "psfree/rop/ps4/850.mjs",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/rop/ps4/850.mjs",
                ),
                (
                    "psfree/rop/ps4/900.mjs",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/rop/ps4/900.mjs",
                ),
                (
                    "psfree/rop/ps4/950.mjs",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/rop/ps4/950.mjs",
                ),
                (
                    "psfree/module/chain.mjs",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/module/chain.mjs",
                ),
                (
                    "psfree/module/constants.mjs",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/module/constants.mjs",
                ),
                (
                    "psfree/module/int64.mjs",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/module/int64.mjs",
                ),
                (
                    "psfree/module/mem.mjs",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/module/mem.mjs",
                ),
                (
                    "psfree/module/memtools.mjs",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/module/memtools.mjs",
                ),
                (
                    "psfree/module/offset.mjs",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/module/offset.mjs",
                ),
                (
                    "psfree/module/rw.mjs",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/module/rw.mjs",
                ),
                (
                    "psfree/module/utils.mjs",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/module/utils.mjs",
                ),
                (
                    "psfree/module/view.mjs",
                    "https://github.com/Nazky/PSFree/raw/refs/heads/main/psfree/module/view.mjs",
                ),
            ]

            results = []

            for local_rel_path, url in files_to_update:
                try:
                    abs_local_path = os.path.abspath(
                        os.path.join(root_dir, local_rel_path)
                    )
                    if not abs_local_path.startswith(root_dir):
                        raise ValueError(f"Invalid path {local_rel_path}")

                    with urllib.request.urlopen(url) as response:
                        new_data = response.read()

                    os.makedirs(os.path.dirname(abs_local_path), exist_ok=True)
                    with open(abs_local_path, "wb") as f:
                        f.write(new_data)

                    results.append(f"{local_rel_path}: updated")

                except Exception as e:
                    results.append(f"{local_rel_path}: error ({e})")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"results": results}).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")


PORT = int(os.getenv("PORT", "52721"))
IP = get_ipv4()

if len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        console.print("[bold red]Usage:[/] python serve.py [port]")
        sys.exit(1)

console.print(
    Panel(
        Text("Simple Python HTTP Server", style="bold white on blue"),
        subtitle="Press [bold yellow]Ctrl+C[/] to stop the server",
        expand=False,
    )
)

console.print(
    f"[green]Server is running![/]\n"
    f"Listening on [bold magenta]http://{IP}:{PORT}[/]\n",
    style="bold",
)

try:
    with TCPServer(("0.0.0.0", PORT), CustomHandler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    console.print("\n[bold red]Server stopped by user.[/]")
except OSError as e:
    console.print(f"[bold red]Error:[/] {e}")
