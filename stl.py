import struct
from model import *

class ParseError(RuntimeError):
    pass

def parseTuple(line):
    return tuple(map(float,line.split(" ")))

def loadAsciiSTL(f):
    m = Model()
    line = f.readline()
    if not line.startswith("solid "):
        raise ParseError("Missing solid delimiter")
    while True:
        line = f.readline().strip()
        if line.startswith("endsolid"):
            return m
        elif line.startswith("facet normal "):
            t = Triangle()
            t.n = parseTuple(line[13:])
            line = f.readline().strip()
            if line != "outer loop":
                raise ParseError("Expected outer loop, got "+line)
            for i in range(3):
                line = f.readline().strip()
                if not line.startswith("vertex "):
                    raise ParseError("Expected vertex, got "+line)
                t.p[i] = parseTuple(line[7:])
            line = f.readline().strip()
            if line != "endloop":
                raise ParseError("Expected endloop, got "+line)
            line = f.readline().strip()
            if line != "endfacet":
                raise ParseError("Expected endfacet, got "+line)
            m.tris.append(t)
        else:
            raise ParseError("Unexpected line "+line)


def loadBinarySTL(f):
    m = Model()
    comment = f.read(80)
    def unpackPoint():
        return struct.unpack("<fff",f.read(12))
    (count,) = struct.unpack("<I",f.read(4))
    print count
    for i in range(count):
        t = Triangle()
        t.n = unpackPoint()
        t.p[0] = unpackPoint()
        t.p[1] = unpackPoint()
        t.p[2] = unpackPoint()
        (attribBytes,) = struct.unpack("<H",f.read(2))
        if attribBytes != 0:
            f.read(attribBytes)
        m.tris.append(t)
    return m

def loadSTL(f):
    try:
        return loadAsciiSTL(f)
    except ParseError as e:
        pass
    f.seek(0)
    return loadBinarySTL(f)

def saveAsciiSTL(m,f):
    f.write("solid bung\n")
    for t in m.tris:
        f.write("  facet normal {0} {1} {2}\n".format(*t.n))
        f.write("    outer loop\n")
        for p in t.p:
            f.write("      vertex {0} {1} {2}\n".format(*p))
        f.write("    endloop\n")
        f.write("  endfacet\n")
    f.write("endsolid\n")

if __name__ == '__main__':
    print "Testing on 40head.stl"
    m = loadSTL(open("octocap.stl"))
    print "Loaded",len(m.tris),"triangles"
