import pygame
import os
import sys

fail = input()

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Program')
FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_screen():
    fon = load_image('fon.jpg')
    screen.blit(pygame.transform.scale(fon, (width, height)), (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self, x, y):
        if 0 <= self.rect.y + y < height and 0 <= self.rect.x + x < width and \
                level_map[(self.rect.y + y) // tile_height][(self.rect.x + x) // tile_width] in ('.', '@'):
            self.rect = self.rect.move(x, y)


clock = pygame.time.Clock()
start_screen()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_level(filename):
    global level_map
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


level_map = None
player, level_x, level_y = generate_level(load_level(fail))
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]:
            player.update(0, tile_height)
        if key[pygame.K_UP]:
            player.update(0, -tile_height)
        if key[pygame.K_LEFT]:
            player.update(-tile_width, 0)
        if key[pygame.K_RIGHT]:
            player.update(tile_width, 0)
    screen.fill((0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
terminate()
