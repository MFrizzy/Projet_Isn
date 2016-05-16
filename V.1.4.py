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
can=Canvas(fen, width =550, height =550)
can.pack(side=TOP,padx=5,pady=5)
x,y=0,0
gamestarted=False
MENU=PhotoImage(file="menu.png")
can.create_image(2,2,image=MENU,anchor=NW,tags="menu")


def menu(event):
    # En entrée     :
    # En sortie     :
    # Effet de bord :
    global x,y,jouer
    x,y=event.x,event.y
    if 107<=event.x<=443 and 160<=event.y<=200 and gamestarted==False:
        print("Nouvelle partie")
        startgame()
    if 107<=event.x<=443 and 230<=event.y<=270 and gamestarted==False:
        print("Quitter")
        fen.destroy()

#PlaySound("musique.wav", SND_ASYNC)

### Initialisation de la fenêtre de jeu ###
herbe=PhotoImage(file="herbe.png")
def startgame():
    # En entrée     :
    # En sortie     :
    # Effet de bord :
    global gamestarted,score,id_joueur1,id_joueur2
    gamestarted=True
    can.delete(ALL)
    can.create_image(0,0,image=herbe,anchor=NW,tags="bg")
    fen.title('BOMBERMAN')
    dessiner_map()
    personnages()
    id_joueur1=can.find_withtag('perso')[0]
    id_joueur2=can.find_withtag('perso2')[0]
    score=Canvas(fen,width=550,height=200,bg="white")
    score.pack(side=BOTTOM)
    score.create_text(70,75,text="Joueur1")
    score.create_text(70,125,text="Joueur2")
    score.create_rectangle(100,50,150,100,fill="red")
    score.create_rectangle(150,50,200,100,fill="red")
    score.create_rectangle(200,50,250,100,fill="red")
    score.create_rectangle(100,100,150,150,fill="blue")
    score.create_rectangle(150,100,200,150,fill="blue")
    score.create_rectangle(200,100,250,150,fill="blue")
    score.create_image(250,50,image=Bombe1,anchor=NW)
    score.create_image(250,100,image=Bombe2,anchor=NW)
    score.create_text(500,68,text="Portée")
    score.create_text(500,82,text="Bombe")
    score.create_text(500,118,text="Portée")
    score.create_text(500,132,text="Bombe")
    score.create_text(540,75,text="1")
    score.create_text(540,125,text="1")

## Vies et scores ##  
scorej1,scorej2=0,0
x,y=1,1
l1,l2=0,0
pvj1=3
pvj2=3

jeufini=PhotoImage(file="gameover.png")
rejouer=PhotoImage(file="rejouer.png")
quitter=PhotoImage(file="quitter.png")
def enleve_vie(joueur):
    # En entrée     :
    # En sortie     :
    # Effet de bord :
    global pvj1,pvj2,score,id_joueur1,id_joueur2
    if joueur==1:
        pvj1-=1
    elif joueur==2:
        pvj2-=1
    if pvj1==2:
        score.create_rectangle(100,50,150,100,fill="white")# premier carré j1
    if pvj1==1:
        score.create_rectangle(150,50,200,100,fill="white")#deuxièmre carré j1
    if pvj1==0:
        score.create_rectangle(200,50,250,100,fill="white")#troisième carré j1
        can.delete(id_joueur1)
        can.create_image(100,225,image=jeufini,anchor=NW) # Gameover 350*100 
        can.create_image(100,335,image=rejouer,anchor=NW) # Rejouer? 100*50
        can.create_image(350,335,image=quitter,anchor=NW) # Quitter? 100*50
        can.bind("<Button-1>",perdu)
        print('Le joueur 2 a gagné')
    if pvj2==2:
        score.create_rectangle(100,100,150,150,fill="white")
    if pvj2==1:
        score.create_rectangle(150,100,200,150,fill="white")
    if pvj2==0:
        score.create_rectangle(200,100,250,150,fill="white")
        can.delete(id_joueur2)
        can.create_image(100,225,image=jeufini,anchor=NW) # Gameover 350*100 
        can.create_image(100,335,image=rejouer,anchor=NW) # Rejouer? 100*50
        can.create_image(350,385,image=quitter,anchor=NW) # Quitter? 100*50
        can.bind("<Button-1>",perdu)
        print('Le joueur 1 a gagné')

