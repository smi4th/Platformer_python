import pygame, sys, os, random,time
pygame.init()

def load_map(path): #pour loader la map dans une variable 'game_map'
    f = open(path + '.txt','r') #j'ouvre l'un des fichiers map
    data = f.read() #je met le contenu du fichier dans une variable 'data'
    f.close() #je ferme le fichier (!!! IMPORTANT !!!)
    data = data.split('\n') #je coupe les retours à la ligne
    game_map = [] #je créé la fameuse variable 'game_map'
    for row in data: #pour chaque ligne dans data,
        game_map.append(list(row)) #, j'ajoute cette ligne dans data
    return game_map #je retourne la valeur

def img(e,second = False):
    if not second:
        return pygame.image.load('Data/Images/' + e + '.png')
    else:
        return pygame.image.load('Data/Images/items/' + e + '.png')

def meta_car(path,coord, letter = None):
    f = open(path + '.txt','r') #j'ouvre l'un des fichiers map
    data = f.read() #je met le contenu du fichier dans une variable 'data'
    f.close() #je ferme le fichier (!!! IMPORTANT !!!)
    data = data.split('\n') #je coupe les retours à la ligne
    game_map = [] #je créé la fameuse variable 'game_map'
    for row in data: #pour chaque ligne dans data,
        game_map.append(list(row)) #, j'ajoute cette ligne dans data
    y = 0
    if not coord == None:
        for b_layer in game_map:
            x = 0
            for b_tile in b_layer:
                if y == coord[1] and x == coord[0]:
                    return b_tile
                x = x + 1
            y = y + 1
    else:
        for b_layer in game_map:
            x = 0
            for b_tile in b_layer:
                if b_tile == letter:
                    return (x,y)
                x = x + 1
            y = y + 1

class ramp_class:
    def __init__(self,x,y,rect,r = 1):
        self.rect = rect
        self.ramp = r
        self.pos = [x,y]
class map_class:
    def __init__(self):
        self.map_path = 'Data/Maps/map_1' #le chemin d'accès aux maps
        self.game_map = load_map(self.map_path)
        self.nb_map = len(os.listdir('Data/Maps')) - 1
        self.nbr_map = 1 #me sert à savoir nous sommes à quel map (la 1, la 2,...)
        self.no_physics_tile = ['0','i','r','m','l'] #la liste des tuiles non physiques
        self.tile_rects = [] #la liste de tuiles qui ont une existance physique
        self.image = {'l':None,'m':None,'g':img('grass'),'d':img('dirt'),'0':img('air'),'e':None,'i':None,'r':None}
        self.ramp_list = []

        #---Meta---#
        self.meta_image = {'s':img('stick',True),'i':img('sword',True)}
        self.meta_name = {'s':'stick','i':'sword'}
        self.meta_map_path = 'Data/Maps/Meta/map_1'
        self.meta_map = load_map(self.meta_map_path)
        self.meta_tile = []
        self.meta_tile_accept = ['e','i']

        #---Entity---#
        self.entity_list = {'m':'mage','l':'gobelin'}

def look_at_meta(meta_map, player, type):
    indice = 0
    y = 0
    for b_layer in meta_map:
        x = 0
        for b_tile in b_layer:
            if b_tile == '1':
                if type == 'e':
                    player.player_rect.y = player.player_rect.y - 64
            x += 1
        y += 1
    return False
