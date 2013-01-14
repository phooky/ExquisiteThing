#
# Model: tris, model, etc.
#

# return an array of pts representing the sliced triangle/poly
def slice(pts,z,below):
    def acceptPt(pt):
        if below:
            return pt[2] <= z
        else:
            return pt[2] >= z
    def findNextGood(i):
        j = (i+1)%len(pts)
        while j != i:
            if i == -1:
                i = j
            if acceptPt(pts[j]):
                return j
            j = (j+1)%len(pts)
        return -1
    # fill out with crossing points as well as pts
    if len(pts) == 0:
        return pts
    out = []
    firstGood = findNextGood(-1)
    if firstGood == -1:
        return []
    out.append(pts[firstGood])
    acc = True
    for k in range(0,len(pts)):
        l = (k+firstGood+1)%len(pts)
        accp = acceptPt(pts[l])
        if accp != acc:
            # add point btwn pts[l] and out[-1]
            p1 = out[-1]
            p2 = pts[l]
            zd = p2[2] - p1[2]
            zdp = p2[2] - z
            p = zdp/zd
            pp = 1-p
            p3 = (p2[0] + (p*(p1[0]-p2[0])),
                  p2[1] + (p*(p1[1]-p2[1])),
                  z)
            out.append(p3)
        if l != firstGood:
            out.append(pts[l])
        acc = accp
    # filter by accept
    return filter(acceptPt,out)

class Triangle:
    def __init__(self):
        self.p = [(0,0,0)]*3
        self.n = (0,0,0)

    def slice(self,zlow,zhigh):
        pts = slice(self.p,zhigh,True)
        pts = slice(pts,zlow,False)
        tris = []
        while len(pts) > 3:
            t = Triangle()
            t.n = self.n
            t.p = [pts[0],pts[1],pts[2]]
            pts = pts[0:1]+pts[2:]
            tris.append(t)
        if len(pts) == 3:
            t = Triangle()
            t.n = self.n
            t.p = pts
            tris.append(t)
        elif len(pts) > 0:
            raise RuntimeError("slice should never return {0} points".format(len(pts)))
        return tris
        
class Model:
    def __init__(self):
        self.tris = []

    def slice(self,zlow,zhigh):
        m = Model()
        for tri in self.tris:
            for t in tri.slice(zlow,zhigh):
                m.tris.append(t)
            #m.tris.append(tri)
        return m
                

