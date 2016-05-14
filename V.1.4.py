#Création et déplacement d'un personnage
#Déplacement avec les flèches
#Détection des s "pleines"
#sur lesquelles le personnage ne peut
#pas aller.



from tkinter import*
from random import*
from winsound import *

### Initialisation de la fenêtre du menu ###

fen=Tk()
fen.title("Menu")
can=Canvas(fen, width =550, height =550, bg ="lime")
can.pack(side=TOP,padx=5,pady=5)
x,y=0,0
can.create_rectangle(200,100,x+350,y+150,fill="red",tags="menu")
can.create_rectangle(200,170,x+350,y+220,fill="red",tags="menu")
can.create_rectangle(200,240,x+350,y+290,fill="red",tags="menu")
can.create_rectangle(200,310,x+350,y+360,fill="red",tags="menu")
can.create_text(275,125,text="Nouvelle partie",tags="menu")
can.create_text(275,195,text="Scores",tags="menu")
can.create_text(275,265,text="Règles",tags="menu")
can.create_text(275,335,text="Quitter",tags="menu")

def menu(event):
    global x,y,jouer
    x,y=event.x,event.y
    if 200<=event.x<=350 and 100<=event.y<=150:
        print("Nouvelle partie")
        startgame()
    if 200<=event.x<=350 and 170<=event.y<=220:
        print("Scores")
    if 200<=event.x<=350 and 240<=event.y<=290:
        print("Règles")
    if 200<=event.x<=350 and 310<=event.y<=360:
        print("Quitter")
        fen.destroy()

PlaySound("musique.wav", SND_ASYNC)

### Initialisation de la fenêtre de jeu ###
def startgame():
    can.delete("menu")
    fen.title('BOMBERMAN')
    dessiner_map()
    dessiner_map()
    personnages()
    
scorej1,scorej2=0,0

### Creation map ###

def dessiner_map():
    # pas d'entrée, ni de sortie
    # effet de bord : Création d'une map composé des briques déstructibles et de blocs indestructibles
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
briques=PhotoImage(file="briques.png")
def ajouter_brique(x,y):
    can.create_image(x*50,y*50,image=briques,anchor=NW,tags="briques")

## Blocs ##
blocs=PhotoImage(file="blocs.png")
def ajouter_bloc(x,y):
    can.create_image(x*50,y*50,image=blocs,anchor=NW,tags="blocs")



### Bombes ###

Bombe1=PhotoImage(file="bomberouge.png")
Bombe2=PhotoImage(file="bombebleue.png")
range_bombe1=0
range_bombe2=0



def bombe1(event):
    # en entrée : event
    # en effet de bord : création d'une 'bombe' à la position du joueur,
    #                    puis explosion au bout d'une seconde
    can.create_image(xj,yj,anchor=NW,image=Bombe1,tags='Bombe1')
    a=xj
    b=yj
    can.after(2000,explosion,a,b,1)

def bombe2(event):
    # en entrée : event
    # en effet de bord : création d'une 'bombe' à la position du joueur
    #                    puis explosion au bout d'une seconde
    can.create_image(xj2,yj2,anchor=NW,image=Bombe2,tags='Bombe2')
    a=xj2
    b=yj2
    can.after(2000,explosion,a,b,2)

