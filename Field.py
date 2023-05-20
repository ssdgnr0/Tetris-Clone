from direct.directbase import DirectStart
from direct.showbase.DirectObject import DirectObject
from panda3d.core import*
import GameSettings as gms
import pprint

class Tile(DirectObject):
    instance_count = 0 
    def __init__(self,name,pos,field,row):
        Tile.instance_count = Tile.instance_count  + 1
        self.id = Tile.instance_count
        self.name = name
        self.model = loader.loadModel("Tile.egg")
        self.model.setPos(pos)
        self.occupied =  False
        self.taken = False
        self.row = row
        self.model.reparentTo(render)

class Field(DirectObject):
  
    def __init__(self,cols,rows):

        row_index = 0
        self.numOfCols = gms.columns
        self.numOfRows = gms.rows
        self.rows = {}
        self.field = {}
        self.startXPos = 0
        self.startZPos = 0     
        #Construct the field
        for r in range(self.numOfRows):
            rowitems = []
            for c in range(self.numOfCols):
                tile = Tile(str(self.startXPos) + str(self.startZPos) ,(self.startXPos,38,self.startZPos),self,"ROW_" + str(r))           
                self.field.setdefault(str(int(self.startXPos)) + str(int(self.startZPos)),tile)
                rowitems.append(tile)
                self.startXPos += (2.0)
            self.rows.setdefault("ROW_" + str(row_index),[])
            self.rowitems = []
            self.startXPos = 0
            self.startZPos += (2)
            row_index = row_index + 2
      
       

   
