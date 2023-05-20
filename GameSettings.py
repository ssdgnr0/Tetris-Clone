import csv

def load_game_settings():
   vals = [] 
   with  open("game_settings.txt","r") as f:
       fr = csv.reader(f)
      
       for count ,line in enumerate(fr):
       
      
           if count <= 2:
            x = line[0].strip("['")
            vals.append(int(x))
           if count > 2:
             s = line[0].strip("'")
             vals.append(s)
           

   return vals

if load_game_settings() == None:
   default_values = [7,12,1,""]
   
else:
    default_values = load_game_settings()

columns = default_values[0]
rows = default_values[1]
level = default_values[2]
sound_path = default_values[3]

def save_game_settings(data):
    with open("game_settings.txt","w") as f:
       fw = csv.writer(f,lineterminator = '\n')
       fw.writerow([data[0]])
       fw.writerow([data[1]])
       fw.writerow([data[2]])
       fw.writerow([data[3]])
    return
