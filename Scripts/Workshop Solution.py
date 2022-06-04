# header (automatically executed by Python console)
# from qgis.core import *
# import qgis.utils

# TASK 1. Adding GeoPackage as Layers into QGIS

# 1.1. change project coordinate system to EPSG:4326 and back to EPGS:31467
QgsProject.instance().setCrs(QgsCoordinateReferenceSystem(4326))
QgsProject.instance().setCrs(QgsCoordinateReferenceSystem(31467))

# 1.2 ask for user input (path to umgebung.gpkg)
envPath = QFileDialog.getOpenFileName(QFileDialog(), 'Environment Layer Select', 'setDefaultPath')[0]
print('Environment file path: ' + envPath)

# 1.3. add the layer with name 'My Layer' and then rename it to `umgebung_neu`
envLayer = iface.addVectorLayer(envPath, 'My Layer', 'ogr')
envLayer.setName('Environment')

# 1.3. add the autobahn layer
abPath = QFileDialog.getOpenFileName(QFileDialog(), 'Autobahn Layer Select', 'setDefaultPath')[0]
print('Autobahn file path: ' + abPath)
abLayer = iface.addVectorLayer(abPath, 'Autobahn', 'ogr')

# TASK 2: Adding Buffers to Autobahn Layer

# 2.3. (optional) clean up: remove all layers that have name 'buffer' in them
lyrCount = 0
for lyr in QgsProject.instance().mapLayers().values():
    if 'buffer' in lyr.name().lower():
        QgsProject.instance().removeMapLayers([lyr.id()])
        lyrCount += 1

print(str(lyrCount) + ' buffer layers removed')

# 2.3. create 20m buffer
inpLayer = QgsProject.instance().mapLayersByName('Autobahn')[0]
inpParam = { 'DISSOLVE' : False, 'DISTANCE' : 20, 'END_CAP_STYLE' : 0, 'INPUT' : inpLayer, 'JOIN_STYLE' : 0, 'MITER_LIMIT' : 2, 'OUTPUT' : 'TEMPORARY_OUTPUT', 'SEGMENTS' : 5 }
outAlgo = processing.run('qgis:buffer', inpParam)
outLayer = QgsProject.instance().addMapLayer(outAlgo['OUTPUT'])
outLayer.setName('Autobahn 20')

# 2.4. create 100m buffer
inpParam = { 'DISSOLVE' : False, 'DISTANCE' : 100, 'END_CAP_STYLE' : 0, 'INPUT' : inpLayer, 'JOIN_STYLE' : 0, 'MITER_LIMIT' : 2, 'OUTPUT' : 'TEMPORARY_OUTPUT', 'SEGMENTS' : 5 }
outAlgo = processing.run('qgis:buffer', inpParam)
outLayer = QgsProject.instance().addMapLayer(outAlgo['OUTPUT'])
outLayer.setName('Autobahn 100')

# 2.4. create 300m buffer
inpParam = { 'DISSOLVE' : False, 'DISTANCE' : 300, 'END_CAP_STYLE' : 0, 'INPUT' : inpLayer, 'JOIN_STYLE' : 0, 'MITER_LIMIT' : 2, 'OUTPUT' : 'TEMPORARY_OUTPUT', 'SEGMENTS' : 5 }
outAlgo = processing.run('qgis:buffer', inpParam)
outLayer = QgsProject.instance().addMapLayer(outAlgo['OUTPUT'])
outLayer.setName('Autobahn 300')

# (optional) 2.4 write reusable buffer function
def buffer_layer(inpLayerName, bufDist, outLayerName):
    # set input layer and parameters
    inpLayer = QgsProject.instance().mapLayersByName(inpLayerName)[0]
    inpParam = { 'DISSOLVE' : False, 'DISTANCE' : bufDist, 'END_CAP_STYLE' : 0, 'INPUT' : inpLayer, 'JOIN_STYLE' : 0, 'MITER_LIMIT' : 2, 'OUTPUT' : 'TEMPORARY_OUTPUT', 'SEGMENTS' : 5 }
    # run algorithm and get output layer reference
    outAlgo = processing.run("qgis:buffer", inpParam)
    outLayer = QgsProject.instance().addMapLayer(outAlgo['OUTPUT'])
    # rename output layer
    outLayer.setName(outLayerName)

