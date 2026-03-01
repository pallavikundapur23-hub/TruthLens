from __future__ import annotations

from typing import Any, Dict, List, Optional

from PIL import Image, ExifTags


_EXIF_TAGS = {v: k for k, v in ExifTags.TAGS.items()}


def _load_exif(image_path: str) -> Dict[str, Any]:
    """
    Load EXIF metadata from an image using Pillow.

    Returns a dict mapping human-readable EXIF tag names to values.
    If no EXIF is present or it cannot be read, an empty dict is returned.
    """
    try:
        with Image.open(image_path) as img:
            exif = getattr(img, "getexif", None)
            if exif is None:
                return {}

            exif_data = exif()  # type: ignore[operator]
            if not exif_data:
                return {}

            readable: Dict[str, Any] = {}
            for tag_id, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
                readable[tag_name] = value

            return readable
    except Exception:
        # Any issue reading EXIF (unsupported format, truncated file, etc.)
        # should not crash callers of check_metadata.
        return {}


def check_metadata(image_path: str) -> Dict[str, Any]:
    """
    Analyze EXIF metadata for an image.

    Returns a dictionary with:
      - metadata_status: "valid", "suspicious", or "missing"
      - camera_model: combined camera make/model string if available, else None
      - software: editing software tag if present, else None
      - suspicious_flags: list of string flags describing suspicious conditions
    """
    exif = _load_exif(image_path)
    suspicious_flags: List[str] = []

    if not exif:
        return {
            "metadata_status": "missing",
            "camera_model": None,
            "software": None,
            "suspicious_flags": ["no_exif_metadata"],
        }

    make: Optional[str] = exif.get("Make")
    model: Optional[str] = exif.get("Model")
    software: Optional[str] = exif.get("Software")

    # Build camera model string
    camera_model: Optional[str]
    if make or model:
        parts = [part for part in (make, model) if part]
        camera_model = " ".join(str(p).strip() for p in parts if str(p).strip())
    else:
        camera_model = None
        suspicious_flags.append("missing_camera_make_model")

    # Editing software tag
    if software:
        software_str = str(software)
        software_lower = software_str.lower()
        editing_keywords = [
            "photoshop",
            "lightroom",
            "gimp",
            "snapseed",
            "pixlr",
            "afterlight",
            "vsco",
            "facetune",
        ]
        if any(keyword in software_lower for keyword in editing_keywords):
            suspicious_flags.append("editing_software_detected")
        else:
            # normal camera software is not suspicious
            pass
    else:
        software_str = None

    if suspicious_flags:
        metadata_status = "suspicious"
    else:
        metadata_status = "valid"

    return {
        "metadata_status": metadata_status,
        "camera_model": camera_model,
        "software": software_str,
        "suspicious_flags": suspicious_flags,
    }
