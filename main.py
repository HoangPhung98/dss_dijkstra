import sys

import numpy as np

import core
import visualization
import myParser

if __name__ == '__main__':
    # data
    maxint = sys.maxsize
    matrix = np.array([[0, 2, maxint, 1, maxint],
                       [2, 0, 5, 2, 2],
                       [maxint, 5, 0, maxint, 5],
                       [1, 2, maxint, 0, 1],
                       [maxint, 2, 5, 1, 0]])

    edges = myParser.matrixDistanceToEdgesList(matrix)
    newEdges, edgeToJamFactors = core.calculateNewDistanceCost(edges,)
    jams = myParser.edgeToJamFactorArrayTojams(newEdges, edgeToJamFactors)
    newMatrix = myParser.edgesListToMatrixDistance(newEdges)
    newMatrix = np.round(newMatrix, 3)
    print("jams")
    print(repr(jams))
    print(newEdges)
    print("new matrix")
    print(repr(newMatrix))
    visualization.draw(newMatrix, jams, matrix)