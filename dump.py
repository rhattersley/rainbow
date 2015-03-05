import struct
import subprocess
import os

def getMax(image):
    return max([max([max(p) for p in row]) for row in image])

def getMin(image):
    return min([min([min(p) for p in row]) for row in image])

def linearMap(image, filename):
    m = getMax(image)
    s = 255.0/m if m > 0 else 1
    f = open(filename, 'wb')
    for row in image:
        for p in row:
            ip = [int(v*s) for v in p]
            f.write(struct.pack('=BBB', *ip))
    f.close()

def powerMap(image, filename):
    m = getMax(image)
    if m == 0:
        m = 1
    e = 0.7
    f = open(filename, 'wb')
    for row in image:
        for p in row:
            #ip = [int(255 * ((v / m) ** e)) for v in p]
            ip = [min(255, int(512 * ((v / m) ** e))) for v in p]
            f.write(struct.pack('=BBB', *ip))
    f.close()

def dump(image, png_path):
    # Write out a RAW file
    rgb_path = png_path + '.rgb'
    #linearMap(image, rgb_path)
    powerMap(image, rgb_path)

    # Convert the RAW file to PNG
    w = len(image[0])
    h = len(image)
    args = ('convert -size %dx%d -depth 8 %s %s' % (w, h, rgb_path, png_path)).split()
    subprocess.check_call(args)

    # Get rid of the RAW file
    args = ('rm %s' % rgb_path).split()
    subprocess.check_call(args)


def dumpExr(image):
    width = len(image[0])
    height = len(image)
    
    f = open('test.exr', 'wb')
    
    # Magic number (4)
    f.write(struct.pack('=BBBB', 0x76, 0x2f, 0x31, 0x01))
    
    # Version, flags (4)
    f.write(struct.pack('=BBBB', 2, 0, 0, 0))
    
    # Header
    #   channels (75)
    f.write(struct.pack('=9s7sI', 'channels', 'chlist', 18*3+1))
    #       ... R:FLOAT:0:0:1:1 (18)
    f.write(struct.pack('=2sIIII', 'R', 2, 0, 1, 1))
    #       ... G:FLOAT:0:0:1:1 (18)
    f.write(struct.pack('=2sIIII', 'G', 2, 0, 1, 1))
    #       ... B:FLOAT:0:0:1:1 (18)
    f.write(struct.pack('=2sIIII', 'B', 2, 0, 1, 1))
    #       ... end (1)
    f.write(struct.pack('=B', 0))
    #   compression (29)
    f.write(struct.pack('=12s12sIB', 'compression', 'compression', 1, 0))
    #   dataWindow (37)
    f.write(struct.pack('=11s6sI4I', 'dataWindow', 'box2i', 16, 0, 0, width-1, height-1))
    #   displayWindow (40)
    f.write(struct.pack('=14s6sI4I', 'displayWindow', 'box2i', 16, 0, 0, width-1, height-1))
    #   lineOrder (25)
    f.write(struct.pack('=10s10sIB', 'lineOrder', 'lineOrder', 1, 0))
    #   pixelAspectRatio (31)
    f.write(struct.pack('=17s6sIf', 'pixelAspectRatio', 'float', 4, 1.0))
    #   [end of header] (1)
    f.write(struct.pack('=B', 0))

    # Scan line offset table
    tableOffset = 4+4+75+29+37+40+25+31+1
    tableSize = height*8
    rowOffset = tableOffset + tableSize
    dataSize = 3*4*width
    rowSize = 8+dataSize
    for y in range(height):
        f.write(struct.pack('Q', rowOffset+y*rowSize))

    # Pixel data
    for y in range(height):
        f.write(struct.pack('II', y, dataSize))
        for p in image[y]:
            f.write(struct.pack('f', p[2]))
        for p in image[y]:
            f.write(struct.pack('f', p[1]))
        for p in image[y]:
            f.write(struct.pack('f', p[0]))
            
    f.close()
