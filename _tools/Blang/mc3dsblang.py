import os
import json
from pathlib import Path

class MC3DSBlangException(Exception):
    def __init__(self, message):
        super().__init__(message)

class BlangFile:
    def __init__(self):
        return
    
    def open(self, path: str = None):
        if path == None:
            raise MC3DSBlangException("path is empty")
        if type(path) != str:
            raise MC3DSBlangException("path must be a 'str'")

        self.filename = Path(path).stem

        with open(path, "rb") as f:
            file_content = list(f.read())

        # Obtener longitud
        long = []
        for i in range(0, 4):
            long.append(file_content[i])
        long = int.from_bytes(bytearray(long), "little")

        # Obtener los elementos del indice
        idx = 4
        data = []
        for i in range(0, long):
            join = []
            for j in range(0, 4):
                join.append(file_content[idx])
                idx += 1
            data.append(join)
            idx += 4

        # Longitud de los textos
        textlong = []
        for i in range(idx, idx + 4):
            textlong.append(file_content[i])
        textlong = int.from_bytes(bytearray(textlong), "little")

        # Obtener los textos
        idx += 4
        texts = []
        for i in range(0, long):
            join = []
            while file_content[idx] != 0:
                join.append(file_content[idx])
                idx += 1
            texts.append(bytearray(join).decode("utf-8"))
            idx += 1

        self.data = data
        self.texts = texts
        return self
    
    def getData(self):
        return self.data

    def getTexts(self):
        return self.texts

    def replace(self, text: str, newtext: str):
        if type(text) != str:
            raise MC3DSBlangException("text must be a 'str'")
        if type(newtext) != str:
            raise MC3DSBlangException("newtext must be a 'str'")

        if text in self.texts:
            if newtext != "" and newtext != '':
                self.texts[self.texts.index(text)] = newtext
            else:
                self.texts[self.texts.index(text)] = " "
        return
    
    def export(self, path: str):
        if type(path) != str:
            raise MC3DSBlangException("path must be a 'str'")

        long = len(self.data)
        indexLong = list(long.to_bytes(4, "little"))

        indexData = []
        textData = []
        for i in range(0, long):
            # Copiar los primeros datos del elemento
            indexData.extend(self.data[i])

            # Posición de texto
            indexData.extend(list(len(textData).to_bytes(4, "little")))
            
            # Agregar texto
            textData.extend(list(self.texts[i].encode("utf-8")))

            # Separador/terminador
            textData.append(0)

        textsLong = list(len(textData).to_bytes(4, "little"))

        # Junta todo en una sola lista
        self.exportData = []
        self.exportData.extend(indexLong)
        self.exportData.extend(indexData)
        self.exportData.extend(textsLong)
        self.exportData.extend(textData)

        self.exportData = bytearray(self.exportData)

        with open(os.path.join(path, f"{self.filename}.blang"), "wb") as f:
            f.write(self.exportData)
        return

    def toJson(self, path: str):
        long = len(self.data)
        dataDictionary = {}
        for i in range(0, long):
            item = self.data[i]
            identifier = []
            for j in range(0, 4):
                identifier.append(item[j])
            identifier = bytearray(identifier)
            identifier = int.from_bytes(identifier, "little")
            identifier = str(identifier)
            
            dataDictionary[identifier] = {}
            dataDictionary[identifier]["order"] = i + 1
            dataDictionary[identifier]["text"] = self.texts[i]
        
        outFile = open(os.path.join(path, f"{self.filename}.json"), "w", encoding="utf-8")
        json.dump(dataDictionary, outFile, indent=4, ensure_ascii=False)
        outFile.close()
        return
    
    def fromJson(self, path: str):
        if type(path) != str:
            raise MC3DSBlangException("path must be a 'str'")

        data = []
        texts = []

        with open(path, "r", encoding="utf-8") as jsonData:
            dataDictionary = json.load(jsonData)

        self.filename = Path(path).stem

        idx = 1
        while idx <= len(dataDictionary):
            for key in dataDictionary:
                if dataDictionary[key]["order"] == idx:
                    data.append(list(int(key).to_bytes(4, "little")))
                    texts.append(dataDictionary[key]["text"])
                    idx += 1
                    break

        self.data = data
        self.texts = texts
        return self