# convert numpy array to ply files
import sys
import numpy as np

class PLYWriter:
    def __init__(self, num_vertices: int, num_faces: int, comment = "created by PLYWriter"):
        assert num_vertices != 0
        self.num_vertices = num_vertices
        self.num_vertex_channels = 0
        self.vertex_channels = []
        self.vertex_data_type = []
        self.vertex_data = []
        self.num_faces = num_faces
        self.num_face_channels = 0
        self.face_channels = []
        self.face_data = []
        self.comment = comment
    
    def add_vertex_channel(self, key: str, type: str, data: np.array):
        if data.ndim == 1:
            assert data.size == self.num_vertices
            self.num_vertex_channels += 1
            if key in self.vertex_channels:
                print("WARNING: duplicate key " + key + " detected")
            self.vertex_channels.append(key)
            self.vertex_data_type.append(type)
            self.vertex_data.append(data)
        else:
            num_col = data.size // self.num_vertices
            assert data.ndim == 2 and data.size == num_col * self.num_vertices
            data.shape = (self.num_vertices, num_col)
            self.num_vertex_channels += num_col
            for i in range(num_col):
                item_key = key + "_" + str(i+1)
                if item_key in self.vertex_channels:
                    print("WARNING: duplicate key " + item_key + " detected")
                self.vertex_channels.append(item_key)
                self.vertex_data_type.append(type)
                self.vertex_data.append(data[:,i])
    
    def add_vertex_pos(self, x: np.array, y: np.array, z: np.array):
        self.add_vertex_channel("x", "float", x)
        self.add_vertex_channel("y", "float", y)
        self.add_vertex_channel("z", "float", z)        
    
    def add_vertex_color(self, r: np.array, g: np.array, b: np.array):
        self.add_vertex_channel("red", "float", r)
        self.add_vertex_channel("green", "float", g)
        self.add_vertex_channel("blue", "float", b)
    
    def add_vertex_color_uchar(self, r: np.array, g: np.array, b: np.array):
        self.add_vertex_channel("red", "uchar", r)
        self.add_vertex_channel("green", "uchar", g)
        self.add_vertex_channel("blue", "uchar", b)  

    def add_face_channels(self, key: str, data: np.array):
        pass # To-do

    def print_header(self, path: str, format: str):
        with open(path, "w") as f:
            f.writelines(["ply\n", "format " + format + " 1.0\n", "comment " + self.comment + "\n"])
            f.write("element vertex " + str(self.num_vertices) + "\n")
            for i in range(self.num_vertex_channels):
                f.write("property " + self.vertex_data_type[i] + " " + self.vertex_channels[i] + "\n")
            f.write("end_header\n")

    def export(self, path):
        self.print_header(path, "binary_" + sys.byteorder + "_endian")
        with open(path, "ab") as f:
            for i in range(self.num_vertices):
                for j in range(self.num_vertex_channels):
                    f.write(self.vertex_data[j][i])

    def export_ascii(self, path):
        self.print_header(path, "ascii")
        with open(path, "a") as f:
            for i in range(self.num_vertices):
                for j in range(self.num_vertex_channels):
                    f.write(str(self.vertex_data[j][i]) + " ")
                f.write("\n")

# example usage
# To-do: do these type casts internally
x = np.float32(np.random.rand(20))
y = np.float32(np.random.rand(20))
z = np.float32(np.random.rand(20))
r = np.ubyte(255*np.random.rand(20))
g = np.ubyte(255*np.random.rand(20))
b = np.ubyte(255*np.random.rand(20))
data1 = np.float32(np.random.rand(20))
data2 = np.uint32(2147483647*np.random.rand(20, 1)) # there is no uint32 in houdini vex, so we can't go beyond int32
data3 = np.float64(np.random.rand(2, 30)) # same here, double will be casted to float in houdini

writer = PLYWriter(20, 0, "example")

writer.add_vertex_pos(x,y,z)
writer.add_vertex_color_uchar(r,g,b)
writer.add_vertex_channel("data1", "float", data1)
writer.add_vertex_channel("data2", "uint", data2)
writer.add_vertex_channel("data3", "double", data3)

writer.export("example.ply")
writer.export_ascii("example_ascii.ply")
