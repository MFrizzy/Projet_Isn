#BOMBERMAN#

### Importations ###

from tkinter import*
from random import*
from winsound import *


### Initialisation de la fenêtre du menu ###

fen=Tk()
fen.title("Menu")
can=Canvas(fen, width =550, height =550)
can.pack(side=TOP,padx=5,pady=5)

### Importation image ###

herbe=PhotoImage(file="herbe.png") # Importation de l'image de fond (herbe.jpg)
jeufini=PhotoImage(file="gameover.png")
rejouer=PhotoImage(file="rejouer.png")
quitter=PhotoImage(file="quitter.png")
vie_rouge=PhotoImage(file="vie_rouge.png")
vie_bleue=PhotoImage(file="vie_bleue.png")
recharge_bonus=PhotoImage(file="bonus_recharge.png")
Bombe1=PhotoImage(file="bomberouge.png")
Bombe2=PhotoImage(file="bombebleue.png")
blocs=PhotoImage(file="blocs.png")
briques=PhotoImage(file="briques.png")
explosionbleue1=PhotoImage(file='explosionbleue1.png')
explosionbleue2=PhotoImage(file='explosionbleue2.png')
explosionbleue3=PhotoImage(file='explosionbleue3.png')
explosionrouge1=PhotoImage(file='explosionrouge1.png')
explosionrouge2=PhotoImage(file='explosionrouge2.png')
explosionrouge3=PhotoImage(file='explosionrouge3.png')
joueur1=PhotoImage(file="joueur1.png") # Importe l'image du joueur 1
joueur2=PhotoImage(file="joueur2.png") # Importe l'image du joueur 2
Bombe_bonus=PhotoImage(file="bonus_range.png")
blanc=PhotoImage(file="blanc.png")
vie_bonus=PhotoImage(file="vie.png")
MENU=PhotoImage(file="menu.png")

### Musique d'ambiance arcade ###

PlaySound("musique.wav", SND_ASYNC)

## Vies et scores ##

scorej1,scorej2=0,0
x,y=1,1
pvj1=3 # Points de vie du joueur 1
pvj2=3 # Points de vie du joueur 2

### Premiere définition des variables de bombes ###

xj,yj=0,0
xj2,yj2=500,500
range_bombe1=0
range_bombe2=0
nb_bombes1=1
nb_bombes2=1
x,y=0,0
gamestarted=False
can.create_image(2,2,image=MENU,anchor=NW,tags="menu")

def menu(event):
    # En entrée     :event permet de détecter le clic de la souris.
    #                On regarde la position du clic pour créer des espaces cliquables, pour déterminer des boutons.
    # En sortie     :Rien
    # Effet de bord :Dans la première condition, le clic démarre la partie,
    #                dans la deuxième, on quitte le jeu.
    global x,y,jouer
    x,y=event.x,event.y # Permet d'utiliser le clic de la souris
    if 107<=event.x<=443 and 160<=event.y<=200 and gamestarted==False: # Vérification:le clic de la souris est-il sur l'image nouvelle partie?
        startgame()
    if 107<=event.x<=443 and 230<=event.y<=270 and gamestarted==False: # Vérification:le clic de la souris est-il sur l'image quitter?
        fen.destroy() # Destruction de la fenêtre pour quitter le jeu

### Initialisation de la fenêtre de jeu ###

def startgame():
    # En entrée     : Aucune entrée
    # En sortie     : Aucune sortie
    # Effet de bord : Création d'un canvas (can) dans lequel s'affiche le jeu
    #                 et affichage du background ,et des barres de vie dans le second canvas.
    global gamestarted,score,id_joueur1,id_joueur2
    gamestarted=True
    can.delete(ALL) # Effaçage de ce qui est contenu dans le canvas can
    can.create_image(0,0,image=herbe,anchor=NW,tags="bg") # Appel de l'image contenue dans la variable herbe pour l'afficher à l'écran
    fen.title('BOMBERMAN') # Changement du titre de la fenêtre
    dessiner_map() # Appel de la fonction qui pose les briques et les blocs
    personnages()  # Appel de la fonction qui affiche les joueurs
    id_joueur1=can.find_withtag('perso')[0] # Récupération de l'id des joueurs (réutilisé dans d'autres fonctions)
    id_joueur2=can.find_withtag('perso2')[0]
    score=Canvas(fen,width=550,height=200,bg="white") # Création du canvas score
    score.pack(side=BOTTOM) # Placement de score en dessous du canvas principal
    score.create_text(70,75,text="Joueur1") # Création d'un texte (Joueur1 et 2) devant les barres de vie des joueurs
    score.create_text(70,125,text="Joueur2")
    score.create_image(100,50,image=vie_rouge,anchor=NW) # Placement des différents coeurs sur le canvas score
    score.create_image(150,50,image=vie_rouge,anchor=NW) 
    score.create_image(200,50,image=vie_rouge,anchor=NW)
    score.create_image(100,100,image=vie_bleue,anchor=NW)
    score.create_image(150,100,image=vie_bleue,anchor=NW)
    score.create_image(200,100,image=vie_bleue,anchor=NW) 
    score.create_image(250,50,image=Bombe1,anchor=NW)  # Appel de l'image bombe pour indiquer le nombre de bombes du joueur 1
    score.create_image(250,100,image=Bombe2,anchor=NW) # Idem joueur 2
    score.create_text(500,68,text="Portée") 
    score.create_text(500,82,text="Bombe")
    score.create_text(500,118,text="Portée")
    score.create_text(500,132,text="Bombe")
    score.create_text(540,75,text="1")
    score.create_text(540,125,text="1")



