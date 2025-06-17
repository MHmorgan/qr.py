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
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer, GappedSquareModuleDrawer, SquareModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image


def create_qr_code(data: str, output_path: Path) -> None:
    """
    Create a QR code from the given data and save it to the specified path.
    
    Args:
        data: The data to encode in the QR code (typically a URL)
        output_path: Path where the QR code image will be saved
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
    
    # Create the image
    img = qr.make_image(fill_color="black", back_color="white")
    
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
        rgb_img = Image.new('RGB', img.size, 'white')
        if img.mode == 'P':
            img = img.convert('RGBA')
        rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = rgb_img
    
    # Save the image
    try:
        img.save(output_path, format=save_format)
        print(f"QR code successfully saved to: {output_path}")
    except Exception as e:
        print(f"Error saving QR code: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main function to handle CLI arguments and generate QR code."""
    parser = argparse.ArgumentParser(
        description="Generate a QR code from a URL and save it to a file.",
        epilog="Supported formats: PNG, JPEG, BMP, GIF, TIFF, WEBP, ICO"
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
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
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
    create_qr_code(args.url, output_path)


if __name__ == "__main__":
    main()