def explosion(x,y,joueur):
    global Victoire, range_bombe1,range_bombe2
    destroy=[]
    if joueur==1:
        bonus=range_bombe1
    elif joueur==2:
        bonus=range_bombe2
    a=0
    explosion_bas=False
    explosion_droite=False
    explosion_haut=False
    explosion_gauche=False
    while explosion_bas==False and a<=bonus:
        for i in range(len(can.find_overlapping(x,y+50,x+50,y+51+a*50))):
            for j in range(len(can.find_withtag('briques'))):
                if can.find_overlapping(x,y+50,x+50,y+51+a*50)[i]==can.find_withtag('briques')[j]:
                    explosion_bas=True
                    xb=can.bbox(can.find_withtag('briques')[j])[0]
                    yb=can.bbox(can.find_withtag('briques')[j])[1]
                    bonus_bombe(xb,yb)
                    destroy.append(can.find_withtag('briques')[j])
            for k in range(len(can.find_withtag('blocs'))):
                if can.find_overlapping(x,y+50,x+50,y+51+a*50)[i]==can.find_withtag('blocs')[k]:
                    explosion_bas=True
        a+=1
    a=0
    while explosion_droite==False and a<=bonus:      
        for i in range(len(can.find_overlapping(x+50,y,x+51+50*a,y+50))):
            for j in range(len(can.find_withtag('briques'))):
                if can.find_overlapping(x+50,y,x+51+50*a,y+50)[i]==can.find_withtag('briques')[j]:
                    explosion_droite=True
                    xb=can.bbox(can.find_withtag('briques')[j])[0]
                    yb=can.bbox(can.find_withtag('briques')[j])[1]
                    bonus_bombe(xb,yb)
                    destroy.append(can.find_withtag('briques')[j])
            for k in range(len(can.find_withtag('blocs'))):
                if can.find_overlapping(x+50,y,x+51+50*a,y+50)[i]==can.find_withtag('blocs')[k]:
                    explosion_droite=True
        a+=1
    a=0
    while explosion_haut==False and a<=bonus:
        for i in range(len(can.find_overlapping(x,y,x+50,y-1-a*50))):
            for j in range(len(can.find_withtag('briques'))):
                if can.find_overlapping(x,y,x+50,y-1-a*50)[i]==can.find_withtag('briques')[j]:
                    explosion_haut=True
                    xb=can.bbox(can.find_withtag('briques')[j])[0]
                    yb=can.bbox(can.find_withtag('briques')[j])[1]
                    bonus_bombe(xb,yb)
                    destroy.append(can.find_withtag('briques')[j])
            for k in range(len(can.find_withtag('blocs'))):
                if can.find_overlapping(x,y,x+50,y-1-a*50)[i]==can.find_withtag('blocs')[k]:
                    explosion_haut=True
        a+=1
    a=0
    while explosion_gauche==False and a<=bonus:
        for i in range(len(can.find_overlapping(x-1-a*50,y,x,y+50))):
            for j in range(len(can.find_withtag('briques'))):
                if can.find_overlapping(x-1-a*50,y,x,y+50)[i]==can.find_withtag('briques')[j]:
                    explosion_gauche=True
                    xb=can.bbox(can.find_withtag('briques')[j])[0]
                    yb=can.bbox(can.find_withtag('briques')[j])[1]
                    bonus_bombe(xb,yb)
                    destroy.append(can.find_withtag('briques')[j])
            for k in range(len(can.find_withtag('blocs'))):
                if can.find_overlapping(x-1-a*50,y,x,y+50)[i]==can.find_withtag('blocs')[k]:
                    explosion_gauche=True
        a+=1
    for i in range(len(destroy)):
        can.delete(destroy[i])
    if joueur==1:
        can.delete('Bombe1')
    if joueur==2:
        can.delete('Bombe2')
### BONUS ###

Bombe_bonus=PhotoImage(file="bonus_bombe.png")

def bonus_bombe(x,y):
    global range_bombe1,range_bombe2,xj,yj,xj2,yj2
    a=randint(0,100)
    if a<=5:
        can.create_image(x,y,image=Bombe_bonus,anchor=NW,tags="bb")

        
def verif_bonus_bombe():
    global xj,yj,range_bombe1,range_bombe2
    destroy=[]
    a=can.find_enclosed(xj,yj,xj+50,yj+50)
    b=can.find_withtag('bb')
    for i in range (len(a)):
        for j in range (len(b)):
            if  a[i]==b[j]:
                destroy.append(b[j])
                range_bombe1+=1
    if len(destroy)==1:
        can.delete(destroy[0])

def verif_bonus_bombe1():
    global xj2,yj2,range_bombe1,range_bombe2
    destroy=[]
    a=can.find_enclosed(xj2,yj2,xj2+50,yj2+50)
    b=can.find_withtag('bb')
    for i in range (len(a)):
        for j in range (len(b)):
            if  a[i]==b[j]:
                destroy.append(b[j])
                range_bombe2+=1
    if len(destroy)==1:
        can.delete(destroy[0])
   
trap1_bonus=PhotoImage(file="trap1.png")
def trap1(event):
    can.create_image(xj,yj,image=trap1_bonus,anchor=NW,tags="tb1")

