import pygame, sys, os, random, time, player, Map, items, entity
clock = pygame.time.Clock()

from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init() # initiates pygame
pygame.mixer.set_num_channels(64)

pygame.display.set_caption('Pygame Platformer')

WINDOW_SIZE = (1880,1000)

screen = pygame.display.set_mode(WINDOW_SIZE,pygame.RESIZABLE) # initiate the window

display = pygame.Surface((300,200)) # used as the surface for rendering, which is scaled

air_timer = 0

jump_sound = pygame.mixer.Sound('Data/Sounds/jump.wav')
grass_sounds = [pygame.mixer.Sound('Data/Sounds/grass_0.wav'),pygame.mixer.Sound('Data/Sounds/grass_1.wav')]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)

pygame.mixer.music.load('Data/Sounds/music.wav')
#pygame.mixer.music.play(-1)

grass_sound_timer = 0

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

class game:
    def __init__(self):
        self.true_scroll = [0,0]
        self.scroll = self.true_scroll.copy()
        self.player = player.joueur_class()
        self.map = Map.map_class()
        self.img_size = 16
        self.items_list = items.item_load(Map.load_map(self.map.map_path),self.map.meta_name,self.map.meta_map) #liste des items dans le monde
        self.friend_list = entity.entity_load(Map.load_map(self.map.map_path),self.img_size)
        self.ennemi_list = entity.entity_load(Map.load_map(self.map.map_path),self.img_size, 'l')
        self.god_mod = 0
        self.actual_map = 1
        self.font = pygame.font.SysFont("Arial", 15)
        self.font2 = pygame.font.SysFont("Arial",13)

JEU = game()

