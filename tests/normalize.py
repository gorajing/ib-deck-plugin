"""
PPTX normalization helper for determinism testing.

A raw PPTX is a ZIP archive containing XML files and metadata. Two renders of
the same spec will produce byte-different ZIPs because:

1. ZIP entry timestamps reflect file creation time
2. docProps/core.xml contains dcterms:created and dcterms:modified timestamps
3. docProps/app.xml may contain application version info
4. Shape IDs may be assigned incrementally (stable across runs but worth checking)

For determinism testing we extract the slide XML content (ppt/slides/slide*.xml
and ppt/slideLayouts/*, ppt/slideMasters/*) and hash that. Everything that
affects what the slide LOOKS LIKE goes into the hash. Metadata that doesn't
affect appearance is excluded.
"""
from __future__ import annotations

import hashlib
import io
import re
import zipfile


# Regexes to strip volatile attributes from XML
_TIMESTAMP_RE = re.compile(r'<dcterms:created[^>]*>[^<]*</dcterms:created>')
_MODIFIED_RE = re.compile(r'<dcterms:modified[^>]*>[^<]*</dcterms:modified>')
_LAST_MODIFIED_BY_RE = re.compile(r'<cp:lastModifiedBy[^>]*>[^<]*</cp:lastModifiedBy>')
_REVISION_RE = re.compile(r'<cp:revision[^>]*>[^<]*</cp:revision>')


def _strip_volatile(xml: str) -> str:
    """Remove volatile timestamp / metadata fields from an XML string."""
    xml = _TIMESTAMP_RE.sub('', xml)
    xml = _MODIFIED_RE.sub('', xml)
    xml = _LAST_MODIFIED_BY_RE.sub('', xml)
    xml = _REVISION_RE.sub('', xml)
    return xml


def pptx_content_hash(pptx_bytes: bytes) -> str:
    """
    Compute a stable hash of a PPTX's visible content.

    Extracts all files under ppt/ (slide XML, layouts, themes, masters) from
    the PPTX zip, strips volatile metadata, sorts by name, and returns a
    SHA-256 hex digest. Two renders of the same spec should produce the
    same hash.

    Metadata files (docProps/*, _rels/* at the top level) are excluded
    because they contain timestamps that legitimately vary.
    """
    hasher = hashlib.sha256()

    with zipfile.ZipFile(io.BytesIO(pptx_bytes)) as zf:
        # Sort entries by name for stable ordering
        entries = sorted(
            name for name in zf.namelist()
            if name.startswith("ppt/") and name.endswith(".xml")
        )

        for name in entries:
            content = zf.read(name).decode("utf-8", errors="replace")
            content = _strip_volatile(content)
            # Include the filename in the hash so reordering is detected
            hasher.update(name.encode("utf-8"))
            hasher.update(b"\0")
            hasher.update(content.encode("utf-8"))
            hasher.update(b"\0")

    return hasher.hexdigest()


def pptx_content_hash_from_path(path: str) -> str:
    """Convenience wrapper that reads a PPTX file from disk."""
    with open(path, "rb") as f:
        return pptx_content_hash(f.read())
