from quantum_perlin_noise import *
import numpy as np

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