def enleve_vie(joueur):
    # En entrée     : Le joueur concerné par le retrait du point de vie.
    # En sortie     : Aucune sortie.
    # Effet de bord : Le joueur perd un point de vie, et on voit à l'écran, dans le canvas score (situé en bas)
    #                 que la barre de vie est modifiée.
    #                 Fait apparaître un écran « Game over », si un joueur n'a plus de vie,
    #                 proposant de rejouer une partie ou bien de quitter via la fonction perdu.
    global pvj1,pvj2,score,id_joueur1,id_joueur2
    if joueur==1: # Vérifie s'il s'agit du joueur 1 ou 2
        pvj1-=1   # et décrémente sa variable de vie de 1
    elif joueur==2:
        pvj2-=1
    if pvj1==2:
        score.create_rectangle(100,50,150,100,fill="white")# Premier carré de la barre de vie de j1
    if pvj1==1:                                            # Création d'un carré blanc pour le recouvrir
        score.create_rectangle(150,50,200,100,fill="white")# Idem pour le deuxièmre carré de j1
    if pvj1==0:
        score.create_rectangle(200,50,250,100,fill="white")# Troisième carré j1
        can.delete(id_joueur1)
        can.create_image(100,225,image=jeufini,anchor=NW) # Images : Gameover 350*100 
        can.create_image(100,335,image=rejouer,anchor=NW) #          Rejouer 100*50
        can.create_image(350,335,image=quitter,anchor=NW) #          Quitter 100*50
        can.bind("<Button-1>",perdu) # Appel du clic de la souris, pour intéragir avec la fonction menu
        can.create_text(270,305,text='Le joueur 2 a gagné', fill='white')
    if pvj2==2:
        score.create_rectangle(100,100,150,150,fill="white")# Idem pour le joueur 2
    if pvj2==1:
        score.create_rectangle(150,100,200,150,fill="white")
    if pvj2==0:
        score.create_rectangle(200,100,250,150,fill="white")
        can.delete(id_joueur2)
        can.create_image(100,225,image=jeufini,anchor=NW) # Images : Gameover 350*100 
        can.create_image(100,335,image=rejouer,anchor=NW) #          Rejouer 100*50
        can.create_image(350,335,image=quitter,anchor=NW) #          Quitter 100*50
        can.bind("<Button-1>",perdu) # Appel du clic de la souris, pour intéragir avec la fonction menu
        can.create_text(270,305,text='Le joueur 1 a gagné', fill='white')

def rajoute_vie(joueur):
    # En entrée     : Le joueur concerné par le rajout du point de vie.
    # En sortie     : Aucune sortie.
    # Effet de bord : Incrémente de 1 la variabe de vie du joueur concerné
    #                 Fait apparaitre un coeur en plus dans le canvas de score
    global pvj1,pvj2,score
    if joueur==1: # Vérification de quel joueur il s'agit et incrémente sa variable de vie
        pvj1+=1
    elif joueur==2:
        pvj2+=1
    if pvj1==4: # Vérification empéchant le joueur 1 d'avoir 4 vies
        pvj1-=1
    if pvj1==3:
        score.create_image(100,50,image=vie_rouge,anchor=NW) # Rajoute un 3ème coeur au joueur 1 dans le canvas score
    if pvj1==2:
        score.create_image(150,50,image=vie_rouge,anchor=NW) # Rajoute un 2ème coeur au joueur 1 dans le canvas score
    if pvj2==4: # Vérification empéchant le joueur 2 d'avoir 4 vies
        pvj2-=1
    if pvj2==3:
        score.create_image(100,100,image=vie_bleue,anchor=NW)# Rajoute un 3ème coeur au joueur 2 dans le canvas score  
    if pvj2==2:
        score.create_image(150,100,image=vie_bleue,anchor=NW)# Rajoute un 2ème coeur au joueur 2 dans le canvas score

## Ecran de game over ##

def perdu(event):
    # En entrée     : Event (comme dans la fonction menu)
    # En sortie     : Aucune sortie
    # Effet de bord : Permet de déterminer si un joueur a perdu, et réinitialise toutes les variables telles que la vie des personnages, 
    #                 leur nombre de bombes ainsi que la portée de l'explosion des bombes.
    global x,y,pvj1,pvj2,xj,yj,xj2,yj2,range_bombe1,range_bombe2,nb_bombes1,nb_bombes2
    x,y=event.x,event.y
    if 350<=event.x<=450 and 335<=event.y<=385:
        fen.quit() # Fait quitter le jeu
    if 100<=event.x<=200 and 335<=event.y<=385:
        print("rejouer?")
        score.destroy() # Détruit le canvas des scores
    # Réinitialisation des variables des joueurs
        pvj1=3
        pvj2=3
        range_bombe1=0 # Portée des bombes
        range_bombe2=0
        nb_bombes1=1 # Nombre de bombes
        nb_bombes2=1
        xj,yj=0,0 # Coordonnées joueurs
        xj2,yj2=500,500
        startgame() # Redémarre le jeu

### Creation map ###