# try out the function but remove the layer afterwards
buffer_layer('Autobahn', 500, 'Autobahn 500')
lyr = QgsProject.instance().mapLayersByName('Autobahn 500')[0]
QgsProject.instance().removeMapLayers([lyr.id()])

# TASK 3. Performing Union on the Buffer Areas

# 3.1. union-ing the inner impact zone
inpLayer1 = QgsProject.instance().mapLayersByName('Autobahn 20')[0]
inpLayer2 = QgsProject.instance().mapLayersByName('Autobahn 100')[0]
inpParam = { 'INPUT' : inpLayer1, 'OUTPUT' : 'TEMPORARY_OUTPUT', 'OVERLAY' : inpLayer2, 'OVERLAY_FIELDS_PREFIX' : '' }
outAlgo = processing.run("qgis:union", inpParam)
outLayer = QgsProject.instance().addMapLayer(outAlgo['OUTPUT'])
outLayer.setName('Inner Impact Area')

# (optional) 3.1. union function
def union_layers(inpLayerName1, inpLayerName2, outLayerName):
    inpLayer1 = QgsProject.instance().mapLayersByName(inpLayerName1)[0]
    inpLayer2 = QgsProject.instance().mapLayersByName(inpLayerName2)[0]
    inpParam = { 'INPUT' : inpLayer1, 'OUTPUT' : 'TEMPORARY_OUTPUT', 'OVERLAY' : inpLayer2, 'OVERLAY_FIELDS_PREFIX' : '' }
    outAlgo = processing.run("qgis:union", inpParam)
    outLayer = QgsProject.instance().addMapLayer(outAlgo['OUTPUT'])
    outLayer.setName(outLayerName)
    
# example usage for Inner Impact Area
# union_layers 'Autobahn 20', 'Autobahn 100', 'Inner Impact Area')

# 3.2. union-ing the overall impact area
inpLayer1 = QgsProject.instance().mapLayersByName('Inner Impact Area')[0]
inpLayer2 = QgsProject.instance().mapLayersByName('Autobahn 300')[0]
inpParam = { 'INPUT' : inpLayer1, 'OUTPUT' : 'TEMPORARY_OUTPUT', 'OVERLAY' : inpLayer2, 'OVERLAY_FIELDS_PREFIX' : '' }
outAlgo = processing.run("qgis:union", inpParam)
outLayer = QgsProject.instance().addMapLayer(outAlgo['OUTPUT'])
outLayer.setName('Impact Area')

# (optional) in case my_union is used
# my_union('Inner Impact Area', 'Autobahn 300', 'Impact Area')

# 3.2. check non-overlapping part of original 100m buffer
outLayer = QgsProject.instance().mapLayersByName('Impact Area')[0]
outLayer.setSubsetString('fid_1 IS NULL AND fid_2 IS NULL') # apply filter
outLayer.setSubsetString('') # remove filter

# 3.3. modifying the attribute table
# adding 3 fields
unionLayer = QgsProject.instance().mapLayersByName('Impact Area')[0]
layerProvider = unionLayer.dataProvider()
layerProvider.addAttributes([QgsField('fid_union', QVariant.Int)])
layerProvider.addAttributes([QgsField('zone', QVariant.String)])
layerProvider.addAttributes([QgsField('zone_area', QVariant.Double)])
unionLayer.updateFields()
# updating the 3 fields
unionFeatures = unionLayer.getFeatures()
unionLayer.startEditing()
for f in unionFeatures:
    # calculate feature zone type
    indFID = unionLayer.fields().indexFromName('fid')
    valFID = f.attributes()[indFID]
    indFID2 = unionLayer.fields().indexFromName('fid_2')
    valFID2 = f.attributes()[indFID2]
    if valFID is None and valFID2 is None:
        valZone = 'Outside'
    elif valFID is None:
        valZone = 'Inside'
    else: 
        valZone = 'Route'
    # calculate feature area
    valArea = f.geometry().area()
    # store attribute values   
    featID = f.id()
    indFIDUnion = unionLayer.fields().indexFromName('fid_union')
    indZone = unionLayer.fields().indexFromName('zone')
    indArea = unionLayer.fields().indexFromName('zone_area')
    valDict = {indFIDUnion: featID, indArea: valArea, indZone: valZone}
    layerProvider.changeAttributeValues({featID: valDict})

