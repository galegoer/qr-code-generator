import zlib

def create_png(matrix, scale=10, filename='checkerboard.png'):
    # Image dimensions
    width = len(matrix[0]) * scale
    height = len(matrix) * scale

    # Create the PNG header
    png_header = b'\x89PNG\r\n\x1a\n'

    # Create IHDR chunk
    ihdr_data = (width).to_bytes(4, 'big') + (height).to_bytes(4, 'big') + b'\x08\x02\x00\x00\x00'
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data).to_bytes(4, 'big')
    ihdr_chunk = b'\x00\x00\x00\x0dIHDR' + ihdr_data + ihdr_crc

    # Generate raw image data (RGB format)
    raw_data = bytearray()
    for row in matrix:
        for _ in range(scale):  # Repeat each row 'scale' times for scaling
            raw_data.append(0)  # Filter type byte
            for cell in row:
                color = (0, 0, 0) if cell == 1 else (255, 255, 255)
                raw_data.extend(color * scale)  # Repeat each color 'scale' times

    # Compress the image data
    compressed_data = zlib.compress(raw_data)
    idat_data = compressed_data
    idat_crc = zlib.crc32(b'IDAT' + idat_data).to_bytes(4, 'big')
    idat_chunk = len(idat_data).to_bytes(4, 'big') + b'IDAT' + idat_data + idat_crc

    # Create IEND chunk
    iend_chunk = b'\x00\x00\x00\x00IEND' + zlib.crc32(b'IEND').to_bytes(4, 'big')

    # Write all chunks to the file
    with open(filename, 'wb') as f:
        f.write(png_header)
        f.write(ihdr_chunk)
        f.write(idat_chunk)
        f.write(iend_chunk)

# Example usage
matrix = [
    [1, 0],
    [0, 1]
]
create_png(matrix)

def create_svg(matrix, scale=10, filename='checkerboard.svg'):
    # Image dimensions
    width = len(matrix[0]) * scale
    height = len(matrix) * scale

    # Start the SVG string
    svg_content = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
    ]

    # Generate rectangles for each cell
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            color = "black" if cell == 1 else "white"
            svg_content.append(
                f'<rect x="{x * scale}" y="{y * scale}" width="{scale}" height="{scale}" fill="{color}" />'
            )

    # Close the SVG tag
    svg_content.append('</svg>')

    # Write to the file
    with open(filename, 'w') as f:
        f.write("\n".join(svg_content))

# Example usage
matrix = [
    [1, 0],
    [0, 1]
]
create_svg(matrix)