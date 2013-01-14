#!/usr/bin/python
import sys
import stl

def usage():
    print "bunger.py INPATH ZLOW ZHIGH OUTPATH"

# Cut a bung out of an STL file.
if __name__ == '__main__':
    if len(sys.argv) < 5:
        usage()
        sys.exit()
    inpath = sys.argv[1]
    zlow = float(sys.argv[2])
    zhigh = float(sys.argv[3])
    outpath = sys.argv[4]
    model = stl.loadSTL(open(inpath)).slice(zlow,zhigh)
    stl.saveAsciiSTL(model,open(outpath,"w"))

