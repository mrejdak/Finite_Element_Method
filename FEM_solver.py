import numpy as np


RHO = 1
NODES, WEIGHTS = np.polynomial.legendre.leggauss(2)

def FEM(N):

    H = 3 / N

    def eps_r(x):
        if 0 <= x <= 1: return 10
        elif 1 < x <= 2: return 5
        return 1


    def x_n(n):
        x = H * n
        return x


    def e_n(x, i):
        if x < x_n(i-1) or x > x_n(i+1):
            return 0.0
        elif x < i * H:
            return (x - x_n(i-1)) / H
        else:
            return (x_n(i+1) - x) / H



    def e_prim(i, x):
        if x_n(i - 1) > x or x > x_n(i + 1):
            return 0.0
        return 1/H if x < x_n(i) else -1/H


    def calculate_B(i, j):
        if abs(i-j) > 1:
            return e_n(0, i) * e_n(0, j)
        a = max((i - 1) * H, (j - 1) * H, 0)
        b = min((i + 1) * H, (j + 1) * H, 3)

        delta = (b-a)/2
        integral_res = 0

        for k in range(len(NODES)):
            integral_res += delta * WEIGHTS[k] * e_prim(i, NODES[k] * delta + (a + b) / 2) * e_prim(j, NODES[k] * delta + (a + b) / 2)

        return e_n(0, i) * e_n(0, j) - integral_res


    def calculate_L(j):
        a = max((j - 1) * H, 0)
        b = min((j + 1) * H, 3)

        delta = (b-a)/2
        integral_res = 0

        for k in range(len(NODES)):
            integral_res += delta * WEIGHTS[k] * (-RHO) * e_n(NODES[k] * delta + (a + b) / 2, j) / eps_r(NODES[k] * delta + (a + b) / 2)
        return 3*e_n(0, j) + integral_res

    def fill_matrix(n):
        matrix_B = [[None for _ in range(n)] for _ in range(n)]
        matrix_L = [None for _ in range(n)]
        for j in range(n):
            for i in range(n):
                matrix_B[j][i] = calculate_B(i, j)
            matrix_L[j] = calculate_L(j)

        return matrix_B, matrix_L


    B, L = fill_matrix(N)
    w = np.linalg.solve(B, L)
    w = np.append(w, 0)
    phi = w + 2
    x = [x_n(i) for i in range(N + 1)]

    return x, phi
