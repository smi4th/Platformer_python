import pygame, sys, os, random,time
pygame.init()

class Items:
    def __init__(self,id):
        self.name = id
        self.img = pygame.image.load('Data/Images/items/' + id + '.png')
        self.rect = pygame.Rect(0,0,16,16)
        self.as_entity = True
        self.actualised = False
        self.animation = 30
        self.angle = 35
        self.damage = 0

def item_load(game_map,meta_name,meta_map):
    item_list = []
    y = 0 #je met à 0 le y, soit la première 'ligne' de la map (en partant du haut)
    for layer in game_map: #je regarde ligne par ligne dans le fichier texte ou se trouve la map
        x = 0 #je met à 0 le x, soit le premier 'bloc' de la map (en partant de la droite)
        for tile in layer: #je regarde du coup 'bloc' par 'bloc' dans chacune des lignes
            if tile == 'i':
                item_list.append(Items(meta_name[meta_map[y][x]]))
                item_list[-1].damage = 10
            x = x + 1
        y = y + 1
    return item_list
