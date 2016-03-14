#Création et déplacement d'un personnage
#Déplacement avec les flèches
#Détection des cases "pleines"
#sur lesquelles le personnage ne peut
#pas aller.


from tkinter import*
from random import*

fen=Tk()
fen.title('Personnage')
can=Canvas(fen, width =448, height =448, bg ='black')
can.pack(side=TOP,padx=5,pady=5)

### variables joueur ###

xj,yj,case=250,250,[]#case: coordonnées de la case
place=[int(xj/50),int(yj/50)]#position du personnage
perso=can.create_rectangle(xj,yj,xj+50,yj+50,fill="red",outline="red"),
oeilgauche=can.create_rectangle(xj+10,yj+10,xj+20,yj+20,fill="black"),#oeil gauche
oeildroit=can.create_rectangle(xj+30,yj+10,xj+40,yj+20,fill="black"),#oeil droit
bouche=can.create_rectangle(xj+15,yj+30,xj+35,yj+35,fill="black")#bouche

### variables ennemis ###

spawn=[[1,0],[3,0],[5,0],[7,0],[0,1],[8,1],[0,3],[8,3],[0,5],[8,5],[0,7],
[8,7],[1,8],[3,8],[5,8],[7,8]]


### Personnage / joueur ###

def animdroite(event):
   	global xj,yj,case,place
   	xj+=50
   	can.coords(perso,xj,yj,xj+50,yj+50)
   	can.coords(oeilgauche,xj+10,yj+10,xj+20,yj+20)
   	can.coords(oeildroit,xj+30,yj+10,xj+40,yj+20)
   	can.coords(bouche,xj+15,yj+30,xj+35,yj+35)
   	place[0]+=1
   	if place[0]%2==0 and place[1]%2==0 or place[0]==9:
   		animgauche(event)
   	print(place)

def animgauche(event):
   	global xj,yj
   	xj-=50
   	can.coords(perso,xj,yj,xj+50,yj+50)
   	can.coords(oeilgauche,xj+10,yj+10,xj+20,yj+20)
   	can.coords(oeildroit,xj+30,yj+10,xj+40,yj+20)
   	can.coords(bouche,xj+15,yj+30,xj+35,yj+35)
   	place[0]-=1
   	if place[0]%2==0 and place[1]%2==0 or place[0]==-1:
   		animdroite(event)
   	print(place)

def animbas(event):
   	global xj,yj
   	yj+=50
   	can.coords(perso,xj,yj,xj+50,yj+50)
   	can.coords(oeilgauche,xj+10,yj+10,xj+20,yj+20)
   	can.coords(oeildroit,xj+30,yj+10,xj+40,yj+20)
   	can.coords(bouche,xj+15,yj+30,xj+35,yj+35)
   	place[1]+=1
   	if place[0]%2==0 and place[1]%2==0 or place[1]==9:
   		animhaut(event)
   	print(place)

def animhaut(event):
   	global xj,yj
   	yj-=50
   	can.coords(perso,xj,yj,xj+50,yj+50)
   	can.coords(oeilgauche,xj+10,yj+10,xj+20,yj+20)
   	can.coords(oeildroit,xj+30,yj+10,xj+40,yj+20)
   	can.coords(bouche,xj+15,yj+30,xj+35,yj+35)
   	place[1]-=1
   	if place[0]%2==0 and place[1]%2==0 or place[1]==-1:
   		animbas(event)
   	print(place)

### Personnage / ennemi ###

def ennemispawn():
    global ennemi,xe,ye
    shuffle(spawn,random=None)
    print(spawn)
    xe=(spawn[0][0])*50
    ye=(spawn[0][1])*50
    ennemi=can.create_oval(xe,ye,xe+50,ye+50,fill="green")
    print(int(xe/50),int(ye/50))
    ennemimove()

def ennemimove():
    global xe,ye,ennemi
    if xe==0:
      ennemidroite()
      #xe=(randrange(0,8,8))
      print(xe)
    elif xe/50==8:
      ennemigauche()
      #xe=(randrange(0,8,8))
      print(xe)
    elif ye==0:
      ennemibas()
      #xe=(randrange(0,8,8))
      print(ye)
    else:
      ennemihaut()
      #xe=(randrange(0,8,8))
      print(ye)

def ennemidroite():
    global xe,ye,ennemi
    xe+=10
    can.coords(ennemi,xe,ye,xe+50,ye+50)
    fen.after(100,ennemidroite)

def ennemigauche():
    global xe,ye,ennemi
    xe-=10
    can.coords(ennemi,xe,ye,xe+50,ye+50)
    fen.after(100,ennemigauche)

def ennemihaut():
    global xe,ye,ennemi
    ye-=10
    can.coords(ennemi,xe,ye,xe+50,ye+50)
    fen.after(100,ennemihaut)

def ennemibas():
    global xe,ye,ennemi
    ye+=10
    can.coords(ennemi,xe,ye,xe+50,ye+50)
    fen.after(100,ennemibas)


      
      



### Grille ###

def grille():
    for j in range(0,10,2):
        for i in range(0,10,2):
        	can.create_rectangle(50*i,50*j,50*(i+1),50*(j+1),fill="blue",outline="blue")
        	case.append([i,j])
       	print(case)

	
### Programme ###

Quitter=Button(fen,text="Quitter",command=fen.quit)
Quitter.pack(side=BOTTOM)
Ennemi=Button(fen,text="Ennemi",command=ennemispawn)
Ennemi.pack(side=LEFT)
grille()
#ennemispawn()
fen.bind("<KeyRelease-Left>",animgauche)
fen.bind("<KeyRelease-Right>",animdroite)
fen.bind("<KeyRelease-Up>",animhaut)
fen.bind("<KeyRelease-Down>",animbas)
fen.mainloop()
fen.destroy()