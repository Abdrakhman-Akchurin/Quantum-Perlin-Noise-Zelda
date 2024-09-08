from ground_generator import *
from objects_generator import *
from boundaries_generator import *
from entities_generator import *
from grass_generator import *
from settings import MAP_SIZE

def generate_level(map_size, square_size, terrain_type):
    # Generate the ground image
    if terrain_type =='simplex':
        heightmap = simplex((square_size, square_size), (10, 10))
    elif terrain_type =='quantum':
        heightmap = create_heightmap()

    # Save the heightmap to a JSON file
    save_heightmap_as_pickle(heightmap, 'heightmap.pkl')
    
    # Create and save the ground image
    create_ground_image(heightmap, map_size)

    # Create the boundaries map
    erase_boundaries(map_size= map_size, square_size=square_size)

    # Create the objects map
    create_objects_map(map_size = map_size, heightmap = heightmap)

    # Create the entities map
    create_entities_map(map_size = map_size, heightmap = heightmap)

    # Create the grass map
    create_grass_map(map_size = map_size, heightmap = heightmap)

def main():
    generate_level(map_size = MAP_SIZE, square_size=200, terrain_type='quantum')

if __name__ == '__main__':
    main()