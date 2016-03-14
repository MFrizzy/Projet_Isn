#Création et déplacement d'un personnage
#Déplacement avec les flèches
#Détection des cases "pleines"
#sur lesquelles le personnage ne peut
#pas aller.


from tkinter import*
from random import*

fen=Tk()
fen.title('Personnage')
can=Canvas(fen, width =550, height =550, bg ='ivory')
can.pack(side=TOP,padx=5,pady=5)
bloc=[]
brique=[]

### Creation map ###

def dessiner_map():
    # pas d'entrée, ni de sortie
    # effet de bord : Création d'une map composé des briques déstructibles et de blocs indestructibles
    #                 avec 2 point de spawn de joueur en haut à gauche et en bas à droite
    global x,y
    for i in range(1,10,2):
        for j in range(1,10,2):
            ajouter_bloc(i,j)
    for j in range(0,11,1):
        for i in range(2,9,2):
            ajouter_brique(i,j)
    for j in range(0,11,2):
        for i in range(3,8,2):
            ajouter_brique(i,j)
    for i in range(2,9,1):
        for j in range(0,11,10):
            ajouter_brique(j,i)
    for i in range(2,9,2):
        for j in range(1,10,8):
            ajouter_brique(j,i)
    ajouter_brique(9,0)
    ajouter_brique(10,0)
    ajouter_brique(10,1)
    ajouter_brique(0,9)
    ajouter_brique(0,10)
    ajouter_brique(1,10)

def ajouter_brique(x,y):
    # en entrée : coordonnées x,y du coin en haut à gauche de la brique destructible
    # en effet de bord : Creation d'une brique gris rayé de 50*50
    global brique
    can.create_rectangle(x*50,y*50,x*50+50,y*50+50,fill="grey")
    can.create_line(x*50,50*y+(50/4),x*50+50,y*50+(50/4))
    can.create_line(x*50,50*y+(2*50/4),x*50+50,y*50+(2*50/4))
    can.create_line(x*50,50*y+(3*50/4),x*50+50,y*50+(3*50/4))
    brique.append([x,y])
    

def ajouter_bloc(x,y):
    # en entrée : coordonnées x,y du coin en haut à gauche du bloc indestructible
    # en effet de bord : Creation d'un bloc noir de 50*50
    global bloc
    can.create_rectangle(x*50,y*50,x*50+50,y*50+50,fill='black')
    bloc.append([x,y])

### variables joueur ###

xj,yj,case=0,0,[] # case : coordonnées de la case
place=[int(xj/50),int(yj/50)] # position du personnage
# Personnage provisoire
perso=can.create_rectangle(xj,yj,xj+50,yj+50,fill="red",outline="red"),   # corps général
oeilgauche=can.create_rectangle(xj+10,yj+10,xj+20,yj+20,fill="black"),    # oeil gauche
oeildroit=can.create_rectangle(xj+30,yj+10,xj+40,yj+20,fill="black"),     # oeil droit
bouche=can.create_rectangle(xj+15,yj+30,xj+35,yj+35,fill="black")         # bouche

### Bombes et boosts ###

def bombe(event):
    # en entrée : event
    # en effet de bord : création d'une 'bombe' à la position du joueur
    global place
    can.create_oval(xj+10,yj+10,xj+40,yj+40,fill='black')

### Personnage / joueur ###

def animdroite(event): # déplace le joueur vers la droite
    global xj,yj,case,place
    xj+=50
    can.coords(perso,xj,yj,xj+50,yj+50)
    can.coords(oeilgauche,xj+10,yj+10,xj+20,yj+20)
    can.coords(oeildroit,xj+30,yj+10,xj+40,yj+20)
    can.coords(bouche,xj+15,yj+30,xj+35,yj+35)
    place[0]+=1
    for i in range (len(brique)): 
        a=brique[i]
        if place[0]==a[0] and place[1]==a[1] or place[0]==9: # Vérification liste de coordonnées des briques et de la bordure
            animgauche(event)
    for i in range (len(bloc)):
        a=bloc[i]
        if place[0]==a[0] and place[1]==a[1]: # Vérification liste de coordonnées des blocs
            animgauche(event)
    print(place)

def animgauche(event): # déplace le joueur vers la gauche
    global xj,yj
    xj-=50
    can.coords(perso,xj,yj,xj+50,yj+50)
    can.coords(oeilgauche,xj+10,yj+10,xj+20,yj+20)
    can.coords(oeildroit,xj+30,yj+10,xj+40,yj+20)
    can.coords(bouche,xj+15,yj+30,xj+35,yj+35)
    place[0]-=1
    for i in range (len(brique)):
        a=brique[i]
        if place[0]==a[0] and place[1]==a[1] or place[0]==-1: # Vérification liste de coordonnées des briques et de la bordure
            animdroite(event)
    for i in range (len(bloc)):
        a=bloc[i]
        if place[0]==a[0] and place[1]==a[1]: # Vérification liste de coordonnées des blocs
            animdroite(event)
    print(place)

def animbas(event): # déplace le joueur vers le bas
    global xj,yj
    yj+=50
    can.coords(perso,xj,yj,xj+50,yj+50)
    can.coords(oeilgauche,xj+10,yj+10,xj+20,yj+20)
    can.coords(oeildroit,xj+30,yj+10,xj+40,yj+20)
    can.coords(bouche,xj+15,yj+30,xj+35,yj+35)
    place[1]+=1
    for i in range (len(brique)):
        a=brique[i]
        if place[0]==a[0] and place[1]==a[1] or place[1]==9: # Vérification liste de coordonnées des briques et de la bordure
            animhaut(event)
    for i in range (len(bloc)):
        a=bloc[i]
        if place[0]==a[0] and place[1]==a[1]: # Vérification liste de coordonnées des blocs
            animhaut(event)
    print(place)

def animhaut(event): # déplace le joueur vers le haut
    global xj,yj
    yj-=50
    can.coords(perso,xj,yj,xj+50,yj+50)
    can.coords(oeilgauche,xj+10,yj+10,xj+20,yj+20)
    can.coords(oeildroit,xj+30,yj+10,xj+40,yj+20)
    can.coords(bouche,xj+15,yj+30,xj+35,yj+35)
    place[1]-=1
    for i in range (len(brique)):
        a=brique[i]
        if place[0]==a[0] and place[1]==a[1] or place[1]==-1: # Vérification liste de coordonnées des briques et de la bordure
            animbas(event)
    for i in range (len(bloc)):
        a=bloc[i]
        if place[0]==a[0] and place[1]==a[1]: # Vérification liste de coordonnées des blocs
            animbas(event)
    print(place)
	
### Programme ###

Quitter=Button(fen,text="Quitter",command=fen.quit)
Quitter.pack(side=BOTTOM)
dessiner_map()
fen.bind("<KeyRelease-Left>",animgauche)
fen.bind("<KeyRelease-Right>",animdroite)
fen.bind("<KeyRelease-Up>",animhaut)
fen.bind("<KeyRelease-Down>",animbas)
fen.bind("<KeyRelease-Return>",bombe)
fen.mainloop()
fen.destroy()
