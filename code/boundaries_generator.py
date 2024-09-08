import csv
from settings import MAP_SIZE

def erase_boundaries(map_size, square_size=200, output_file=r'map\map_FloorBlocks.csv'):
    # Initialize the map with -1 values
    map_grid = [[-1 for _ in range(map_size[1])] for _ in range(map_size[0])]
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(map_grid)


def create_boundaries(map_size, square_size=200, output_file=r'map\map_FloorBlocks.csv'):
    # Initialize the map with -1 values
    map_grid = [[-1 for _ in range(map_size[1])] for _ in range(map_size[0])]

    # Calculate starting and ending indices for the 200x200 square
    start_x = (map_size[0] - square_size) // 2
    start_y = (map_size[1] - square_size) // 2
    end_x = start_x + square_size
    end_y = start_y + square_size

    # Set the boundary outside the square to 0
    for x in range(start_x - 1, end_x + 1):
        map_grid[x][start_y - 2] = 0  # Top side of the square boundary
        map_grid[x][end_y + 1] = 0  # Bottom side of the square boundary

    for y in range(start_y - 1, end_y + 1):
        map_grid[start_x - 2][y] = 0  # Left side of the square boundary
        map_grid[end_x + 1][y] = 0  # Right side of the square boundary

    # Write the boundary map to a CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(map_grid)


def main():
    create_boundaries(map_size= MAP_SIZE, square_size=200)

if __name__ == "__main__":
    main()