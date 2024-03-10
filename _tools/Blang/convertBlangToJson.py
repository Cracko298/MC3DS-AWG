import os
from mc3dsblang import *

id = ".\\in"
od = ".\\out"

os.makedirs(id,exist_ok=True)
os.makedirs(od,exist_ok=True)

for filename in os.listdir(id):
    if filename.endswith(".blang"):
        print(filename)
        blangFile = BlangFile().open(f"{id}\\{filename}")
        blangFile.toJson(od)

if os.name == 'nt':
    os.system('pause')