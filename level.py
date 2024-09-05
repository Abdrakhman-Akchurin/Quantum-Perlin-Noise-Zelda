import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from ground_generator import *

class Level:
    def __init__(self):

        # get the display surface 
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()
    
    def calculate_scaling_factors(self, window_size, map_size):
        scale_x = window_size[0] / map_size[0]
        scale_y = window_size[1] / map_size[1]
        return min(scale_x, scale_y)  # Maintain aspect ratio by using the smallest scale factor
    
    def create_map(self):
        self.player = Player((2000, 2000), [self.visible_sprites], self.obstacles_sprites)
        for x in range(200):
            for y in range(200):
                if height_to_tile(heightmap[x, y]) not in tiles['water']:
                    if random.random() < 0.01:
                        if height_to_tile(heightmap[x, y]) in tiles['grass']:
                            img_name = random.choice(['01', '02', '03', '04', '09', '13', '14', '18', '19', '20'])
                        elif height_to_tile(heightmap[x, y]) in tiles['sand_grass'] or height_to_tile(heightmap[x, y]) in tiles['sand']:
                            img_name = random.choice(['08', '11', '12', '15', '16', '17'])
                        elif height_to_tile(heightmap[x, y]) in tiles['snow']:
                            img_name = random.choice(['0', '05', '06', '07', '10', '13', '14', '18', '19', '20'])
                        else: 
                            continue
                        
                        # Use a context manager to open the image
                        img_path = fr'Quantum Perlin Noise Game\graphics\objects\{img_name}.png'
                        with Image.open(img_path) as object_image:

                            # Convert to a format that supports transparency
                            object_image = object_image.convert('RGBA')
                            # Convert to a surface that Pygame can use
                            object_surface = pygame.image.fromstring(object_image.tobytes(), object_image.size, object_image.mode).convert_alpha()

                            x_scaled = TILESIZE * x
                            y_scaled = TILESIZE * y
                            Tile((x_scaled, y_scaled), [self.visible_sprites, self.obstacles_sprites], 'object', object_surface)


       

    def run(self):
        # update and draw the game 
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #creating the floor
        self.floor_surf = pygame.image.load(r'Quantum Perlin Noise Game\ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))

    def custom_draw(self, player):

        # getting the offset 
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #drawing the floor 
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        
        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
