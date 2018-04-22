class PolymeshDescription(object):
    class Vertex(object):
        def __init__(self, index, position, normal):
            '''Create a vertex by setting it index, position (as array or tuple of three elements) and normal (array or tuple of three elements)'''
            self._index = index
            self._position = (position[0], position[1], position[2])
            self._normal = (normal[0], normal[1], normal[2])

        def get_position_x(self):
            '''Return x-coordinate of the vertex'''
            return self._position[0]

        def get_position_y(self):
            '''Return y-coordinate of the vertex'''
            return self._position[1]

        def get_position_z(self):
            '''Return z-coordinate of the vertex'''
            return self._position[2]

        def get_position(self):
            '''Return position of the vertex as tuple of three elements (x, y, z)'''
            return self._position

        def get_normal(self):
            '''Return normal vector of the vertex as tuple of three elements (x, y, z)'''
            return self._normal

        def get_index(self):
            '''Return the index of the vertex'''
            return self._index

    class uvCoordinates(object):
        def __init__(self, uv):
            '''Create the pair of two values (u, v)'''
            self._uv = (uv[0], uv[1])

        def get_uv(self):
            '''Return the pair (u, v)'''
            return self._uv

    class Polygon(object):
        def __init__(self, p_index, size, v_indexes, normal):
            '''Create the polygon with index p_index. Size is the number of vertices, v_indexes is an array of vertices indexes, normal is a normal of polygon (as tuple of three elements)'''
            self._size = size
            self._index = p_index
            self._vertices = v_indexes
            self._normal = (normal[0], normal[1], normal[2])
            self._uv_coordinates = []  # stores all coordinates for uv0, then for uv1 and so on. The length of array is equal to size * uv_count

        def get_size(self):
            '''Return the number of vertices of the polygon'''
            return self._size

        def get_index(self):
            '''Return the index of the polygon'''
            return self._index

        def get_vetices(self):
            '''Return the vertices indexes of the polygon as array'''
            return self._vertices

        def get_normal(self):
            '''Return the norla of the polygon'''
            return self._normal

        def add_uv_coordinates(self, uv_data):
            '''Add uv-coordinates to polygon. The uv_data is an array of the same size as polygon size. The elements of uv_data are pairs (u, v) for each vertex of the polygon'''
            for uv in uv_data:
                self._uv_coordinates.append(PolymeshDescription.uvCoordinates(uv))

        def get_uv_array(self, uv_index):
            '''Return uv-data array of the polygon as array of pairs (u, v)'''
            return self._uv_coordinates[uv_index * self._size: (uv_index + 1) * self._size]

        def get_uv_array_expand(self, uv_index):
            '''Return the full list of uv-data of the polygon. This list contains size*uv_count pairs. The first segment of size elements represents the first set of uv-data, the second segment is for second uv-data and so on'''
            to_return = []
            for v_index in range(self._size):
                uv = self._uv_coordinates[uv_index * self._size + v_index].get_uv()
                to_return.append(uv[0])
                to_return.append(uv[1])
            return to_return

    def __init__(self, name):
        '''Init hte empty PolygonMesh object with specific name'''
        self._name = name
        self._vertices = []
        self._vertex_count = 0
        self._polygons = []
        self._polygons_count = 0
        self._uv_count = 0
        self._uv_names = []

    def get_name(self):
        '''Return the name of the PolygonMesh object'''
        return self._name

    def add_vertices(self, p_array, n_array=[]):
        '''Add vertices to the mesh. p_array is array of 3-tuples with coordinates, n_array is array of 3-tuples with normals of vertices'''
        self._vertex_count = len(p_array)
        for v_index in range(self._vertex_count):
            self._vertices.append(PolymeshDescription.Vertex(v_index, p_array[v_index], n_array[v_index] if v_index < len(n_array) else (0.0, 0.0, 0.0)))

    def add_polygon(self, v_indexes, normal):
        '''Add one polygon to the mesh by setting indexes of vertices and normal'''
        self._polygons.append(PolymeshDescription.Polygon(self._polygons_count, len(v_indexes), v_indexes, normal))
        self._polygons_count = self._polygons_count + 1

    def add_uv(self, uv_array, uv_name=""):
        '''Add uv-data to the mesh by setting uv_array as plain array of values (not (u, v)-pairs). The length should be equal to the sum of polygon sizes. Array contains data at the beginig for the first polygon, next for second and so on'''
        self._uv_names.append(uv_name if len(uv_name) > 0 else "uv" + str(len(self._uv_names)))
        uv_shift = 0
        for polygon in self._polygons:
            p_size = polygon.get_size()
            p_uv = []
            for i in range(p_size):
                p_uv.append((uv_array[uv_shift + 2*i], uv_array[uv_shift + 2*i + 1]))
            polygon.add_uv_coordinates(p_uv)
            uv_shift += 2*p_size
        self._uv_count = self._uv_count + 1

    def get_vertex_count(self):
        '''Return the count of vertices in the PolygonMesh'''
        return self._vertex_count

    def get_polygons_count(self):
        '''Return the nmber of polygons'''
        return self._polygons_count

    def get_uv_count(self):
        '''Return the number of stored uv-coordinates'''
        return self._uv_count

    def get_uv_name(self, uv_index):
        '''Return the name of uv-coordinates data'''
        return self._uv_names[uv_index]

    def get_vertices_raw(self):
        '''Return an array of vertices as Vertex-class items'''
        return self._vertices

    def get_polygons_raw(self):
        '''Return an arary of polygons as Polygon-class items'''
        return self._polygons

    def get_polygons_array(self):
        '''Return polygon vertices as plain array of integers: [s1, v1, v2, ..., v_s1, s2, v1, v2, ..., v_s2, ...]. Here s1 - the size of the first polygon , s2 - of the second and so on'''
        return_array = []
        for p in self._polygons:
            return_array.append(p.get_size())
            return_array += p.get_vetices()
        return tuple(return_array)

    def get_vertices_array(self):
        '''Return coordinates of vertices as plain array of float: [v1_x, v1_y, v1_z, v2_x, v2_y, x2_z, ...]'''
        to_return = []
        for v in self._vertices:
            to_return.append(v.get_position_x())
            to_return.append(v.get_position_y())
            to_return.append(v.get_position_z())
        return to_return

    def get_uv_data(self, uv_index):
        '''Return uv-coordinates as plain array of integers'''
        to_return = []
        for polygon in self._polygons:
            to_return.extend(polygon.get_uv_array_expand(uv_index))
        return to_return

    def get_complete_uv_data(self):
        if self._uv_count == 0:
            return []
        else:
            to_return = self.get_uv_data(0)
            for uv_index in range(1, self._uv_count):
                to_return.extend(self.get_uv_data(uv_index))
            return to_return