def dessiner_map():
    # En entrée     : Aucune entrée
    # En sortie     : Aucune sortie
    # Effet de bord : Création d'une map composé des briques déstructibles et de blocs indestructibles
    #                 avec 2 point de spawn de joueur en haut à gauche et en bas à droite
    global x,y
    for i in range(-1,12):
        for j in range(-1,12,12):
            ajouter_bloc(i,j)
    for i in range(-1,12,12):
        for j in range(0,12):
            ajouter_bloc(i,j)
    for i in range(1,10,2):
        for j in range(1,10,2):
            ajouter_bloc(i,j)
    for j in range(0,11,1):
        for i in range(2,9,2):
            ajouter_brique(i,j)
    for j in range(0,11,2):
        for i in range(3,8,2):
            ajouter_brique(i,j)
    for i in range(0,11,10):
        for j in range(2,9,1):
            ajouter_brique(i,j)
    for i in range(1,10,8):
        for j in range(2,9,2):
            ajouter_brique(i,j)
    ajouter_brique(9,0)
    ajouter_brique(10,0)
    ajouter_brique(10,1)
    ajouter_brique(0,9)
    ajouter_brique(0,10)
    ajouter_brique(1,10)
    
## Briques ##
    
def ajouter_brique(x,y):
    # En entrée     : x et y respectivement l'abcisse et l'odonnée de la brique
    # En sortie     : Aucune sortie
    # Effet de bord : Pose une image de la brique aux coordonnées indiqués avec le tag 'briques'
    can.create_image(x*50,y*50,image=briques,anchor=NW,tags="briques")

## Blocs ##

def ajouter_bloc(x,y):
    # En entrée     : x et y respectivement l'abcisse et l'ordonnée du bloc
    # En sortie     : Aucune sortie
    # Effet de bord : Pose une image du bloc aux coordonnées indiqués avec le tag 'blocs'
    can.create_image(x*50,y*50,image=blocs,anchor=NW,tags="blocs")

### Bombes ###

def bombe1(event):
    # En entrée     : Event
    # En sortie     : Aucune sortie
    # Effet de bord : Création d'une 'bombe' à la position du joueur 1,
    #                 puis explosion au bout de 2,5 seconde
    global nb_bombes1
    if nb_bombes1>0:
        can.create_image(xj,yj,anchor=NW,image=Bombe1,tags='Bombe1')
        a=xj
        b=yj
        nb_bombes1-=1
        can.after(2500,explosion,a,b,1)

def bombe2(event):
    # En entrée     : Event
    # En sortie     : Aucune sortie
    # Effet de bord : Création d'une 'bombe' à la position du joueur 2,
    #                 puis explosion au bout de 2,5 seconde
    global nb_bombes2
    if nb_bombes2>0:
        can.create_image(xj2,yj2,anchor=NW,image=Bombe2,tags='Bombe2')
        a=xj2
        b=yj2
        nb_bombes2-=1
        can.after(2500,explosion,a,b,2)


