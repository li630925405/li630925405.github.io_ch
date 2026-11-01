#!/usr/bin/env python3
"""Check that the generated blog works under its GitHub Pages project path."""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
BASE = "/li630925405.github.io_ch/"
HOST = "li630925405.github.io"


class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ("href", "src", "action", "poster", "data-src"):
            value = attrs.get(key)
            if value:
                self.links.append((value, True))
        if tag == "meta" and attrs.get("property", "").startswith("og:"):
            value = attrs.get("content")
            if value:
                self.links.append((value, attrs.get("property") != "og:image"))


def check():
    errors = []
    missing_metadata_images = set()
    pages = sorted(ROOT.rglob("*.html"))
    checked = 0
    for page in pages:
        text = page.read_text(encoding="utf-8")
        parser = PageLinks()
        parser.feed(text)
        name = page.relative_to(ROOT)
        for value, require_target in parser.links:
            url = urlsplit(value)
            if url.hostname == "example.com":
                errors.append(f"{name}: placeholder site URL {value}")
                continue
            if url.netloc and url.hostname != HOST:
                continue
            if not url.path.startswith("/"):
                continue
            checked += 1
            if not url.path.startswith(BASE):
                errors.append(f"{name}: URL escapes blog directory: {value}")
                continue
            local = ROOT / unquote(url.path[len(BASE):])
            if local.is_dir():
                local = local / "index.html"
            if not local.is_file():
                if require_target:
                    errors.append(f"{name}: URL has no local target: {value}")
                else:
                    missing_metadata_images.add(value)
        match = re.search(r"var CONFIG = (\{[^\n]+\});", text)
        if not match or json.loads(match.group(1)).get("root") != BASE:
            errors.append(f"{name}: theme root must be {BASE}")
    if errors:
        print(f"FAIL: {len(errors)} errors across {len(pages)} pages")
        print("\n".join(errors[:12]))
        return 1
    print(f"PASS: {len(pages)} pages, {checked} local URLs, and all theme roots")
    if missing_metadata_images:
        print(f"NOTE: {len(missing_metadata_images)} old article images referenced by metadata are missing from the repository")
    return 0


if __name__ == "__main__":
    sys.exit(check())
