import random
import csv
import pickle
from settings import MAP_SIZE
from ground_generator import terrain_type


def create_entities_map(map_size, heightmap, output_file=r'map\map_Entities.csv'):
        map_grid = [[-1 for _ in range(map_size[1])] for _ in range(map_size[0])]
        width, height = map_size
        map_grid[int(width/2)][int(height/2)]= 394
        # Loop through the expanded map
        for x in range(map_size[0]):
            for y in range(map_size[1]):
                height = heightmap[x, y]

                # Determine tile type based on height
                tile_type = terrain_type(height)


                # Place objects on non-water tiles
                if tile_type != 'water':
                    # 1% chance to place an object on the tile
                    if random.random() < 0.001:
                        if tile_type == 'grass':
                            map_grid[x][y] = random.choice([390, 391, 392])
                        elif tile_type in ['sand_grass', 'sand']:
                            map_grid[x][y] = random.choice([390, 391, 392])
                        elif tile_type == 'snow':
                            map_grid[x][y] = random.choice([390, 391, 392])

        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(map_grid)

def load_heightmap_from_pickle(filename):
    with open(filename, 'rb') as f:
        heightmap = pickle.load(f)
    return heightmap

def main():
    heightmap = load_heightmap_from_pickle('heightmap.pkl')
    create_entities_map(map_size = MAP_SIZE, heightmap = heightmap)

if __name__ == '__main__':
    main()