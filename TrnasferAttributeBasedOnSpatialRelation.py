# this script will transfer attribute source feature class to target feture class based on spatial relation
#with in i.e if any point feature falls in a ploygon feature then based on this spatial relation and Fileds mapping
# excel file attributes will be transfer fronm source filed of source feature to target field of target fearture
#This Script will run on Arcmap will not run on arcgis pro.
# format of fields mapping excel file should be following
# Source_ Fields            Terget_Fields
# source field name 1         Target field name 1
# source field name 2         Target field name 2
# and so on................
#..............................................
import arcpy
import os
import xlrd

#path = "E:\FiledMapping\Fieldmapping.xlsx"

sfc = arcpy.GetParameterAsText(0)
tfc = arcpy.GetParameterAsText(1)
path = arcpy.GetParameterAsText(2)
count = 1



def updatefc(sfn,tfn,sfc,tfc):
    sfn.append("SHAPE@")
    tfn.append("SHAPE@")
    with arcpy.da.SearchCursor(sfc, sfn) as subcur:

        for subrow in subcur:
            subshp = subrow[-1]
            with arcpy.da.UpdateCursor(tfc, tfn) as fcur:
                for frow in fcur:
                    fshp = frow[-1]
                    if fshp.within(subshp) == True:

                        for i in range(len(sfn) - 1):

                            frow[i] = subrow[i]
                            fcur.updateRow(frow)


def Read_Source_Field(exc):
    wb = xlrd.open_workbook(exc)
    Source_Fields = []
    sheet  = wb.sheet_by_index(0)
    for row in range(sheet.nrows):
         Source_Fields.append(sheet.cell_value(row,0))
    Source_Fields.pop(0)
    try:
        Source_Fields.remove("")
    finally:
        return Source_Fields



def Read_Target_Field(exc):
    wb = xlrd.open_workbook(exc)
    Target_Fields = []
    sheet  = wb.sheet_by_index(0)
    for row in range(sheet.nrows):
         Target_Fields.append(sheet.cell_value(row,1))
    Target_Fields.pop(0)
    try:
        Target_Fields.remove("")
    finally:
        return Target_Fields

sfn = Read_Source_Field(path)
tfn = Read_Target_Field(path)


updatefc(sfn,tfn,sfc,tfc)
