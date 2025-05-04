import os

def create_tile_config(rows, cols, tile_width, tile_height, output_dir="."):
    """
    Create a TileConfiguration.txt file for a grid of images.
    
    Args:
        rows (int): Number of rows in the grid
        cols (int): Number of columns in the grid
        tile_width (float): Width of each tile in pixels
        tile_height (float): Height of each tile in pixels
        output_dir (str): Directory to save the configuration file
    """
    config_lines = [
        "# Tile coordinates are in index space, not physical space",
        "dim = 2",
        ""
    ]
    
    for row in range(rows):
        for col in range(cols):
            x = col * tile_width
            y = row * tile_height
            filename = f"tile_{row*cols + col}.nrrd"
            config_lines.append(f"{filename};;({x}, {y})")
    
    config_path = os.path.join(output_dir, "TileConfiguration.txt")
    with open(config_path, 'w') as f:
        f.write('\n'.join(config_lines))
    
    print(f"Created TileConfiguration.txt in {output_dir}")

# Example usage:
# create_tile_config(rows=5, cols=4, tile_width=309.35, tile_height=189.39) 