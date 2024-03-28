#este es el programa principal que no debería ser cambiado nunca jamás
from array import array
import pygame # Main module to develope the game
import random # Just a random module
from scipy.special import jv
import numpy as np
import os # Module to read and create directories
import rgb2sml # Module that contains the functions necessary to read the calibration file and make the transformations between rgb and sml
import Intro # Module that contains the start scene of the expriments and creates the file systems to save the data
import datetime # MOdule to print the date time of the experiment
import auxiliar_function as af
from ML_estimator import * 
 # Initializes the game
pygame.init()
# Monitor Info (height and width)
Monitor= pygame.display.Info();
h= Monitor.current_h
w= Monitor.current_w

global outputfile # These variable will account for the outputfile of the experiment

global k_espacial # This variable account for the spatial frequency of the stimulus

#k_espacial = 1 #1.25,1.5,0.75,0.25,0.1

up = 0

down = 1

right = 2

left = 3



"""Here I load the calibration file (see module rgb2sml), which has to be the only file with the endname rgb2sml in main file directory"""
calib= rgb2sml.calibration(rgb2sml.openfile()) # Load the parameters of the calibration file
transf= rgb2sml.transformation(calib.A0(), calib.AMatrix(), calib.Gamma()) # Creates an object transf that has as methods all the needed transformations
Stimuli = transf.listS() # This list constains all the possible values to be used as stimuli

escala = 6 #ESTO TIENE QUE SER 6 NO SE TOCA AAA
""" Class for patch stimulus, you choose the position, size and color"""

""" Choosing the background """
#print("Which background (1)?")
#start = int(input())
#print("You choosed: "+ str(start) )

start = 1

class Patch():
    def __init__(self, back_color,pos,delta_s):
        self.pos = pos
        self.center = [0,0]
        self.size_x = w/escala
        self.size_y = h/escala
        self.back_color = np.round(back_color)
        self.delta_s = delta_s
    
    def update_amplitude(self, amplitude): # This function should be defined according to what it means to move 1 step in your experiment
        self.delta_s = amplitude
      
    def render(self,screen):

    
        position_mapping = {
        up: [int(self.size_x/2), int(self.size_y*3/8)],
        down: [int(self.size_x/2), int(self.size_y*5/8)],
        right: [int(self.size_x/2) + int(self.size_y/8), int(self.size_y/2)],
        left: [int(self.size_x/2) - int(self.size_y/8), int(self.size_y/2)]
        }

         
        array_circular = np.zeros((int(self.size_x),int(self.size_y),3))

        if self.pos in position_mapping:
            screen_center = position_mapping[self.pos]
                

        for i in range(int(self.size_x)):
            for j in range(int(self.size_y)):                                     
                    modulacion = jv(0,k_espacial*af.dist(i-screen_center[0],j-screen_center[1]))*np.sqrt(k_espacial)                  
                    array_circular[i,j,:] = transf.changeS(  self.back_color, self.delta_s*modulacion )
                           
        surf = pygame.surfarray.make_surface(array_circular)
        surf = pygame.transform.scale(surf, (self.size_x*escala, self.size_y*escala))
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
        screen.fill(self.back.color)
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
                if self.patch.pos == position[0]:
                    return True
                else:
                    return False
            if pressed[pygame.K_RIGHT]:
                if self.patch.pos == position[1]:
                    return True
                else:
                    return False
            if pressed[pygame.K_DOWN]:
                if self.patch.pos == position[2]:
                    return True
                else:
                    return False
            if pressed[pygame.K_LEFT]:
                if self.patch.pos == position[3]:
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

def CreateBacks (N, background_RGB):
    Backs = []
    for _ in range(N):
        Backs.append( Background( af.colortopygame( background_RGB ) ) ) 
    return( Backs)



""" Creates the list of Patches initialization used in the experiment"""

def CreatePatches(Nt, background_RGB):
    Patches= []

    max_deltaS = 0.07

    delta_S = [max_deltaS/5,max_deltaS*2/5,max_deltaS*3/5,max_deltaS*4/5,max_deltaS]
    minus_delta_S = [-x for x in delta_S]
    possible_S = delta_S + minus_delta_S

    for _ in range(Nt):

        delta_s = random.choice(possible_S)
        pos = random.randint(0,3)
        rgbaux = transf.changeS(  background_RGB, delta_s )
        Patches.append(   Patch( background_RGB, pos,delta_s      ) ) # In this case I create a random position for each Trial
    
    return Patches


