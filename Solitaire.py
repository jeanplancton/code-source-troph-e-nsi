import pyxel
from random import randint

pyxel.init(352, 350, title="Trophée de la NSI")
pyxel.load("solitaire_sprite-1.pyxres")


fin_du_jeu = None
espacement = 32

#creation du plateau=======================================================================
def creation_case(x,y):
    pos_x = x
    pos_y = y
    z = [pos_x,pos_y]
    c = [z,1]
    return c

def creation_ligne(numero_ligne):
    x = 136
    y = 40 + espacement * numero_ligne
    ligne = []
    espace = 0
    for i in range(3):
        espace = espacement * i
        case = creation_case(x + espace,y)
        ligne.append(case)
    return ligne

def creation_grande_ligne(numero_ligne):
    x = 40
    y = 136 + espacement * numero_ligne
    ligne = []
    espace = 0
    for i in range(9):
        espace = espacement * i
        case = creation_case(x + espace,y)
        ligne.append(case)
    return ligne


def creation_plateau():
    plateau = []
    ligne = []
    for i in range(3):
        ligne = creation_ligne(i)
        plateau += ligne
    for i in range(3):
        ligne = creation_grande_ligne(i)
        plateau += ligne
    for i in range(3):
        ligne = creation_ligne(6 + i)
        plateau += ligne
    return plateau


plateau = creation_plateau()
"""dans le plateau le tuple correspond au coordonné d'une case du plateau et le 1 precise si la case est prise, il devient 0 si elle est vide """
#class Solitaire=======================================================================
class Solitaire:

    def __init__(self,pos):
        self.pos_boule = pos
        self.x_boule = self.pos_boule[0]
        self.y_boule = self.pos_boule[1]
        self.boule_proche = True #true si la boule est entourée
        self.presence = True #verifie si la boule est ssu rle terrain mais est peut etre inutile
        self.selection = False # egale à 16 si selectionnée pour modifier le sprite
        self.boule_selectionne = False #permet de deplacer la boule si elle est selectionné
        self.deplacement_verif = [] #si vide deplacement impossible





    def affiche(self):
        if self.presence == True:
            pyxel.blt(self.x_boule,self.y_boule,0,0 + self.selection,0,16,16,0)

    def voisin(self):
        """donne les boules voisine de la boule selectionné
            sortie: liste des coordonné des boules voisine"""
        L = []
        C = []
        L.append([self.x_boule + 32,self.y_boule])
        L.append([self.x_boule - 32,self.y_boule])
        L.append([self.x_boule,self.y_boule + 32])
        L.append([self.x_boule,self.y_boule - 32])
        for case in plateau:
            for i in L:
                if i == case[0] and case[1] == 1:
                    C.append(i)
        return C


    def __repr__(self):
        return str(self.pos_boule)

def suppression():
    """supprimme la premiere boule selectionnée"""
    pos = [pyxel.mouse_x,pyxel.mouse_y]
    if len(boule_liste) == 45:
        for boule in boule_liste:
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                if pos[0] < boule.x_boule + 16 and pos[0] > boule.x_boule and pos[1] < boule.y_boule + 16 and pos[1] > boule.y_boule:
                    for i in range(len(plateau)):
                        if [boule.x_boule,boule.y_boule] == plateau[i][0]:
                            plateau[i][1] = 0
                    boule.presence = False
                    boule_liste.remove(boule)