def explosion(x,y,joueur):
    # En entrée     : x et y respectivement l'abcisse et l'ordonnée du bonus et le joueur qui a posé la bombe
    # En sortie     : Aucune sortie
    # Effet de bord : Explose les briques qui sont dans la portée de l'explosion de la bombe
    #                 Dessine les animations d'explosion et les fait disparaitre
    #                 Enleve une vie au joueur qui est dans la portée de la bombe
    #                 Fait apparaitre aléatoirement des bonus à l'endroit de l'explosion
    global range_bombe1,range_bombe2,nb_bombes1,nb_bombes2,id_joueur1,id_joueur2
    destroy=[]
    if joueur==1:
        bonus=range_bombe1 # On assigne a la variable bonus la valeur du bonus de portée du joueur 1
        nb_bombes1+=1      # On incrémente de 1 le nombre maximal de bombe que le joueur 1 peut poser
    elif joueur==2:
        bonus=range_bombe2 # On assigne a la variable bonus la valeur du bonus de portée du joueur 2
        nb_bombes2+=1      # On incrémente de 1 le nombre maximal de bombe que le joueur 2 peut poser
    a=0
    # On définit des booléans qui deviennent vrai lorsque l'explosion rencontre un obstacle dans la direction concernée
    explosion_bas=False
    explosion_droite=False
    explosion_haut=False
    explosion_gauche=False
    case_bombe=can.find_overlapping(x,y,x+50,y+50)
    for i in range(len(case_bombe)):
        if id_joueur1==case_bombe[i]: # On vérifie si le joueur 1 est sur la bombe
            enleve_vie(1) 
        elif id_joueur2==case_bombe[i]: # On vérifie si le joueur 2 est sur la bombe
            enleve_vie(2)
    # Les commentaires qui suivent sont aussi valables pour toutes les boucles while de cette fonction
    while explosion_bas==False and a<=bonus:
        for i in range(len(can.find_overlapping(x,y+(a+1)*50,x+50,y+51+a*50))):
            for j in range(len(can.find_withtag('briques'))):
                if can.find_overlapping(x,y+(a+1)*50,x+50,y+51+a*50)[i]==can.find_withtag('briques')[j]: # On vérifie si c'est brique
                    explosion_bas=True # on arrete la boucle while
                    xb=can.bbox(can.find_withtag('briques')[j])[0]
                    yb=can.bbox(can.find_withtag('briques')[j])[1]
                    bonus_bombe(xb,yb) # Apparition du bonus de portée de la bombe
                    bonus_vie(xb,yb) # Apparition du bonus de vie
                    bonus_recharge(xb,yb) # Apparition du bonus de bombe maximal
                    if joueur==2:
                        can.create_image(xb,yb,anchor=NW,image=explosionbleue3,tags='explosionbleue') # Affichage de l'animation de l'explosion du joueur 2
                    elif joueur==1:
                        can.create_image(xb,yb,anchor=NW,image=explosionrouge3,tags='explosionrouge') # Affichage de l'animation de l'explosion du joueur 1
                    destroy.append(can.find_withtag('briques')[j])
            for k in range(len(can.find_withtag('blocs'))):
                if can.find_overlapping(x,y+(a+1)*50,x+50,y+51+a*50)[i]==can.find_withtag('blocs')[k]: # On vérifie si c'est un bloc
                    explosion_bas=True # On arrete la boucle while
            if id_joueur1==can.find_overlapping(x,y+(a+1)*50,x+50,y+51+a*50)[i] and joueur==1: # On vérifie si le joueur 1 est dans la portée de la bombe
                enleve_vie(1) # On enleve un coeur au joueur 1
                can.create_image(x,y+(a+1)*50,anchor=NW,image=explosionrouge3,tags='explosionrouge') # On affiche l'animation de l'explosion sur le joueur 1
            elif id_joueur1==can.find_overlapping(x,y+(a+1)*50,x+50,y+51+a*50)[i] and joueur==2: # On vérifie si le joueur 1 est dans la portée de la bombe
                enleve_vie(1) # On enleve un coeur au joueur 1
                can.create_image(x,y+(a+1)*50,anchor=NW,image=explosionbleue3,tags='explosionbleue')
            elif id_joueur2==can.find_overlapping(x,y+(a+1)*50,x+50,y+51+a*50)[i] and joueur==1: # On vérifie si le joueur 2 est dans la portée de la bombe
                enleve_vie(2) # On enleve un coeur au joueur 2
                can.create_image(x,y+(a+1)*50,anchor=NW,image=explosionrouge3,tags='explosionrouge')# On affiche l'animation de l'explosion sur le joueur 2
            elif id_joueur2==can.find_overlapping(x,y+(a+1)*50,x+50,y+51+a*50)[i] and joueur==2: # On vérifie si le joueur 2 est dans la portée de la bombe
                enleve_vie(2) # On enleve un coeur au joueur 2
                can.create_image(x,y+(a+1)*50,anchor=NW,image=explosionbleue3,tags='explosionbleue')# On affiche l'animation de l'explosion sur le joueur 2
        if len(can.find_overlapping(x,y+(a+1)*50,x+50,y+51+a*50))==1 and joueur==2: # S'il n'y a que l'image de fond on affiche l'animation de l'explotion
            can.create_image(x,y+(a+1)*50,anchor=NW,image=explosionbleue3,tags='explosionbleue')
        elif len(can.find_overlapping(x,y+(a+1)*50,x+50,y+51+a*50))==1 and joueur==1:
            can.create_image(x,y+(a+1)*50,anchor=NW,image=explosionrouge3,tags='explosionrouge')
        a+=1
    a=0
    while explosion_droite==False and a<=bonus:      
        for i in range(len(can.find_overlapping(x+(a+1)*50,y,x+51+50*a,y+50))):
            for j in range(len(can.find_withtag('briques'))):
                if can.find_overlapping(x+(a+1)*50,y,x+51+50*a,y+50)[i]==can.find_withtag('briques')[j]:
                    explosion_droite=True
                    xb=can.bbox(can.find_withtag('briques')[j])[0]
                    yb=can.bbox(can.find_withtag('briques')[j])[1]
                    bonus_bombe(xb,yb)
                    bonus_vie(xb,yb)
                    bonus_recharge(xb,yb)
                    if joueur==2:
                        can.create_image(xb,yb,anchor=NW,image=explosionbleue2,tags='explosionbleue')
                    elif joueur==1:
                        can.create_image(xb,yb,anchor=NW,image=explosionrouge2,tags='explosionrouge')
                    destroy.append(can.find_withtag('briques')[j])
            for k in range(len(can.find_withtag('blocs'))):
                if can.find_overlapping(x+(a+1)*50,y,x+51+50*a,y+50)[i]==can.find_withtag('blocs')[k]:
                    explosion_droite=True
            if id_joueur1==can.find_overlapping(x+(a+1)*50,y,x+51+50*a,y+50)[i] and joueur==1:
                enleve_vie(1)
                can.create_image(x+(a+1)*50,y,anchor=NW,image=explosionrouge2,tags='explosionrouge')
            elif id_joueur1==can.find_overlapping(x+(a+1)*50,y,x+51+50*a,y+50)[i] and joueur==2:
                enleve_vie(1)
                can.create_image(x+(a+1)*50,y,anchor=NW,image=explosionbleue2,tags='explosionbleue')
            elif id_joueur2==can.find_overlapping(x+(a+1)*50,y,x+51+50*a,y+50)[i] and joueur==1:
                enleve_vie(2)
                can.create_image(x+(a+1)*50,y,anchor=NW,image=explosionrouge2,tags='explosionrouge')
            elif id_joueur2==can.find_overlapping(x+(a+1)*50,y,x+51+50*a,y+50)[i] and joueur==2:
                enleve_vie(2)
                can.create_image(x+(a+1)*50,y,anchor=NW,image=explosionbleue2,tags='explosionbleue')
        if len(can.find_overlapping(x+(a+1)*50,y,x+51+50*a,y+50))==1 and joueur==2:
            can.create_image(x+(a+1)*50,y,anchor=NW,image=explosionbleue2,tags='explosionbleue')
        elif len(can.find_overlapping(x+(a+1)*50,y,x+51+50*a,y+50))==1 and joueur==1:
            can.create_image(x+(a+1)*50,y,anchor=NW,image=explosionrouge2,tags='explosionrouge')
        a+=1
    a=0
    while explosion_haut==False and a<=bonus:
        for i in range(len(can.find_overlapping(x,y-(a+1)*50,x+50,y-1-a*50))):
            for j in range(len(can.find_withtag('briques'))):
                if can.find_overlapping(x,y-(a+1)*50,x+50,y-1-a*50)[i]==can.find_withtag('briques')[j]:
                    explosion_haut=True
                    xb=can.bbox(can.find_withtag('briques')[j])[0]
                    yb=can.bbox(can.find_withtag('briques')[j])[1]
                    bonus_bombe(xb,yb)
                    bonus_vie(xb,yb)
                    bonus_recharge(xb,yb)
                    if joueur==2:
                        can.create_image(xb,yb,anchor=NW,image=explosionbleue3,tags='explosionbleue')
                    elif joueur==1:
                        can.create_image(xb,yb,anchor=NW,image=explosionrouge3,tags='explosionrouge')
                    destroy.append(can.find_withtag('briques')[j])
            for k in range(len(can.find_withtag('blocs'))):
                if can.find_overlapping(x,y-(a+1)*50,x+50,y-1-a*50)[i]==can.find_withtag('blocs')[k]:
                    explosion_haut=True
            if id_joueur1==can.find_overlapping(x,y-(a+1)*50,x+50,y-1-a*50)[i] and joueur==1:
                enleve_vie(1)
                can.create_image(x,y-(a+1)*50,anchor=NW,image=explosionrouge3,tags='explosionrouge')
            elif id_joueur1==can.find_overlapping(x,y-(a+1)*50,x+50,y-1-a*50)[i] and joueur==2:
                enleve_vie(1)
                can.create_image(x,y-(a+1)*50,anchor=NW,image=explosionbleue3,tags='explosionbleue')
            elif id_joueur2==can.find_overlapping(x,y-(a+1)*50,x+50,y-1-a*50)[i] and joueur==1:
                enleve_vie(2)
                can.create_image(x,y-(a+1)*50,anchor=NW,image=explosionrouge3,tags='explosionrouge')
            elif id_joueur2==can.find_overlapping(x,y-(a+1)*50,x+50,y-1-a*50)[i] and joueur==2:
                enleve_vie(2)
                can.create_image(x,y-(a+1)*50,anchor=NW,image=explosionbleue3,tags='explosionbleue')
        if len(can.find_overlapping(x,y-(a+1)*50,x+50,y-1-a*50))==1 and joueur==2:
            can.create_image(x,y-(a+1)*50,anchor=NW,image=explosionbleue3,tags='explosionbleue')
        elif len(can.find_overlapping(x,y-(a+1)*50,x+50,y-1-a*50))==1 and joueur==1:
            can.create_image(x,y-(a+1)*50,anchor=NW,image=explosionrouge3,tags='explosionrouge')
        a+=1
    a=0
    while explosion_gauche==False and a<=bonus:
        for i in range(len(can.find_overlapping(x-1-a*50,y,x-(a+1)*50,y+50))):
            for j in range(len(can.find_withtag('briques'))):
                if can.find_overlapping(x-1-a*50,y,x-(a+1)*50,y+50)[i]==can.find_withtag('briques')[j]:
                    explosion_gauche=True
                    xb=can.bbox(can.find_withtag('briques')[j])[0]
                    yb=can.bbox(can.find_withtag('briques')[j])[1]
                    bonus_bombe(xb,yb)
                    bonus_vie(xb,yb)
                    bonus_recharge(xb,yb)
                    if joueur==2:
                        can.create_image(xb,yb,anchor=NW,image=explosionbleue2,tags='explosionbleue')
                    elif joueur==1:
                        can.create_image(xb,yb,anchor=NW,image=explosionrouge2,tags='explosionrouge')
                    destroy.append(can.find_withtag('briques')[j])
            for k in range(len(can.find_withtag('blocs'))):
                if can.find_overlapping(x-1-a*50,y,x-(a+1)*50,y+50)[i]==can.find_withtag('blocs')[k]:
                    explosion_gauche=True
            if id_joueur1==can.find_overlapping(x-1-a*50,y,x-(a+1)*50,y+50)[i] and joueur==1:
                enleve_vie(1)
                can.create_image(x-(a+1)*50,y,anchor=NW,image=explosionrouge2,tags='explosionrouge')
            elif id_joueur1==can.find_overlapping(x-1-a*50,y,x-(a+1)*50,y+50)[i] and joueur==2:
                enleve_vie(1)
                can.create_image(x-(a+1)*50,y,anchor=NW,image=explosionbleue2,tags='explosionbleue')
            elif id_joueur2==can.find_overlapping(x-1-a*50,y,x-(a+1)*50,y+50)[i] and joueur==1:
                enleve_vie(2)
                can.create_image(x-(a+1)*50,y,anchor=NW,image=explosionrouge2,tags='explosionrouge')
            elif id_joueur2==can.find_overlapping(x-1-a*50,y,x-(a+1)*50,y+50)[i] and joueur==2:
                enleve_vie(2)
                can.create_image(x-(a+1)*50,y,anchor=NW,image=explosionbleue2,tags='explosionbleue')
        if len(can.find_overlapping(x-1-a*50,y,x-(a+1)*50,y+50))==1 and joueur==2:
            can.create_image(x-(a+1)*50,y,anchor=NW,image=explosionbleue2,tags='explosionbleue')
        elif len(can.find_overlapping(x-1-a*50,y,x-(a+1)*50,y+50))==1 and joueur==1:
            can.create_image(x-(a+1)*50,y,anchor=NW,image=explosionrouge2,tags='explosionrouge')
        a+=1
    for i in range(len(destroy)):
        can.delete(destroy[i])
    if joueur==1:       
        can.delete(can.find_withtag('Bombe1')[0])
        can.create_image(x,y,anchor=NW,image=explosionrouge1,tags='explosionrouge')
        can.after(500,destruction_animation_explosion,1)
    if joueur==2:
        can.delete(can.find_withtag('Bombe2')[0])
        can.create_image(x,y,anchor=NW,image=explosionbleue1,tags='explosionbleue')
        can.after(500,destruction_animation_explosion,2)
    

