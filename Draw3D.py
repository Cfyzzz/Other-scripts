import copy
from math import cos, sin
import simple_draw as sd


martix_ident = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
]

matrix = copy.deepcopy(martix_ident)


def vec_mul_matrix(vec, matrix):
    x = (vec[0] * matrix[0][0] +
         vec[1] * matrix[0][1] +
         vec[2] * matrix[0][2] +
         matrix[0][3]
         )
    y = (vec[0] * matrix[1][0] +
         vec[1] * matrix[1][1] +
         vec[2] * matrix[1][2] +
         matrix[1][3]
         )
    z = (vec[0] * matrix[2][0] +
         vec[1] * matrix[2][1] +
         vec[2] * matrix[2][2] +
         matrix[2][3]
         )
    return [x, y, z]


def matrix_mul_matrix(matrix1, matrix2):
    _matrix = copy.deepcopy(martix_ident)
    _matrix[0][0] = matrix1[0][0] * matrix2[0][0] + matrix1[0][1] * matrix2[1][0] + matrix1[0][2] * matrix2[2][0] + \
                    matrix1[0][3] * matrix2[3][0]
    _matrix[0][1] = matrix1[0][0] * matrix2[0][1] + matrix1[0][1] * matrix2[1][1] + matrix1[0][2] * matrix2[2][1] + \
                    matrix1[0][3] * matrix2[3][1]
    _matrix[0][2] = matrix1[0][0] * matrix2[0][2] + matrix1[0][1] * matrix2[1][2] + matrix1[0][2] * matrix2[2][2] + \
                    matrix1[0][3] * matrix2[3][2]
    _matrix[0][3] = matrix1[0][0] * matrix2[0][3] + matrix1[0][1] * matrix2[1][3] + matrix1[0][2] * matrix2[2][3] + \
                    matrix1[0][3] * matrix2[3][3]

    _matrix[1][0] = matrix1[1][0] * matrix2[0][0] + matrix1[1][1] * matrix2[1][0] + matrix1[1][2] * matrix2[2][0] + \
                    matrix1[1][3] * matrix2[3][0]
    _matrix[1][1] = matrix1[1][0] * matrix2[0][1] + matrix1[1][1] * matrix2[1][1] + matrix1[1][2] * matrix2[2][1] + \
                    matrix1[1][3] * matrix2[3][1]
    _matrix[1][2] = matrix1[1][0] * matrix2[0][2] + matrix1[1][1] * matrix2[1][2] + matrix1[1][2] * matrix2[2][2] + \
                    matrix1[1][3] * matrix2[3][2]
    _matrix[1][3] = matrix1[1][0] * matrix2[0][3] + matrix1[1][1] * matrix2[1][3] + matrix1[1][2] * matrix2[2][3] + \
                    matrix1[1][3] * matrix2[3][3]

    _matrix[2][0] = matrix1[2][0] * matrix2[0][0] + matrix1[2][1] * matrix2[1][0] + matrix1[2][2] * matrix2[2][0] + \
                    matrix1[2][3] * matrix2[3][0]
    _matrix[2][1] = matrix1[2][0] * matrix2[0][1] + matrix1[2][1] * matrix2[1][1] + matrix1[2][2] * matrix2[2][1] + \
                    matrix1[2][3] * matrix2[3][1]
    _matrix[2][2] = matrix1[2][0] * matrix2[0][2] + matrix1[2][1] * matrix2[1][2] + matrix1[2][2] * matrix2[2][2] + \
                    matrix1[2][3] * matrix2[3][2]
    _matrix[2][3] = matrix1[2][0] * matrix2[0][3] + matrix1[2][1] * matrix2[1][3] + matrix1[2][2] * matrix2[2][3] + \
                    matrix1[2][3] * matrix2[3][3]

    _matrix[3][0] = matrix1[3][0] * matrix2[0][0] + matrix1[3][1] * matrix2[1][0] + matrix1[3][2] * matrix2[2][0] + \
                    matrix1[3][3] * matrix2[3][0]
    _matrix[3][1] = matrix1[3][0] * matrix2[0][1] + matrix1[3][1] * matrix2[1][1] + matrix1[3][2] * matrix2[2][1] + \
                    matrix1[3][3] * matrix2[3][1]
    _matrix[3][2] = matrix1[3][0] * matrix2[0][2] + matrix1[3][1] * matrix2[1][2] + matrix1[3][2] * matrix2[2][2] + \
                    matrix1[3][3] * matrix2[3][2]
    _matrix[3][3] = matrix1[3][0] * matrix2[0][3] + matrix1[3][1] * matrix2[1][3] + matrix1[3][2] * matrix2[2][3] + \
                    matrix1[3][3] * matrix2[3][3]
    return _matrix


def translate(vec):
    _matrix = copy.deepcopy(martix_ident)
    _matrix[0][3] = vec[0]
    _matrix[1][3] = vec[1]
    _matrix[2][3] = vec[2]
    return _matrix


