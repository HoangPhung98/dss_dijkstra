import numpy as np

import dataGenerator
from myParser import Edge


def getIFRFromEdgesToJamFactors(numberOfEdge=7, numberOfJamFactor=4):
    jamFactorList = []
    subKernel = np.dtype([("membership_function", np.float), ("non_membership_function", np.float)])
    # jamFactorList.append(("vertices", np.int))
    for i in range(0, numberOfJamFactor):
        jamLabel = "Jam area " + str(i + 1)
        jamFactorList.append((jamLabel, subKernel))
    edgeKernel = np.dtype(jamFactorList, (4,))
    IFREdgesToJamFactors = np.zeros(numberOfEdge, dtype=edgeKernel)
    IFREdgesToJamFactors = dataGenerator.getVirtualEdgesToJamFactors(edgeKernel, numberOfEdge, numberOfJamFactor)
    return IFREdgesToJamFactors


def geJamFactorstoCostFactors(numberOfJamArea=4, numberOfCostFactor=4):
    dtKernel = np.dtype([("membership_function", np.float), ("non_membership_function", np.float)])
    jamCosts = np.zeros((numberOfJamArea, numberOfCostFactor), dtype=dtKernel)
    return jamCosts


def initJamFactorstoCostFactorsData(jamCosts):
    """
    Gía trị ảo sinh ra để mô phỏng
    :param jamCosts:
    :return:
    """
    jamCosts = np.array([[(0.4, 0), (0.7, 0), (0.3, 0.3), (0.1, 0.7)],
                         [(0.3, 0.5), (0.2, 0.6), (0.6, 0.1), (0.2, 0.4)],
                         [(0.1, 0.7), (0, 0.9), (0.2, 0.7), (0.8, 0)],
                         [(0.4, 0.3), (0.4, 0.3), (0.2, 0.6), (0.2, 0.7)]],
                        [("membership_function", np.float), ("non_membership_function", np.float)])
    return jamCosts


def getEdgesToCostFactorsMatrix(numberOfEdges=6, numberOfCostFactor=4):
    costFactorList = []
    costFactorKernel = np.dtype([("membership_function", np.float), ("non_membership_function", np.float)])
    for i in range(0, numberOfCostFactor):
        costFactorLabel = "Cost factor " + str(i + 1)
        costFactorList.append((costFactorLabel, costFactorKernel))
    # verticesKernel = [("vertices", np.dtype([("first_vertex", np.int), ("second_vertex", np.int)]))]
    kernel = np.dtype(costFactorList)
    matrix = np.zeros(numberOfEdges, dtype=kernel)
    return matrix


def calculateEdgesToCostFactors(EdgeToJamFactor, jamCosts):
    result = getEdgesToCostFactorsMatrix(numberOfEdges=EdgeToJamFactor.shape, numberOfCostFactor=4)

    for costFactorIndex, costFactor in enumerate(jamCosts.T):

        for edgeIndex, edge in enumerate(EdgeToJamFactor):

            u = []
            v = []
            for jamIndex, jamFactor in enumerate(edge):
                u.append(min(jamFactor[0], jamCosts[jamIndex, costFactorIndex][0]))
                v.append(max(jamFactor[1], jamCosts[jamIndex, costFactorIndex][1]))
            maxU = max(u)
            minV = min(v)
            result[edgeIndex][costFactorIndex] = (maxU, minV)
    return result


def calculateJam(edge):
    jams = []
    for costFactor in edge:
        jamCost = costFactor[0] - costFactor[1] * (1 - (costFactor[0] + costFactor[1]))
        jams.append(np.round(jamCost, 3))
    return jams
    pass


def getJamCost(edgesToCostFactor, edges: Edge):
    finalDistance = []
    jamMatrix = []
    for edgeIndex, edge in enumerate(edgesToCostFactor):
        jams = calculateJam(edge)
        jamMatrix.append(jams)
        temp = 0
        for jam in jams:
            temp = temp + edges[edgeIndex].distance * jam
        finalDistance.append(np.round(temp, 3))
    return jamMatrix, finalDistance
    pass


def getDistance(numberOfEdges):
    """
    Hàm chỉ để sinh dữ liệu ảo
    :param numberOfEdges:
    :return:
    """
    dist = [3, 5, 9, 7, 2, 8]
    return dist


def calculateNewDistanceCost(edges: Edge, ):
    """
    Import module core thì chỉ chạy hàm này
    :return:
    """
    edgeToJamFactors = getIFRFromEdgesToJamFactors(len(edges))
    jamFactorsToCostFactors = initJamFactorstoCostFactorsData(geJamFactorstoCostFactors(4, 4))
    edgesToCostFactor = calculateEdgesToCostFactors(edgeToJamFactors, jamFactorsToCostFactors)

    (jamCostofEdges, finalDistance) = getJamCost(edgesToCostFactor, edges)
    for idx,edge in enumerate(edges):
        edge.setNewDistance(finalDistance[idx])
    return edges, edgeToJamFactors
    pass


if __name__ == '__main__':
    # Determination of edges that have jam factors.
    pass