def rajoute_vie(joueur):
    # En entrée     :
    # En sortie     :
    # Effet de bord :
    global pvj1,pvj2,score
    if joueur==1:
        pvj1+=1
    elif joueur==2:
        pvj2+=1
    if pvj1==4:
        pvj1-=1
    if pvj1==3:
        score.create_rectangle(100,50,150,100,fill="red")
    if pvj1==2:
        score.create_rectangle(150,50,200,100,fill="red")
    if pvj2==4:
        pvj2-=1
    if pvj2==3:
        score.create_rectangle(100,100,150,150,fill="blue")    
    if pvj2==2:
        score.create_rectangle(150,100,200,150,fill="blue")

## Ecran de game over ##

def perdu(event):
    global x,y,pvj1,pvj2,xj,yj,xj2,yj2,range_bombe1,range_bombe2,nb_bombes1,nb_bombes2
    x,y=event.x,event.y
    if 350<=event.x<=450 and 335<=event.y<=385:
        fen.quit()
    if 100<=event.x<=200 and 335<=event.y<=385:
        print("rejouer?")
        score.destroy()
        startgame()
    # réinitialisation des variables des joueurs
        pvj1=3
        pvj2=3
        range_bombe1=0
        range_bombe2=0
        nb_bombes1=1
        nb_bombes2=1
        xj,yj=0,0
        xj2,yj2=500,500

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
    # En entrée     :
    # En sortie     :
    # Effet de bord :
    can.create_image(x*50,y*50,image=briques,anchor=NW,tags="briques")

## Blocs ##
blocs=PhotoImage(file="blocs.png")
def ajouter_bloc(x,y):
    # En entrée     :
    # En sortie     :
    # Effet de bord :
    can.create_image(x*50,y*50,image=blocs,anchor=NW,tags="blocs")

### Bombes ###

Bombe1=PhotoImage(file="bomberouge.png")
Bombe2=PhotoImage(file="bombebleue.png")
range_bombe1=0
range_bombe2=0
nb_bombes1=1
nb_bombes2=1

def bombe1(event):
    # En entrée     :
    # En sortie     :
    # Effet de bord :
    global nb_bombes1
    # en entrée : event
    # en effet de bord : création d'une 'bombe' à la position du joueur,
    #                    puis explosion au bout d'une seconde
    if nb_bombes1>0:
        can.create_image(xj,yj,anchor=NW,image=Bombe1,tags='Bombe1')
        a=xj
        b=yj
        nb_bombes1-=1
        can.after(2500,explosion,a,b,1)

def bombe2(event):
    # En entrée     :
    # En sortie     :
    # Effet de bord :
    global nb_bombes2
    # en entrée : event
    # en effet de bord : création d'une 'bombe' à la position du joueur
    #                    puis explosion au bout d'une seconde
    if nb_bombes2>0:
        can.create_image(xj2,yj2,anchor=NW,image=Bombe2,tags='Bombe2')
        a=xj2
        b=yj2
        nb_bombes2-=1
        can.after(2500,explosion,a,b,2)

### Images des animations de l'explosion ###

explosionbleue1=PhotoImage(file='explosionbleue1.png')
explosionbleue2=PhotoImage(file='explosionbleue2.png')
explosionbleue3=PhotoImage(file='explosionbleue3.png')
explosionrouge1=PhotoImage(file='explosionrouge1.png')
explosionrouge2=PhotoImage(file='explosionrouge2.png')
explosionrouge3=PhotoImage(file='explosionrouge3.png')

