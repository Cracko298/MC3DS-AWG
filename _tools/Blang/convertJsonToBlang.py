import os
from mc3dsblang import *

id = ".\\in"
od = ".\\out"

os.makedirs(id,exist_ok=True)
os.makedirs(od,exist_ok=True)

for filename in os.listdir(id):
    if filename.endswith(".json"):
        print(filename)
        inputFile = os.path.join(id, filename)
        blangFile = BlangFile().fromJson(inputFile)
        blangFile.export(od)

if os.name == "nt":
    os.system("pause")
