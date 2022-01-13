# this script will check the three consecutive vertex of a polyline, if the angle between first point and second
# point is eqaual angle between second and third point, it will delete second point
# but path of polyline will remain same.Sometime on a utility network dataset like electrical network when you create
# the network geometric network lines intersecting each other get a vertex by at intersection place by default due to
# due to network creation tool this script is helpful to delete these unwanted vertex due to the network creation.





import arcpy
import numpy as np
import math
from math import atan2, degrees

aprx = arcpy.mp.ArcGISProject("CURRENT")
maps = aprx.listMaps()[0]
maplayrs = maps.listLayers()

fc = arcpy.GetParameterAsText(0)

def angle_between(p1, p2):
    xDiff = p2[0] - p1[0]
    yDiff = p2[1] - p1[1]
    return degrees(atan2(yDiff, xDiff))


def vertextodelete(lst):
    lstvertex = []
    i = 0
    for i in range(len(lst) - 2):
        pnt1 = lst[i]
        pnt2 = lst[i + 1]
        pnt3 = lst[i + 2]
        ang = angle_between(pnt1, pnt2)
        ang1 = angle_between(pnt2, pnt3)
        if math.ceil(ang) == math.ceil(ang1):
            lstvertex.append(pnt2)
        else:
            i = i + 1
    print(i)
    return lstvertex


def deletevtx(lst1, lst2):
    baselst = lst1
    for itm in lst2:
        lst1.remove(itm)
    return lst1


def createnewline(pntlst):
    arr = []
    for j in pntlst:
        x = j[0]
        y = j[1]
        point = arcpy.Point(x, y)
        arr.append(point)
    return arr


with arcpy.da.UpdateCursor(fc, ["shape@"]) as cursor:
    for row in cursor:
        lst = []
        pl = row[0]
        for part in pl:
            for pnt in part:
                pnlst = [pnt.X, pnt.Y]
                lst.append(pnlst)
        vtbd = vertextodelete(lst)
        vtlst = deletevtx(lst, vtbd)
        aray = createnewline(vtlst)
        pyaray = arcpy.Array(aray)
        pl = arcpy.Polyline(pyaray)
        row[0] = pl
        cursor.updateRow(row)
