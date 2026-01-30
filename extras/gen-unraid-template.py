#!/usr/bin/env python3
from __future__ import annotations

import os
import sys

TEMPLATE_VARS = os.path.join("extras", "unraid-vars.yml")
OUTPUT_XML = os.path.join("extras", "unraid-template.xml")


def die(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def load_yaml(path: str) -> dict:
    try:
        import yaml  # type: ignore
    except Exception:
        die("Missing dependency: pyyaml. Install with: pip install pyyaml")

    if not os.path.exists(path):
        die(f"Missing file: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        die(f"{path} did not parse to a dictionary/object.")

    return data


def get(d: dict, *keys: str, default=None):
    cur = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def bool_text(v) -> str:
    return "true" if bool(v) else "false"


def xml_tag(name: str, value: str | None = None, indent: int = 2) -> str:
    pad = " " * indent
    if value is None:
        return f"{pad}<{name}/>"
    return f"{pad}<{name}>{value}</{name}>"


def main() -> int:
    data = load_yaml(TEMPLATE_VARS)

    name = get(data, "container", "name")
    repo = get(data, "image", "repository")
    tag = get(data, "image", "tag")
    registry = get(data, "image", "registry")
    network = get(data, "runtime", "network")
    shell = get(data, "runtime", "shell", default="bash")
    privileged = bool(get(data, "runtime", "privileged", default=False))

    webui = get(data, "ui", "webui")
    icon = get(data, "ui", "icon")
    category = get(data, "category", default="")

    overview = get(data, "overview", default="")

    config_items = get(data, "config", default=[])
    if not isinstance(config_items, list):
        die("extras/unraid-vars.yml: config must be a list")

    # Basic required checks (minimal)
    if not name:
        die("extras/unraid-vars.yml: container.name is required")
    if not repo or not tag:
        die("extras/unraid-vars.yml: image.repository and image.tag are required")
    if not webui:
        die("extras/unraid-vars.yml: ui.webui is required")

    repository_full = f"{repo}:{tag}"

    # Build XML (keeps empty tags as <Tag/>)
    lines: list[str] = []
    lines.append('<?xml version="1.0"?>')
    lines.append('<Container version="2">')
    lines.append(xml_tag("Name", str(name)))
    lines.append(xml_tag("Repository", repository_full))
    lines.append(xml_tag("Registry", str(registry) if registry else ""))

    lines.append(xml_tag("Network", str(network) if network else "bridge"))
    lines.append(xml_tag("MyIP", None))
    lines.append(xml_tag("Shell", str(shell)))
    lines.append(xml_tag("Privileged", bool_text(privileged)))

    lines.append(xml_tag("Category", str(category) if category else None))
    lines.append(xml_tag("Support", None))
    lines.append(xml_tag("Project", None))

    # Overview block: preserve exactly, including &#xD; etc.
    lines.append("  <Overview>")
    if overview:
        # Do NOT escape; overview already contains entity codes and/or unicode.
        for ln in str(overview).splitlines():
            lines.append(ln)
    lines.append("  </Overview>")

    lines.append(xml_tag("WebUI", str(webui)))
    lines.append(xml_tag("TemplateURL", None))
    lines.append(xml_tag("Icon", str(icon) if icon else ""))

    lines.append(xml_tag("ExtraParams", None))
    lines.append(xml_tag("PostArgs", None))
    lines.append(xml_tag("CPUset", None))
    lines.append(xml_tag("DonateText", None))
    lines.append(xml_tag("DonateLink", None))
    lines.append(xml_tag("Requires", None))

    # Config entries
    for c in config_items:
        if not isinstance(c, dict):
            die("extras/unraid-vars.yml: each config entry must be a map/object")

        cname = c.get("name", "")
        target = c.get("target", "")
        default = c.get("default", "")
        ctype = c.get("type", "")
        display = c.get("display", "")
        required = bool_text(c.get("required", False))
        mask = bool_text(c.get("mask", False))
        desc = c.get("description", "")

        if not cname or not target or not ctype:
            die("extras/unraid-vars.yml: config item missing name/target/type")

        # Match your exact Config formatting (self-closing with attributes)
        lines.append(
            f'  <Config Name="{cname}" Target="{target}" Default="{default}" '
            f'Type="{ctype}" Display="{display}" Required="{required}" Mask="{mask}" '
            f'Description="{desc}" />'
        )

    lines.append(xml_tag("TailscaleStateDir", None))
    lines.append("</Container>")
    lines.append("")  # newline at EOF

    os.makedirs(os.path.dirname(OUTPUT_XML), exist_ok=True)
    with open(OUTPUT_XML, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))

    print(f"Wrote: {OUTPUT_XML}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