def destruction_animation_explosion(joueur):
    # En entrée     : Le joueur concerné
    # En sortie     : Aucune sortie
    # Effet de bord : Détruit les images de l'animation de l'explosion de la bombe selon le joueur indiqué
    if joueur==2: # Si c'est le 2ème joueur, on supprime l'animation d'explosion de la bombe bleue
        can.delete('explosionbleue')
    elif joueur==1: # Et si c'est le 1er joueur, on supprime l'animation d'explosion de la bombe rouge
        can.delete('explosionrouge')

### BONUS ###

def bonus_bombe(x,y):
    # En entrée     : x et y respectivement l'abcisse et l'ordonnée du bonus
    # En sortie     : Aucune sortie
    # Effet de bord : Crée une image du bonus en (x,y)
    global range_bombe1,range_bombe2,xj,yj,xj2,yj2
    a=randint(0,100)
    if a<=10:
        can.create_image(x,y,image=Bombe_bonus,anchor=NW,tags="bb")

        
def verif_bonus_bombe():
    # En entrée     : Aucune entrée
    # En sortie     : Aucune sortie
    # Effet de bord : Supprime l'image, augmente la portée de 1 du joueur 1
    #                 et affiche la nouvelle portée du joueur 1 dans le canvas score
    global xj,yj,range_bombe1,range_bombe2
    destroy=[]
    a=can.find_enclosed(xj,yj,xj+50,yj+50)
    b=can.find_withtag('bb')
    for i in range (len(a)):
        for j in range (len(b)):
            if  a[i]==b[j]: # Trouve l'id du bonus de bombe
                destroy.append(b[j]) # ajoute l'identifiant numérique de l'image dans une liste
                range_bombe1+=1
                score.create_image(500,50,image=blanc,anchor=NW) # Je ne supprime pas le dernier chiffre mais j'ajoute une image blanche pour réécrire dessus
                score.create_text(500,68,text="Portée")
                score.create_text(500,82,text="Bombe")
                score.create_text(540,75,text=range_bombe1+1)
    if len(destroy)==1:
        can.delete(destroy[0])
        
