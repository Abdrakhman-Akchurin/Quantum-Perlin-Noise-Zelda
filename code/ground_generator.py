from quantum_perlin_noise import *
import numpy as np
import random
from PIL import Image
import pickle
from settings import MAP_SIZE

def create_heightmap():
    n = 10
    shots = 4**n

    L = get_L(n)
    Z = simplex(L,[10,10])

    grid = make_grid(n)
    state = height2state(Z,grid)

    counts = state2counts(state)
    Z = counts2height(counts,grid)

    Z, grid = quantum_tartan(Z,0.01)

    Z,grid = shuffle_height(Z,grid)

    samples = 300
    tartans = []
    for j in range(samples):
        randZ,_ =  shuffle_height(Z,grid)
        randZ = rotate_height(randZ,random.random())
        tartans.append( randZ )

    # Define the size of the height map
    reduced_size = (10, 10)

    # Generate random peaks and valleys
    peak_box = np.random.choice([True, False], size=reduced_size, p=[0.3, 0.7])
    valley_box = np.random.choice([True, False], size=reduced_size, p=[0.3, 0.7])

    # Create the height map based on the rules
    Zs = np.zeros(reduced_size)
    for y in range(reduced_size[1]):
        for x in range(reduced_size[0]):
            if not peak_box[x, y]:
                Zs[x, y] = 1  # Peak
            elif valley_box[x, y]:
                Zs[x, y] = 0  # Valley
            else:
                Zs[x, y] = 0.5  # Flat terrain

    Zs = blur(Zs,reduced_size,steps=1)

    size = [200,200]
    Z_islands = islands(size,Zs,tartans)
    
    return Z_islands

# Load the tilemap image
tilemap = Image.open(r'graphics\tilemap\Floor.png')
detailmap = Image.open(r'graphics\tilemap\details.png')

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

def terrain_type(height):
    if height < 0.0:
        # Water tile
        tile_type = 'water'
    elif height < 0.00:
        # Sand tile
        tile_type = 'sand'
    elif height < 0.3:
    # Sand-grass tile
        tile_type = 'sand_grass'
    elif height < 0.60:
        # Grass tile
        tile_type = 'grass'
    else:
        # Snow tile
        tile_type = 'snow'

    return tile_type

# Function to map height to tile
# Function to map height to tile using terrain_type
def height_to_tile(height):
    terrain = terrain_type(height)  # Get terrain type using the height

    # Dictionary of tiles and their respective weights for random selection
    tile_weights = {
        'water': ([1, 3, 3, 3, 10], tiles['water']),
        'sand': ([1, 1, 10], tiles['sand']),
        'sand_grass': ([10, 1, 1, 1, 1], tiles['sand_grass']),
        'grass': ([10, 3, 3, 3, 3], tiles['grass']),
        'snow': ([10, 3, 3, 3, 3], tiles['snow'])
    }

    # Select the appropriate tile list and weight
    weights, tile_list = tile_weights[terrain]

    # Randomly select a tile from the appropriate list based on weights
    return random.choices(tile_list, weights=weights, k=1)[0]
    
