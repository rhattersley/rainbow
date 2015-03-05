import numpy

import scene
import tracer


class Image(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = numpy.empty((height, width, 3), dtype=numpy.float32)

    def add_fragment(self, fragment):
        x1, y1, x2, y2, image = fragment
        self.image[y1:y2, x1:x2] = image

    def save(self, path):
        # Since we don't have access to a PNG library we write the image out as
        # raw RGB data and use ImageMagick to convert it.
        import dump
        dump.dump(self.image, path)


def show_scenes():
    print 'Scene names:'
    for name in scene.scene_names():
        print '  ', name


def trace_fragment(scene_name, width, height, x1, y1, x2, y2, preview):
    scene_description = scene.getScene(scene_name, preview)
    image = tracer.getImage(scene_description, width, height, 4, x1, y1, x2, y2)
    return (x1, y1, x2, y2, image)
