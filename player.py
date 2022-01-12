import pygame, sys, os, random,time, math
pygame.init()

animation_frames = {}

def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1] #me permet d'avoir juste le nom de l'animation
    animation_frame_data = [] #je créé une base de donnée des frames
    n = 0 #me permet d'obtenir le numéro de l'animation (mon fichier est enregistré avec un numéro à la fin (ex : 'run_1'))
    for frame in frame_durations: #les 'frames_durations' sont de 7 soit toutes les 7 ticks dans frame_duration
        animation_frame_id = animation_name + '_' + str(n) #me premet d'obtenir le fameux nom de cette
        img_loc = path + '/' + animation_frame_id + '.png' #la, je reconstitu le chemni d'accès au fichier
        #un exemple de chemin d'accès : 'player_animations/idle/idle_0.png'
        animation_image = pygame.image.load(img_loc).convert() #permet de charger l'image de l'animation
        animation_image.set_colorkey((255,255,255)) #j'efface la couleur blanc (code RGB)
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def collision_test(rect,tiles):
    hit_list = [] #la liste des collisions avec les 'blocs'
    for tile in tiles: #je regarde chaque tuile qui a une présence physique
        if rect.colliderect(tile): #je regarde si elle est en collision avec quelque chose
            hit_list.append(tile) #si oui je l'ajoute à la liste de collion
    return hit_list #je retourne cette liste

def change_action(action_var,frame,new_value): #pour ne pas changer constament les images, ca pourrait faire laguer
    if action_var != new_value: #on regarde si l'actuel image est différente de la nouvelle
        action_var = new_value #si oui, alors l'actuel devient la nouvelle
        frame = 0 #et les frames sont remisent à 0
    return action_var,frame #et on return tout ca

