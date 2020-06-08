# example usage of the PLYWriter

import numpy as np
from np2ply import PLYWriter

# set up the numpy arrays to output
# vertex positions
x = np.random.rand(20)
y = np.random.rand(20)
z = np.random.rand(20)
# vertex colors
r = 255*np.random.rand(20)
g = 255*np.random.rand(20)
b = 255*np.random.rand(20)
# vertex data channels
vdata1 = np.random.rand(20)
vdata2 = 2147483647*np.random.rand(20, 1) # a vertex int channel. There is no uint32 in houdini vex, so we can't go beyond int32
# vertex normal
vdata3 = np.random.rand(3,20)
# face vertex indices
findices = (20*np.random.rand(5, 4)).astype(int)
# face channel
fdata = np.random.rand(5)

# set up the PLYWriter
writer = PLYWriter(num_vertices=20, num_faces=5, face_type="quad")
# fill required channels
writer.add_vertex_pos(x,y,z)
writer.add_faces(findices)
# fill optional channels
writer.add_vertex_color_uchar(r,g,b)
writer.add_vertex_channel("vdata1", "float", vdata1)
writer.add_vertex_channel("vdata2", "uint", vdata2)
writer.add_vertex_normal(vdata3[0,:], vdata3[1,:], vdata3[2,:])
writer.add_face_channel("fdata", "float", fdata)
# export binary ply file
writer.export("example.ply")
# export ascii ply file
writer.export_ascii("example_ascii.ply")
