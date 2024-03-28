
from array import array
import pygame # Main module to develope the game
import random # Just a random module
import numpy as np
import os # Module to read and create directories
import rgb2sml # Module that contains the functions necessary to read the calibration file and make the transformations between rgb and sml
import Intro # Module that contains the start scene of the expriments and creates the file systems to save the data
import datetime # MOdule to print the date time of the experiment

up = 0
right = 1
down = 2
left = 3

global outputfile # These variable will account for the outputfile of the experiment


"""Here I load the calibration file (see module rgb2sml), which has to be the only file with the endname rgb2sml in main file directory"""
calib= rgb2sml.calibration(rgb2sml.openfile()) # Load the parameters of the calibration file
transf= rgb2sml.transformation(calib.A0(), calib.AMatrix(), calib.Gamma()) # Creates an object transf that has as methods all the needed transformations
Stimuli = transf.listS() # This list constains all the possible values to be used as stimuli
L= int( len(Stimuli)) 

""" Choosing the background """
print("Which background (1-8)?")
start = int(input())

print("You choosed: "+ str(start) )



def colortopygame( color):  # This functions receives an array and returns a pygame Color object
    return pygame.Color( int(color[0]) %256  ,int(color[1]) %256,int(color[2]) %256)

def  convexvalues(rgb): # This functions receives rgb values and returns the matrix of vectors A and vector b of coordinates for the convex combination. rgb=np.dot(b,A)
    rgb=np.array(rgb)
    ref = np.round(rgb)
    delta = rgb - ref
    
    C=np.zeros((3,3))
    C[0] = ref + np.sign(delta[0]) *np.array([1,0,0])
    C[1] = ref + np.sign(delta[1]) *np.array([0,1,0])
    C[2] = ref + np.sign(delta[2]) *np.array([0,0,1])
    O =  ref + np.sign(delta) 
    delta = np.abs(delta)
    deltaO = delta.min()
    ind= list(delta).index(delta.min())
    print(np.append([ref],C,axis=0))
    if np.sum(delta) <1:
        return (  np.append([ref],C ,axis=0), np.append(1- np.sum(delta), delta )  )
    else:
        delta = delta - delta[ind]
        delta[ind] = deltaO
        C[ind] = O
        return( np.append([ref],C,axis=0), np.append(1- np.sum(delta), delta )  ) 
        
def surfarray(size , rgb ): # Creates the surface array
    C, prob = convexvalues(rgb)
   
    index= np.random.choice([0,1,2,3],p=prob, size= (int(size),int(size)))
    
    

    return C[index]


""" Class for patch stimulus, you choose the position, size and color"""

class Patch():
    def __init__(self, center, size, color, back_color,pos):
        self.center = center 
        self.size= size
        self.color = color
        self.back_color = back_color
        self.pos = pos
    
    def update(self, color): # This function should be defined according to what it means to move 1 step in your experiment
        self.color=color
      
    def render(self,screen):

        self.color = [0,0,0]
        k = 0.5
       

        def dist(i,j):
            distancia = float(np.sqrt((i)**2 +(j)**2))
            return distancia

        surf = pygame.surfarray.make_surface(surfarray(self.size,self.color)) # Creates the surface
        

    
        array_circular = np.zeros((int(self.size)+1,int(self.size)+1,3))

       

        surf = pygame.surfarray.make_surface(array_circular)

        




       

    


        screen.blit(surf, self.center)    # center is actually the top-left coordinates

"""  Class for background, for now it's a uniform colored background """

class Background():
    def __init__(self,color):
        self.color=np.round(color)

    def update(self,newcolor):
        self.color= np.round(newcolor)

    def back_color():
        return Background.color
    


