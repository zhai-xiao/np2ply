# example usage of the PLYWriter

import numpy as np
from np2ply import PLYWriter

# set up the numpy arrays to output
num_vert = 20
num_face = 5
# vertex positions
x = np.random.rand(num_vert)
y = np.random.rand(num_vert)
z = np.random.rand(num_vert)
# vertex colors
r = np.random.rand(num_vert)
g = np.random.rand(num_vert)
b = np.random.rand(num_vert)
a = np.random.rand(num_vert)
# vertex data channels
vdata1 = np.random.rand(num_vert)
vdata2 = 2147483647*np.random.rand(num_vert, 1) # a vertex int channel. There is no uint32 in houdini vex, so we can't go beyond int32
# vertex normal
vdata3 = np.random.rand(3,num_vert)
# face vertex indices
findices = (num_vert*np.random.rand(num_face, 4)).astype(int)
# face channel
fdata = np.random.rand(num_face)

# set up the PLYWriter
writer = PLYWriter(num_vertices=20, num_faces=5, face_type="quad")
# fill required channels
writer.add_vertex_pos(x,y,z)
writer.add_faces(findices)
# fill optional channels
writer.add_vertex_normal(vdata3[0,:], vdata3[1,:], vdata3[2,:])
writer.add_vertex_rgba(r,g,b,a)
writer.add_vertex_id()
writer.add_vertex_piece(np.ones(num_vert))
writer.add_vertex_channel("vdata1", "float", vdata1)
writer.add_vertex_channel("vdata2", "uint", vdata2)
writer.add_face_id()
writer.add_face_piece(2*np.ones(num_face))
writer.add_face_channel("fdata", "float", fdata)
# export binary ply file
writer.export("example.ply")
# export ascii ply file
writer.export_ascii("example_ascii.ply")
