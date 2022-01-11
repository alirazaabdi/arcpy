import arcpy

aprx = arcpy.mp.ArcGISProject("CURRENT")

maps = aprx.listMaps()[0]

maplayrs = maps.listLayers()

alllayers = arcpy.GetParameterAsText(0)

layerlist = arcpy.GetParameterAsText(1)
maxscale = arcpy.GetParameterAsText(2)
minscale = arcpy.GetParameterAsText(3)

listOfLayers = [x.strip() for x in layerlist.split(";")]

if alllayers == 'true':

    for lay in maplayrs:
        lay.maxThreshold = maxscale
        lay.minThreshold = minscale
else:
    for lay in maplayrs:
        if lay.name in listOfLayers:
            lay.maxThreshold = maxscale
            lay.minThreshold = minscale
        else:
            pass