def explosion(x,y,joueur):
    # En entrée     :
    # En sortie     :
    # Effet de bord :
    global Victoire, range_bombe1,range_bombe2,nb_bombes1,nb_bombes2,id_joueur1,id_joueur2
    destroy=[]
    if joueur==1:
        bonus=range_bombe1
        nb_bombes1+=1
    elif joueur==2:
        bonus=range_bombe2
        nb_bombes2+=1
    a=0
    explosion_bas=False
    explosion_droite=False
    explosion_haut=False
    explosion_gauche=False
    for i in range(len(can.find_overlapping(x,y,x+50,y+50))):
        if id_joueur1==can.find_overlapping(x,y,x+50,y+50)[i]:
            enleve_vie(1)
        elif id_joueur2==can.find_overlapping(x,y,x+50,y+50)[i]:
            enleve_vie(2)
    while explosion_bas==False and a<=bonus:
        for i in range(len(can.find_overlapping(x,y+(a+1)*50,x+50,y+51+a*50))):
            for j in range(len(can.find_withtag('briques'))):
                if can.find_overlapping(x,y+(a+1)*50,x+50,y+51+a*50)[i]==can.find_withtag('briques')[j]:
                    explosion_bas=True
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
                if can.find_overlapping(x,y+(a+1)*50,x+50,y+51+a*50)[i]==can.find_withtag('blocs')[k]:
                    explosion_bas=True
            if id_joueur1==can.find_overlapping(x,y+(a+1)*50,x+50,y+51+a*50)[i]:
                enleve_vie(1)
                can.create_image(x,y+(a+1)*50,anchor=NW,image=explosionrouge3,tags='explosionrouge')
            elif id_joueur2==can.find_overlapping(x,y+(a+1)*50,x+50,y+51+a*50)[i]:
                enleve_vie(2)
                can.create_image(x,y+(a+1)*50,anchor=NW,image=explosionbleue3,tags='explosionbleue')
        if len(can.find_overlapping(x,y+(a+1)*50,x+50,y+51+a*50))==1 and joueur==2:
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
            if id_joueur1==can.find_overlapping(x+(a+1)*50,y,x+51+50*a,y+50)[i]:
                enleve_vie(1)
                can.create_image(x+(a+1)*50,y,anchor=NW,image=explosionrouge2,tags='explosionrouge')
            elif id_joueur2==can.find_overlapping(x+(a+1)*50,y,x+51+50*a,y+50)[i]:
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
            if id_joueur1==can.find_overlapping(x,y-(a+1)*50,x+50,y-1-a*50)[i]:
                enleve_vie(1)
                can.create_image(x,y-(a+1)*50,anchor=NW,image=explosionrouge3,tags='explosionrouge')
            elif id_joueur2==can.find_overlapping(x,y-(a+1)*50,x+50,y-1-a*50)[i]:
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
            if id_joueur1==can.find_overlapping(x-1-a*50,y,x-(a+1)*50,y+50)[i]:
                enleve_vie(1)
                can.create_image(x-(a+1)*50,y,anchor=NW,image=explosionrouge2,tags='explosionrouge')
            elif id_joueur2==can.find_overlapping(x-1-a*50,y,x-(a+1)*50,y+50)[i]:
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
    # En entrée     :
    # En sortie     :
    # Effet de bord :
    if joueur==2: 
        can.delete('explosionbleue')
    elif joueur==1:
        can.delete('explosionrouge')
### BONUS ###
coeur=0
Bombe_bonus=PhotoImage(file="bonus_range.png")

def bonus_bombe(x,y):
    # En entrée     :
    # En sortie     :
    # Effet de bord :
    global range_bombe1,range_bombe2,xj,yj,xj2,yj2
    a=randint(0,100)
    if a<=10:
        can.create_image(x,y,image=Bombe_bonus,anchor=NW,tags="bb")
blanc=PhotoImage(file="blanc.png")
        
def verif_bonus_bombe():
    # En entrée     :
    # En sortie     :
    # Effet de bord :
    global xj,yj,range_bombe1,range_bombe2
    destroy=[]
    a=can.find_enclosed(xj,yj,xj+50,yj+50)
    b=can.find_withtag('bb')
    for i in range (len(a)):
        for j in range (len(b)):
            if  a[i]==b[j]:
                destroy.append(b[j])
                range_bombe1+=1
                score.create_image(500,50,image=blanc,anchor=NW)
                score.create_text(500,68,text="Portée")
                score.create_text(500,82,text="Bombe")
                score.create_text(540,75,text=range_bombe1+1)
    if len(destroy)==1:
        can.delete(destroy[0])

def verif_bonus_bombe1():
    # En entrée     :
    # En sortie     :
    # Effet de bord :
    global xj2,yj2,range_bombe1,range_bombe2
    destroy=[]
    a=can.find_enclosed(xj2,yj2,xj2+50,yj2+50)
    b=can.find_withtag('bb')
    for i in range (len(a)):
        for j in range (len(b)):
            if  a[i]==b[j]:
                destroy.append(b[j])
                range_bombe2+=1
                can.delete("txt1")
                score.create_image(550,50,image=blanc,anchor=NW)
                score.create_text(500,118,text="Portée")
                score.create_text(500,132,text="Bombe")
                score.create_text(540,125,text=range_bombe2+1)
    if len(destroy)==1:
        can.delete(destroy[0])

vie_bonus=PhotoImage(file="vie.png")

