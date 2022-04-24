# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

def CreateRectangle():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.rectangle(point1=(0.0, 0.0), point2=(33.75, 22.5))
    s.ObliqueDimension(vertex1=v[3], vertex2=v[0], textPoint=(14.7341156005859, 
        -9.99102210998535), value=40.0)
    s.ObliqueDimension(vertex1=v[2], vertex2=v[3], textPoint=(49.3877563476563, 
        7.98025131225586), value=30.0)
    p = mdb.models['Model-1'].Part(name='Rect', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Rect']
    p.BaseSolidExtrude(sketch=s, depth=20.0)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Rect']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']

CreateRectangle()
