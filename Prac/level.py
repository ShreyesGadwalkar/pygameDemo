from support import *
import pygame
from map import *
from tile import Tile
from player import *


class Level:
    def __init__(self):
        #get the display surface 
        self.display_surface = pygame.display.get_surface()
        
        #setup sprites
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        #sprite setup
        self.create_map()
    
    def create_map(self):
        layouts = {
            "boundary": import_csv_layout("map/map_FloorBlocks.csv"),
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(WORLD_MAP):
                for col_index, col in enumerate(row):
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE
        #         if col == 'x':
        #             Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
        #         if col == 'p':
        #             self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)                    
        self.player = Player((2000, 1430), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        self.visible_sprites.draw(self.player)
        self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] / 2
        self.half_height = self.display_surface.get_size()[1] / 2
        self.offset = pygame.math.Vector2()

        self.floor_surface = pygame.image.load("art_assets/graphics/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def draw(self, player):

        #getting offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.y - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        #drawing sprites
        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)