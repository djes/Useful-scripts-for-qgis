def create_relation(referencing_layer_name, referencing_layer_key, referenced_layer_name, referenced_layer_key, relation_id, relation_name):
    layer1 = QgsProject.instance().mapLayersByName(referencing_layer_name)[0]
    layer2 = QgsProject.instance().mapLayersByName(referenced_layer_name)[0]
    if layer1 and layer2:
        rel = QgsRelation()
        rel.setReferencingLayer( layer1.id() )
        rel.setReferencedLayer( layer2.id() )
        rel.addFieldPair( referencing_layer_key, referenced_layer_key )
        rel.setId( relation_id )
        rel.setName( relation_name )
        # rel.isValid() # It will only be added if it is valid. If not, check the ids and field names
        QgsProject.instance().relationManager().addRelation( rel )
        return rel
    else:
        return
