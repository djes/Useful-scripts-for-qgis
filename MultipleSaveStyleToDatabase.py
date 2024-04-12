# Save default style to database

from qgis.PyQt.QtXml import QDomDocument

selectedLayers = iface.layerTreeView().selectedLayersRecursive()
for layer in selectedLayers:
    if isinstance(layer, QgsVectorLayer):       
        #print(myDocument.toString())
        layer.saveStyleToDatabase(layer.name(), '', True, '')        
        print(layer.name())
    layer.triggerRepaint()
    