# Même fonction que la précédante mais applicable pour le joueur 2

def verif_bonus_bombe1():
    # En entrée     : Aucune entrée
    # En sortie     : Aucune sortie
    # Effet de bord : Supprime l'image, augmente la portée de 1 du joueur 2
    #                 et affiche la nouvelle portée du joueur 2 dans le canvas score
    global xj2,yj2,range_bombe1,range_bombe2
    destroy=[]
    a=can.find_enclosed(xj2,yj2,xj2+50,yj2+50)
    b=can.find_withtag('bb')
    for i in range (len(a)):
        for j in range (len(b)):
            if  a[i]==b[j]: # Trouve l'id du bonus de bombe
                destroy.append(b[j]) # ajoute l'identifiant numérique de l'image dans une liste
                range_bombe2+=1
                score.create_image(500,100,image=blanc,anchor=NW) # Je ne supprime pas le dernier chiffre mais j'ajoute une image blanche pour réécrire dessus
                score.create_text(500,118,text="Portée")
                score.create_text(500,132,text="Bombe")
                score.create_text(540,125,text=range_bombe2+1)
    if len(destroy)==1:
        can.delete(destroy[0])

def bonus_vie(x,y):
    # En entrée     : x et y respectivement l'abscisse et l'ordonnée du bonus
    # En sortie     : Rien 
    # Effet de bord : Crée une image du bonus en (x,y)
    global pvj1,pvj2,xj,yj,xj2,yj2
    a=randint(0,100)
    if a<=2: # Représente 2% de chance 
        can.create_image(x,y,image=vie_bonus,anchor=NW,tags="bv")
        
def verif_bonus_vie():
    # En entrée     : Rien 
    # En sortie     : Rien
    # Effet de bord : Supprime l'image du bonus de coeur et rajoute une vie au joueur 1 dans le canvas score
    global xj,yj,pvj1,coeur
    destroy=[]
    a=can.find_enclosed(xj,yj,xj+50,yj+50)
    b=can.find_withtag('bv')
    for i in range (len(a)):
        for j in range (len(b)):
            if  a[i]==b[j]:
                destroy.append(b[j])
                rajoute_vie(1) # cette fonction ajoute une vie au joueur  1 et affiche une nouvelle vie dans le canvas create
    if len(destroy)==1:
        can.delete(destroy[0])

# Même fonction que la précédante mais applicable pour le joueur 2

def verif_bonus_vie1():
    # En entrée     : Rien
    # En sortie     : Rien
    # Effet de bord : Supprime l'image du bonus de coeur et rajoute une vie au joueur 2 dans le canvas score
    global xj2,yj2,pvj2
    destroy=[]
    a=can.find_enclosed(xj2,yj2,xj2+50,yj2+50)
    b=can.find_withtag('bv')
    for i in range (len(a)):
        for j in range (len(b)):
            if  a[i]==b[j]:
                destroy.append(b[j])
                rajoute_vie(2) # cette fonction ajoute une vie au joueur  2 et affiche une nouvelle vie dans le canvas create
    if len(destroy)==1:
        can.delete(destroy[0])


