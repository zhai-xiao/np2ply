# convert numpy array to ply files
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
            self.vertex_channels.append(key)
            self.vertex_data_type.append(type)
            self.vertex_data.append(data)
        else:
            num_col = data.size // self.num_vertices
            assert data.ndim == 2 and data.size == num_col * self.num_vertices
            data.shape = (self.num_vertices, num_col)
            self.num_vertex_channels += num_col
            for i in range(num_col):
                self.vertex_channels.append(key + "_" + str(i+1))
                self.vertex_data_type.append(type)
                self.vertex_data.append(data[:,i])

    def add_face_channels(self, key: str, data: np.array):
        pass # To-do

    def export(self, path):
        with open(path, "w") as f:
            f.writelines(["ply\n", "format ascii\n", "comment " + self.comment + "\n"])
            f.write("element vertex " + str(self.num_vertices) + "\n")
            for i in range(self.num_vertex_channels):
                f.write("property " + self.vertex_data_type[i] + " " + self.vertex_channels[i] + "\n")
            f.write("end_header\n")
            for i in range(self.num_vertices):
                for j in range(self.num_vertex_channels):
                    f.write(str(self.vertex_data[j][i]) + " ")
                f.write("\n")


# example usage

writer = PLYWriter(20, 0)

x = np.random.rand(20)
y = np.random.rand(20)
z = np.random.rand(20)
data1 = np.random.rand(20)
data2 = np.random.rand(20, 1).astype(int)
data3 = np.random.rand(2, 30)

writer.add_vertex_channel("x", "yfloat", x)
writer.add_vertex_channel("y", "float", y)
writer.add_vertex_channel("z", "float", z)
writer.add_vertex_channel("data1", "float", data1)
writer.add_vertex_channel("data2", "int", data2)
writer.add_vertex_channel("data3", "double", data3)

writer.export(r"d:\example.ply")