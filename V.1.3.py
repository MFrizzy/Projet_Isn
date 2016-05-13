#Création et déplacement d'un personnage
#Déplacement avec les flèches
#Détection des s "pleines"
#sur lesquelles le personnage ne peut
#pas aller.



from tkinter import*
from random import*

fen=Tk()
fen.title('BOMBERMAN')
can=Canvas(fen, width =550, height =550, bg ='ivory')
can.pack(side=TOP,padx=5,pady=5)

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
    
### Briques ###
briques=PhotoImage(file="briques.png")
def ajouter_brique(x,y):
    can.create_image(x*50,y*50,image=briques,anchor=NW,tags="briques")

### Blocs ###
blocs=PhotoImage(file="blocs.png")
def ajouter_bloc(x,y):
    can.create_image(x*50,y*50,image=blocs,anchor=NW,tags="blocs")

### variables joueur 1 ###

xj,yj=0,0 #  : coordonnées de la 

### variables joueur 2 ###
xj2,yj2=500,500

# Personnage 1 provisoire #
place=[int(xj/50),int(yj/50)] # position du personnage
joueur1=PhotoImage(file="joueur1.png")
perso=can.create_image(xj,yj,anchor=NW,image=joueur1,tags="perso")

# Personnage 2 provisoire #
place2=[int(xj2/50),int(yj2/50)]
joueur2=PhotoImage(file="joueur2.png")
perso2=can.create_image(xj2,yj2,anchor=NW,image=joueur2,tags="perso2")

### Bombes et boosts ###

def bombe(event):
    # en entrée : event
    # en effet de bord : création d'une 'bombe' à la position du joueur
    global place
    can.create_oval(xj+10,yj+10,xj+40,yj+40,fill='black',tags='bombe')
    a=xj
    b=yj
    explosion(a,b)

def explosion(xj,yj):
    print(can.find_overlapping(xj,yj,xj+50,yj+50))
    destroy=[]
    a=can.find_overlapping(xj-1,yj-1,xj+51,yj+51)
    b=can.find_withtag('briques')
    for i in range (len(a)):
        for j in range (len(b)):
            if  a[i]==b[j]:
                destroy.append(b[j])
                print(b[j])
    for i in range(len(destroy)):
        can.delete(destroy[i])
    can.delete('bombe')
    
def bombe2(event):
    # en entrée : event
    # en effet de bord : création d'une 'bombe' à la position du joueur
    can.create_oval(xj2+10,yj2+10,xj2+40,yj2+40,fill='black')

### Personnage / joueur ###
    ### Joueur 1 ###
    
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

def animgauche(event): # déplace le joueur vers la gauche
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

def animbas(event): # déplace le joueur vers le bas
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

def animhaut(event): # déplace le joueur vers le haut
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

    ### Joueur 2 ###

def animdroite2(event): # déplace le joueur vers la droite
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

def animgauche2(event): # déplace le joueur vers la gauche
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

def animbas2(event): # déplace le joueur vers le bas
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

def animhaut2(event): # déplace le joueur vers le haut
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
	
### Programme ###
Quitter=Button(fen,text="Quitter",command=fen.quit)
Quitter.pack(side=BOTTOM)
dessiner_map()
# Commande joueur 1 #
fen.bind("<KeyRelease-Left>",animgauche)
fen.bind("<KeyRelease-Right>",animdroite)
fen.bind("<KeyRelease-Up>",animhaut)
fen.bind("<KeyRelease-Down>",animbas)

# Commande joueur 2 #
fen.bind("<KeyRelease-q>",animgauche2)
fen.bind("<KeyRelease-d>",animdroite2)
fen.bind("<KeyRelease-z>",animhaut2)
fen.bind("<KeyRelease-s>",animbas2)
fen.bind("<Key-Return>",bombe2)
fen.bind("<space>",bombe)
fen.mainloop()
fen.destroy()
    
