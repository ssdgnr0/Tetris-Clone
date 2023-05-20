import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
import random
from panda3d.core import Point3
import math
import GameSettings as gms

class Tetri(DirectObject):
   
    next_piece = random.randint(0,6)
    field = []
    next_parts = [] #The parts of the next piece
    score = 0 
    level = 1
    level_limiter = 0
    count = 0
    game_over = False
    GM = None
    instance_count = 0
    instances_ = []
    game_paused = False
    base.cam.setPos(7,-60,16)
    dlight = DirectionalLight('my dlight')
    dlnp = render.attachNewNode(dlight)
    dlnp.setPos((gms.rows*2),33,(gms.columns*2))
    field_bg = loader.loadModel("field_Background.egg")
    field_bg.reparentTo(base.camera)
    field_bg.setBin('background', -1000)
    field_bg.setPos(7,( 39),20)
    field_bg.setScale(4)
    
    def __init__(self,field,GMM):
       
        Tetri.field = field
        
        
        self.models = [['HBartetrimino.egg',1],['Crowntetrimino.egg',2],['Cubetetrimino.egg',3],
                  ['RFLtetrimino.egg',4],['Ltetrimino.egg',5],['RPointertetrimino.egg',6],['LPointertetrimino.egg',7]]
        base.cam.setPos(7,-50,20)
        types = [[5,3,2,6],[1,5,6,7],[3,5,6,7],[1,2,5,6],[1,5,9,13],[2,5,6,7],[1,2,6,7]]
        self.current_piece = Tetri.next_piece 
        Tetri.next_piece  = random.randint(0,6)
        self.type_ = types[self.current_piece]
        self.ntype_ = types[Tetri.next_piece]
        
        self.rotations = types[0]
        self.center = self.type_[3]        
        self.rotation =  0
        Tetri.count = Tetri.count + 1
        if Tetri.GM == None: Tetri.GM = GMM
        Tetri.instance_count = Tetri.instance_count + 1   
        self.x = 6
        self.y = ((gms.rows*2) - 4)
        self.id = Tetri.instance_count      
        self.parts = []
        self.frozen = False
        self.descending = True
        self.instanceType = self.models[0][1]
        self.dt = 0       
        self.draw()
        self.draw_next_piece()
        Tetri.instances_.append(self)
        self.musicMgr = base.sfxManagerList[0]
        self.music =  loader.loadSfx('Sounds/effect1.ogg')
        self.music.setVolume(4)
        if(self.descending == True):
         self.accept("u", self.translate, extraArgs = [True,2])
         self.accept("s", self.translate, extraArgs = [True,-2])
         self.accept("d", self.translate, extraArgs = [False,2])
         self.accept("a", self.translate, extraArgs = [False,-2])
         self.accept("w", self.rotate, extraArgs = [])
         self.accept("escape",self.pause_or_savegame,extraArgs = [])
        taskMgr.add(self.lower_field, "lower_field")
        taskMgr.add(self.update, "Update")
      
    def draw(self):
        for i in self.type_:    
         part =  loader.loadModel(self.models[self.current_piece][0])# part = A single block of the tetris piece
         part.setLight(Tetri.dlnp)
         part.setPythonTag("owner",self)
         part.reparentTo(render)
         x = self.x + (((i%4)-1)*2)
         y = self.y - (((math.ceil(i/4))-1)*2)              
         tile = Tetri.field.field[str(int(x)) + str(int(y))]
         #t.taken = True
         part.setPos(tile.model.getX(),37,tile.model.getZ())       
         self.parts.append(part)
         
    def draw_next_piece(self):
        x = 0
        y = 0
        dummy_node = render.attachNewNode("Dummy Node Name")
        if(len(Tetri.next_parts) > 0):
            for nxtp in Tetri.next_parts:
                nxtp.removeNode()       
        for i in self.ntype_:    
         part =  loader.loadModel(self.models[Tetri.next_piece][0])
         part.setLight(Tetri.dlnp)
         part.setPythonTag("owner",self)
         part.reparentTo(dummy_node)         
         x = x + (((i%4)-1)*2)
         y = y - (((math.ceil(i/4))-1)*2)
         part.setPos(x,0,y)
         Tetri.next_parts.append(part)
         x = 0
         y = 0
        dummy_node.setScale(0.5)
        dummy_node.setPos(((gms.columns*2) + 3),37,(gms.rows))
       
    def can_translate(self,positions,vertical_axis,direction):
              
        if vertical_axis:
         for p in positions:
            new_position_key = str(int(p.getX())) + str(int(p.getZ() + direction))
            if(new_position_key in Tetri.field.field):
              tile = Tetri.field.field[str(int(p.getX())) + str(int(p.getZ() + direction))]
              if(tile.taken):
                self.descending = False
                return False
            if(new_position_key not in Tetri.field.field):
                if(direction < 2):
                 self.descending = False
                 return False
                if(direction >= 1):
                    return 
        if not vertical_axis:
          for p in positions:
            new_position_key = str(int(p.getX() + direction)) + str(int(p.getZ()))
            if(new_position_key in Tetri.field.field):
              tile = Tetri.field.field[str(int(p.getX() + direction)) + str(int(p.getZ()))]
              if(tile.taken):
                return False
            if(new_position_key not in Tetri.field.field):
                return False
            
        return True
    def can_rotate(self):
        
          center = self.parts[2]
          for i in self.parts:
           if(i != center):
              relative_x = i.getX() - center.getX()
              relative_z = i.getZ() - center.getZ()
              new_relative_x = (relative_x * 0) + (relative_z * - 1)
              new_relative_z = (relative_x * 1) + (relative_z * 0)                          
              rotated_x = new_relative_x + center.getX()
              rotated_z = new_relative_z + center.getZ()            
              position_key = str(int(rotated_x)) + str(int(rotated_z))
              if(position_key in Tetri.field.field):
                  tile = Tetri.field.field[str(int(rotated_x)) + str(int(rotated_z))]
                  if(tile.taken == True):
                      return False
                      print("Taken")                
              if(position_key not in Tetri.field.field):
                  return False                  
          return  True 
  
    def end(self):
        if Tetri.game_over:
            return
        self.descending = False
        self.ignore('a')
        self.ignore('d')
        self.ignore('w')
        self.ignore('s')
        self.ignore('l')
        self.ignore("escape")
        for p in self.parts:
            position_key = str(int(p.getX())) + str(int(p.getZ()))
            Tetri.field.rows["ROW_" + str(int(p.getZ()))].append(p)
            tile = Tetri.field.field[position_key]
            tile.taken = True
        self.clearLines()         
        for p in self.parts:
            if p.getZ() == ((gms.rows*2)-4):
                Tetri.game_over = True
                Tetri.GM.manage_state("playing")
                
                
        
    def descend(self):       
        self.dt += globalClock.getDt()
        if(self.dt > (1 - (Tetri.level*0.1))):             
           if(self.descending == True):
            if(self.can_translate(self.parts,True,-2)):
             for i in self.parts:
              i.setFluidZ(i,-2)
              self.music.play()  
              self.dt = 0     
        
    def rotate(self):
        center = self.parts[2]      
        if self.can_rotate():
         for p in self.parts:       
           if(p != center):
              relative_x = p.getX() - center.getX()
              relative_z = p.getZ() - center.getZ()
              new_relative_x = (relative_x * 0) + (relative_z * - 1)
              new_relative_z = (relative_x * 1) + (relative_z * 0)
              rotated_x = new_relative_x + center.getX()
              rotated_z = new_relative_z + center.getZ()              
              p.setPos(rotated_x ,37,rotated_z)
         self.rotation = (self.rotation + 1) % 4
       
    def translate(self,vertical_axis,direction):
        if vertical_axis:
            if self.can_translate(self.parts,True,direction):
              for p in self.parts:
                self.music.play()
                self.y = self.y + direction
                p.setFluidZ(p,direction)
        if not vertical_axis:
            if self.can_translate(self.parts,False,direction):
                for p in self.parts:
                 self.music.play()
                 self.x = self.x + direction
                 p.setFluidX(p,direction)
            
    def move_down(self,p):
        #moves the  given part/block down 
        if(int(p.getZ()) >= 0):              
            position_below_key = str(int(p.getX())) + str(int(p.getZ() -2))
            if(position_below_key in Tetri.field.field):
              tile = Tetri.field.field[str(int(p.getX())) + str(int(p.getZ() -2))]
              if(tile.taken):
                  pass             
              if(tile.taken == False):
                current_tile = Tetri.field.field[str(int(p.getX())) + str(int(p.getZ()))]
                current_tile.taken =  False                
                p.setFluidZ(p,-2)
                new_tile = Tetri.field.field[str(int(p.getX())) + str(int(p.getZ()))]
                new_tile.taken = True               
                Tetri.field.rows["ROW_" + str(int(p.getZ()))].append(p)
                return True               
        return False
        
    def clearLines(self):
        self.hl = 0
        lines = 0
        for i in range(0,((gms.rows*2)-2),2):
            if(len(Tetri.field.rows["ROW_" + str(i)]) >=  gms.columns):                
               for x in Tetri.field.rows["ROW_" + str(i)]:                  
                  owner = x.getPythonTag("owner")
                  owner.remove_part(x)
                  self.hl = self.hl + 1                 
               Tetri.field.rows["ROW_" + str(i)] = []
               lines += 1
        if(lines == 1):
            Tetri.score += 100
            Tetri.level_limiter += 100
        if(lines >= 2):
            Tetri.score = Tetri.score + (200 * lines)
            Tetri.level_limiter = Tetri.level_limiter + (200 * lines)
        return

    def lower_field(self,task):
        moved_downs = []
        
        for b in range(2,((gms.rows*2)-2),2):        
          if(len(Tetri.field.rows["ROW_" + str(b)]) >  0):
            if(len(Tetri.field.rows["ROW_" + str(b-2)]) <=  0):               
               for part in Tetri.field.rows["ROW_" + str(b)]:             
                 owner = part.getPythonTag("owner")               
                 moved_down = owner.move_down(part)
                 if(moved_down == True):
                    moved_downs.append(part)
               while len(Tetri.field.rows["ROW_" + str(b)]) > 0:
                  del Tetri.field.rows["ROW_" + str(b)][0]
               
        return task.cont
       
    def remove_part(self,part):
              
               if(part in self.parts):
                 new_position_key = str(int(part.getX())) + str(int(part.getZ()))
                 if(new_position_key in Tetri.field.field):                    
                   tile = Tetri.field.field[new_position_key]
                   tile.taken =  False
                   self.parts.remove(part)                   
                   part.removeNode()
                   
               return
    def pause_or_savegame(self):
        #Tetri.game_paused = True
        self.ignore('u')
        self.ignore('d')
        self.ignore('w')
        self.ignore('s')
        self.ignore('w')
        self.ignore("escape")
        Tetri.GM.manage_state("save_pause_screen")
    def resume_game(self):
        
         self.accept("u", self.translate, extraArgs = [True,2])
         self.accept("s", self.translate, extraArgs = [True,-2])
         self.accept("d", self.translate, extraArgs = [False,2])
         self.accept("a", self.translate, extraArgs = [False,-2])
         self.accept("w", self.rotate, extraArgs = [])
         self.accept("escape",self.pause_or_savegame,extraArgs = [])      
         taskMgr.add(self.update, "Update")
         Tetri.GM.manage_state("selection_screen")
    def destroy_game(self):
        taskMgr.remove("bd")
        Tetri.score = 0
        Tetri.level = 1
        #Tetri.level_limiter = 0
        for inst in Tetri.instances_:
           for p in inst.parts:            
              p.removeNode()
        self = None
        for nxtp in  Tetri.next_parts:
            nxtp.removeNode()
            nxtp = None
        Tetri.next_parts = []
        
   
    def update(self,task):
       
       if Tetri.GM.game_state == "save_pause_screen":          
           task.remove()
       if Tetri.game_over:
           task.remove()
           return
       if(self.descending == True):
           self.descend()
       if(self.descending == False):
           if(self.frozen == False):
            self.end()
            self.frozen = True
           if(len(self.parts) <= 0):
              Tetri.instances_.remove(self)
              self = None
              return task.done
       if Tetri.level_limiter >= 1000:
           Tetri.level += 1
           Tetri.level_limiter = Tetri.level_limiter - 1000
           
       for i in self.parts:
           if(i.getZ() < 0):
               for i in self.parts:
                   i.setZ(i,+2)
       if Tetri.game_over:
           self.destroy_game()
           Tetri.GM.manage_state("playing")
           self = None
           return
       return task.cont