def suppression_jeu(pos_depart,pos_new):
    """supprime la boule qui est entre l'anciene et la nouvelle position de la boule selctionné
        entrée : tuple des positions de la boule selectionnée"""
    x = pos_new[0] - pos_depart[0]
    y = pos_new[1] - pos_depart[1]
    pos = [pos_depart[0] + (x // 2),pos_depart[1] + (y // 2)]
    for boule in boule_liste:
        if [boule.x_boule,boule.y_boule] == pos:
            for i in range(len(plateau)):
                if [boule.x_boule,boule.y_boule] == plateau[i][0]:
                    plateau[i][1] = 0
            boule.presence = False
            boule_liste.remove(boule)




def deplacement():
    """deplace la boule selectionnée"""
    pos = [pyxel.mouse_x,pyxel.mouse_y]
    for boule in boule_liste:
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            if pos[0] < boule.x_boule + 16 and pos[0] > boule.x_boule and pos[1] < boule.y_boule + 16 and pos[1] > boule.y_boule:
                boule.selection = 16
            else:
                boule.selection = False
        boule.boule_selectionne = True
        pos_boule = boule.pos_boule
        for i in range(len(boule.deplacement_verif)):
            if boule.boule_selectionne == True and pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT) and boule.selection == 16:
                if pos[0] < boule.deplacement_verif[i][0] + 16 and pos[0] > boule.deplacement_verif[i][0] and pos[1] < boule.deplacement_verif[i][1] + 16 and pos[1] > boule.deplacement_verif[i][1]:
                    for i in range(len(plateau)):
                        if [boule.x_boule,boule.y_boule] == plateau[i][0]:
                            plateau[i][1] = 0
                        if pos[0] < plateau[i][0][0] + 16 and pos[0] > plateau[i][0][0] and pos[1] < plateau[i][0][1] + 16 and pos[1] > plateau[i][0][1]:
                            pos = plateau[i][0]
                            plateau[i][1] = 1
                            boule.selection = False
                            suppression_jeu(pos_boule,pos)
                    boule.x_boule,boule.y_boule = pos[0],pos[1]
                    boule.pos_boule = [boule.x_boule,boule.y_boule]
                    pyxel.play(0,2)
        boule.boule_selectionne = False



def fin_de_partie():
    """verifie si le joeur a atteind une situation de fin de jeu"""
    global fin_du_jeu
    compteur = 0
    for boule in boule_liste:
        x = boule.voisin()
        if x == []:
            boule.boule_proche = False
    for boule in boule_liste:
        if boule.boule_proche == False:
            compteur = compteur + 1
    if compteur == len(boule_liste):
        fin_du_jeu = False
    else:
        if len(boule_liste) == 1:
            fin_du_jeu = True


def verification_deplacement():
    """verifie si la boule est dans les conditions de deplacement"""
    C = []
    D = []
    for boule in boule_liste:
        boule.deplacement_verif = []
        if boule.selection == 16:
            C.append([boule.x_boule + 32 ,boule.y_boule])
            C.append([boule.x_boule ,boule.y_boule + 32])
            C.append([boule.x_boule - 32 ,boule.y_boule])
            C.append([boule.x_boule ,boule.y_boule - 32])
            D.append([boule.x_boule + 64 ,boule.y_boule])
            D.append([boule.x_boule ,boule.y_boule + 64])
            D.append([boule.x_boule - 64 ,boule.y_boule])
            D.append([boule.x_boule ,boule.y_boule - 64])
            for i in range(len(plateau)):
                for j in range(len(D)):
                    if C[j] == plateau[i][0] and plateau[i][1] == 1:
                        for e in range(len(plateau)):
                            if D[j] == plateau[e][0] and plateau[e][1] == 0:
                                boule.deplacement_verif.append(D[j])
                    for v in range(len(boule.deplacement_verif)):
                        if boule.deplacement_verif[v] == D[j]:
                                pyxel.blt(D[j][0],D[j][1],0,48,0,16,16,0)
                        elif boule.deplacement_verif[v] != D[j]:
                            if D[j] == plateau[i][0]:
                                pyxel.blt(D[j][0],D[j][1],0,32,0,16,16,0)


def ecran_victoire():
    """retourne les ecrans de victoire et de defaite"""
    global fin_du_jeu
    if fin_du_jeu == True:
        pyxel.bltm(0,0,0,516,0,352,350)
        pyxel.text(156, 175, 'victoire' , 11)
        #pyxel.play(0,1)
    if fin_du_jeu == False:
        pyxel.bltm(0,0,0,516,0,352,350)
        pyxel.text(156, 175, 'defaite' , 11)
        #pyxel.play(0,0)


#creation des objets bille ou boule

def creation_bille():
    liste = []
    for i in range(len(plateau)):
        bille = Solitaire(plateau[i][0])
        liste.append(bille)
    return liste


boule_liste = creation_bille()



def update():
    suppression()
    deplacement()
    fin_de_partie()

def draw():

    # vide la fenetre
    pyxel.cls(0)
    pyxel.mouse(True)
    pyxel.bltm(0,0,0,0,0,500,350)

    for bille in boule_liste:
            bille.affiche()

    verification_deplacement()
    ecran_victoire()


pyxel.run(update, draw)