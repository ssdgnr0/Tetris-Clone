import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from panda3d.core import *
from GUIManager import *
from Tetri import *
from Field import *
from MediaPlayer import*
import GameSettings as gms
import csv
import pprint


class GameManager(DirectObject):
      gamestates = ("splash_screen","selection_screen","playing",
                    "paused","game_over","save_pause_screen","settings_screen")
         
      def __init__(self):

          base.cam.setPos(7,-60,16)
          self.gui_m = GUIManager(self)
          self.game_over = False
          self.game_state = GameManager.gamestates[0]
          self.prev_state = "None"
          self.initial_game = True
          self.media_p = Media_Player(4)
          taskMgr.add(self.update,"Update")
          
      def manage_state(self,state):
          if state == "splash_screen":
              self.game_state =  GameManager.gamestates[1]
          if state == "selection_screen":
              self.game_state =  GameManager.gamestates[2]
          if state == "playing":
              self.game_state =  GameManager.gamestates[4]
          if state == "save_pause_screen":
              self.game_state =  GameManager.gamestates[5]
          if state == "settings_screen":
              self.game_state =  GameManager.gamestates[6]
           
          return   
      def start_new_game(self):
            
         if not self.initial_game: 
           Tetri.game_over = False
           Tetri.next_parts = []
           Tetri.score = 0 
           Tetri.level = 1
           Tetri.count = 0
           Tetri.instances_ = []
           
         self.dt = 0           
         self.field = Field(gms.rows,gms.columns)         
         self.tetri = Tetri(self.field,self)
         self.gui_m.setup_HUD(Tetri.score,Tetri.level)
         self.initial_game = False
      def save_game(self):
         
          gmSGD = [self.game_over, self.game_state, self.prev_state, self.initial_game]
          Tetri_SGD = [Tetri.score,  Tetri.level,  Tetri.count,
                        Tetri.game_over, len(Tetri.instances_)]
          Tetri_p_SGD = {}
          count = 0
          key = "instance"
          pdata = 0
          parts_x_cord = []
          parts_z_cord = []
          for tti in  Tetri.instances_:
                 parts_x_cord = [p.getX() for p in tti.parts]
                 parts_z_cord  = [p.getZ() for p in tti.parts]
                 pdata = [tti.current_piece, tti.type_  , tti.ntype_  ,
                          tti.rotations  ,tti.center  ,tti.rotation,
                          tti.x  ,tti.y  ,tti.id  ,parts_x_cord ,parts_z_cord, 
                          tti.frozen  ,tti.descending  ,tti.instanceType]
                 Tetri_p_SGD.setdefault(key + str(count),pdata)
                 pdata = []
                 parts_x_cord  = []
                 parts_z_cord  = []
                 count = count + 1
                 
          pprint.pprint(Tetri_p_SGD)
                 
          with  open("save_game_file.txt","w") as file:
              fileWriter = csv.writer(file, lineterminator = '\n')
              fileWriter.writerow(gmSGD)      
              fileWriter.writerow(Tetri_SGD)
              for key in  Tetri_p_SGD:
                  c = Tetri_p_SGD[key]
                  fileWriter.writerow(Tetri_p_SGD[key])
                
         
      def resume_game(self):
            if self.game_state == GameManager.gamestates[5]:
             self.tetri.resume_game()
      def parseboolean(self,val):
            if val == "False":
                  return False
            if val == "True":
                  return True                
      def load_game(self):
          with open("save_game_file.txt","r") as file:
            file_reader = csv.reader(file)            
            def parse_string_arr(strval):
               if strval == "[]":                   
                     return []
               
               vals = strval.strip("[]")
               vals = vals.split(",")
               arr = [int(float(item.strip("'"))) for item in vals]
               
               return arr
            
            for count , line in enumerate(file_reader):
                 
                  if count == 0:
                    self.game_over =  self.parseboolean(line[0])
                    self.game_state = line[1]
                    self.prev_state = line[2]
                    self.initial_game = self.parseboolean(line[3])
                    base.camera.setPos(7,-30,8)
                    self.dt = 0 

                  if count == 1:
                        Tetri.score = int(float(line[0].strip("'")))
                        Tetri.level = int(float(line[1].strip("'")))
                        Tetri.count = int(float(line[2].strip("'")))                        
                        Tetri.game_over = self.parseboolean(line[3])
                        self.dt = 0           
                        self.field = Field(7,8)
      
                  if count >= 2:
                        
                        self.tetri = Tetri(self.field,self)
                        self.tetri.current_piece = int(float(line[0].strip("'")))
                        self.tetri.type_ = parse_string_arr(line[1])                                
                        self.tetri.ntype_ = parse_string_arr(line[2])
                        self.tetri.rotations = parse_string_arr(line[3])
                        self.tetri.center = int(float(line[4].strip("'")))
                        self.tetri.rotation = int(float(line[5].strip("'")))
                        self.tetri.x = int(float(line[6].strip("'")))
                        self.tetri.y = int(float(line[7].strip("'")))
                        self.tetri.id = int(float(line[8].strip("'")))
                        self.tetri.frozen = self.parseboolean(line[11])
                        self.tetri.descending = self.parseboolean(line[12])
                        self.tetri.instanceType = int(float(line[13].strip("'")))
                        parts_x_cord  = parse_string_arr(line[9])
                        parts_z_cord  = parse_string_arr(line[10])               
                        hl = []
                        for count2 , p in enumerate(parts_x_cord):
                              x = parts_x_cord[count2]
                              z = parts_z_cord[count2]                             
                              for p in range(len(self.tetri.parts)):
                                    self.tetri.parts[count2].setPos(x,37,z)
                                  
                              list_difference = len(self.tetri.parts) - len(parts_x_cord)
                              for dif in range(list_difference):
                                    self.tetri.parts[-1].removeNode()
                                    del self.tetri.parts[-1]
                              for p in range(len(self.tetri.parts)):                                  
                                  self.tetri.parts[count2].setPos(x,37,z)
                                  hl.append(self.tetri.parts[count2])
                                                   
                        if self.tetri.descending == False:                             
                                self.tetri.end()
          self.gui_m.remove_selection_screen()
          self.gui_m.setup_HUD(Tetri.score,Tetri.level)
          self.game_state =  GameManager.gamestates[2]
          self.dt = -6
          return
      def save_game_settings(self,save_data):
            gms.save_game_settings(save_data)
            self.gui_m.remove_settings_screen()
      def update(self, task):
        #print(self.game_state)
        if self.game_state == "splash_screen":          
            if self.prev_state != self.game_state:
              self.gui_m.setup_splash_screen()
         
        if self.game_state == GameManager.gamestates[1]:
            if self.prev_state != self.game_state:
               self.gui_m.setup_selection_screen()
                           
        if self.game_state == GameManager.gamestates[2]:
            self.gui_m.update_HUD(Tetri.score,Tetri.level)
            if self.prev_state != self.game_state:
               pass
            self.dt += globalClock.getDt()
            if(self.tetri.descending == False):
              if(self.dt > 0.5):
                 self.tetri = Tetri(self.field,self)
                 self.dt = 0
            
        if self.game_state == GameManager.gamestates[4]:
            if self.prev_state != self.game_state:
               self.gui_m.setup_game_over_screen()
               self.tetri = None
               self.field =  None
                           
        if self.game_state == GameManager.gamestates[5]:
            if self.prev_state != self.game_state:
                  self.gui_m.setup_save_pause_screen()
                        
        self.prev_state =  self.game_state 
        return task.cont
          
          
Game = GameManager()
base.run()
