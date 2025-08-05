import tempfile
import os
from pathlib import Path
from svg_renderer import render_svg_to_png

def test_render_svg_to_png_basic():
    svg_content = '''<svg height="100" width="100">
      <circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow" />
    </svg>'''
    with tempfile.TemporaryDirectory() as tmpdir:
        svg_path = Path(tmpdir) / "test.svg"
        png_path = Path(tmpdir) / "test.png"
        with open(svg_path, "w") as f:
            f.write(svg_content)
        out_path = render_svg_to_png(str(svg_path), str(png_path))
        assert os.path.exists(out_path)
        assert out_path == str(png_path)
        assert os.path.getsize(out_path) > 0


def test_render_svg_to_png_file_not_found():
    try:
        render_svg_to_png("/nonexistent/file.svg")
    except FileNotFoundError:
        pass
    else:
        assert False, "Expected FileNotFoundError"
