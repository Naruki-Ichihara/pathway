import pathway as p
from svgpathtools import Path, Line
import numpy as np

# IO
path = 'circle.gcode'

# Settings
nozzleTemp = 260
bedTemp = 60
feedSpeed = 600
layerHeight = 0.125

# Center point
x_c = 130
y_c = 100

# Geometries
hatch = 1.0
r0 = 5
N = 20

# Stack number
stack = 24


w = hatch
paths = []
orig = x_c+y_c*1j
prev = orig
for theta in range(360*N):
    r = r0 + w/360*theta
    current = r*np.cos(np.deg2rad(theta))+r*np.sin(np.deg2rad(theta))*1j + orig
    line = Path(Line(prev, current))
    paths.append(line)
    prev = current
paths = Path(*paths).reversed()

settings = {'retractionLiftZ': 0.8,
            'retractionSpeed': 0.0,
            'startExtraLength': 55, #45
            'startCompression': 0.1,
            'startCompressionTime': 2.5}

header = '\nM104 S{} T1\nM140 S{}\nM109 S{} T1\nM190 S{}\nG21\nG90\nM82\nG28\nM530 S1\nG1 Z10 F900\nM400\nT0 R\nG92 U0\n'.format(nozzleTemp, bedTemp, nozzleTemp, bedTemp)
footer = 'M400\nM104 S0 T0\nM106 P1 S0\nG91\nG1 Z20 F900\nG90\nG28\nM530 S0'
cut = 'M400\nM280 P0 S30\nG4 P100\nM280 P0 S90\nM400\n'
mergin = 44

# Position wise values
ex = lambda x, y: 1.0
feed = lambda x, y: feedSpeed

# svg paths to gPath class list
gpaths = [p.gPath(path) for path in paths]

# Set primary layer
layer = p.Layer(gpaths, ex, feed)
layer.cuttingConfig(cut, mergin=mergin)

# Set model with printer setting
model = p.Model(settings)
model.set_header(header)
model.set_footer(footer)

for i in range(stack):
    model.stack(layer, layerHeight*i+0.025)

# Generate g-code
model.generate(path)