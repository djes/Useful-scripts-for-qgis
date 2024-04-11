# Fast way to find a layer by its table name
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

def MapLayersByTableName(tablename):
    #selectedLayers = iface.layerTreeView().selectedLayersRecursive()
    #for layer in selectedLayers:
    for layer in QgsProject.instance().mapLayers().values():
        if isinstance(layer, QgsVectorLayer):
            try: 
                l = LayerDbInfo(layer.source())
                t = l.getTable()
                if t == tablename:
                    return layer
            except: 
                pass
    return null

print(MapLayersByTableName('cs_720_pol_inconnu'))