class joueur_class:
    def __init__(self):
        self.name = 'hero'
        self.action_button = False
        self.moving_right = False #me sert à savoir si le joueur bouge vers la droite
        self.moving_left = False #me sert à savoir si le joueur bouge vers la gauche
        self.vertical_momentum = 0 #le gravité
        self.animation_frames = animation_frames #je le met dans un dico
        self.player_rect = pygame.Rect(192,153,21,38) #je créé un rectangle qui me permettera de modifier la position du joueur ainsi que de tester si il entre en collision avec quelque chose
        self.player_movement = [0,0] #la liste comprenant les mouvements du joueur
        self.collision_types = {'top':False,'bottom':False,'right':False,'left':False} #les différents moyen de rentrer en collision
        self.life_img = pygame.image.load('Data/Images/life_bar.png')
        self.life = 80
        self.invulnerable = 0

        #---souris---#
        self.clicking = [False,False]

        #---inventaire---#
        self.inv = ["","","","",""]
        self.inv_nbr = [0,0,0,0,0]
        self.inv_img = pygame.image.load('Data/Images/inv_img.png')

        #---animation---#
        self.anim_data_base = {'idle':10,'run':10,'attack':4,'death':10}
        self.anim_velocity = {'idle':10,'run':4,'attack':7,'death':10}
        self.action = 'idle' #l'action du joueur (uniquement pour les animations)
        self.frame = 1 #de base la frame du joueur est à 1
        self.false_frame = 1
        self.flip = False #me permettera de retourener l'image du joueur
        self.img = pygame.image.load('Data/Images/hero/Idle/1.png')
        self.img_size = self.img.get_width(),self.img.get_height()

    def animation(self):
        if self.false_frame + 1 > self.anim_velocity[self.action]:
            self.false_frame = 1
            self.frame = self.frame + 1
        else:
            self.false_frame = self.false_frame + 1
        if self.frame > self.anim_data_base[self.action]:
            self.frame = 1
        self.img = pygame.image.load('Data/Images/' + self.name + '/' + self.action + '/' + str(self.frame) + '.png')


    def attack(self, ennemi_list):
        for i in range(len(self.inv)):
            if self.inv[i] != "":
                if self.inv[i].name == 'sword':
                    self.action = 'attack'
                    collisions = collision_test(self.player_rect,ennemi_list)
                    for collid in collisions:
                        if self.frame == self.anim_data_base['attack']:
                            collid.life -= self.inv[i].damage


    def syncronisateur_de_realite(self,coord,scroll,img_size):
        return coord.x+scroll[0], coord.y+scroll[1]

    def loot(self,items,scroll,img_size):
        """
        items est une liste des items
        """
        for item in items:
            new_item = pygame.Rect(self.syncronisateur_de_realite(item.rect,scroll,img_size)[0],self.syncronisateur_de_realite(item.rect,scroll,img_size)[1],item.rect.width,item.rect.height)
            if self.player_rect.colliderect(new_item):
                for i in range(len(self.inv)):
                    if self.inv[i] != "": #élément non vide
                        if not item.name in self.inv[i].name:
                            self.inv[i] = item
                        else:
                            self.inv_nbr[i] = self.inv_nbr[i] + 1
                        item.as_entity = False
                    elif self.inv[i] == "" and item.as_entity == True:
                        self.inv[i] = item
                        item.as_entity = False
                        self.inv_nbr[i] = self.inv_nbr[i] + 1

    def access_inv(self,el):
        return self.inv[el]

    def test_movement(self):
        if self.moving_right == True: #si il bouge vers la droite
            self.action = 'run'
            self.player_movement[0] += 2 #j'ajoute 2pixels à la première case
            self.flip = False
        if self.moving_left == True:
            self.action = 'run'
            self.player_movement[0] -= 2 #si il va vers la gauche j'en enlève 2
            self.flip = True
        self.player_movement[1] += self.vertical_momentum
        self.vertical_momentum += 0.2
        if self.vertical_momentum > 3:
            self.vertical_momentum = 3
        if self.moving_right == False and self.moving_left == False:
            self.action = 'idle'

    def move(self,rect,movement,tiles,ramps): #rect = joueur, #tiles = la liste de tuiles avec une présence physique
        #movement = liste. movement[0] = mouvement en x par pixels, movement[1] =  mouvement en y par pixels
        self.collision_types = {'top':False,'bottom':False,'right':False,'left':False} #les différents moyen de rentrer en collision
        rect.x += movement[0] #je déplace le joueur en x par le mouvement par pixels inscrits
        hit_list = collision_test(rect,tiles) #je teste si le joueur est en collision avec une tuile
        for tile in hit_list: #je regarde tuile par tuile dans la liste des tuiles physique
            if movement[0] > 0: #si le mouvement x est superieur à 0 alors le joueur veut aller à droite
                rect.right = tile.left #honnetement, allez sur internet pour ça, flemme d'expliquer mdr
                self.collision_types['right'] = True #quelle type de collision a t-on
            elif movement[0] < 0: #tout le reste c'est la meme chose mais avec les 3 axes restants
                rect.left = tile.right
                self.collision_types['left'] = True
        rect.y += movement[1]
        hit_list = collision_test(rect,tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                self.collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                self.collision_types['top'] = True
        for ramp in ramps:
            pos_height = 0
            hitbox = self.tile_rect(ramp,16)
            if rect.colliderect(hitbox):
                rel_x = rect.x - hitbox.x
                if ramp.ramp == 1:
                    pos_height = rel_x + rect.width
                elif ramp.ramp == 2:
                    pos_height = 16 - rel_x

                pos_height = min(pos_height,16)
                pos_height = max(pos_height,0)

                target_y = hitbox.y + 16 - pos_height

                if rect.bottom > target_y:
                    rect.bottom = target_y

                self.collision_types['bottom'] = False
        return rect, self.collision_types #je renvoi la nouvelle position du joueur ainsi que les types de collisions, toujours utile au cas ou

    def tile_rect(self,t,tile_size):
        return pygame.Rect(t.pos[0] * tile_size, t.pos[1] * tile_size, tile_size, tile_size)

    def print_life(self):
        self.life_img = pygame.transform.chop(self.life_img,pygame.Rect(0,0,80 - self.life,0))
        return self.life_img

    def take_damage(self,amount):
        self.life = self.life - amount
        if self.life <= 0:
            self.action = 'death'