if __name__ == "__main__":
    # PolymeshDescription can be used for store very basic data of polygon mesh object
    # This data contains vertices, polygons, polygon normals and sets of uv-coordiantes.
    # Here is example of storing cube
    mesh = PolymeshDescription("cube_object")
    vertices = [(-1.0, -1.0, -1.0), (-1.0, 1.0, -1.0), (1.0, 1.0, -1.0), (1.0, -1.0, -1.0), (-1.0, -1.0, 1.0), (-1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, -1.0, 1.0)]
    mesh.add_vertices(vertices)  # does not set vertex normals, because this is nonsense
    # next set polygons
    mesh.add_polygon([0, 1, 2, 3], (0.0, 0.0, -1.0))  # bottom
    mesh.add_polygon([4, 7, 6, 5], (0.0, 0.0, 1.0))  # top
    mesh.add_polygon([0, 3, 7, 4], (0.0, -1.0, 0.0))  # front
    mesh.add_polygon([1, 5, 6, 2], (0.0, 1.0, 0.0))  # back
    mesh.add_polygon([0, 4, 5, 1], (-1.0, 0.0, 0.0))  # left
    mesh.add_polygon([2, 6, 7, 3], (1.0, 0.0, 0.0))  # right
    # next set uv-coordinates. Full quad (0, 0) - (1, 1) per face
    uv_array = [0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0] * 6
    mesh.add_uv(uv_array, "uv0")