# save the attribute table
unionLayer.commitChanges()
# remove original fields
fieldsAll = unionLayer.fields().names()
fieldsKeep = ['fid_union', 'zone', 'zone_area']
fieldsRemove = [i for i in fieldsAll if i not in fieldsKeep]
fieldsRemoveIndex = [unionLayer.fields().indexFromName(i) for i in fieldsRemove]
layerProvider.deleteAttributes(fieldsRemoveIndex)
unionLayer.updateFields()

# TASK 4. Performing Intersection on Environment and Impact Area

# try using Environment layer directly -> error
unionLayer = QgsProject.instance().mapLayersByName('Impact Area')[0]
envLayer = QgsProject.instance().mapLayersByName('Environment')[0]
inpParam = { 'INPUT' : unionLayer, 'INPUT_FIELDS' : [], 'OUTPUT' : 'TEMPORARY_OUTPUT', 'OVERLAY' : envLayer, 'OVERLAY_FIELDS' : [], 'OVERLAY_FIELDS_PREFIX' : '' }
# outAlgo = processing.run("qgis:intersection", inpParam) # will generate error: QgsProcessingException

# run fix geometries tool first
inpParam = { 'INPUT' : envLayer, 'OUTPUT' : 'TEMPORARY_OUTPUT' }
outAlgo = processing.run('qgis:fixgeometries', inpParam)
envLayerFixed = outAlgo['OUTPUT']

# run intersection tool again with fixed geometry layer
inpParam = { 'INPUT' : unionLayer, 'INPUT_FIELDS' : [], 'OUTPUT' : 'TEMPORARY_OUTPUT', 'OVERLAY' : envLayerFixed, 'OVERLAY_FIELDS' : [], 'OVERLAY_FIELDS_PREFIX' : '' }
outAlgo = processing.run("qgis:intersection", inpParam)
outLayer = QgsProject.instance().addMapLayer(outAlgo['OUTPUT'])
outLayer.setName('Impact Area Intersect')

# (optional) function to perform geometry check and intersection
inpParam = { 'ERROR_OUTPUT' : 'TEMPORARY_OUTPUT', 'IGNORE_RING_SELF_INTERSECTION' : False, 'INPUT_LAYER' : envLayer, 'INVALID_OUTPUT' : 'TEMPORARY_OUTPUT', 'METHOD' : 2, 'VALID_OUTPUT' : 'TEMPORARY_OUTPUT' }
outAlgo = processing.run("qgis:checkvalidity", inpParam)

# helper function to return fixed geometry layer
def fix_geometry(inpLayer):
    inpParam = { 'ERROR_OUTPUT' : 'TEMPORARY_OUTPUT', 'IGNORE_RING_SELF_INTERSECTION' : False, 'INPUT_LAYER' : inpLayer, 'INVALID_OUTPUT' : 'TEMPORARY_OUTPUT', 'METHOD' : 2, 'VALID_OUTPUT' : 'TEMPORARY_OUTPUT' }
    outAlgo = processing.run("qgis:checkvalidity", inpParam)
    nInvalid = outAlgo['INVALID_COUNT']
    if nInvalid > 0:
        # return fixed geometry layer
        inpParam = { 'INPUT' : inpLayer, 'OUTPUT' : 'TEMPORARY_OUTPUT' }
        outAlgo = processing.run("qgis:fixgeometries", inpParam)
        inpLayerFixed = outAlgo['OUTPUT']
        print('geometry fixed for layer ' + inpLayer.name())
        return inpLayerFixed
    else:
        # return layer
        print('no geometry fix needed for layer ' + inpLayer.name())
        return inpLayer

