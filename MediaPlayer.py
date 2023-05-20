import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from direct.gui.DirectGui import *
import random
from panda3d.core import Point3
import math
import GameSettings as gms
from panda3d.core import AudioManager
try:
    import Tkinter as tk
    import tkFileDialog as fd
except:
    import tkinter as tk
    from tkinter import filedialog as fd
from panda3d.core import Filename

class Media_Player():

    def __init__(self,pos):
        self.audio_list = ["Sounds/sound01.wav"]
        self.musicMgr = base.sfxManagerList[0]
        self.music =  loader.loadSfx(self.audio_list[0])
        self.musicMgr.setVolume(0.5)    
        self.music.play()
        self.gui = loader.loadModel("media_player_gui.egg")
        self.direct_frame =  DirectFrame(geom = self.gui.find("**/frame"),
                                         frameSize = (0.01,0.001,0.001,0.001),
                                         pos = (-0.9,0,-0.78))
        self.direct_frame.setScale(0.1)
        base.enableMusic(True)
        self.next_button = DirectButton(geom = self.gui.find("**/next_button"),pos = (0,0,0.0),parent = self.direct_frame,command = self.next_)
        self.prev_button = DirectButton(geom = self.gui.find("**/prev_button") ,pos = (0,0,0.0),parent = self.direct_frame,command = self.prev)
        self.pause_button = DirectButton(geom = self.gui.find("**/pause_button") ,pos = (0,0,0.0),parent = self.direct_frame,command = self.pause)
        self.select_audio_button = DirectButton(geom = self.gui.find("**/select_audio_button"),pos = (0,0,-0.07),parent = self.direct_frame,command = self.add_audio)
        taskMgr.add(self.update, "Update")
        self.track_num = 0
    def play(self):
       
        if self.music.status() == self.music.READY:
            self.music.setTime(self.pause_time + 0.1)
            self.play_button.destroy()
            self.musicMgr.update()
        self.musicMgr.setVolume(0.5)  
        self.music.play()             
        self.pause_button = DirectButton(geom = self.gui.find("**/pause_button") ,pos = (0,0,0.0),parent = self.direct_frame,command = self.pause)
        return
    
    def pause(self):
    
        if self.music.status() == self.music.READY:
            return
        self.pause_time = self.music.getTime()
        self.music.stop()
        self.pause_button.destroy()
        self.play_button = DirectButton(geom = self.gui.find("**/play_button"),pos = (0,0,0.0),parent = self.direct_frame,command = self.play)
        return
    
    def next_(self):
        if self.music.status() == self.music.READY:
         self.play_button.destroy()
         self.pause_button = DirectButton(geom = self.gui.find("**/pause_button") ,pos = (0,0,0.0),parent = self.direct_frame,command = self.pause)
        self.music.setTime(self.music.getTime() + 7)
        self.musicMgr.setVolume(0.5) 
        self.music.play()
        self.musicMgr.update()
        self.musicMgr.update()
        return
    def prev(self):
        if self.music.status() == self.music.READY:
         self.play_button.destroy()
         self.pause_button = DirectButton(geom = self.gui.find("**/pause_button") ,pos = (0,0,0.0),parent = self.direct_frame,command = self.pause)
        self.music.setTime(self.music.getTime() - 7)
        self.musicMgr.setVolume(0.5) 
        self.music.play()
        self.musicMgr.update()
        self.musicMgr.update()        
        return
    def add_audio(self):

        root = tk.Tk()
        root.withdraw()
        file_path = fd.askopenfilename()
        panda_file_path = str(Filename.fromOsSpecific(file_path))
        self.audio_list.append(panda_file_path)
        self.musicMgr.update()
        return
    def update(self,task):
      
        if self.music.length() == self.music.getTime():
            self.track_num = (self.track_num + 1)%len(self.audio_list)
            self.music = loader.loadSfx(self.audio_list[self.track_num])
            self.musicMgr.update()
            self.musicMgr.setVolume(0.5) 
            self.music.play()
        return task.cont
            
        
        
        


        
