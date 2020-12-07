import numpy as np


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def init_distance():
    distance = np.random.randint(0, 100, (5, 5))
    return distance


def init_costFactor(numberOfJamArea=3, numberOfFactorRelate=3):
    dtKernel = np.dtype([('member', np.float), ('non_member', np.float)])
    costFactor = np.zeros((numberOfJamArea, numberOfFactorRelate), dtype=dtKernel)
    costFactor[0, 0] = (0.4, 0)
    costFactor[0, 1] = (0.6, 0.3)
    costFactor[0, 2] = (0.1, 0.7)
    costFactor[1, 0] = (0.3, 0.5)
    costFactor[1, 1] = (0.2, 0.6)
    costFactor[1, 2] = (0.6, 0.1)
    costFactor[2, 0] = (0.1, 0.7)
    costFactor[2, 1] = (0, 0.9)
    costFactor[2, 2] = (0.2, 0.7)
    return costFactor.T


def calC(costFactor, U, V):
    u = 0
    v = 0


def getKernel(numberOfSubKernel, cLabeltemp, subKernel):
    cList = []
    for i in range(0, numberOfSubKernel):
        cLabel = cLabeltemp + str(i + 1)
        cList.append((cLabel, subKernel))
    kernel = np.dtype(cList)
    return kernel


def getCostOfEdgesPerFactor(ifss, costCoefficient, n):
    """
    Tính chi phi của các độ phụ thuộc, không phụ thuộc giữa cạnh và các nhân tố
    :return:
    """
    dtKernel = np.dtype([('member', np.float), ('non_member', np.float)])
    costKernel = getKernel(len(ifss), 'c', dtKernel)

    cost = np.zeros((n, n), dtype=costKernel)
    for i, coefficient in enumerate(costCoefficient):
        numberofCoefficient = len(coefficient)
        for vertex in range(0, n):
            for edge in range(vertex + 1, n):
                u = []
                v = []
                for j, ifs in enumerate(ifss):
                    u.append(min(ifs[vertex][edge][0], coefficient[j][0]))
                    v.append(max(ifs[vertex][edge][1], coefficient[j][1]))
                    # print("ifs:", end='')
                    # print(ifs[vertex][edge])
                    # print("cost:", end='')
                    # print(coefficient[j])
                maxU = max(u)
                minV = min(v)
                cost[vertex][edge][i] = (maxU, minV)
    return cost


def initIFS(jam, n):
    """
    trả về ma trận nxn chứa độ phụ thuộc và độ không phụ thuộc
    IFS[i][j] =(u, v)
    """
    dtKernel = np.dtype([('member', np.float), ('non_member', np.float)])
    ifs = np.zeros((n, n), dtype=dtKernel)
    for i in range(0, n):
        for j in range(i + 1, n):
            u, v = 0, 0
            if i in jam and j in jam:
                u = round(np.random.uniform(0.1, 1), 1)
                v = round(np.random.uniform(0.0, 1 - u), 1)
            else:
                v = 1.0
            ifs[i][j] = (u, v)
    return ifs
    pass


# Press the green button in the gutter to run the script.
def calculateJ(jam):
    kernel = getKernel(3, "J",np.float)
    res = np.zeros(1,dtype= kernel)
    for idx, x in enumerate(jam):
        j = x[0] - x[1] * (1 - (x[0] + x[1]))
        res[0][idx] = j
    return res
    pass


def calculateJamCost(jamCost, cost):
    for idx, jam in np.ndenumerate(cost):
        temp = calculateJ(jam)
        jamCost[idx] = temp

    return jamCost



if __name__ == '__main__':
    numOfVertices = 5
    numOfEdges = numOfVertices ** 2
    numOfJam = 3

    dist = init_distance()
    costFactor = init_costFactor(3, 3)

    Jam1 = [0, 1, 2, 4]
    Jam2 = [1, 3]
    ifs1 = np.array([[(0., 0.), (0.8, 0.15), (0.5, 0.2), (0., 1.), (0.6, 0.2)],
                     [(0., 0.), (0., 0.), (0.7, 0.2), (0., 1.), (0.7, 0.3)],
                     [(0., 0.), (0., 0.), (0., 0.), (0., 1.), (0.4, 0.2)],
                     [(0., 0.), (0., 0.), (0., 0.), (0., 0.), (0., 1.)],
                     [(0., 0.), (0., 0.), (0., 0.), (0., 0.), (0., 0.)]],
                    dtype=[('member', '<f8'), ('non_member', '<f8')])
    ifs2 = np.array([[(0., 0.), (0.4, 0.35), (0., 1.), (0., 1.), (0., 1.)],
                     [(0., 0.), (0., 0.), (0., 1.), (0.8, 0.), (0., 1.)],
                     [(0., 0.), (0., 0.), (0., 0.), (0., 1.), (0., 1.)],
                     [(0., 0.), (0., 0.), (0., 0.), (0., 0.), (0., 1.)],
                     [(0., 0.), (0., 0.), (0., 0.), (0., 0.), (0., 0.)]],
                    dtype=[('member', '<f8'), ('non_member', '<f8')])
    ifs3 = np.array([[(0., 0.), (0., 1.), (0., 1.), (0., 1.), (0., 1.)],
                     [(0., 0.), (0., 0.), (0., 1.), (0.8, 0.), (0., 1.)],
                     [(0., 0.), (0., 0.), (0., 0.), (0., 1.), (0., 1.)],
                     [(0., 0.), (0., 0.), (0., 0.), (0., 0.), (0., 1.)],
                     [(0., 0.), (0., 0.), (0., 0.), (0., 0.), (0., 0.)]],
                    dtype=[('member', '<f8'), ('non_member', '<f8')])
    ifss = (ifs1, ifs2, ifs3)
    cost = getCostOfEdgesPerFactor(ifss, costFactor, numOfVertices)
    print("Cost:")
    print(cost)
    kernel = getKernel(numOfJam, "Jam", np.float)
    jamCost = np.zeros((numOfVertices, numOfVertices), dtype=kernel)

    print("jamCost:")
    print(jamCost)
    jamCost = calculateJamCost(jamCost, cost)
    print("jamCost after calculated:")
    print(jamCost)