"""  Class Trial, it will sum up all the objects necesary for each trial, in this case: background and patch """
class Trial():
    def __init__(self, back, patch):
        self.back=back
        self.patch=patch
    
    def show(self,screen, time): # Presents the stimulus on the screen for (time) seconds 
        screen.fill(self.back.color)
        pygame.draw.circle(screen,(0,0,0),(int(screen.get_width()/2), int(screen.get_height()/2) ),3)
        pygame.display.flip()
        t=pygame.time.get_ticks()
        while (pygame.time.get_ticks()-t < 500):
            for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                     pygame.quit()
                 if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                     pygame.quit()
        self.patch.render(screen)
        pygame.display.flip()
        t=pygame.time.get_ticks()
        while (pygame.time.get_ticks()-t < 1000*time):
            for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                     pygame.quit()
                 if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                     pygame.quit()
        
        
        
    def response(self, screen, position): # Checks the response of the subjects and returns whether if the response was right or not.
        screen.fill(self.back.color)
        pygame.display.flip()
        while(1):
            for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                     pygame.quit()
                 if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                     pygame.quit()
                                      
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP]:
                if self.patch.center== position[0]:
                    return True
                else:
                    return False
            if pressed[pygame.K_RIGHT]:
                if self.patch.center== position[1]:
                    return True
                else:
                    return False
            if pressed[pygame.K_DOWN]:
                if self.patch.center== position[2]:
                    return True
                else:
                    return False
            if pressed[pygame.K_LEFT]:
                if self.patch.center== position[3]:
                    return True
                else:
                    return False
            if pressed[pygame.K_SPACE]:
                return False 
    
    def wait(self, screen):
        screen.fill(self.back.color)
        pygame.display.flip()
        done= False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    done= True
        
#### Definition of the experiemnt stimuli
                     
                     

""" Create the list of Backgrounds used in the experiment  """

def CreateBacks (Nb, Nr,Nd):
    Backs = []
    for i in np.linspace(0.2*L,0.96*L, Nb)   :
        Baux= Stimuli[    int( i)]
        for j in range(Nr*Nd):
            Backs.append( Background( colortopygame( Baux ) ) )
     
    return( Backs)



""" Creates the list of Patches initialization used in the experiment"""

def CreatePatches(Nb, Nr, Nd, position, size):
    Patches= []
    Paux=[]
    Sincrements= np.array([ 0.006     ,  0.00628571,  0.00757143,  0.00885714,  0.01014286,
        0.01142857,  0.01271429,  0.014     ])

    
    for i in range(8) :
        for j in range(Nd):
            rgbaux = transf.changeS(  Stimuli[int(np.linspace(0.2*L,0.96*L, Nb)[i])], -((Nd-1)/2 - j )*Sincrements[i] )
            rgb_fondo = Stimuli[int(np.linspace(0.2*L,0.96*L, Nb)[i])]
            for k in range(Nr):
                Paux.append(   Patch( position[random.randint(0,3)] , size,  rgbaux, rgb_fondo      ) ) # In this case I create a random position for each Trial
        random.shuffle(Paux)
        Patches= Patches + Paux
       
        
        Paux=[]
    print("Patches es:")
    print(Patches)

    return Patches


""" Creates the list of Trials initialization used in the experiment, Nr accounts for number of repetitions"""

def CreateTrials(Backs, Patches):
    Trials=[]
    for j in range(len(Backs)):
        Trials.append(   Trial(Backs[j],Patches[j] ) )

    return( Trials )



""" Saving data function """

def SaveTrial(output,trial, response,time):
            output.write("%lf\t%lf\t%i\t%lf\n" % (  transf.rgb2sml(trial.back.color)[0],transf.rgb2sml(trial.patch.color)[0], response, time/1000 ) )


""" Main function of experiment """
    

