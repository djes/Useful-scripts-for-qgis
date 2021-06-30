# Load default style from database on selected layers
# Warning on duplicated layers with style saved in project...

from qgis.PyQt.QtXml import QDomDocument

selectedLayers = iface.layerTreeView().selectedLayersRecursive()
#selectedLayers = iface.layerTreeView().selectedLayers()

for layer in selectedLayers:
    print(layer.name())
    if isinstance(layer, QgsVectorLayer):
        listedStyles = layer.listStylesInDatabase()
        numberOfStyles = listedStyles[0]
        if numberOfStyles > 0:
            print('style trouvé')
            defaultStyleId = listedStyles[1][0]
            # defaultStyleName = listedStyles[2][0]
            # defaultStyleDate = listedStyles[3][0]
            styledoc = QDomDocument()
            styleTuple = layer.getStyleFromDatabase(defaultStyleId)
            styleqml = styleTuple[0]
            styledoc.setContent(styleqml)
            layer.importNamedStyle(styledoc)
            layer.triggerRepaint()
    #
    #layer.saveStyleToDatabase("NameOfStyle","Description",True,"uiFileContent")