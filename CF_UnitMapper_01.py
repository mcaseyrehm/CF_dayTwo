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
    bX = mapValue(pt.X,bbMin[0],bbMax[0],0.0,1.0)
    bY = mapValue(pt.Y,bbMin[1],bbMax[1],0.0,1.0)
    return[bX,bY]

def main():
    unitRectMin = rs.GetPoint("select unit rect MIN")
    unitRectMax = rs.GetPoint("select unit rect MAX")
    
    unit = rs.GetObject("select polyline", 4)
    mesh = rs.GetObject("select mesh",32)
    
    unitPts = []
    unitCoords =[]
    
    polylinePts = rs.PolylineVertices(unit)
    
    for pt in polylinePts:
        bc = calcBiLinear(pt,unitRectMin,unitRectMax)
        unitCoords.append(bc)
        unitPts.append(pt)
    
    v = rs.MeshVertices(mesh)
    faceVerts = rs.MeshFaceVertices(mesh)
    
    for fv in faceVerts:
        v0 = v[fv[0]]
        v1 = v[fv[1]]
        v2 = v[fv[2]]
        v3 = v[fv[3]]
        
        newPts = []
        for i in range(0, len(unitPts)):
            bLC = unitCoords[i]
            nX1 = lerp(v0,v1,bLC[0])
            nX2 = lerp(v3,v2 ,bLC[0])
            pt = lerp(nX1,nX2,bLC[1])
            rs.AddPoint(pt)
            newPts.append(pt)
            
        rs.AddPolyline(newPts)


if __name__ == "__main__":
    main()