def bonus_recharge(x,y):
    # En entrée     : x et y respectivement l'abscisse et l'ordonnée du bonus
    # En sortie     : Aucune sortie
    # Effet de bord : Crée une image du bonus en (x,y)
    a=randint(0,100)
    if a<=7: # Représente 8% de chance
        can.create_image(x,y,image=recharge_bonus,anchor=NW,tags='br')

def verif_bonus_recharge():
    # En entrée     : Aucune entrée
    # En sortie     : Aucune sortie
    # Effet de bord : Supprime l'image, augmente le nombre de bombes que le joueur 1 peut poser en même temps et affiche une nouvelle bombe dans le canvas score
    global xj,yj,nb_bombes1
    destroy=[]
    a=can.find_enclosed(xj,yj,xj+50,yj+50)
    b=can.find_withtag('br')
    for i in range (len(a)):
        for j in range (len(b)):
            if  a[i]==b[j]:
                destroy.append(b[j])
                nb_bombes1+=1
                if nb_bombes1==5: # Permet au joueur de poser un maximum de  4 bombes à la fois 
                    nb_bombes1-=1
                score.create_image(200+nb_bombes1*50,50,image=Bombe1,anchor=NW)# Pose des bombes les une à côtés des autres représentant
    if len(destroy)==1:
        can.delete(destroy[0])
        
# Même fonction que la précédante mais applicable pour le joueur 2

def verif_bonus_recharge1():
    # En entrée     : Aucune entrée
    # En sortie     : Aucune sortie
    # Effet de bord : Supprime l'image, augmente le nombre de bombes que le joueur 2 peut poser en même temps et affiche une nouvelle bombe dans le canvas score
    global xj,yj,nb_bombes2
    destroy=[]
    a=can.find_enclosed(xj2,yj2,xj2+50,yj2+50)
    b=can.find_withtag('br')
    for i in range (len(a)):
        for j in range (len(b)):
            if  a[i]==b[j]:
                destroy.append(b[j])
                nb_bombes2+=1
                if nb_bombes2==5: # Permet au joueur de poser un maximum de  4 bombes à la fois 
                    nb_bombes2-=1
                score.create_image(200+nb_bombes2*50,100,image=Bombe2,anchor=NW) # Pose des bombes les une à côtés des autres représentant
    if len(destroy)==1:
        can.delete(destroy[0])
        
                
### Personnages / joueurs ###

def personnages():
    # En entrée     :rien
    # En sortie     :rien
    # Effet de bord :affiche les personnages en appelant 2 images
    # Personnage 1 #
    perso=can.create_image(0,0,anchor=NW,image=joueur1,tags="perso")
    # Personnage 2 #
    perso2=can.create_image(500,500,anchor=NW,image=joueur2,tags="perso2")
    
## Mouvements Joueur 1 ##

def animdroite(event): # Toutes les fonctions de déplacement fonctionnent de la même façon
    # En entrée     : Appui sur la touche flèche droite
    # En sortie     : Aucune sortie
    # Effet de bord : Déplace le joueur 1 vers la droite
    global xj,yj
    a=True
    for i in range (len(can.find_enclosed(xj+49,yj-1,xj+101,yj+51))):#
        for j in range (len(can.find_withtag('briques'))):
            if can.find_enclosed(xj+49,yj-1,xj+101,yj+51)[i]==can.find_withtag('briques')[j]:
                a=False
            # Vérifie pour chaque élément se trouvant dans la direction vers laquelle le joueur veut se déplacer si l'élément est une brique ou un bloc :
        for k in range (len(can.find_withtag('blocs'))):
            if can.find_enclosed(xj+49,yj-1,xj+101,yj+51)[i]==can.find_withtag('blocs')[k]:
                a=False # Si oui, rien ne se passe
    if a==True: # Si non le joueur se déplace
        xj+=50
        can.coords("perso",xj,yj) # Déplace le personnage (joueur)
        verif_bonus_bombe()
        verif_bonus_vie()
        verif_bonus_recharge()

def animgauche(event): 
    # En entrée     : Appui sur la touche flèche gauche
    # En sortie     : Aucune sortie
    # Effet de bord : Déplace le joueur 1 vers la gauche
    global xj,yj
    a=True
    for i in range (len(can.find_enclosed(xj+1,yj-1,xj-51,yj+51))):
        for j in range(len(can.find_withtag('briques'))):
            if can.find_enclosed(xj+1,yj-1,xj-51,yj+51)[i]==can.find_withtag('briques')[j]:
                a=False
        for k in range(len(can.find_withtag('blocs'))):
            if can.find_enclosed(xj+1,yj-1,xj-51,yj+51)[i]==can.find_withtag('blocs')[k]:
                a=False
    if a==True:
        xj-=50
        can.coords("perso",xj,yj)
        verif_bonus_bombe()
        verif_bonus_vie()
        verif_bonus_recharge()


def animbas(event): 
    # En entrée     : Appui sur la touche flèche bas
    # En sortie     : Aucune sortie
    # Effet de bord : Déplace le joueur 1 vers le bas
    global xj,yj
    a=True
    for i in range (len(can.find_enclosed(xj-1,yj+49,xj+51,yj+101))):
        for j in range(len(can.find_withtag('briques'))):
            if can.find_enclosed(xj-1,yj+49,xj+51,yj+101)[i]==can.find_withtag('briques')[j]:
                a=False
        for k in range(len(can.find_withtag('blocs'))):
            if can.find_enclosed(xj-1,yj+49,xj+51,yj+101)[i]==can.find_withtag('blocs')[k]:
                a=False
    if a==True:
        yj+=50
        can.coords("perso",xj,yj)
        verif_bonus_bombe()
        verif_bonus_vie()
        verif_bonus_recharge()