def tile_to_transition(heightmap, tile_coords, x, y):
    # Determine terrain type of adjacent tiles using terrain_type
    right = terrain_type(heightmap[x, min(y + 1, 199)])
    bottom = terrain_type(heightmap[min(x + 1, 199), y])
    left = terrain_type(heightmap[x, max(y - 1, 0)])
    top = terrain_type(heightmap[max(x - 1, 0), y])
    top_right = terrain_type(heightmap[max(x - 1, 0), min(y + 1, 199)])
    top_left = terrain_type(heightmap[max(x - 1, 0), max(y - 1, 0)])
    bottom_right = terrain_type(heightmap[min(x + 1, 199), min(y + 1, 199)])
    bottom_left = terrain_type(heightmap[min(x + 1, 199), max(y - 1, 0)])

    # Convert tile_coords to terrain type to match checks
    tile_type = terrain_type(heightmap[x, y])

    if tile_type in ['sand', 'sand_grass']:
        if right == 'grass' and top == 'grass' and left == 'grass' and bottom == 'grass':
            return 0, (14*64, 9*64)

    if tile_type == 'sand_grass':
        if right == 'grass' and top == 'grass':
            return 0, (64 * 4, 320 + 64)
        elif right == 'grass' and bottom == 'grass':
            return 270, (64 * 4, 320 + 64)
        elif left == 'grass' and bottom == 'grass':
            return 180, (64 * 4, 320 + 64)
        elif left == 'grass' and top == 'grass':
            return 90, (64 * 4, 320 + 64)

        elif right == 'grass':
            return 0, (64 * 3, 320 + 64)
        elif bottom == 'grass':
            return 270, (64 * 3, 320 + 64)
        elif left == 'grass':
            return 180, (64 * 3, 320 + 64)
        elif top == 'grass':
            return 90, (64 * 3, 320 + 64)

        elif top_right == 'grass':
            return 180, (64 * 5, 320 + 64)
        elif bottom_right == 'grass':
            return 90, (64 * 5, 320 + 64)
        elif bottom_left == 'grass':
            return 0, (64 * 5, 320 + 64)
        elif top_left == 'grass':
            return 270, (64 * 5, 320 + 64)

    if tile_type == 'snow':
        if right == 'grass' and top == 'grass':
            return 0, (64, 1536)
        elif right == 'grass' and bottom == 'grass':
            return 270, (64, 1536)
        elif left == 'grass' and bottom == 'grass':
            return 180, (64, 1536)
        elif left == 'grass' and top == 'grass':
            return 90, (64, 1536)

        elif right == 'grass':
            return 0, (0, 1536)
        elif bottom == 'grass':
            return 270, (0, 1536)
        elif left == 'grass':
            return 180, (0, 1536)
        elif top == 'grass':
            return 90, (0, 1536)

        elif top_right == 'grass':
            return 180, (64 * 2, 1536)
        elif bottom_right == 'grass':
            return 90, (64 * 2, 1536)
        elif bottom_left == 'grass':
            return 0, (64 * 2, 1536)
        elif top_left == 'grass':
            return 270, (64 * 2, 1536)

    if tile_type == 'water':
        if right == 'sand' and top == 'sand' and left == 'sand' and bottom == 'sand':
            return 0, (14*64, 3*64)

        elif right == 'sand' and top == 'sand' and left == 'sand':
            return 0, (14 * 64, 0)
        elif right == 'sand' and top == 'sand' and bottom == 'sand':
            return 270, (14 * 64, 0)
        elif right == 'sand' and left == 'sand' and bottom == 'sand':
            return 180, (14 * 64, 0)
        elif left == 'sand' and top == 'sand' and bottom == 'sand':
            return 90, (14 * 64, 0)

        elif right == 'sand' and top == 'sand':
            return 270, (11 * 64, 0)
        elif right == 'sand' and bottom == 'sand':
            return 180, (11 * 64, 0)
        elif left == 'sand' and top == 'sand':
            return 0, (11 * 64, 0)
        elif left == 'sand' and bottom == 'sand':
            return 90, (11 * 64, 0)

        elif right == 'sand':
            return 270, (12 * 64, 0)
        elif bottom == 'sand':
            return 180, (12 * 64, 0)
        elif left == 'sand':
            return 90, (12 * 64, 0)
        elif top == 'sand':
            return 0, (12 * 64, 0)

        elif top_right == 'sand':
            return 90, (16 * 64, 64)
        elif bottom_right == 'sand':
            return 0, (16 * 64, 64)
        elif bottom_left == 'sand':
            return 270, (16 * 64, 64)
        elif top_left == 'sand':
            return 180, (16 * 64, 64)

    if tile_type == 'sand':
        if right == 'grass' and top == 'grass' and left == 'grass' and bottom == 'grass':
            return 0, (3*64, 3*64)
        elif right == 'sand_grass' and top == 'sand_grass' and left == 'sand_grass':
            return 0, (3 * 64, 0)
        elif right == 'sand_grass' and bottom == 'sand_grass' and left == 'sand_grass':
            return 270, (3 * 64, 0)
        elif right == 'sand_grass' and left == 'sand_grass' and bottom == 'sand_grass':
            return 180, (3 * 64, 0)
        elif left == 'sand_grass' and top == 'sand_grass' and bottom == 'sand_grass':
            return 90, (3 * 64, 0)

        elif right == 'sand_grass' and top == 'sand_grass':
            return 270, (0, 0)
        elif right == 'sand_grass' and bottom == 'sand_grass':
            return 180, (0, 0)
        elif left == 'sand_grass' and top == 'sand_grass':
            return 0, (0, 0)
        elif left == 'sand_grass' and bottom == 'sand_grass':
            return 90, (0, 0)

        elif right == 'sand_grass':
            return 270, (64, 0)
        elif bottom == 'sand_grass':
            return 180, (64, 0)
        elif left == 'sand_grass':
            return 90, (64, 0)
        elif top == 'sand_grass':
            return 0, (64, 0)

        elif top_right == 'sand_grass':
            return 90, (5 * 64, 64)
        elif bottom_right == 'sand_grass':
            return 0, (5 * 64, 64)
        elif bottom_left == 'sand_grass':
            return 270, (5 * 64, 64)
        elif top_left == 'sand_grass':
            return 180, (5 * 64, 64)

    return 0, tile_coords