def intersect_layers(inpLayerName1, inpLayerName2, outLayerName):
    # get layer references
    inpLayer1 = QgsProject.instance().mapLayersByName(inpLayerName1)[0]
    inpLayer2 = QgsProject.instance().mapLayersByName(inpLayerName2)[0]
    # get fixed layer references
    inpLayer1Fixed = fix_geometry(inpLayer1)
    inpLayer2Fixed = fix_geometry(inpLayer2)
    # run the tool
    inpParam = { 'INPUT' : inpLayer1Fixed, 'INPUT_FIELDS' : [], 'OUTPUT' : 'TEMPORARY_OUTPUT', 'OVERLAY' : inpLayer2Fixed, 'OVERLAY_FIELDS' : [], 'OVERLAY_FIELDS_PREFIX' : '' }
    outAlgo = processing.run("qgis:intersection", inpParam)
    outLayer = QgsProject.instance().addMapLayer(outAlgo['OUTPUT'])
    outLayer.setName(outLayerName)

# try out function and remove it
intersect_layers('Impact Area', 'Environment', 'Impact Area Intersect 2')
lyr = QgsProject.instance().mapLayersByName('Impact Area Intersect 2')[0]
QgsProject.instance().removeMapLayers([lyr.id()])

# TASK 5. Selecting Features from Queries

# 5.2. Translating Query Feature into Pythonic Code
intLayer = QgsProject.instance().mapLayersByName('Impact Area Intersect')[0]
selExpr = QgsExpression("ffh_typ_nr = 1 or geschuetzt_biotop = 1 or bedeutend_gruenland_typ = 1")
intSelFeatures = intLayer.getFeatures(QgsFeatureRequest(selExpr)) #QgsFeatureIterator
ids = [i.id() for i in intSelFeatures]
intLayer.selectByIds(ids)

# 5.3. Translating Vector Layer Adding into Pythonic Code
# create layer from selection
selLayer = intLayer.materialize(QgsFeatureRequest().setFilterFids(ids)) # alternative for ids: intLayer.selectedFeatureIds()
selLayer.setName("Environment Selection")
QgsProject.instance().addMapLayer(selLayer)
# clear selection
intLayer.selectByIds([])

# TASK 6. Reordering and Stylizing
# 6.1. Cleaning up Layers
lyrKeep = ['Environment', 'Autobahn', 'Autobahn 20', 'Autobahn 100', 'Autobahn 300', 'Inner Impact Area', 'Impact Area', 'Impact Area Intersect', 'Environment Selection']
lyrAll = [layer.name() for layer in QgsProject.instance().mapLayers().values()]
lyrRemove = [i for i in lyrAll if i not in lyrKeep]
for lyrName in lyrRemove:
    lyr = QgsProject.instance().mapLayersByName(lyrName)[0]
    QgsProject.instance().removeMapLayers([lyr.id()])
    
# 6.2. Reordering and Hiding layers
lyrOrder = ['Environment Selection', 'Impact Area Intersect', 'Impact Area', 'Inner Impact Area', 'Autobahn 20', 'Autobahn 100', 'Autobahn 300', 'Autobahn', 'Environment']
lyrVisible = ['Environment', 'Impact Area', 'Environment Selection']

# get the layer tree root of the project
lyrTreeRoot = QgsProject.instance().layerTreeRoot() # QgsLayerTree

# apply correct layer order by inserting cloned layer and removing the original
for i in range(len(lyrOrder)):
    lyrOrig = QgsProject.instance().mapLayersByName(lyrOrder[i])[0] # QgsVectorLayer
    # find the layer you want to reorder and clone them
    lyrTreeOrig = lyrTreeRoot.findLayer(lyrOrig.id()) # QgsLayerTreeLayer
    lyrClone = lyrTreeOrig.clone()
    # get a pointer to the parent object of the layer
    lyrParent = lyrTreeOrig.parent() # QgsLayerTree
    # insert the clones into the parent node and remove the original layer
    lyrParent.insertChildNode(i, lyrClone)
    lyrParent.removeChildNode(lyrTreeOrig)
    # set layer visibility
    lyrName = lyrOrder[i]
    lyrID = QgsProject.instance().mapLayersByName(lyrName)[0].id()
    if lyrName in lyrVisible:
        QgsProject.instance().layerTreeRoot().findLayer(lyrID).setItemVisibilityChecked(True)
    else:
        QgsProject.instance().layerTreeRoot().findLayer(lyrID).setItemVisibilityChecked(False) 