""" Creates the list of Trials initialization used in the experiment, Nr accounts for number of repetitions"""

def CreateTrials(Backs, Patches):
    Trials=[]
    for j in range(len(Backs)):
        Trials.append(   Trial(Backs[j],Patches[j] ) )

    return( Trials )



""" Saving data function """

def SaveTrial(output,trial, response,time):
            output.write("%lf\t%lf\t%i\t%lf\n" % (  transf.rgb2sml(trial.back.color)[0], trial.patch.delta_s, response, time/1000 ) )


""" Main function of experiment """
    

def main(start):

    start = start -1 

    backgrounds = [[128, 128, 128]]

    background_RGB = backgrounds[start]
    
    pygame.mouse.set_visible(False)

    #Adaptation time in seconds
    adpt=120
    #Frames per second (important for the flickering)
    fps=60
    # Builds the Object screen in Fullmode
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    # Creates Backgrounds, initializes back with the first one, choose number of repetitions
    #Nb=1  # Number of backgrounds 8        
    #Nr= 4 # Number of repetitions for each color 20
    #Nd= 1 # Number of bins where you will mesaure  15

    Nt = 50 #Total number of trials 

    backs= CreateBacks(Nt,background_RGB)
       
    # Creates Patches: patch size, position and number of patches, initialize patch 
    size_1= h/2  #original h/10
    size_2 = int(np.sqrt(2)*size_1)
    center=  (int( w/2 )   , int( h/2 ) )
    UP=  ( w/2 - size_2/2,  0   )
    RIGHT= ( w/2 ,  h/2 - size_2/2)
    DOWN = ( w/2 - size_2/2,  h/2 )
    LEFT = ( w/2 - size_1  ,  h/2 - size_2/2)
    position =[ up, right, down, left]
    size_1 = h/escala
    size_2 = w/escala
    patches = CreatePatches(Nt, background_RGB)
    exp=1 # Time of exposition of the Stimuli
    
    # Create trials
    trials = CreateTrials(backs,patches)

    done = False #initial loop state
    i=0 #this index goes over the iteration of the experiment
    trial=trials[0]
   
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
    # Time of exposure to the stimulus
    outputfile.write( "Exposure time:" +str(exp) + "\n" )    
    # spatial frecuency of the modulation
    outputfile.write( "Spatial frequency k:" + str(k_espacial) + "\n" )
    # Escala variable 
    outputfile.write( "Escala:" + str(escala) + "\n" )
    # RGB coordinates of reference color
    outputfile.write("Background RGB:" +str(trial.back.color) +"\n")

    outputfile.write("Background (S) :  Amplitude (S) : R or W : Time \n")
    outputfile.write("adaptation \n")
    
    
    
    
    
    
    
    time= pygame.time.get_ticks()  # Starts the clock

    amplitudes = []

    results = []
    
    while not done:
        
        while pygame.time.get_ticks() - time < 1000*adpt:


            #trial.patch.update_amplitude( transf.changeS(trial.patch.color, 0.2*np.power(-1,i) ))   
            amplitudes.append(trial.patch.delta_s)
            trial.show(screen, exp)
            resp = trial.response(screen,position)
            results.append(resp)
            SaveTrial(outputfile,trial,resp, pygame.time.get_ticks() - time )
            trial.wait(screen)
            
            i= ((i+1) % (Nt) )
            trial= trials[i]
      
        amplitudes = amplitudes[-11:-1]
        results = results[-11:-1]      

        outputfile.write("adapted \n")
        backs = CreateBacks(Nt,background_RGB)
        patches = CreatePatches(Nt, background_RGB)
        trials = CreateTrials(backs,patches)

        for i, trial in enumerate(trials):

            h_estimation = estimador(amplitudes, results)

            new_amplitude = 1.317*h_estimation.params[0]
            
            trial.patch.update_amplitude(new_amplitude)                        
            trial.show(screen, exp)
            resp= trial.response(screen,position)

            amplitudes.append(trial.patch.delta_s)
            results.append(resp)

            SaveTrial(outputfile,trial,resp, pygame.time.get_ticks() - time )
            trial.wait(screen)
    
        done= True;
    
    pygame.quit()
    quit()

outputfile, k_espacial = Intro.game_intro()



main(start) # runs Main, the variable start receives as input the background number choose by the user
        

                
        