def animhaut(event):
    # En entrée     : Appui sur la touche flèche haut
    # En sortie     : Aucune sortie
    # Effet de bord : Déplace le joueur 1 vers le haut
    global xj,yj
    a=True
    for i in range (len(can.find_enclosed(xj-1,yj+1,xj+51,yj-51))):
        for j in range(len(can.find_withtag('briques'))):
            if can.find_enclosed(xj-1,yj+1,xj+51,yj-51)[i]==can.find_withtag('briques')[j]:
                a=False
        for k in range(len(can.find_withtag('blocs'))):
            if can.find_enclosed(xj-1,yj+1,xj+51,yj-51)[i]==can.find_withtag('blocs')[k]:
                a=False
    if a==True:
        yj-=50
        can.coords("perso",xj,yj)
        verif_bonus_bombe()
        verif_bonus_vie()
        verif_bonus_recharge()

## Mouvements Joueur 2 ##

def animdroite2(event):  
    # En entrée     : Appui sur la touche D
    # En sortie     : Aucune sortie
    # Effet de bord : Déplace le joueur 2 vers la droite
    global xj2,yj2
    a=True
    for i in range (len(can.find_enclosed(xj2+49,yj2-1,xj2+101,yj2+51))):
        for j in range (len(can.find_withtag('briques'))):
            if can.find_enclosed(xj2+49,yj2-1,xj2+101,yj2+51)[i]==can.find_withtag('briques')[j]:
                a=False
        for k in range (len(can.find_withtag('blocs'))):
            if can.find_enclosed(xj2+49,yj2-1,xj2+101,yj2+51)[i]==can.find_withtag('blocs')[k]:
                a=False
    if a==True:
        xj2+=50
        can.coords("perso2",xj2,yj2)
        verif_bonus_bombe1()
        verif_bonus_vie1()
        verif_bonus_recharge1()

def animgauche2(event): 
    # En entrée     : Appui sur la touche Q
    # En sortie     : Aucune sortie
    # Effet de bord : Déplace le joueur 2 vers la gauche
    global xj2,yj2
    a=True
    for i in range (len(can.find_enclosed(xj2+1,yj2-1,xj2-51,yj2+51))):
        for j in range(len(can.find_withtag('briques'))):
            if can.find_enclosed(xj2+1,yj2-1,xj2-51,yj2+51)[i]==can.find_withtag('briques')[j]:
                a=False
        for k in range(len(can.find_withtag('blocs'))):
            if can.find_enclosed(xj2+1,yj2-1,xj2-51,yj2+51)[i]==can.find_withtag('blocs')[k]:
                a=False
    if a==True:
        xj2-=50
        can.coords("perso2",xj2,yj2)
        verif_bonus_bombe1()
        verif_bonus_vie1()
        verif_bonus_recharge1()

def animbas2(event): 
    # En entrée     : Appui sur la touche S
    # En sortie     : Aucune sortie
    # Effet de bord : Déplace le joueur 2 vers le bas
    global xj2,yj2
    a=True
    for i in range (len(can.find_enclosed(xj2-1,yj2+49,xj2+51,yj2+101))):
        for j in range(len(can.find_withtag('briques'))):
            if can.find_enclosed(xj2-1,yj2+49,xj2+51,yj2+101)[i]==can.find_withtag('briques')[j]:
                a=False
        for k in range(len(can.find_withtag('blocs'))):
            if can.find_enclosed(xj2-1,yj2+49,xj2+51,yj2+101)[i]==can.find_withtag('blocs')[k]:
                a=False
    if a==True:
        yj2+=50
        can.coords("perso2",xj2,yj2)
        verif_bonus_bombe1()
        verif_bonus_vie1()
        verif_bonus_recharge1()

def animhaut2(event): 
    # En entrée     : Appui sur la touche Z
    # En sortie     : Aucune sortie
    # Effet de bord : Déplace le joueur 2 vers le haut
    global xj2,yj2
    a=True
    for i in range (len(can.find_enclosed(xj2-1,yj2+1,xj2+51,yj2-51))):
        for j in range(len(can.find_withtag('briques'))):
            if can.find_enclosed(xj2-1,yj2+1,xj2+51,yj2-51)[i]==can.find_withtag('briques')[j]:
                a=False
        for k in range(len(can.find_withtag('blocs'))):
            if can.find_enclosed(xj2-1,yj2+1,xj2+51,yj2-51)[i]==can.find_withtag('blocs')[k]:
                a=False
    if a==True:
        yj2-=50
        can.coords("perso2",xj2,yj2)
        verif_bonus_bombe1()
        verif_bonus_vie1()
        verif_bonus_recharge1()
	
### Programme ###

## Fenêtre du menu ##

can.bind("<Button-1>",menu)
score=can
## Fenêtre du jeu ##

Quitter=Button(fen,text="Quitter",command=fen.quit)
Quitter.pack(side=BOTTOM)


## Commandes joueur 1 ##
fen.bind("<KeyRelease-Left>",animgauche)
fen.bind("<KeyRelease-Right>",animdroite)
fen.bind("<KeyRelease-Up>",animhaut)
fen.bind("<KeyRelease-Down>",animbas)
fen.bind("<Key-Return>",bombe1)

## Commandes joueur 2 ##
fen.bind("<KeyRelease-q>",animgauche2)
fen.bind("<KeyRelease-d>",animdroite2)
fen.bind("<KeyRelease-z>",animhaut2)
fen.bind("<KeyRelease-s>",animbas2)
fen.bind("<space>",bombe2)

fen.mainloop()
fen.destroy() 
    
