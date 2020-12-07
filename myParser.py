import numpy as np
import sys



class Edge:
    def __init__(self, vertices, distance):
        self.vertices = vertices
        self.distance = distance

    def setNewDistance(self, newDistance):
        self.newDistance = newDistance

    def __str__(self) -> str:
        return 'Edge(vertices=' + self.vertices + ', distance=' + self.distance + ')'

    def __repr__(self):
        return "Vertices: {}, distance: {}, new distance: {}".format(self.vertices, self.distance, self.newDistance)


def matrixDistanceToEdgesList(matrix) -> list:
    maxint = sys.maxsize
    edges = []
    for x, row in enumerate(matrix):
        for y in range(x, row.size):
            if matrix[x][y] != 0 and matrix[x][y] != maxint:
                edge = Edge((x, y), matrix[x][y])
                edges.append(edge)
    return edges


def edgesListToMatrixDistance(newEdges):
    np.set_printoptions(suppress=True, precision=3)
    maxint = sys.maxsize
    matrix = np.full((5, 5), maxint, dtype=np.float)
    for edge in newEdges:
        matrix[edge.vertices[0]][edge.vertices[1]] = edge.newDistance

    # đưa đường chéo về 0 vì không có khoảng cách từ cạnh x đến x
    for i in range(5):
        matrix[i][i] = 0.0
    return matrix

def edgeToJamFactorArrayTojams(edges, edgeToJamFactors):
    subKernel = np.dtype([("membership_function", np.float), ("non_membership_function", np.float)])
    kernelList = []
    for i in range(len(edgeToJamFactors.dtype)):
        jamLabel = "jam area " + str(i + 1)
        kernelList.append((jamLabel, subKernel))
    kernel = np.dtype(kernelList)
    jams = np.zeros((5, 5), dtype=np.dtype(kernel))
    for edgeIndex,edge in enumerate(edges):
        for i in range(len(edgeToJamFactors.dtype)):
            jams[edge.vertices[0]][edge.vertices[1]][i] = edgeToJamFactors[edgeIndex][i]

    return jams


if __name__ == '__main__':
    pass
