
import argparse
from svg_renderer import render_svg_to_png
from png2latex import png_to_latex
import os
from pathlib import Path


def convert_svg(svg_path, png_path=None, scale=1.0):
    try:
        out_path = render_svg_to_png(svg_path, png_path, scale)
        print(f"PNG saved to: {out_path}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

def convert_png_to_latex(png_path, model_name=None):
    try:
        latex = png_to_latex(png_path, model_name)
        print(f"LaTeX for {png_path}:")
        print(latex)
        return latex
    except Exception as e:
        print(f"Error processing {png_path}: {e}")
        return None

def batch_png_to_latex(directory, model_name=None):
    dir_path = Path(directory)
    png_files = list(dir_path.glob("*.png"))
    if not png_files:
        print(f"No PNG files found in {directory}")
        return
    for png_file in png_files:
        print("-" * 40)
        convert_png_to_latex(str(png_file), model_name)
        print("-" * 40)

def main():
    parser = argparse.ArgumentParser(description="SVG to PNG and PNG to LaTeX converter.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    svg_parser = subparsers.add_parser("svg2png", help="Convert SVG to PNG.")
    svg_parser.add_argument("svg_path", help="Path to the SVG file.")
    svg_parser.add_argument("-o", "--output", dest="png_path", help="Path to save the PNG file. Default: <svg_path>.png", default=None)
    svg_parser.add_argument("-s", "--scale", dest="scale", type=float, help="Scale factor for the output PNG. Default: 1.0", default=1.0)

    png_parser = subparsers.add_parser("png2latex", help="Convert PNG to LaTeX.")
    png_parser.add_argument("png_path", help="Path to the PNG file.")
    png_parser.add_argument("-m", "--model", dest="model_name", help="pix2tex model name. Default: uses default model", default=None)

    batch_parser = subparsers.add_parser("batch-png2latex", help="Convert all PNGs in a directory to LaTeX.")
    batch_parser.add_argument("directory", help="Directory containing PNG files.")
    batch_parser.add_argument("-m", "--model", dest="model_name", help="pix2tex model name. Default: uses default model", default=None)

    args = parser.parse_args()

    if args.command == "svg2png":
        convert_svg(args.svg_path, args.png_path, args.scale)
    elif args.command == "png2latex":
        convert_png_to_latex(args.png_path, args.model_name)
    elif args.command == "batch-png2latex":
        batch_png_to_latex(args.directory, args.model_name)


if __name__ == "__main__":
    main()