# refresh the map canvas
iface.mapCanvas().refresh()
print('Reordered and set visibility of ' + str(len(lyrOrder)) + ' layers')

# 6.3. stylizing layer
# get unique values of the layer
layerName = 'Environment Selection'
colName = 'ffh_typ_text'
layer = QgsProject.instance().mapLayersByName(layerName)[0]
colIndex = layer.fields().indexFromName(colName)
uniqueVal = layer.uniqueValues(colIndex)

# set fill properties for each unique value
from random import randrange
categories = []
for unique_value in uniqueVal:
    # initialize the default symbol for this geometry type
    symbol = QgsSymbol.defaultSymbol(layer.geometryType())
    # configure a symbol layer
    layer_style = {}
    layer_style['color'] = '%d, %d, %d' % (randrange(0, 256), randrange(0, 256), randrange(0, 256))
    layer_style['outline'] = '#000000'
    symbol_layer = QgsSimpleFillSymbolLayer.create(layer_style)
    # replace default symbol layer with the configured one
    if symbol_layer is not None:
        symbol.changeSymbolLayer(0, symbol_layer)
    # create renderer object
    category = QgsRendererCategory(unique_value, symbol, str(unique_value))
    # entry for the list of category items
    categories.append(category)
    
# apply and repaint
renderer = QgsCategorizedSymbolRenderer(colName, categories)
if renderer is not None:
    layer.setRenderer(renderer)

layer.triggerRepaint()

# (optional) formatting for the Impact Area layer
layerName = 'Impact Area'
colName = 'fid_union'
layer = QgsProject.instance().mapLayersByName(layerName)[0]
colIndex = layer.fields().indexFromName(colName)
uniqueVal = list(layer.uniqueValues(colIndex)) # list conversion needed for for loop
# blue RGB values to be applied
rgb1 = [30, 63, 102]
rgb2 = [82, 138, 174]
rgb3 = [188, 210, 232]
rgbs = [rgb1, rgb2, rgb3]

categories = []
for i in range(3):
    unique_value = uniqueVal[i]
    # initialize the default symbol for this geometry type
    symbol = QgsSymbol.defaultSymbol(layer.geometryType())
    # configure a symbol layer
    layer_style = {}
    layer_style['color'] = '%d, %d, %d' % (rgbs[i][0], rgbs[i][1], rgbs[i][2])
    layer_style['outline'] = '#000000'
    symbol_layer = QgsSimpleFillSymbolLayer.create(layer_style)
    # replace default symbol layer with the configured one
    if symbol_layer is not None:
        symbol.changeSymbolLayer(0, symbol_layer)
    # create renderer object
    category = QgsRendererCategory(unique_value, symbol, str(unique_value))
    # entry for the list of category items
    categories.append(category)

renderer = QgsCategorizedSymbolRenderer(colName, categories)
if renderer is not None:
    layer.setRenderer(renderer)

layer.triggerRepaint()

# 6.4. add base layer + move it to the background
envPath = QFileDialog.getOpenFileName(QFileDialog(), "Raster Layer Select", "setDefaultPath")[0]
env = iface.addRasterLayer(envPath)
env.setName("heli")
lyrOrig = env
lyrTreeOrig = lyrTreeRoot.findLayer(lyrOrig.id()) # QgsLayerTreeLayer
lyrClone = lyrTreeOrig.clone()
lyrParent = lyrTreeOrig.parent() # QgsLayerTree
lyrCount = len(QgsProject.instance().mapLayers().values())
lyrParent.insertChildNode(lyrCount + 1, lyrClone)
lyrParent.removeChildNode(lyrTreeOrig)

# extra: add OSM layer (uncomment last line)
tms = 'type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0'
layer = QgsRasterLayer(tms,'OSM', 'wms')
# QgsProject.instance().addMapLayer(layer)

# zoom to extent of Environment layer
lyrEnv = QgsProject.instance().mapLayersByName('Environment')[0]
cnvs = iface.mapCanvas()
cnvs.setExtent(lyrEnv.extent())
cnvs.refresh()