while True: # game loop

    display.fill((146,244,255)) # du bleu ciel en fond

    #---Background---#

    if grass_sound_timer > 0:
        grass_sound_timer -= 1
    pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,300,80))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-JEU.scroll[0]*background_object[0],background_object[1][1]-JEU.scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display,(20,170,150),obj_rect)
        else:
            pygame.draw.rect(display,(15,76,73),obj_rect)

    #---Background---#

    #---Joueur---#

    JEU.true_scroll[0] += (JEU.player.player_rect.x-JEU.true_scroll[0]-156)/8
    JEU.true_scroll[1] += (JEU.player.player_rect.y-JEU.true_scroll[1]-106)/8
    JEU.scroll = JEU.true_scroll.copy()
    JEU.scroll[0] = int(JEU.scroll[0])
    JEU.scroll[1] = int(JEU.scroll[1])
    JEU.player.player_movement = [0,0] #la liste comprenant les mouvements du joueur
    JEU.player.animation()
    JEU.player.test_movement()
    JEU.player.player_rect,JEU.player.collisions = JEU.player.move(JEU.player.player_rect,JEU.player.player_movement,JEU.map.tile_rects,JEU.map.ramp_list) #regarde les commentaires de cette fonction tu comprendra surement
    if JEU.player.collision_types['bottom'] == True or JEU.player.collision_types['top'] == True:
        air_timer = 0
        JEU.player.vertical_momentum = 0
        if JEU.player.player_movement[0] != 0:
            if grass_sound_timer == 0:
                grass_sound_timer = 30
                random.choice(grass_sounds).play()
    else:
        air_timer += 1
    JEU.player.loot(JEU.items_list,JEU.scroll,JEU.img_size)
    if JEU.player.clicking[0]:
        JEU.player.attack(JEU.ennemi_list)
    if JEU.player.life <= 0:
        JEU.player.player_rect.height = 14
        if JEU.player.frame == JEU.player.anim_data_base['death'] and JEU.player.false_frame == JEU.player.anim_velocity['death']:
            time.sleep(0.5)
            break
    #---Joueur---#

    #---Entity---#

    for entity in JEU.friend_list:
        entity.distance(JEU.player.player_rect,JEU.img_size,JEU.scroll)
        entity.animation()
        if entity.speak():
            if JEU.player.action_button:
                entity.speaking = not entity.speaking

    #---Entity---#

    #---Ennemis---#

    for entity in JEU.ennemi_list:
        if not entity.life <= 0:
            entity.movement = [0,0]
            entity.animation()
            entity.move_to_player(JEU.player.player_rect)
            entity.rect, entity.collision = entity.move(JEU.map.tile_rects,JEU.map.ramp_list)
            JEU.player.take_damage(entity.test_attack(JEU.player.player_rect))
        if entity.collision['bottom'] == True or entity.collision['top'] == True:
            entity.vertical_momentum = 0
        if entity.rect.y > 700:
            JEU.ennemi_list.remove(entity)

    #---Ennemis---#

    #---Map---#


    for ennemi in JEU.ennemi_list:
         ennemi.actualised = False
    for item in JEU.items_list:
         item.actualised = False
    for entity in JEU.friend_list:
        entity.actualised = False
    JEU.map.game_map = Map.load_map(JEU.map.map_path)
    JEU.map.tile_rects = []
    JEU.map.meta_tile = []
    y = 0 #je met à 0 le y, soit la première 'ligne' de la map (en partant du haut)
    for layer in JEU.map.game_map: #je regarde ligne par ligne dans le fichier texte ou se trouve la map
        x = 0 #je met à 0 le x, soit le premier 'bloc' de la map (en partant de la droite)
        for tile in layer: #je regarde du coup 'bloc' par 'bloc' dans chacune des lignes
            if tile == 'i':
                for item in JEU.items_list:
                    if not item.actualised:
                        item.rect.x = x*JEU.img_size-JEU.scroll[0]
                        if item.animation > 30:
                            item.animation = item.animation + 1
                            item.rect.y = y*JEU.img_size-JEU.scroll[1] - 0.01
                            if item.animation > 60:
                                item.animation = 0
                        else:
                            item.animation = item.animation + 1
                            item.rect.y = y*JEU.img_size-JEU.scroll[1] + 0.01
                        item.actualised = True
                        if item.as_entity:
                            display.blit(item.img,(item.rect.x,item.rect.y))
                        else:
                            item.rect.x, item.rect.y = (-1000,0)
                        break
            if tile == 'r':
                if Map.meta_car(JEU.map.meta_map_path[:-1] + str(JEU.actual_map),(x,y)) == '2':
                    display.blit(pygame.transform.flip(pygame.image.load('Data/Images/ramps.png'),True, False),(x*JEU.img_size-JEU.scroll[0],y*JEU.img_size-JEU.scroll[1]))
                else:
                    display.blit(pygame.image.load('Data/Images/ramps.png'),(x*JEU.img_size-JEU.scroll[0],y*JEU.img_size-JEU.scroll[1]))
                JEU.map.ramp_list.append(Map.ramp_class(x,y,pygame.Rect(x*JEU.img_size,y*JEU.img_size,JEU.img_size,JEU.img_size),int(Map.meta_car(JEU.map.meta_map_path[:-1] + str(JEU.actual_map),(x,y)))))
            if tile in JEU.map.entity_list:
                for entity in JEU.friend_list:
                    if JEU.map.entity_list[tile] == entity.name:
                        display.blit(entity.img,(x*JEU.img_size-JEU.scroll[0] - (entity.img_size[0] - JEU.img_size),y*JEU.img_size-JEU.scroll[1] - (entity.img_size[1] - JEU.img_size)))
                for ennemi in JEU.ennemi_list:
                    if tile in ennemi.ennemi_list:
                        display.blit(JEU.map.image['0'],(x*JEU.img_size-JEU.scroll[0],y*JEU.img_size-JEU.scroll[1]))
            if not JEU.map.image[tile] == None:
                display.blit(JEU.map.image[tile],(x*JEU.img_size-JEU.scroll[0],y*JEU.img_size-JEU.scroll[1])) #j'affiche son image correspondante ("dirt_img")
            else:
                if tile != 'i' and tile != 'r' and not tile in JEU.map.entity_list:
                    display.blit(JEU.map.meta_image[Map.meta_car(JEU.map.meta_map_path[:-1] + str(JEU.actual_map),(x,y))],(x*JEU.img_size-JEU.scroll[0],y*JEU.img_size-JEU.scroll[1]))
            if tile not in JEU.map.no_physics_tile: #la je teste si la tuile ne fait pas partie des tuiles qui ne doivent pas avoirs de collisions
                JEU.map.tile_rects.append(pygame.Rect(x*JEU.img_size,y*JEU.img_size,JEU.img_size,JEU.img_size)) #là, je fait un rectangle au coordonées de la tuile qui aura une présence physique et j'ajoute ce rectangle dans une liste
            if tile in JEU.map.meta_tile_accept:
                JEU.map.meta_tile.append(pygame.Rect(x*JEU.img_size,y*JEU.img_size,JEU.img_size,JEU.img_size))
                if JEU.player.action_button:
                    JEU.player.action_button = not JEU.player.action_button
                    Map.look_at_meta(Map.load_map(JEU.map.meta_map_path[:-1] + str(JEU.actual_map)), JEU.player, tile)
            x += 1 #j'ajoute 1 au x pour vérifier la tuile suivante
        y += 1 # j'ajoute 1 au y pour vérifier la ligne suivante

    if JEU.god_mod == 1:
        JEU.map.tile_rects = []

    #---Map---#

    #---Inputs---#

    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                JEU.player.clicking[0] = True
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                JEU.player.clicking[0] = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_w:
                JEU.player.inv[0] = ""
                JEU.items_list.pop(0)
            if event.key == K_RIGHT:
                JEU.player.moving_right = True
            if event.key == K_LEFT:
                JEU.player.moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    jump_sound.play()
                    JEU.player.vertical_momentum = -5
            if event.key == K_e:
                JEU.player.action_button = True
        if event.type == KEYUP:
            if event.key == K_e:
                JEU.player.action_button = False
            if event.key == K_RIGHT:
                JEU.player.moving_right = False
            if event.key == K_LEFT:
                JEU.player.moving_left = False

    #---Inputs---#
    #---Other---#

    for i in range(len(JEU.player.inv)):
        text_label = JEU.font.render(str(JEU.player.inv_nbr[i]), True, (0, 0, 0))
        text_rect = text_label.get_rect(bottomright = WINDOW_SIZE)
        text_rect.x = 210+(18*i)
        text_rect.y = 180
        if not JEU.player.inv[i] == "":
            display.blit(JEU.player.inv[i].img,(210+(18*i),182))
        display.blit(text_label, text_rect)
    display.blit(JEU.player.inv_img,(208,180))
    display.blit(pygame.transform.flip(JEU.player.print_life(),True,False),(0,0))
    #display.blit(pygame.transform.flip(pygame.transform.scale(JEU.player.img,(17,32)),JEU.player.flip,False),(JEU.player.player_rect.x-JEU.scroll[0],JEU.player.player_rect.y-JEU.scroll[1]))
    display.blit(pygame.transform.flip(JEU.player.img,JEU.player.flip,False),(JEU.player.player_rect.x-JEU.scroll[0],JEU.player.player_rect.y-JEU.scroll[1]))
    for ennemi in JEU.ennemi_list:
        if not ennemi.life <= 0:
            display.blit(pygame.transform.flip(ennemi.img,ennemi.flip,False),(ennemi.rect.x-JEU.scroll[0],ennemi.rect.y-JEU.scroll[1]))
    for entity in JEU.friend_list:
        if entity.speak():
            display.blit(pygame.image.load('Data/Images/bubble.png'),(entity.rect.x*JEU.img_size+JEU.scroll[0],entity.rect.y*JEU.img_size+JEU.scroll[1]+100))
        if entity.name == 'mage' and entity.speaking:
            if JEU.player.action_button:
                JEU.player.action_button = False
                if len(entity.list_speach) == 1:
                    entity.speaking = False
                    entity.list_speach = entity.text()
                    entity.speach = entity.list_speach[0]
                    break
                else:
                    entity.list_speach.pop(0)
                    entity.speach = entity.list_speach[0]
            display.blit(pygame.image.load('Data/Images/big_bubble.png'),(0,141))
            text_label = JEU.font2.render(entity.speach,True,(0,0,0))
            text_rect = text_label.get_rect(bottomright = WINDOW_SIZE)
            text_rect.x = entity.rect.x + 10
            text_rect.y = entity.rect.y + 150
            display.blit(text_label, text_rect)
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)

    #---Other---#

#---Game Over---#

false_frame = 1
frame = 1
while True:

    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    if false_frame + 1 > 23:
        false_frame = 1
        frame = frame + 1
    else:
        false_frame = false_frame + 1
    if frame > 23:
        frame = 1

    screen.blit(pygame.transform.scale(pygame.image.load('Data/Images/game_over/' + str(frame) + '.gif'),WINDOW_SIZE),(0,0))
    pygame.display.update()

#---Game Over---#