def main(start):
    # Initializes the game
    pygame.init()
    # Monitor Info (height and width)
    Monitor= pygame.display.Info();
    h= Monitor.current_h
    w= Monitor.current_w
    pygame.mouse.set_visible(False)

    #Adaptation time
    adpt=120
    #Frames per second (important for the flickering)
    fps=60
    # Builds the Object screen in Fullmode
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    # Creates Backgrounds, initializes back with the first one, choose number of repetitions
    Nb=8  # Number of backgrounds 8
    Nr=3 # Number of repetitions for each color 20
    Nd=4 # Number of bins where you will mesaure  15
    backs= CreateBacks(Nb,Nr, Nd)
   
    # Creates Patches: patch size, position and number of patches, initialize patch 
    size= h/4  #original h/10
    center=  (int( w/2 )   , int( h/2 ) )
    UP=  ( w/2 - size/2,  h/2 - size/2 - size   )
    RIGHT= ( w/2 - size/2  + size ,  h/2 - size/2)
    DOWN = ( w/2 - size/2,  h/2 - size/2 + size)
    LEFT = ( w/2 - size/2   - size,  h/2 - size/2)
    position =[ UP, RIGHT, DOWN, LEFT]
    patches = CreatePatches(Nb,Nr,Nd, position, size)
    exp=0.2 # Time of exposition of the Stimuli original 0.15
    
    # Create trials
    Nt=Nd*Nb*Nr # Total number of trials
    trials = CreateTrials(backs,patches)
 


    done = False #initial loop state
    i=0 #this index goes over the iteration of the experiment
    k=(start-1)*Nr*Nd # Initial trial Number regarding to the choosen background by the user
  
    trial=trials[k]
   
    global outputfile
    """ This part checks what calibration is being used and saves the info in the outputfile """
    basepath= './'
    with os.scandir(basepath) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith("rgb2lms"):
                calibname= entry.name
    #Date
    outputfile.write(str(datetime.datetime.now())+"\n")
    # Calibration used
    outputfile.write("Calibration: "+calibname+"\n")
    # Adaptation time
    outputfile.write("Adaptation time: " + str(adpt)+ "sec \n")
    # Sorting type
    outputfile.write("Sorting: Crescent \n")
    #  Monitor 
    outputfile.write("Monitor:" +str(w)+"x"+str(h)+"\n")
    # Patch size
    outputfile.write( "Patch Size:" +str(h/5) +"\n")
    # Patch  distance
    outputfile.write( "Patch distance: " +str( h/5) +"\n")
    outputfile.write( "Exposure time:" +str(exp) + "\n" )
    outputfile.write( "spatial frequency k:" +str(k) + "\n" )

    
    outputfile.write("Background number:"+ str(start)+"\n")
    outputfile.write("Background RGB:" +str(trial.back.color) +"\n")
    outputfile.write("Background (S) :  Patch (S)  : R or W : Time \n")
    outputfile.write("adaptation \n")
    
    
    
    
    
    
    
    time= pygame.time.get_ticks()  # Starts the clock
    
    while not done:
        
        while pygame.time.get_ticks() - time < 1000*adpt:
            if k + i  < (start-1)*Nr*Nd  + 5:
                trial.patch.update( transf.changeS(trial.patch.color, 0.2*np.power(-1,i) ))   
                
            trial.show(screen, exp)
            resp= trial.response(screen,position)
            SaveTrial(outputfile,trial,resp, pygame.time.get_ticks() - time )
            trial.wait(screen)
            
            i= ((i+1) % (Nr*Nd) )
            trial= trials[i+k]
      
        
        if k % (Nr*Nd)==0 : 
            outputfile.write("adapted \n")
            backs= CreateBacks(Nb,Nr, Nd)
            patches = CreatePatches(Nb,Nr,Nd, position, size)
            trials = CreateTrials(backs,patches)
         
        
        trial= trials[k]
        trial.show(screen, exp)
        resp= trial.response(screen,position)
        SaveTrial(outputfile,trial,resp, pygame.time.get_ticks() - time )
        trial.wait(screen)
        k+=1
        if (k==start*Nr*Nd): done= True; continue 
        trial= trials[k]
        
        
        
       
        
            
           
 
       
    
    pygame.quit()
    quit()

outputfile= Intro.game_intro()

main(start) # runs Main, the variable start receives as input the background number choose by the user
        

                
        
