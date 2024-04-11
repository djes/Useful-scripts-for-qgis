# Rename selected vector layers based on their table name in db
# Jésahel Benoist, apr 11, 2024

import re

class LayerDbInfo:
    # Thanks to spencerrecneps on https://gis.stackexchange.com/a/156799/144543
    def __init__(self, layerInfo):
        if layerInfo[:6] == 'dbname':
            layerInfo = layerInfo.replace('\'','"')
            vals = dict(re.findall('(\S+)="?(.*?)"? ', layerInfo))
            # self.dbName = str(vals['dbname'])
            # self.key = str(vals['key'])
            # self.user = str(vals['user'])
            # self.password = str(vals['password'])
            # self.srid = int(vals['srid'])
            # self.type = str(vals['type'])
            # self.host = str(vals['host'])
            # self.port = int(vals['port'])

            # need some extra processing to get table name and schema
            try:
                table = vals['table'].split('.')
                self.schemaName = table[0].strip('"')
                self.tableName = table[1].strip('"')
            except:
                raise 
        else:
            raise

    # def getDBName(self):
    #     return self.dbName

    # def getHost(self):
    #     return self.host

    # def getPort(self):
    #     return self.port

    # def getKey(self):
    #     return self.key

    # def getUser(self):
    #     return self.user

    # def getPassword(self):
    #     return self.password

    # def getSRID(self):
    #     return self.srid

    # def getType(self):
    #     return self.type

    def getSchema(self):
        return self.schemaName

    def getTable(self):
        return self.tableName

def CreateLayersDict():
    #selectedLayers = iface.layerTreeView().selectedLayersRecursive()
    #for layer in selectedLayers:
    for layer in QgsProject.instance().mapLayers().values():
        if isinstance(layer, QgsVectorLayer):
            try: 
                l = LayerDbInfo(layer.source())
                t = l.getTable()
                LayersDict[layer.id()] = t
            except: 
                pass
    return 0

# Creates a dictionary for faster access
# dict{] = layer_id : "tablename"

LayersDict = {}
CreateLayersDict()
#print(LayersDict)

selectedLayers = iface.layerTreeView().selectedLayersRecursive() 
for layer in selectedLayers:
    if isinstance(layer, QgsVectorLayer) and layer.id() in LayersDict:
        tableName = LayersDict[layer.id()]
        layer.setName(tableName)
        layer.triggerRepaint()
    