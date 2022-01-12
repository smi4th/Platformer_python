import pygame, sys, os, random, time, math

def entity_load(game_map, img_size,letter = 'm'):
    entity_list = []
    ennemi_list = []
    y = 0 #je met à 0 le y, soit la première 'ligne' de la map (en partant du haut)
    for layer in game_map: #je regarde ligne par ligne dans le fichier texte ou se trouve la map
        x = 0 #je met à 0 le x, soit le premier 'bloc' de la map (en partant de la droite)
        for tile in layer: #je regarde du coup 'bloc' par 'bloc' dans chacune des lignes
            if tile == 'm' == letter:
                entity_list.append(entity_class('mage'))
                entity_list[-1].anim_data_base = 30
                return entity_list
            if tile == 'l' == letter:
                ennemi_list.append(ennemi_class('gobelin'))
                ennemi_list[-1].rect.x = x*img_size
                ennemi_list[-1].rect.y = y*img_size - (ennemi_list[-1].img_size[1] - img_size)
                ennemi_list[-1].damage = 80
            x = x + 1
        y = y + 1
    return ennemi_list

class ennemi_class:
    def __init__(self,name):
        self.name = name
        self.img = pygame.image.load('Data/Images/' + name + '/idle/1.png')
        self.img_size = self.img.get_width(),self.img.get_height()
        self.rect = pygame.Rect(0,0,self.img_size[0],self.img_size[1])
        self.frame = 1
        self.false_frame = 1
        self.anim_data_base = 0
        self.distance_away = 0
        self.actualised = False
        self.action = 'idle'
        self.anim_data_base = {'idle':4,'run':4,'attack':7}
        self.anim_velocity = {'idle':10,'run':4,'attack':11}
        self.range = 80
        self.collision = {'top':False,'bottom':False,'right':False,'left':False}
        self.movement = [0,0]
        self.ennemi_list = ['l']
        self.flip = False
        self.range_attack = 16
        self.life = 10
        self.damage = 0
        self.vertical_momentum = 0

    def test_attack(self,player_rect):
        if self.frame == self.anim_data_base['attack']:
            if self.false_frame == self.anim_velocity['attack']:
                if self.rect.colliderect(player_rect):
                    return self.damage
        return 0

    def move_to_player(self, player_rect):
        if math.sqrt(((player_rect.x-self.rect.x)**2)+((player_rect.y-self.rect.y)**2)) < self.range_attack:
            self.action = 'attack'
        elif  math.sqrt(((player_rect.x-self.rect.x)**2)+((player_rect.y-self.rect.y)**2)) < self.range:
            if player_rect.x < self.rect.x:
                self.movement[0] -= 1
                self.flip = True
            if player_rect.x > self.rect.x:
                self.movement[0] += 1
                self.flip = False
            self.action = 'run'
        else:
            self.action = 'idle'

    def animation(self):
        if self.false_frame + 1 > self.anim_velocity[self.action]:
            self.false_frame = 1
            self.frame = self.frame + 1
        else:
            self.false_frame = self.false_frame + 1
        if self.frame > self.anim_data_base[self.action]:
            self.frame = 1
        self.img = pygame.image.load('Data/Images/' + self.name + '/' + self.action + '/' + str(self.frame) + '.png')

    def collision_test(self,tiles):
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)
        return collisions

    def tile_rect(self,t,tile_size):
        return pygame.Rect(t.pos[0] * tile_size, t.pos[1] * tile_size, tile_size, tile_size)

    def move(self,tiles,ramps):
        self.collision = {'top':False,'bottom':False,'right':False,'left':False}
        self.rect.x = self.rect.x + self.movement[0]
        collisions = self.collision_test(tiles)
        for tile in collisions:
            if self.movement[0] < 0:
                self.rect.x = tile.left + self.img_size[0]
                self.collision['right'] = True
            if self.movement[0] > 0:
                self.rect.x = tile.right
                self.collision['left'] = True
        self.movement[1] += self.vertical_momentum
        self.vertical_momentum += 0.2
        if self.vertical_momentum > 3:
            self.vertical_momentum = 3
        self.rect.y += self.movement[1]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[1] > 0:
                self.rect.bottom = tile.top
                self.collision['bottom'] = True
            elif self.movement[1] < 0:
                self.rect.top = tile.bottom
                self.collision['top'] = True
        """for ramp in ramps:
            hitbox = self.tile_rect(ramp,16)
            if self.rect.colliderect(hitbox):
                rel_x = self.rect.x - hitbox.x
                if ramp.ramp == 1:
                    pos_height = rel_x + self.rect.width
                elif ramp.ramp == 2:
                    pos_height = 16 - rel_x
                pos_height = min(pos_height,16)
                pos_height = max(pos_height,0)
                target_y = hitbox.y + 16 - pos_height
                if self.rect.bottom > target_y:
                    self.rect.bottom = target_y
                self.collision['bottom'] = False"""
        return self.rect, self.collision

class entity_class:
    def __init__(self,name):
        self.name = name
        self.img = pygame.image.load('Data/Images/' + name + '/1.png')
        self.img_size = self.img.get_width(),self.img.get_height()
        self.rect = pygame.Rect(0,0,self.img_size[0],self.img_size[1])
        self.frame = 1
        self.false_frame = 1
        self.anim_data_base = 0
        self.distance_away = 0
        self.actualised = False
        self.speaking = False
        self.list_speach = self.text()
        self.speach = self.list_speach[0]

    def text(self):
        a = []
        f = open('Data/speach/' + self.name + '/speach.txt','r').readlines()
        for i in range(len(f)):
            a.append(f[i][:-1])
        return a

    def speach_func(self):
        return text(str(self.speach),self.name)

    def distance(self,player_rect,img_size,scroll):
        self.distance_away = math.sqrt(((player_rect.x-self.rect.x)**2)+((player_rect.y-self.rect.y)**2)) - 372

    def speak(self):
        if -16 < self.distance_away < 16:
            return True
        return False

    def animation(self):
        if self.false_frame + 1 > self.anim_data_base:
            self.false_frame = 1
            if self.frame + 1 > self.anim_data_base/10:
                self.frame = 1
            else:
                self.frame = self.frame + 1
        else:
            self.false_frame = self.false_frame + 1
        self.img = pygame.image.load('Data/Images/' + self.name + '/' + str(self.frame) + '.png')
