import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from panda3d.core import *
import GameSettings as gms 

class GUIManager(DirectObject):
    
    def __init__(self,GM):
        
        self.GM = GM       
       
    def setup_splash_screen(self):
           
          self.splash_screen = loader.loadModel("splash_screen.egg")
          self.splash_screen.reparentTo(aspect2d)
          self.splash_screen.setScale(2.7)
          self.textObject = OnscreenText(text = 'Well Come To Probably The\n    Most Played Game', pos = (-0.5, 0.02), scale = 0.1,fg = (1,1,1,1))
          self.textObject2 = OnscreenText(text = 'Please Press Enter', pos = (-0.5, -0.5,0.8), scale = 0.1,fg = (1,1,1,1))
          self.accept("enter",self.splash_screen_handler)
          return
    def setup_HUD(self,score,level):
          
          self.HUD = TextNode('HUD')
          cmr12 = loader.loadFont('cmr12.egg')        
          self.HUD.setText("Score " + str(score) + "\nlevel " + str(level))
          self.HUD.setFont(cmr12)
          self.HUDNodePath = render.attachNewNode(self.HUD)
          self.HUDNodePath.setPos(((gms.columns*2) + 3),37,((gms.rows*2) - 4))
          self.HUDNodePath.setScale(3.00)
          self.HUD.setTextColor(0.5, 0.5, 0.5, 1)
          self.HUD.setFrameColor(1, 1, 1, 1)
          self.HUD.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)
          self.HUD.setCardColor(1, 1, 1, 1)
          self.HUD.setCardAsMargin(0, 0, 0, 0)
          self.HUD.setCardDecal(True)
          return
    
    def update_HUD(self,score,level):
        
        self.HUD.setText("Score " + str(score) + "\nlevel " + str(level))
        return
    def remove_HUD(self):
        self.HUD = None
        self.HUDNodePath.removeNode()
        return
    def splash_screen_handler(self):
        self.textObject.destroy()
        self.textObject2.destroy()
        self.splash_screen.removeNode()     
        self.GM.manage_state("splash_screen")
        self.ignore("enter")
        return
         
    def setup_selection_screen(self):

        self.selection_screen = loader.loadModel("selection_screen.egg")
        self.selection_screen.reparentTo(aspect2d)
        self.selection_screen.setPos(0,2,0)
        self.new_game_button = DirectButton(scale = 0.08,text = ("New Game"),command = self.execute_new_game,pos = (0,0,0.5))
        self.settings_button = DirectButton(scale = 0.08,text = ("Settings"),command = self.setup_settings_screen,pos = (0,0,0.2))
        self.load_game_button = DirectButton(scale = 0.08,text = ("Load Game"),command = self.load_game,pos = (0,0,-0.1),pressEffect = 0.9)
        return

    def remove_selection_screen(self):
        self.new_game_button.destroy()
        self.settings_button.destroy()
        self.load_game_button.destroy()
        self.selection_screen.removeNode()
        return
        
    def execute_new_game(self):
        self.remove_selection_screen()
        self.GM.start_new_game()
        self.GM.manage_state("selection_screen")
    def replay(self):
        self.remove_game_over_screen()
        self.GM.start_new_game()
        self.GM.manage_state("selection_screen")
    def setup_game_over_screen(self):
        
        self.game_over_model = loader.loadModel("GameOver.egg")
        self.game_over_model.reparentTo(aspect2d)
        self.new_game_button = DirectButton(scale = 0.08,text = ("New Game"),command = self.replay,pos = (-0.3,0,-0.4),pressEffect = 0.9)
        self.exit_game_button = DirectButton(scale = 0.08,text = ("Exit"),command = self.exit,pos = (0.3,0,-0.4),pressEffect = 0.9) 
        self.game_over_model.setScale(0.27)
        self.remove_HUD()
        
    def remove_game_over_screen(self):
         self.game_over_model.removeNode()
         self.new_game_button.destroy()
         self.exit_game_button.destroy()
    def exit(self):
        exit()
    def setup_save_pause_screen(self):
        self.spcframe = DirectFrame(frameSize = (1,-1,1,-1),frameColor = (0.2,0,0.6,0.4),pos = (0,0,0))
        self.save_game_button = DirectButton(scale = 0.08,text = ("Save Game"),command = self.save_game,pos = (-0.3,0,-0.4),pressEffect = 0.9)
        self.resume_game_button = DirectButton(scale = 0.08,text = ("Resume Game"),command = self.resume_game,pos = (0.0,0,-0.1),pressEffect = 0.9)
        self.exit_game_button = DirectButton(scale = 0.08,text = ("Exit"),command = self.exit,pos = (0.3,0,-0.4),pressEffect = 0.9)
        self.accept("escape", self.resume_game, extraArgs = [])
        self.labelGP = DirectLabel(text = "Game Paused",pos = (0,0,0.4),scale = 0.2,text_fg=(0.9,0.9,0.8,1),relief = None)
    def resume_game(self):
        self.spcframe.destroy()
        self.save_game_button.destroy()
        self.resume_game_button.destroy()
        self.exit_game_button.destroy()
        self.labelGP.destroy()
        self.ignore("escape")
        self.GM.resume_game()
        
    def save_game(self):
        self.GM.save_game()
    def load_game(self):
        self.GM.load_game()
    
    def setup_settings_screen(self):

        self.remove_selection_screen()
        self.GM.manage_state("settings_screen")
        self.settings_frame = DirectFrame(frameSize = (1.33,-1.33,1,-1),frameColor = (0.2,0,0.6,1),pos = (0,0,0))
        self.col_label = DirectLabel(text = "Number of cloums",pos = (0,0,0.7),scale = 0.08,text_fg=(0.9,0.9,0.8,1),relief = None)        
        self.colEntry = DirectEntry(text = "" ,scale=.05,initialText="", numLines = 2,focus=1, pos = (-0.26,0,0.6))
        self.row_label = DirectLabel(text = "Number of rows",pos = (0,0,0.4),scale = 0.08,text_fg=(0.9,0.9,0.8,1),relief = None)        
        self.rowEntry = DirectEntry(text = "" ,scale=.05,initialText="", numLines = 2,focus=1, pos = (-0.26,0,0.3), focusInExtraArgs = [])
        self.level_label = DirectLabel(text = "Set level",pos = (-0.1,0,0.1),scale = 0.08,text_fg=(0.9,0.9,0.8,1),relief = None)        
        self.levelEntry = DirectEntry(text = "" ,scale=.05,initialText="", numLines = 2,focus=1, pos = (-0.26,0,0.0))
        self.save_sttngs_error_msg =  TextNode('node name')
        self.save_sttngs_error_msg_NodePath = self.settings_frame.attachNewNode(self.save_sttngs_error_msg)
        self.save_sttngs_error_msg_NodePath.setScale(0.09)
        self.save_sttngs_error_msg_NodePath.setPos(-0.56,0,-0.45)
        self.save_sttngs_error_msg.setTextColor(1,1,1,1)
        self.save_settings_button = DirectButton(scale = 0.08,text = ("Save Settings"),command = self.save_game_settings,pos = (0.0,0,-0.7),pressEffect = 0.9)
    def isNumber(self,str_sample):
        nums = ["1","2","3","4","5","6","7","8","9","0"]
        
        for char in str_sample:
            print(char)
            if char not in nums:
                print("AV")
                return False
        if str_sample == '':
            return False
         
        return True
            
    def save_game_settings(self):
        all_clear = True
        cols = self.colEntry.get()
        rows = self.rowEntry.get()
        level = self.levelEntry.get()
        if self.isNumber(cols):
           cols = int(cols)
        else:
            all_clear = False
        if self.isNumber(rows):
           rows = int(rows)
        else:
            all_clear = False
        if self.isNumber(level):
            level = int(level)
        else:
            all_clear = False
        if all_clear:
            self.GM.save_game_settings([cols,str(rows),level,"i"])
        if all_clear == False:          
           self.save_sttngs_error_msg.setText("Please try again you have \n entered some invalid data")      
        return
    def remove_settings_screen(self):
         self.settings_frame.destroy()
         self.col_label.destroy()
         self.colEntry.destroy()
         self.row_label.destroy()
         self.rowEntry.destroy()
         self.level_label.destroy()
         self.levelEntry.destroy()
         self.save_settings_button.destroy()
         self.save_sttngs_error_msg.setText("")
         self.GM.manage_state("splash_screen")

         return
  
