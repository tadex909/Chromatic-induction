#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 11:35:18 2019

@author: nicovattuone
"""
import inputbox
import pygame
import os




def game_intro():

    pygame.init()
    
    Monitor= pygame.display.Info();
    h= Monitor.current_h
    w= Monitor.current_w
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    screen.fill((250,250,250))
    start= pygame.image.load("./Images/Startscene.png")
    screen.blit(pygame.transform.scale(start,(w,h)), (0,0))
    Name=inputbox.ask(screen, "Name")
    
    basepath= "./"
    s=0
    # Checks for the existence of the folder Subjects, if it does not exist it creates it
    with os.scandir(basepath) as entries:
        for entry in entries:
           if entry.is_dir():
               s+= (entry.name == "Subjects")
    if s==0:
        os.mkdir("Subjects")         
    # Checks for subject name
    s=0
    with os.scandir( basepath +  "Subjects/" ) as entries:
        for entry in entries:
            if entry.is_dir():
                s+= (entry.name==Name)
 
    if s==0:
        os.mkdir(basepath+"Subjects/"+Name)
    # Checks for sessions
    i=0
    with os.scandir( basepath + "Subjects/"+ Name) as entries:
        for entry in entries:
           if entry.name.startswith(Name):
               if int( entry.name[len(Name):-len(".dat")]  ) > i:
                  i=int(entry.name[len(Name):-len(".dat")])
            
            

    pygame.display.flip()
    out =  open("./Subjects/"+Name+"/"+Name+str(i+1)+".dat","w")
    
    out.write("Subject:"+Name+" \n")
    out.write("Session Nr:"+str(i+1)+"\n")
       
    return out

