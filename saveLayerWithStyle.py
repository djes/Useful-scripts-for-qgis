layer_name = 'test3' #change me
gpkg_name = 'c:\\temp\\mytest.gpkg' #output, change me if needed

#- First, saves the layer
src_layer = QgsProject.instance().mapLayersByName(layer_name)[0]
options = QgsVectorFileWriter.SaveVectorOptions()
options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
options.layerName = layer_name
#options.SymbologyExport = QgsVectorFileWriter.FeatureSymbology
#options.driverName = "GPKG"
error = QgsVectorFileWriter.writeAsVectorFormatV2(src_layer, gpkg_name, QgsProject.instance().transformContext(), options)

if error[0] == QgsVectorFileWriter.ErrCreateDataSource:
    print("Create mode")
    options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile #Create mode
    error = QgsVectorFileWriter.writeAsVectorFormatV2(src_layer, gpkg_name, QgsProject.instance().transformContext(), options)
del options
if error[0] == QgsVectorFileWriter.NoError:
    print('Layer "' + layer_name + '" saved in "' + gpkg_name + '"')        
else:
    print(error)
    raise Exception('Failed to save layer')

#- Second, saves the style
#- Load just saved layer
dst_layer = QgsVectorLayer(f'{gpkg_name}|layername={layer_name}', layer_name, 'ogr')
if not dst_layer.isValid():
    raise Exception('Failed to load layer')
#print(dst_layer)

myDocument = QDomDocument('qgis')
src_layer.exportNamedStyle(myDocument)
#print(myDocument.toString())
success, message = dst_layer.importNamedStyle(myDocument)
dst_layer.saveStyleToDatabase(layer_name, '', True, '')
QgsProject.instance().removeMapLayer(dst_layer)
del src_layer
del dst_layer
del myDocument