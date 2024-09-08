import os
import pygame
from random import choice
from support import import_folder

class AnimationPlayer:
    def __init__(self):
        # Base path for graphics
        base_graphics_path = os.path.join('graphics', 'particles')
        
        self.frames = {
            # magic
            'flame': import_folder(os.path.join(base_graphics_path, 'flame', 'frames')),
            'aura': import_folder(os.path.join(base_graphics_path, 'aura')),
            'heal': import_folder(os.path.join(base_graphics_path, 'heal', 'frames')),
            
            # attacks 
            'claw': import_folder(os.path.join(base_graphics_path, 'claw')),
            'slash': import_folder(os.path.join(base_graphics_path, 'slash')),
            'sparkle': import_folder(os.path.join(base_graphics_path, 'sparkle')),
            'leaf_attack': import_folder(os.path.join(base_graphics_path, 'leaf_attack')),
            'thunder': import_folder(os.path.join(base_graphics_path, 'thunder')),

            # monster deaths
            'squid': import_folder(os.path.join(base_graphics_path, 'smoke_orange')),
            'raccoon': import_folder(os.path.join(base_graphics_path, 'raccoon')),
            'spirit': import_folder(os.path.join(base_graphics_path, 'nova')),
            'bamboo': import_folder(os.path.join(base_graphics_path, 'bamboo')),
            
            # leafs 
            'leaf': (
                import_folder(os.path.join(base_graphics_path, 'leaf1')),
                import_folder(os.path.join(base_graphics_path, 'leaf2')),
                import_folder(os.path.join(base_graphics_path, 'leaf3')),
                import_folder(os.path.join(base_graphics_path, 'leaf4')),
                import_folder(os.path.join(base_graphics_path, 'leaf5')),
                import_folder(os.path.join(base_graphics_path, 'leaf6')),
                self.reflect_images(import_folder(os.path.join(base_graphics_path, 'leaf1'))),
                self.reflect_images(import_folder(os.path.join(base_graphics_path, 'leaf2'))),
                self.reflect_images(import_folder(os.path.join(base_graphics_path, 'leaf3'))),
                self.reflect_images(import_folder(os.path.join(base_graphics_path, 'leaf4'))),
                self.reflect_images(import_folder(os.path.join(base_graphics_path, 'leaf5'))),
                self.reflect_images(import_folder(os.path.join(base_graphics_path, 'leaf6')))
            )
        }

    def reflect_images(self, frames):
        new_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, animation_type, pos, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
