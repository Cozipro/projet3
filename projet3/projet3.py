import matplotlib.pyplot as plt
import numpy as np
import matplotlib.widgets as wdg

class rayon:
    def __init__(self,figure, x =0, y=0, teta=0, color = "k", direction = True, origine = None):
        self.x = x  #abscisse d'origine
        self.y =y   #ordonnée d'origine
        self.teta = teta    #angle du rayon par rapport à l'axe des abscisses
        self.color = color  #Couleur du rayon
        self.direction = direction  #Direction du rayon
        self.origine = origine      #Permet de savoir l'origine du rayon (de quel miroir il provient), utile pour le débogage
        
        self.fig, self.ax = figure  #Figure sur laquelle tracer
        
        
        
        if self.direction: #Défini le vecteur x conrrespondant a la direction du rayon
            self.x_array = np.linspace(self.x,self.x+20)
        else:
            self.x_array = np.linspace(self.x, self.x-20)
        
        if origine != None:
            self.color="C1"
        
        
        #On appelle la méthode check() permettant de déterminer si le rayon entre en contact avec un miroir
        self.check()
        
    def trace(self):
        #méthode traçant le rayon
        y = (self.x_array-self.x)*np.tan(self.teta) +self.y #vecteur y
        
        self.ax.plot(self.x_array, y,self.color) #plot
        
    def check(self):
        for miroir in lst_miroir: #On regarde si le rayon entre en contact avec chaque miroir
            
            #Résolution de l'équation
            A = 1+(np.tan(self.teta)**2)
            B = -2*(miroir.x-miroir.r) -2*self.x*(np.tan(self.teta)**2)+2*self.y*np.tan(self.teta)
            C = (miroir.x-miroir.r)**2 + (self.x**2)*(np.tan(self.teta)**2) - 2*self.y*self.x*np.tan(self.teta) + (self.y**2) - (miroir.r**2)

            delta = (B**2)-(4*A*C)

            #Si r>0, la solution est sur la droite du "cercle", sinon elle est sur la gauche du "cercle"
            if miroir.r>0:
                X1 = (-B+np.sqrt(delta))/(2*A)
            else:
                X1 = (-B-np.sqrt(delta))/(2*A)
            Y1 = (X1-self.x)*np.tan(self.teta) +self.y  #Calcul de l'ordonnée du point de contact

            if round(X1) == round(self.x): #Sécurité pour éviter de créer un deuxième rayon réfléchi au point de départ d'un rayon réfléchi
                continue

            #On vérifie si le programme n'as pas choisi la mauvaise solution, et que la solution est bien sur le miroir
            if Y1 < miroir.max and Y1 > miroir.min and (((self.direction == False) and (self.x > miroir.x)) or ((self.direction == True) and (self.x < miroir.x))) and X1 >= np.min(miroir.xc) and X1 <= round(np.max(miroir.xc)) and X1 <= max(self.x_array):


                self.x_array = np.linspace(self.x,X1,100)  #On créé le vecteur x entre le point de départ et d'arrivée
                teta_rayon = np.arcsin(Y1/miroir.r)        #On calcule l'angle de la normale
                teta_nouveau = -np.pi + 2*teta_rayon - self.teta    #On calcule l'angle du rayon réfléchi
                    
                if abs(teta_nouveau) > np.pi/2 and abs(teta_nouveau) < 3*np.pi/2: #On définit la direction du rayon en fonction de son angle
                    direction = False
                else:
                    direction = True
                
                #On créé un nouveau rayon (réfléchi) en fonction du point de contact avec le miroir, l'angle et sa direction
                lst_ray.append(rayon((self.fig,self.ax),X1,Y1, teta_nouveau, origine = miroir, direction = direction))

        self.trace()    #On trace le rayon incident

class source:
    def __init__(self,figure, x, y, angle, N, inf = False, height = 0):
        self.figure = figure    #Figure sur laquelle tracer
        self.x = x              #Position x,y de la source
        self.y = y
        self.alpha = angle      #Demie angle d'ouverture de la source
        self.N = N              #Nombre de rayon créés par la source
        self.infiny = inf       #Source à l'infinie
        self.height = height    #Hauteur de création des rayons en mode infini

        self.create_ray()

    def create_ray(self):
        lst_angle = np.linspace(-self.alpha, self.alpha, self.N)    #Liste des angles pour chaque rayon de la source

        if self.infiny: #Si la source est à l'infini
            for y in np.linspace(-self.height/2, self.height/2, self.N):
                lst_ray.append(rayon(self.figure, self.x, y, 0))    #Création d'un rayon d'angle 0rad
        else:
            for angle in lst_angle:
                lst_ray.append(rayon(self.figure, self.x, self.y, angle)) #Sinon on trace un rayon avec l'angle correspondant


    
class miroir:
    def __init__(self,figure, position =0, r = 10, dia = np.pi/3, color ="k"):
        self.x = position       #position du miroir sur l'axe des abscisses
        self.diametre = dia     #demi-diamètre d'ouverture
        self.r = r              #Rayon du miroir
        self.color = color      #Couleur du miroir
        self.fig, self.ax = figure  #Figure sur laquelle tracer le miroir

        self.max = abs(self.r) * np.sin(self.diametre) #Ordonnée max du cercle utile lors d'une condition dans la méthode rayon.check()
        self.min = -self.max    #Idem que pour le max, mais avec le minimum

        self.trace()    #On trace le miroir

    def trace(self):
        teta = np.linspace(-self.diametre, self.diametre,500)   #Vecteur teta correspondant à l'angle de chaque point du cercle par rapport à l'axe des x
        
        self.xc = self.r*np.cos(teta) - self.r + self.x #array des x
        self.yc = self.r*np.sin(teta)   #array des y
        
        self.ax.plot(self.xc, self.yc, color = self.color) #tracé du miroir
        #self.ax.plot(self.x - self.r, 0,marker = "o", color = self.color) #Tracé du centre du miroir
        
        
    
if __name__ == "__main__":
    fig = plt.subplots()      

    lst_ray = []
    lst_miroir = []
    lst_source = []
    
    def test():
        for rayon in lst_ray:
            del rayon
        for sourcee in lst_source:
            del sourcee
        plt.clf
        lst_miroir.append(miroir(position = 7, r=-5, figure = fig, color = "blue"))

        lst_source.append(source(fig,-4,-1.5,np.pi/6-0.2, 6))

    test()
    fig[1].grid(True)
    fig[1].set_aspect("equal")
    fig[1].set_xlim(-10,10)
    fig[1].set_ylim(-7,7)
        

    plt.show()
