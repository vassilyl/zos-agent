from typing import Optional
from pathlib import Path

try:
    from cairosvg import svg2png
except ImportError:
    raise ImportError("cairosvg is required. Install it with 'pip install cairosvg'.")

def render_svg_to_png(svg_path: str, png_path: Optional[str] = None, scale: float = 1.0) -> str:
    """
    Render an SVG file and save it as a PNG file.

    Args:
        svg_path (str): Path to the SVG file.
        png_path (Optional[str]): Path to save the PNG file. If None, saves as svg_path + '.png'.
        scale (float): Scale factor for the output PNG.

    Returns:
        str: Path to the saved PNG file.
    """
    svg_path = Path(svg_path)
    if not svg_path.exists():
        raise FileNotFoundError(f"SVG file not found: {svg_path}")

    if png_path is None:
        png_path = str(svg_path) + ".png"
    else:
        png_path = str(png_path)

    with open(svg_path, "rb") as svg_file:
        svg_data = svg_file.read()
        # Render to PNG in memory first
        import io
        from PIL import Image
        png_bytes = io.BytesIO()
        svg2png(bytestring=svg_data, write_to=png_bytes, scale=scale)
        png_bytes.seek(0)
        img = Image.open(png_bytes)
        # If image has alpha, paste on white background
        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
            bg.paste(img, mask=img.split()[-1])
            img = bg.convert("RGB")
        else:
            img = img.convert("RGB")
        img.save(png_path, format="PNG")

    return png_path
