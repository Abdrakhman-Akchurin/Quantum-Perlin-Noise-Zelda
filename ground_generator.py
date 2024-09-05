import random
from PIL import Image
from settings import *
from map_generator import *

# Load the tilemap image
tilemap = Image.open(r'Quantum Perlin Noise Game\graphics\tilemap\Floor.png')
detailmap = Image.open(r'Quantum Perlin Noise Game\graphics\tilemap\details.png')




# Define tile coordinates for different heights (manually based on the tilemap)
# This is an example, and you'll need to adjust the coordinates based on your tilemap
tiles = {
    'sand': [(0, 4*64), (64, 4*64), (11*64, 5*64)],
    'sand_grass': [(0, 320), (64, 320),(64*2, 320), (64*3, 320), (64*4, 320)],
    'grass': [(0, 768), (64, 768),(64*2, 768), (64*3, 768), (64*4, 768)],
    'water': [(6*64, 768),(7*64, 768), (64*8, 768), (64*9, 768), (64*10, 768)],
    'snow': [(0, 1472), (64, 1472), (64*2, 1472), (64*3, 1472), (64*4, 1472)]
}

details = {
    'sand': [(0, 0), (64, 0), (2*64, 0), (3*64, 0), (4*64, 0), (5*64, 0), (6*64, 0), (7*64, 0), (8*64, 0), (9*64, 0), (10*64, 0), (11*64, 0), (12*64, 0), (13*64, 0), (14*64, 0), (15*64, 0)],
    'grass': [(0, 128), (64, 128), (2*64, 128), (3*64, 128), (4*64, 128), (5*64, 128), (6*64, 128), (7*64, 128)],
    'snow': [(0, 192), (64, 192), (2*64, 192), (3*64, 192), (4*64, 192), (5*64, 192), (6*64, 192), (7*64, 192)]
}

tile_size = 64  # Assuming each tile is 32x32 pixels

# Function to map height to tile
def height_to_tile(height):
    if height < 0.20:
        weights = [1, 3, 3, 3, 10]
        return random.choices(tiles['water'], weights=weights, k=1)[0]
    elif height < 0.40:
        weights = [1, 1, 10]
        return random.choices(tiles['sand'], weights=weights, k=1)[0]
    elif height < 0.60:
        weights = [10, 1, 1, 1, 1]
        return random.choices(tiles['sand_grass'], weights=weights, k=1)[0]
    elif height < 0.80:
        weights = [10, 3, 3, 3, 3]
        return random.choices(tiles['grass'], weights=weights, k=1)[0]
    else:
        weights = [10, 3, 3, 3, 3]
        return random.choices(tiles['snow'], weights=weights, k=1)[0]
    
