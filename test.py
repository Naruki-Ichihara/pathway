import pathway as p
from svgpathtools import Path, Line

paths = []
for i in range(13):
    shift = 6*i
    if i%2 == 0:
        paths.append(Path(Line((70+50j)+(0+shift*1j), (220+50j)+(0+shift*1j))))
    else:
        paths.append(Path(Line((220+50j)+(0+shift*1j), (70+50j)+(0+shift*1j))))
paths = p.readSVG('/workspace/svgs/circle.svg')
paths = p.paths2LinePaths(paths, division=100, sorting=False)

settings = {'extruderTemp': 260,
            'bedTemp': 60,
            'fanSpeed': 255,
            'retractionLiftZ': 0.8,
            'retractionSpeed': 0.0,
            'startExtraLength': 55, #45
            'startCompression': 0.05,
            'startCompressionTime': 2.5}

cut = 'M400\nM280 P0 S30\nG4 P100\nM280 P0 S90\nM400\n'
mergin = 44

# Position wise values
ex = lambda x, y: 1.0   # Extrusion map
feed = lambda x, y: 300 # Feedrate map

# svg paths to gPath class list
gpaths = [p.gPath(path) for path in paths]

# Set primary layer
layer = p.Layer(gpaths, ex, feed)
layer.cuttingConfig(cut, mergin=mergin)

# Set model with printer setting
model = p.Model(settings)

model.stack(layer, 0.2)

# Generate g-code
model.generate('test.gcode')