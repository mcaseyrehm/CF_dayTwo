import rhinoscriptsyntax as rs

def mapValue(val, inMin, inMax, outMin, outMax):
    outR = outMax - outMin
    inR = inMax - inMin
    inVal = val - inMin
    newVal = (inVal/inR) * outR
    return outMin + newVal

def lerp(startPt, endPt, T):
    len = rs.VectorSubtract(endPt, startPt)
    nVec = rs.VectorScale(len, T)
    return rs.VectorAdd(startPt, nVec)

def calcBiLinear(pt, bbMin, bbMax):
    bX = mapValue(pt.x,bbMin[0],bbMax[0],0.0f,1.0f)
    bY = mapValue(pt.y,bbMin[1],bbMax[1],0.0f,1.0f)
    return[bX,bY]

def main():
    unitRectMin = rs.GetPoint("select unit rect MIN")
    unitRectMax = rs.GetPoint("select unit rect MAX")
    
    unit = rs.GetObject("select polyline", 4)
    
    unitPts = []
    unitCoords =[]
    
    polylinePts = rs.PolylineVertices(unit)
    
    for pt in polylinePts:
        bc = calcBiLinear(pt,unitRectMin,unitRectMax)
        unitCoords.append(bc)
        



