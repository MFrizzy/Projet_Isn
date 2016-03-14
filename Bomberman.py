# Bomberman
# Fonction qui dessine la  map
# Ligne de commentaire test pour git

from tkinter import*

def dessiner_map():
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

# Toujours une ligne de commentaire test pour git (2)
# Toujours et encore l'inimitable ligne inutile pour le test de merde
    

def ajouter_brique(x,y):
    can.create_rectangle(x*50,y*50,x*50+50,y*50+50,fill="grey")
    can.create_line(x*50,50*y+(50/4),x*50+50,y*50+(50/4))
    can.create_line(x*50,50*y+(2*50/4),x*50+50,y*50+(2*50/4))
    can.create_line(x*50,50*y+(3*50/4),x*50+50,y*50+(3*50/4))

def ajouter_bloc(x,y):
    can.create_rectangle(x*50,y*50,x*50+50,y*50+50,fill='black')

### c'est la bite
    
###### Programme #######
fen=Tk()
fen.title('Bomberman')
can = Canvas(fen, width =550, height =550, bg ='ivory')
can.pack(side =TOP, padx =5, pady =5)
dessiner_map()
fen.mainloop()