def get_random_detail_tile(tile_coords):
    if tile_coords in tiles['sand_grass'] or tile_coords in tiles['sand']:
        return random.choice(details['sand'])
    elif tile_coords in tiles['grass']:
        return random.choice(details['grass'])
    elif tile_coords in tiles['snow']:
        return random.choice(details['snow'])
    


def create_ground_image(heightmap, map_size):

    # Create the ground image
    ground_img = Image.new('RGBA', (map_size[0] * tile_size, map_size[1] * tile_size))

    for i in range(map_size[0]):
        for j in range(map_size[1]):
            tile_coords = height_to_tile(heightmap[i, j])
            rotate, tile_coords = tile_to_transition(heightmap=heightmap, tile_coords=tile_coords, x =i,y= j)
            tile = tilemap.crop((
                tile_coords[0], tile_coords[1],
                tile_coords[0] + tile_size, tile_coords[1] + tile_size
            ))
            tile = tile.rotate(rotate, expand = True)
            ground_img.paste(tile, (j * tile_size, i * tile_size))

    # Save or show the ground image
    ground_img.save(r'graphics\tilemap\ground.png')

def expand_heightmap(heightmap, original_size=200, border_size=50):
    new_size = original_size + 2 * border_size
    new_heightmap = {}
    
    # Fill the extended heightmap with new values (0 for water)
    for x in range(new_size):
        for y in range(new_size):
            # If within the original heightmap bounds, keep the original height value
            if border_size <= x < original_size + border_size and border_size <= y < original_size + border_size:
                new_heightmap[(x, y)] = heightmap[(x - border_size, y - border_size)]
            else:
                # Assign 0 (water) to the new border areas
                new_heightmap[(x, y)] = 0.0
    
    return new_heightmap

def save_heightmap_as_pickle(heightmap, filename):
    with open(filename, 'wb') as f:
        pickle.dump(heightmap, f)

def main():
    heightmap = simplex((200, 200), (10, 10))

    heightmap = expand_heightmap(heightmap, border_size= 50)

    # Save the heightmap to a JSON file
    save_heightmap_as_pickle(heightmap, 'heightmap.pkl')
    
    # Create and save the ground image
    create_ground_image(heightmap, MAP_SIZE)

if __name__ == '__main__':
    main()