def tile_to_transition(tile_coords, x, y):
    right = height_to_tile(heightmap[x, min(y+1, 199)])
    bottom = height_to_tile(heightmap[min(x+1, 199), y])
    left = height_to_tile(heightmap[x, max(y-1, 0)])
    top = height_to_tile(heightmap[max(x-1, 0), y])
    top_right = height_to_tile(heightmap[max(x-1, 0), min(y+1, 199)])
    top_left = height_to_tile(heightmap[max(x-1, 0), max(y-1, 0)])
    bottom_right = height_to_tile(heightmap[min(x+1, 199), min(y+1, 199)])
    bottom_left = height_to_tile(heightmap[min(x+1, 199),  max(y-1, 0)])

    if tile_coords in tiles['sand_grass']:
        if right in tiles['grass'] and top in tiles['grass']:
            return 0, (64*4, 320+64)
        elif right in tiles['grass'] and bottom in tiles['grass']:
            return 270, (64*4, 320+64)
        elif left in tiles['grass'] and bottom in tiles['grass']:
            return 180, (64*4, 320+64)
        elif left in tiles['grass'] and top in tiles['grass']:
            return 90, (64*4, 320+64)
        
        elif right in tiles['grass']:
            return 0, (64*3, 320+64)
        elif bottom in tiles['grass']:
            return 270, (64*3, 320+64)
        elif left in tiles['grass']:
            return 180, (64*3, 320+64)
        elif top in tiles['grass']:
            return 90, (64*3, 320+64)
        
        elif top_right in tiles['grass']:
            return 180, (64*5, 320+64)
        elif bottom_right in tiles['grass']:
            return 90, (64*5, 320+64)
        elif bottom_left in tiles['grass']:
            return 0, (64*5, 320+64)
        elif top_left in tiles['grass']:
            return 270, (64*5, 320+64)
            
        
    if tile_coords in tiles['snow']:
        if right in tiles['grass'] and top in tiles['grass']:
            return 0, (64, 1536)
        elif right in tiles['grass'] and bottom in tiles['grass']:
            return 270, (64, 1536)
        elif left in tiles['grass'] and bottom in tiles['grass']:
            return 180, (64, 1536)
        elif left in tiles['grass'] and top in tiles['grass']:
            return 90, (64, 1536)
        
        elif right in tiles['grass']:
            return 0, (0, 1536)
        elif bottom in tiles['grass']:
            return 270, (0, 1536)
        elif left in tiles['grass']:
            return 180, (0, 1536)
        elif top in tiles['grass']:
            return 90, (0, 1536)
        
        elif top_right in tiles['grass']:
            return 180, (64*2, 1536)
        elif bottom_right in tiles['grass']:
            return 90, (64*2, 1536)
        elif bottom_left in tiles['grass']:
            return 0, (64*2, 1536)
        elif top_left in tiles['grass']:
            return 270, (64*2, 1536)
        
    if tile_coords in tiles['water']:
        if right in tiles['sand'] and top in tiles['sand'] and left in tiles['sand']:
            return 0, (14*64, 0)
        elif right in tiles['sand'] and top in tiles['sand'] and bottom in tiles['sand']:
            return 270, (14*64, 0)
        elif right in tiles['sand'] and left in tiles['sand'] and bottom in tiles['sand']:
            return 180, (14*64, 0)
        elif left in tiles['sand'] and top in tiles['sand'] and bottom in tiles['sand']:
            return 90, (14*64, 0)

        elif right in tiles['sand'] and top in tiles['sand']:
            return 270, (11*64, 0)
        elif right in tiles['sand'] and bottom in tiles['sand']:
            return 180, (11*64, 0)
        elif left in tiles['sand'] and top in tiles['sand']:
            return 0, (11*64, 0)
        elif left in tiles['sand'] and bottom in tiles['sand']:
            return 90, (11*64, 0)
        
        elif right in tiles['sand']:
            return 270, (12*64, 0)
        elif bottom in tiles['sand']:
            return 180, (12*64, 0)
        elif left in tiles['sand']:
            return 90, (12*64, 0)
        elif top in tiles['sand']:
            return 0, (12*64, 0)
        
        elif top_right in tiles['sand']:
            return 90, (16*64, 64)
        elif bottom_right in tiles['sand']:
            return 0, (16*64, 64)
        elif bottom_left in tiles['sand']:
            return 270, (16*64, 64)
        elif top_left in tiles['sand']:
            return 180, (16*64, 64)
        
    if tile_coords in tiles['sand']:
        if right in tiles['sand_grass'] and top in tiles['sand_grass'] and left in tiles['sand_grass']:
            return 0, (3*64, 0)
        elif right in tiles['sand_grass'] and top in tiles['sand_grass'] and left in tiles['sand_grass']:
            return 270, (3*64, 0)
        elif right in tiles['sand_grass'] and top in tiles['sand_grass'] and left in tiles['sand_grass']:
            return 180, (3*64, 0)
        elif right in tiles['sand_grass'] and top in tiles['sand_grass'] and left in tiles['sand_grass']:
            return 90, (3*64, 0)

        elif right in tiles['sand_grass'] and top in tiles['sand_grass']:
            return 270, (0, 0)
        elif right in tiles['sand_grass'] and bottom in tiles['sand_grass']:
            return 180, (0, 0)
        elif left in tiles['sand_grass'] and top in tiles['sand_grass']:
            return 0, (0, 0)
        elif left in tiles['sand_grass'] and bottom in tiles['sand_grass']:
            return 90, (0, 0)
        
        elif right in tiles['sand_grass']:
            return 270, (64, 0)
        elif bottom in tiles['sand_grass']:
            return 180, (64, 0)
        elif left in tiles['sand_grass']:
            return 90, (64, 0)
        elif top in tiles['sand_grass']:
            return 0, (64, 0)
        
        elif top_right in tiles['sand_grass']:
            return 90, (5*64, 64)
        elif bottom_right in tiles['sand_grass']:
            return 0, (5*64, 64)
        elif bottom_left in tiles['sand_grass']:
            return 270, (5*64, 64)
        elif top_left in tiles['sand_grass']:
            return 180, (5*64, 64)
        
    return 0, tile_coords


def get_random_detail_tile(tile_coords):
    if tile_coords in tiles['sand_grass'] or tile_coords in tiles['sand']:
        return random.choice(details['sand'])
    elif tile_coords in tiles['grass']:
        return random.choice(details['grass'])
    elif tile_coords in tiles['snow']:
        return random.choice(details['snow'])
    



# Load the heightmap (assuming a 200x200 numpy array with values between 0 and 1)
heightmap= create_heightmap() # Replace with actual heightmap loading

# Create the ground image
ground_img = Image.new('RGBA', (200 * tile_size, 200 * tile_size))

for i in range(200):
    for j in range(200):
        tile_coords = height_to_tile(heightmap[i, j])
        rotate, tile_coords = tile_to_transition(tile_coords=tile_coords, x =i,y= j)
        tile = tilemap.crop((
            tile_coords[0], tile_coords[1],
            tile_coords[0] + tile_size, tile_coords[1] + tile_size
        ))
        tile = tile.rotate(rotate, expand = True)
        ground_img.paste(tile, (j * tile_size, i * tile_size))

        if random.random() < 0.10:  # 10% chance to place a detail
            detail_coords = get_random_detail_tile(tile_coords = tile_coords)
            if detail_coords is None:
                continue
            detail_tile = detailmap.crop((
                detail_coords[0], detail_coords[1],
                detail_coords[0] + tile_size, detail_coords[1] + tile_size
            ))
            ground_img.paste(detail_tile, (j * tile_size, i * tile_size), detail_tile)
# Save or show the ground image
ground_img.save(r'Quantum Perlin Noise Game\ground.png')