def scale(vec):
    _matrix = copy.deepcopy(martix_ident)
    _matrix[0][0] = vec[0]
    _matrix[1][1] = vec[1]
    _matrix[2][2] = vec[2]
    return _matrix


def rotateX(angle):
    _matrix = copy.deepcopy(martix_ident)
    _matrix[1][1] = cos(angle)
    _matrix[2][1] = -sin(angle)
    _matrix[1][2] = sin(angle)
    _matrix[2][2] = cos(angle)
    return _matrix


def rotateY(angle):
    _matrix = copy.deepcopy(martix_ident)
    _matrix[0][0] = cos(angle)
    _matrix[0][2] = sin(angle)
    _matrix[2][0] = -sin(angle)
    _matrix[2][2] = cos(angle)
    return _matrix


def rotateZ(angle):
    _matrix = copy.deepcopy(martix_ident)
    _matrix[0][0] = cos(angle)
    _matrix[0][1] = -sin(angle)
    _matrix[1][0] = sin(angle)
    _matrix[1][1] = cos(angle)
    return _matrix


def length_line(a, b):
    """Длина линии между двумя точками"""
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5


def get_point_line(a, b, percent=0.5):
    vector = (b.x - a.x, b.y - a.y)
    vector_2 = (vector[0] * percent, vector[1] * percent)
    point_end = sd.get_point(x=a.x + vector_2[0], y=a.y + vector_2[1])
    return point_end


class Mesh:

    def __init__(self, vertices, polygons):
        self.vertices = []
        self.polygons = polygons
        self.angle = 0
        self.origin = sd.get_point(0, 0)
        self._prepare_vertices(vertices)
        self._calculate_origin()

    def _prepare_vertices(self, vertices):
        for vertex in vertices:
            self.vertices.append([vertex[0], vertex[1], 0])

    def _calculate_origin(self):
        left_x = min([vert[0] for vert in self.vertices])
        right_x = max([vert[0] for vert in self.vertices])
        top_y = min([vert[1] for vert in self.vertices])
        bottom_y = max([vert[1] for vert in self.vertices])
        x = (left_x + right_x) // 2
        y = (top_y + bottom_y) // 2
        self.origin = sd.get_point(x, y)

    def move_to(self, point):
        dx = point.x - self.origin.x
        dy = point.y - self.origin.y
        for vertex in self.vertices:
            vertex[0] += dx
            vertex[1] += dy
        self.origin = point

    def scale(self, scaleXY):
        mat_scale = scale([scaleXY[0], scaleXY[1], 1])
        mat_trans = translate([-self.origin.x, -self.origin.y, 0])
        mat = matrix_mul_matrix(mat_trans, mat_scale)
        self.apply_matrix(mat)
        old_origin = self.origin
        self._calculate_origin()
        self.move_to(old_origin)

    def rotate(self, angle_deg):
        mat_trans = translate([-self.origin.x, -self.origin.y, 0])
        mat_rot = rotateZ(6.30 * angle_deg / 360)
        mat = matrix_mul_matrix(mat_trans, mat_rot)
        self.apply_matrix(mat)
        old_origin = self.origin
        self._calculate_origin()
        self.move_to(old_origin)

    def rotateY(self, angle_deg):
        mat_trans = translate([-self.origin.x, -self.origin.y, 0])
        mat_rot = rotateY(6.30 * angle_deg / 360)
        mat = matrix_mul_matrix(mat_trans, mat_rot)
        self.apply_matrix(mat)
        old_origin = self.origin
        self._calculate_origin()
        self.move_to(old_origin)

    def apply_matrix(self, matrix):
        for idx, vertex in enumerate(self.vertices):
            self.vertices[idx] = vec_mul_matrix(vertex, matrix)

    def render(self, color, color_back=None, need_edge=False):
        for polygon in self.polygons:
            _color = copy.deepcopy(color)
            if self._check_polygon(polygon):
                if color_back is None:
                    continue
                else:
                    _color = copy.deepcopy(color_back)

            points_array = []
            changed_color = copy.deepcopy(_color)
            for vert_idx in polygon:
                vertex = self.vertices[vert_idx]
                points_array.append(sd.get_point(x=int(vertex[0]), y=int(vertex[1])))
                if vertex[2] != 0 and changed_color == _color:
                    changed_color = [int(col * .9) for col in _color]

            sd.polygon(point_list=points_array, width=0, color=changed_color)
            if need_edge:
                sd.polygon(point_list=points_array, width=1, color=sd.COLOR_BLACK)

    def _check_polygon(self, polygon):
        p1 = self.vertices[polygon[0]]
        p2 = self.vertices[polygon[1]]
        p3 = self.vertices[polygon[2]]
        dx1 = p2[0] - p1[0]
        dx2 = p3[0] - p2[0]
        dy1 = p2[1] - p1[1]
        dy2 = p3[1] - p2[1]
        r = dx1 * dy2 - dx2 * dy1
        if r >= 0:
            return True
        else:
            return False
