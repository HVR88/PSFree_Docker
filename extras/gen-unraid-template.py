#!/usr/bin/env python3
from __future__ import annotations

import os
import sys

TEMPLATE_VARS = os.path.join("extras", "unraid-vars.yml")
OUTPUT_XML = "unraid-template.xml"


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


# Helper: True if value is not None and not blank string
def has_value(v) -> bool:
    if v is None:
        return False
    if isinstance(v, str):
        return v.strip() != ""
    return True


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
    template_url = get(data, "ui", "template_url")

    category = get(data, "category", default="")

    # Links may be stored either under `links:` or as flat/top-level keys
    support = get(data, "links", "support") or get(data, "support")
    project = get(data, "links", "project") or get(data, "project")

    myip = get(data, "runtime", "myip")

    extra_params = get(data, "runtime", "extra_params")
    post_args = get(data, "runtime", "post_args")
    cpuset = get(data, "runtime", "cpuset")

    donate_text = get(data, "links", "donate_text") or get(data, "donate_text")
    donate_link = get(data, "links", "donate_link") or get(data, "donate_link")

    requires = get(data, "requires")

    tailscale_state_dir = get(data, "runtime", "tailscale_state_dir")

    overview = get(data, "overview", default="")

    config_items = get(data, "config", default=[])
    if config_items is None:
        config_items = []
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
    if has_value(registry):
        lines.append(xml_tag("Registry", str(registry)))

    lines.append(xml_tag("Network", str(network) if has_value(network) else "bridge"))
    if has_value(myip):
        lines.append(xml_tag("MyIP", str(myip)))
    lines.append(xml_tag("Shell", str(shell)))
    lines.append(xml_tag("Privileged", bool_text(privileged)))

    if has_value(category):
        lines.append(xml_tag("Category", str(category)))
    if has_value(support):
        lines.append(xml_tag("Support", str(support)))
    if has_value(project):
        lines.append(xml_tag("Project", str(project)))

    # Overview block: preserve exactly, including &#xD; etc.
    lines.append("  <Overview>")
    if overview:
        # Do NOT escape; overview already contains entity codes and/or unicode.
        for ln in str(overview).splitlines():
            lines.append(ln)
    lines.append("  </Overview>")

    lines.append(xml_tag("WebUI", str(webui)))
    if has_value(template_url):
        lines.append(xml_tag("TemplateURL", str(template_url)))
    if has_value(icon):
        lines.append(xml_tag("Icon", str(icon)))

    if has_value(extra_params):
        lines.append(xml_tag("ExtraParams", str(extra_params)))
    if has_value(post_args):
        lines.append(xml_tag("PostArgs", str(post_args)))
    if has_value(cpuset):
        lines.append(xml_tag("CPUset", str(cpuset)))
    if has_value(donate_text):
        lines.append(xml_tag("DonateText", str(donate_text)))
    if has_value(donate_link):
        lines.append(xml_tag("DonateLink", str(donate_link)))
    if has_value(requires):
        lines.append(xml_tag("Requires", str(requires), indent=2))

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

    if has_value(tailscale_state_dir):
        lines.append(xml_tag("TailscaleStateDir", str(tailscale_state_dir)))
    lines.append("</Container>")
    lines.append("")  # newline at EOF

    out_dir = os.path.dirname(OUTPUT_XML)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(OUTPUT_XML, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))

    print(f"Wrote: {OUTPUT_XML}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