trap2_bonus=PhotoImage(file="trap2.png")
def trap2(event):
    can.create_image(xj2,yj2,image=trap2_bonus,anchor=NW,tags="tb2")

def verif_trap1():
    global xj2,yj2
    destroy=[]
    a=can.find_enclosed(xj2,yj2,xj2+50,yj2+50)
    b=can.find_withtag('tb1')
    for i in range (len(a)):
        for j in range (len(b)):
            if  a[i]==b[j]:
                destroy.append(b[j])
    if len(destroy)==1:
        can.delete(destroy[0])
    
def verif_trap2():
    global xj,yj
    destroy=[]
    a=can.find_enclosed(xj,yj,xj+50,yj+50)
    b=can.find_withtag('tb2')
    for i in range (len(a)):
        for j in range (len(b)):
            if  a[i]==b[j]:
                destroy.append(b[j])
    if len(destroy)==1:
        can.delete(destroy[0])

                
### Personnages / joueurs ###

## Définitions Joueurs ##

# Coordonnées/Paramètres joueur1 #
xj,yj=0,0
joueur1=PhotoImage(file="joueur1.png")
# Coordonnées/Paramètres joueur2 #
xj2,yj2=500,500
joueur2=PhotoImage(file="joueur2.png")

def personnages():
    # Personnage 1 #
    place=[int(xj/50),int(yj/50)] # position du personnage
    perso=can.create_image(xj,yj,anchor=NW,image=joueur1,tags="perso")

    # Personnage 2 #
    place2=[int(xj2/50),int(yj2/50)]
    perso2=can.create_image(xj2,yj2,anchor=NW,image=joueur2,tags="perso2")
    
## Mouvements Joueur 1 ##
    
def animdroite(event): # déplace le joueur vers la droite
    global xj,yj
    a=True
    for i in range (len(can.find_enclosed(xj+49,yj-1,xj+101,yj+51))):
        for j in range (len(can.find_withtag('briques'))):
            if can.find_enclosed(xj+49,yj-1,xj+101,yj+51)[i]==can.find_withtag('briques')[j]:
                a=False
        for k in range (len(can.find_withtag('blocs'))):
            if can.find_enclosed(xj+49,yj-1,xj+101,yj+51)[i]==can.find_withtag('blocs')[k]:
                a=False
    if a==True:
        xj+=50
        can.coords("perso",xj,yj)
        verif_bonus_bombe()
        verif_trap2()

def animgauche(event): # déplace le joueur1 vers la gauche
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
        verif_trap2()

def animbas(event): # déplace le joueur1 vers le bas
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
        verif_trap2()

def animhaut(event): # déplace le joueur1 vers le haut
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
        verif_trap2()

    ### Joueur 2 ###

## Mouvements Joueur 2 ##

def animdroite2(event): # déplace le joueur2 vers la droite
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
        verif_trap1()

def animgauche2(event): # déplace le joueur2 vers la gauche
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
        verif_trap1()

def animbas2(event): # déplace le joueur2 vers le bas
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
        verif_trap1()

def animhaut2(event): # déplace le joueur2 vers le haut
    global xj2,yj2,place2
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
        verif_trap1()
	
### Programme ###

## Fenêtre du menu ##

can.bind("<Button-1>",menu)

## Fenêtre du jeu ##

Quitter=Button(fen,text="Quitter",command=fen.quit)
Quitter.pack(side=BOTTOM)


## Commandes joueur 1 ##
fen.bind("<KeyRelease-Left>",animgauche)
fen.bind("<KeyRelease-Right>",animdroite)
fen.bind("<KeyRelease-Up>",animhaut)
fen.bind("<KeyRelease-Down>",animbas)
fen.bind("<Key-Return>",bombe1)
fen.bind("<KeyRelease-a>",trap2)

## Commandes joueur 2 ##
fen.bind("<KeyRelease-q>",animgauche2)
fen.bind("<KeyRelease-d>",animdroite2)
fen.bind("<KeyRelease-z>",animhaut2)
fen.bind("<KeyRelease-s>",animbas2)
fen.bind("<space>",bombe2)
fen.bind("<KeyRelease-0>",trap1)

fen.mainloop()
fen.destroy() 
    