def bonus_vie(x,y):
    # En entrée     :
    # En sortie     :
    # Effet de bord :
    global pvj1,pvj2,xj,yj,xj2,yj2
    a=randint(0,100)
    if a<=2:
        can.create_image(x,y,image=vie_bonus,anchor=NW,tags="bv")
        
def verif_bonus_vie():
    # En entrée     :
    # En sortie     :
    # Effet de bord :
    global xj,yj,pvj1,coeur
    destroy=[]
    a=can.find_enclosed(xj,yj,xj+50,yj+50)
    b=can.find_withtag('bv')
    for i in range (len(a)):
        for j in range (len(b)):
            if  a[i]==b[j]:
                destroy.append(b[j])
                rajoute_vie(1)
    if len(destroy)==1:
        can.delete(destroy[0])

def verif_bonus_vie1():
    # En entrée     :
    # En sortie     :
    # Effet de bord :
    global xj2,yj2,pvj2
    destroy=[]
    a=can.find_enclosed(xj2,yj2,xj2+50,yj2+50)
    b=can.find_withtag('bv')
    for i in range (len(a)):
        for j in range (len(b)):
            if  a[i]==b[j]:
                destroy.append(b[j])
                rajoute_vie(2)
    if len(destroy)==1:
        can.delete(destroy[0])

recharge_bonus=PhotoImage(file="bonus_recharge.png")

def bonus_recharge(x,y):
    # En entrée     :
    # En sortie     :
    # Effet de bord :
    a=randint(0,100)
    if a<=7:
        can.create_image(x,y,image=recharge_bonus,anchor=NW,tags='br')

def verif_bonus_recharge():
    # En entrée     :
    # En sortie     :
    # Effet de bord :
    global xj,yj,nb_bombes1
    destroy=[]
    a=can.find_enclosed(xj,yj,xj+50,yj+50)
    b=can.find_withtag('br')
    for i in range (len(a)):
        for j in range (len(b)):
            if  a[i]==b[j]:
                destroy.append(b[j])
                nb_bombes1+=1
                if nb_bombes1==5:
                    nb_bombes1-=1
                score.create_image(200+nb_bombes1*50,50,image=Bombe1,anchor=NW)
    if len(destroy)==1:
        can.delete(destroy[0])

def verif_bonus_recharge1():
    # En entrée     :
    # En sortie     :
    # Effet de bord :
    global xj,yj,nb_bombes2
    destroy=[]
    a=can.find_enclosed(xj2,yj2,xj2+50,yj2+50)
    b=can.find_withtag('br')
    for i in range (len(a)):
        for j in range (len(b)):
            if  a[i]==b[j]:
                destroy.append(b[j])
                nb_bombes2+=1
                if nb_bombes2==5:
                    nb_bombes2-=1
                score.create_image(200+nb_bombes2*50,100,image=Bombe2,anchor=NW) 
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
    # En entrée     :
    # En sortie     :
    # Effet de bord :
    # Personnage 1 #
    perso=can.create_image(0,0,anchor=NW,image=joueur1,tags="perso")
    # Personnage 2 #
    perso2=can.create_image(500,500,anchor=NW,image=joueur2,tags="perso2")
    
## Mouvements Joueur 1 ##
    
def animdroite(event): # déplace le joueur vers la droite
    # En entrée     :
    # En sortie     :
    # Effet de bord :
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
        verif_bonus_vie()
        verif_bonus_recharge()

def animgauche(event): # déplace le joueur1 vers la gauche
    # En entrée     :
    # En sortie     :
    # Effet de bord :
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


def animbas(event): # déplace le joueur1 vers le bas
    # En entrée     :
    # En sortie     :
    # Effet de bord :
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

def animhaut(event): # déplace le joueur1 vers le haut
    # En entrée     :
    # En sortie     :
    # Effet de bord :
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

    ### Joueur 2 ###

## Mouvements Joueur 2 ##

def animdroite2(event): # déplace le joueur2 vers la droite
    # En entrée     :
    # En sortie     :
    # Effet de bord :
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

def animgauche2(event): # déplace le joueur2 vers la gauche
    # En entrée     :
    # En sortie     :
    # Effet de bord :
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

def animbas2(event): # déplace le joueur2 vers le bas
    # En entrée     :
    # En sortie     :
    # Effet de bord :
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

def animhaut2(event): # déplace le joueur2 vers le haut
    # En entrée     :
    # En sortie     :
    # Effet de bord :
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
    
