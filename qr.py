#!/usr/bin/env python3
"""
QR Code Generator Script

Creates a QR code from a given URL and saves it to a specified file.
The output format is automatically detected from the file extension.
"""

import argparse
import sys
from pathlib import Path
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    RoundedModuleDrawer, 
    CircleModuleDrawer, 
    GappedSquareModuleDrawer, 
    SquareModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer
)
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image, ImageColor


def parse_color(color_str: str) -> tuple[int, int, int]:
    """
    Parse color string and return a valid RGB color tuple.
    Supports hex colors (#RRGGBB), named colors, and RGB tuples.
    
    Args:
        color_str: Color string to parse
        
    Returns:
        RGB color tuple (R, G, B)
    """
    # Remove any whitespace
    color_str = color_str.strip()
    
    # Check if it's an RGB tuple like "255,0,0"
    if ',' in color_str and not color_str.startswith('#'):
        try:
            rgb = tuple(int(x.strip()) for x in color_str.split(','))
            if len(rgb) == 3 and all(0 <= x <= 255 for x in rgb):
                return rgb
        except ValueError:
            pass
    
    # Use PIL's ImageColor to parse hex colors and named colors
    try:
        # This handles hex colors (#RRGGBB, #RGB) and named colors (red, blue, etc.)
        rgb = ImageColor.getrgb(color_str)
        return rgb
    except ValueError as e:
        print(f"Error: Invalid color '{color_str}'. Using black as fallback.", file=sys.stderr)
        return (0, 0, 0)


def create_qr_code(
    data: str, 
    output_path: Path,
    style: str = "square",
    fill_color: str = "black",
    back_color: str = "white"
) -> None:
    """
    Create a QR code from the given data and save it to the specified path.
    
    Args:
        data: The data to encode in the QR code (typically a URL)
        output_path: Path where the QR code image will be saved
        style: Style of QR code modules (square, rounded, dots, gapped, vertical, horizontal)
        fill_color: Color of the QR code modules
        back_color: Background color
    """
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR code (1 is the smallest)
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,  # Size of each box in pixels
        border=4,  # Border size in boxes
    )
    
    # Add data to QR code
    qr.add_data(data)
    qr.make(fit=True)
    
    # Parse colors to RGB tuples
    fill = parse_color(fill_color)
    back = parse_color(back_color)
    
    # Select module drawer based on style
    module_drawers = {
        'square': SquareModuleDrawer(),
        'rounded': RoundedModuleDrawer(),
        'dots': CircleModuleDrawer(),
        'gapped': GappedSquareModuleDrawer(),
        'vertical': VerticalBarsDrawer(),
        'horizontal': HorizontalBarsDrawer()
    }
    
    module_drawer = module_drawers.get(style, SquareModuleDrawer())
    
    # Create the image with styling
    if style != 'square':
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            color_mask=SolidFillColorMask(front_color=fill, back_color=back)
        )
    else:
        # Use simple image for square style (faster)
        img = qr.make_image(fill_color=fill, back_color=back)
    
    # Determine the format from file extension
    file_extension = output_path.suffix.lower()
    
    # Map common extensions to PIL format names
    format_map = {
        '.jpg': 'JPEG',
        '.jpeg': 'JPEG',
        '.png': 'PNG',
        '.bmp': 'BMP',
        '.gif': 'GIF',
        '.tiff': 'TIFF',
        '.tif': 'TIFF',
        '.webp': 'WEBP',
        '.ico': 'ICO',
    }
    
    # Get the format or default to PNG
    save_format = format_map.get(file_extension, 'PNG')
    
    # Handle format-specific requirements
    if save_format == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
        # Convert RGBA to RGB for JPEG
        rgb_img = Image.new('RGB', img.size, back)
        if img.mode == 'P':
            img = img.convert('RGBA')
        rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = rgb_img
    
    # Save the image
    try:
        img.save(output_path, format=save_format)
        print(f"QR code successfully saved to: {output_path}")
        print(f"Style: {style}, Fill: {fill_color}, Background: {back_color}")
    except Exception as e:
        print(f"Error saving QR code: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main function to handle CLI arguments and generate QR code."""
    parser = argparse.ArgumentParser(
        description="Generate a QR code from a URL and save it to a file.",
        epilog="Supported formats: PNG, JPEG, BMP, GIF, TIFF, WEBP, ICO\n"
               "Colors: hex (#RRGGBB), named (red, blue), or RGB (255,0,0)",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'url',
        help='The URL or text to encode in the QR code'
    )
    
    parser.add_argument(
        'file_output',
        help='Output file path (format detected from extension)'
    )
    
    parser.add_argument(
        '-s', '--style',
        choices=['square', 'rounded', 'dots', 'gapped', 'vertical', 'horizontal'],
        default='square',
        help='Style of QR code modules (default: square)'
    )
    
    parser.add_argument(
        '-f', '--fill-color',
        default='black',
        help='Color of QR code modules (default: black). Supports hex (#RRGGBB), named colors, or RGB (255,0,0)'
    )
    
    parser.add_argument(
        '-b', '--back-color',
        default='white',
        help='Background color (default: white). Supports hex (#RRGGBB), named colors, or RGB (255,0,0)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.1.0'
    )
    
    args = parser.parse_args()
    
    # Convert output path to Path object
    output_path = Path(args.file_output)
    
    # Check if the output directory exists
    output_dir = output_path.parent
    if output_dir and not output_dir.exists():
        print(f"Error: Output directory does not exist: {output_dir}", file=sys.stderr)
        sys.exit(1)
    
    # Generate the QR code
    create_qr_code(
        args.url, 
        output_path,
        style=args.style,
        fill_color=args.fill_color,
        back_color=args.back_color
    )


if __name__ == "__main__":
    main()
