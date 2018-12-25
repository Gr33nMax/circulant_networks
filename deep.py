import csv
from os import listdir
import re
import numpy as np


def find_the_best_way(
        N: int,
        N1: int,
        N2: int,
        L: np.ndarray,
        S: np.ndarray):
    """
    Поиск наилучшего пути из N1 в N2 среди всех путей
    (абсолютная сумма коэффициентов должна быть минимальной, а сумма
    коэффициентов должна быть равна L1 или L2 при движении вправо или влево
    соответственно)
    """

    L_right_sums    = np.dot(L[0], S)
    L_left_sums     = np.dot(L[1], -S)
    L_right_r_sums  = np.dot(L[2], S)
    L_left_l_sums   = np.dot(L[3], -S)

    res_sum_right   = 10e+5
    res_sum_left    = 10e+5
    res_sum_right_r = 10e+5
    res_sum_left_l  = 10e+5

    res_right       = 0
    res_left        = 0
    res_right_r     = 0
    res_left_l      = 0

    for idx_right, t_right in enumerate(L[0]):
        abs_sum_right = np.sum(np.abs(t_right))
        if (N1 + L_right_sums[idx_right]) % N == N2 and abs_sum_right < \
                res_sum_right:
            res_sum_right = abs_sum_right
            res_right = t_right

    for idx_left, t_left in enumerate(L[1]):
        abs_sum_left = np.sum(np.abs(t_left))
        if (N1 + N - L_left_sums[idx_left]) % N == N2 \
                and abs_sum_left < res_sum_left:
            res_sum_left = abs_sum_left
            res_left = t_left

    for idx_right_r, t_right_r in enumerate(L[2]):
        abs_sum_right_r = np.sum(np.abs(t_right_r))
        if (N1 + L_right_r_sums[idx_right_r]) % N == N2 and abs_sum_right_r < \
                res_sum_right_r:
            res_sum_right_r = abs_sum_right_r
            res_right_r = t_right_r

    for idx_left_l, t_left_l in enumerate(L[3]):
        abs_sum_left_l = np.sum(np.abs(t_left_l))
        if (N1 + L_left_l_sums[idx_left_l]) % N == N2 and abs_sum_left_l < \
                res_sum_left_l:
            res_sum_left_l = abs_sum_left_l
            res_left_l = t_left_l

    res_pairs = (
        (res_right, res_sum_right),
        (res_right_r, res_sum_right_r),
        (res_left, res_sum_left),
        (res_left_l, res_sum_left_l)
    )

    res = min(res_pairs, key=lambda r: r[1])
    return res[0]


def general(N2, N, N1, S1, S2, S3):
    """ Основной алгоритм, расчет всех маршрутов """
    L1 = N2 - N1
    L2 = N - L1
    L3 = L1 + N
    L4 = L2 + N
    # L = a3*S3 + a2*S2 + a1*S1
    a3 = np.array(
        [
            [
                0,                      # 0
                L1 // S3,               # 1
                L1 // S3 + 1,           # 2
                L1 // (S1 + S2 + S3),   # 3
                L1 // (S1 - S2 + S3),   # 4
                L1 // (-S1 + S2 + S3),  # 5
                L1 // (S1 + S2),        # 6
                L1 // (S1 + S3),        # 7
                L1 // (S2 + S3),        # 8
                L1 // (S3 - S2),        # 9
                L1 // (S3 - S1),        # 10
                L1 // (S2 - S1),        # 11
            ],
            [
                0,                      # 0
                L2 // S3,               # 1
                L2 // S3 + 1,           # 2
                L2 // (S1 + S2 + S3),   # 3
                L2 // (S1 - S2 + S3),   # 4
                L2 // (-S1 + S2 + S3),  # 5
                L2 // (S1 + S2),        # 6
                L2 // (S1 + S3),        # 7
                L2 // (S2 + S3),        # 8
                L2 // (S3 - S2),        # 9
                L2 // (S3 - S1),        # 10
                L2 // (S2 - S1),        # 11
            ],
            [
                0,                      # 0
                L3 // S3,               # 1
                L3 // S3 + 1,           # 2
                L3 // (S1 + S2 + S3),   # 3
                L3 // (S1 - S2 + S3),   # 4
                L3 // (-S1 + S2 + S3),  # 5
                L3 // (S1 + S2),        # 6
                L3 // (S1 + S3),        # 7
                L3 // (S2 + S3),        # 8
                L3 // (S3 - S2),        # 9
                L3 // (S3 - S1),        # 10
                L3 // (S2 - S1),        # 11
            ],
            [
                0,                      # 0
                L4 // S3,               # 1
                L4 // S3 + 1,           # 2
                L4 // (S1 + S2 + S3),   # 3
                L4 // (S1 - S2 + S3),   # 4
                L4 // (-S1 + S2 + S3),  # 5
                L4 // (S1 + S2),        # 6
                L4 // (S1 + S3),        # 7
                L4 // (S2 + S3),        # 8
                L4 // (S3 - S2),        # 9
                L4 // (S3 - S1),        # 10
                L4 // (S2 - S1),        # 11
            ]
        ]
    )
    a2 = np.array(
        [
            [
                0,                          # 0
                (L1 % S3) // S2,            # 1
                (L1 % S3) // S2 + 1,        # 2
                (S3 - L1 % S3) // S2,       # 3
                (S3 - L1 % S3) // S2 + 1,   # 4
                L1 // S2,                   # 5
                L1 // S2 + 1,               # 6
                S3 // S2 + 1,               # 7
                L1 // S2 - S3 // S2,        # 8
                L1 // S2 + 1 + S3 // S2,    # 9
            ],
            [
                0,                          # 0
                (L2 % S3) // S2,            # 1
                (L2 % S3) // S2 + 1,        # 2
                (S3 - L2 % S3) // S2,       # 3
                (S3 - L2 % S3) // S2 + 1,   # 4
                L2 // S2,                   # 5
                L2 // S2 + 1,               # 6
                S3 // S2 + 1,               # 7
                L2 // S2 - S3 // S2,        # 8
                L2 // S2 + 1 + S3 // S2,    # 9
            ],
            [
                0,                          # 0
                (L3 % S3) // S2,            # 1
                (L3 % S3) // S2 + 1,        # 2
                (S3 - L3 % S3) // S2,       # 3
                (S3 - L3 % S3) // S2 + 1,   # 4
                L3 // S2,                   # 5
                L3 // S2 + 1,               # 6
                S3 // S2 + 1,               # 7
                L3 // S2 - S3 // S2,        # 8
                L3 // S2 + 1 + S3 // S2,    # 9
            ],
            [
                0,                          # 0
                (L4 % S3) // S2,            # 1
                (L4 % S3) // S2 + 1,        # 2
                (S3 - L4 % S3) // S2,       # 3
                (S3 - L4 % S3) // S2 + 1,   # 4
                L4 // S2,                   # 5
                L4 // S2 + 1,               # 6
                S3 // S2 + 1,               # 7
                L4 // S2 - S3 // S2,        # 8
                L4 // S2 + 1 + S3 // S2,    # 9
            ]
        ]
    )
    a1 = np.array(
        [
            [
                0,                                  # 0
                ((L1 % S3) % S2) // S1,             # 1
                (S2 - (L1 % S3) % S2) // S1,        # 2
                ((S3 - L1 % S3) % S2) // S1,        # 3
                (S2 - (S3 - L1 % S3) % S2) // S1,   # 4
                (L1 % S3) // S1,                    # 5
                (S3 - L1 % S3) // S1,               # 6
                (L1 % S2) // S1,                    # 7
                (S2 - L1 % S2) // S1,               # 8
                L1 // S1,                           # 9
                S3 // S1 + 1,                       # 10
                S2 // S1 + 1,                       # 11
                L1 // S1 - S2 // S1,                # 12
                L1 // S1 - S3 // S1,                # 13
                L1 // S1 + 1 + S2 // S1,            # 14
                L1 // S1 + 1 + S3 // S1,            # 15
            ],
            [
                0,                                  # 0
                ((L2 % S3) % S2) // S1,             # 1
                (S2 - (L2 % S3) % S2) // S1,        # 2
                ((S3 - L2 % S3) % S2) // S1,        # 3
                (S2 - (S3 - L2 % S3) % S2) // S1,   # 4
                (L2 % S3) // S1,                    # 5
                (S3 - L2 % S3) // S1,               # 6
                (L2 % S2) // S1,                    # 7
                (S2 - L2 % S2) // S1,               # 8
                L2 // S1,                           # 9
                S3 // S1 + 1,                       # 10
                S2 // S1 + 1,                       # 11
                L2 // S1 - S2 // S1,                # 12
                L2 // S1 - S3 // S1,                # 13
                L2 // S1 + 1 + S2 // S1,  # 14
                L2 // S1 + 1 + S3 // S1,  # 15
            ],
            [
                0,                                  # 0
                ((L3 % S3) % S2) // S1,             # 1
                (S2 - (L3 % S3) % S2) // S1,        # 2
                ((S3 - L3 % S3) % S2) // S1,        # 3
                (S2 - (S3 - L3 % S3) % S2) // S1,   # 4
                (L3 % S3) // S1,                    # 5
                (S3 - L3 % S3) // S1,               # 6
                (L3 % S2) // S1,                    # 7
                (S2 - L3 % S2) // S1,               # 8
                L3 // S1,                           # 9
                S3 // S1 + 1,                       # 10
                S2 // S1 + 1,                       # 11
                L3 // S1 - S2 // S1,                # 12
                L3 // S1 - S3 // S1,                # 13
                L3 // S1 + 1 + S2 // S1,            # 14
                L3 // S1 + 1 + S3 // S1,            # 15
            ],
            [
                0,  # 0
                ((L4 % S3) % S2) // S1,             # 1
                (S2 - (L4 % S3) % S2) // S1,        # 2
                ((S3 - L4 % S3) % S2) // S1,        # 3
                (S2 - (S3 - L4 % S3) % S2) // S1,   # 4
                (L4 % S3) // S1,                    # 5
                (S3 - L4 % S3) // S1,               # 6
                (L4 % S2) // S1,                    # 7
                (S2 - L4 % S2) // S1,               # 8
                L4 // S1,                           # 9
                S3 // S1 + 1,                       # 10
                S2 // S1 + 1,                       # 11
                L4 // S1 - S2 // S1,                # 12
                L4 // S1 - S3 // S1,                # 13
                L4 // S1 + 1 + S2 // S1,            # 14
                L4 // S1 + 1 + S3 // S1,            # 15
            ]
        ]
    )
    L = np.array(
        [
            [
                # движение в правую сторону
                # проход по S1
                [a3[0][0], a2[0][0], a1[0][9]],         # 0
                # проход по S2
                [a3[0][0], a2[0][5], a1[0][0]],         # 1
                # проход по S3
                [a3[0][1], a2[0][0], a1[0][0]],         # 2

                # проход по S2 не доходя, по S1 доходя
                [a3[0][0], a2[0][5], a1[0][7]],         # 3
                # проход по S2 переходя, по S1 возвращаясь
                [a3[0][0], a2[0][6], -a1[0][8]],        # 4
                # проход по S3 не доходя, по S1 доходя
                [a3[0][1], a2[0][0], a1[0][5]],         # 5
                # проход по S3 переходя, по S1 возвращаясь
                [a3[0][2], a2[0][0], -a1[0][6]],        # 6
                # проход по S3 не доходя, по S2 доходя
                [a3[0][1], a2[0][1], a1[0][0]],         # 7
                # проход по S3 переходя, по S2 возвращаясь
                [a3[0][2], -a2[0][3], a1[0][0]],        # 8

                # проход по S3 не доходя, по S2 не доходя, по S1 доходя
                [a3[0][1], a2[0][1], a1[0][1]],         # 9
                # проход по S3 не доходя, по S2 переходя, по S1 возвращаясь
                [a3[0][1], a2[0][2], -a1[0][2]],        # 10
                # проход по S3 переходя, по S2 не доходя, по S1 доходя
                [a3[0][2], -a2[0][3], -a1[0][3]],       # 11
                # проход по S3 переходя, по S2 переходя, по S1 возвращаясь
                [a3[0][2], -a2[0][4], a1[0][4]],        # 12

                # проход по S2, переходя S3
                [-1, a2[0][7], a1[0][0]],               # 13
                # проход по S1, переходя S3
                [-1, a2[0][0], a1[0][10]],              # 14
                # проход по S1, переходя S2
                [a3[0][0], -1, a1[0][11]],              # 15

                # проход по S2 до тех пор, пока расстояние до конечного узла
                # не будет меньше, чем шаг по S3
                [1, a2[0][8], a1[0][0]],                # 16
                # проход по S1 до тех пор, пока расстояние до конечного узла
                # не будет меньше, чем шаг по S2
                [a3[0][0], 1, a1[0][12]],               # 17
                # проход по S1 до тех пор, пока расстояние до конечного узла
                # не будет меньше, чем шаг по S3
                [1, a2[0][0], a1[0][13]],               # 18

                # проход по S2 до тех пор, пока расстояние до конечного узла
                #  не будет меньше, чем шаг по S3 в обратную сторону
                [-1, a2[0][9], a1[0][0]],               # 19
                # проход по S1 до тех пор, пока расстояние до конечного узла
                #  не будет меньше, чем шаг по S2 в обратную сторону
                [a3[0][0], -1, a1[0][14]],              # 20
                # проход по S1 до тех пор, пока расстояние до конечного узла
                #  не будет меньше, чем шаг по S3 в обратную сторону
                [-1, a2[0][0], a1[0][15]],              # 21

                # проход по сумме S1 + S2 + S3
                [a3[0][3], a3[0][3], a3[0][3]],         # 22
                # проход по сумме S1 - S2 + S3
                [a3[0][4], -a3[0][4], a3[0][4]],        # 23
                # проход по сумме -S1 + S2 + S3
                [-a3[0][5], a3[0][5], a3[0][5]],        # 25

                # проход по сумме S1 + S2
                [a3[0][0], a3[0][6], a3[0][6]],         # 26
                # проход по сумме S1 + S3
                [a3[0][7], a3[0][0], a3[0][7]],         # 27
                # проход по сумме S2 + S3
                [a3[0][8], a3[0][8], a3[0][0]],         # 28
                # проход по разности S3 - S2
                [a3[0][9], -a3[0][9], a3[0][0]],        # 29
                # проход по разности S3 - S1
                [a3[0][10], a3[0][0], -a3[0][10]],      # 30
                # проход по разности S2 - S1
                [a3[0][0], a3[0][11], -a3[0][11]],      # 31

                # 9, 10, 11, 12 только в другую сторону
                # проход по S3 не доходя, по S2 не доходя, по S1 доходя
                [-a3[0][1], -a2[0][1], -a1[0][1]],      # 32
                # проход по S3 не доходя, по S2 переходя, по S1 возвращаясь
                [-a3[0][1], -a2[0][2], a1[0][2]],       # 33
                # проход по S3 переходя, по S2 не доходя, по S1 доходя
                [-a3[0][2], a2[0][3], a1[0][3]],        # 34
                # проход по S3 переходя, по S2 переходя, по S1 возвращаясь
                [-a3[0][2], a2[0][4], -a1[0][4]],       # 35

                # оставшиеся случаи
                # S1*k + S2 + S3
                [(L1 - S2 - S3) // S1, 1, 1],  # 36
                # S1*k + S2 - S3
                [(L1 - S2 + S3) // S1, 1, -1],  # 37
                # S1*k - S2 + S3
                [(L1 + S2 - S3) // S1, -1, 1],  # 38
                # S1*k - S2 - S3
                [(L1 + S2 + S3) // S1, -1, -1],  # 39
                # -S1*k + S2 + S3
                [-(L1 - S2 - S3) // S1, 1, 1],  # 40
                # -S1*k + S2 - S3
                [-(L1 - S2 + S3) // S1, 1, -1],  # 41
                # -S1*k - S2 + S3
                [-(L1 + S2 - S3) // S1, -1, 1],  # 42
                # -S1*k - S2 - S3
                [(L1 + S2 + S3) // S1, -1, -1],  # 43

                # S1 + S2*k + S3
                [1, (L1 - S1 - S3) // S2, 1],  # 44
                # S1 + S2*k - S3
                [1, (L1 - S1 + S3) // S2, -1],  # 45
                # S1 - S2*k + S3
                [1, -(L1 - S1 - S3) // S2, 1],  # 46
                # S1 - S2*k - S3
                [1, -(L1 - S1 + S3) // S2, -1],  # 47
                # -S1 + S2*k + S3
                [-1, (L1 + S1 - S3) // S2, 1],  # 48
                # -S1 + S2*k - S3
                [-1, (L1 + S1 + S3) // S2, -1],  # 49
                # -S1 - S2*k + S3
                [-1, -(L1 + S1 - S3) // S2, 1],  # 50
                # -S1 - S2*k - S3
                [-1, (L1 + S1 + S3) // S2, -1],  # 51

                # S1 + S2 + S3*k
                [1, 1, (L1 - S1 - S2) // S3],  # 52
                # S1 + S2 - S3*k
                [1, 1, -(L1 - S1 - S2) // S3],  # 53
                # S1 - S2 + S3*k
                [1, -1, (L1 - S1 + S2) // S3],  # 54
                # S1 - S2 - S3*k
                [1, -1, -(L1 - S1 + S2) // S3],  # 55
                # -S1 + S2 + S3*k
                [-1, 1, (L1 + S1 - S2) // S3],  # 56
                # -S1 + S2 - S3*k
                [-1, 1, -(L1 + S1 - S2) // S3],  # 57
                # -S1 - S2 + S3*k
                [-1, -1, (L1 + S1 + S2) // S3],  # 58
                # -S1 - S2 - S3*k
                [-1, -1, -(L1 + S1 + S2) // S3],  # 59
            ],
            [
                # движение в левую сторону
                # проход по S1
                [-a3[1][0], -a2[1][0], -a1[1][9]],      # 0
                # проход по S2
                [-a3[1][0], -a2[1][5], -a1[1][0]],      # 1
                # проход по S3
                [-a3[1][1], -a2[1][0], -a1[1][0]],      # 2

                # проход по S2 не доходя, по S1 доходя
                [-a3[1][0], -a2[1][5], -a1[1][7]],      # 3
                # проход по S2 переходя, по S1 возвращаясь
                [-a3[1][0], -a2[1][6], a1[1][8]],       # 4
                # проход по S3 не доходя, по S1 доходя
                [-a3[1][1], -a2[1][0], -a1[1][5]],      # 5
                # проход по S3 переходя, по S1 возвращаясь
                [-a3[1][2], -a2[1][0], a1[1][6]],       # 6
                # проход по S3 не доходя, по S2 доходя
                [-a3[1][1], -a2[1][1], -a1[1][0]],      # 7
                # проход по S3 переходя, по S2 возвращаясь
                [-a3[1][2], a2[1][3], -a1[1][0]],       # 8

                # проход по S3 не доходя, по S2 не доходя, по S1 доходя
                [-a3[1][1], -a2[1][1], -a1[1][1]],      # 9
                # проход по S3 не доходя, по S2 переходя, по S1 возвращаясь
                [-a3[1][1], -a2[1][2], a1[1][2]],       # 10
                # проход по S3 переходя, по S2 не доходя, по S1 доходя
                [-a3[1][2], a2[1][3], a1[1][3]],        # 11
                # проход по S3 переходя, по S2 переходя, по S1 возвращаясь
                [-a3[1][2], a2[1][4], -a1[1][4]],       # 12

                # проход по S2, переходя S3
                [1, -a2[1][7], -a1[1][0]],              # 13
                # проход по S1, переходя S3
                [1, -a2[1][0], -a1[1][10]],             # 14
                # проход по S1, переходя S2
                [-a3[1][0], 1, -a1[1][11]],             # 15

                # проход по S2 до тех пор, пока расстояние до конечного узла
                # не будет меньше, чем шаг по S3
                [-1, -a2[1][8], -a1[1][0]],             # 16
                # проход по S1 до тех пор, пока расстояние до конечного узла
                # не будет меньше, чем шаг по S2
                [-a3[1][0], -1, -a1[1][12]],            # 17
                # проход по S1 до тех пор, пока расстояние до конечного узла
                # не будет меньше, чем шаг по S3
                [-1, -a2[1][0], -a1[1][13]],            # 18

                # проход по S2 до тех пор, пока расстояние до конечного узла
                #  не будет меньше, чем шаг по S3 в обратную сторону
                [1, -a2[1][9], -a1[1][0]],              # 19
                # проход по S1 до тех пор, пока расстояние до конечного узла
                #  не будет меньше, чем шаг по S2 в обратную сторону
                [-a3[1][0], 1, -a1[1][14]],             # 20
                # проход по S1 до тех пор, пока расстояние до конечного узла
                #  не будет меньше, чем шаг по S3 в обратную сторону
                [1, -a2[1][0], -a1[1][15]],             # 21

                # проход по сумме S1 + S2 + S3
                [-a3[1][3], -a3[1][3], -a3[1][3]],      # 22
                # проход по сумме S1 - S2 + S3
                [-a3[1][4], a3[1][4], -a3[1][4]],       # 23
                # проход по сумме -S1 + S2 + S3
                [a3[1][5], -a3[1][5], -a3[1][5]],       # 25

                # проход по сумме S1 + S2
                [-a3[1][0], -a3[1][6], -a3[1][6]],      # 26
                # проход по сумме S1 + S3
                [-a3[1][7], -a3[1][0], -a3[1][7]],      # 27
                # проход по сумме S2 + S3
                [-a3[1][8], -a3[1][8], -a3[1][0]],      # 28
                # проход по разности S3 - S2
                [-a3[1][9], a3[1][9], -a3[1][0]],       # 29
                # проход по разности S3 - S1
                [-a3[1][10], -a3[1][0], a3[1][10]],     # 30
                # проход по разности S2 - S1
                [-a3[1][0], -a3[1][11], a3[1][11]],     # 31

                # 9, 10, 11, 12 только в другую сторону
                # проход по S3 не доходя, по S2 не доходя, по S1 доходя
                [a3[0][1], a2[0][1], a1[0][1]],         # 32
                # проход по S3 не доходя, по S2 переходя, по S1 возвращаясь
                [a3[0][1], a2[0][2], -a1[0][2]],        # 33
                # проход по S3 переходя, по S2 не доходя, по S1 доходя
                [a3[0][2], -a2[0][3], -a1[0][3]],       # 34
                # проход по S3 переходя, по S2 переходя, по S1 возвращаясь
                [a3[0][2], -a2[0][4], a1[0][4]],        # 35

                # оставшиеся случаи
                # S1*k + S2 + S3
                [-(L2 - S2 - S3) // S1, -1, -1],  # 36
                # S1*k + S2 - S3
                [-(L2 - S2 + S3) // S1, -1, 1],  # 37
                # S1*k - S2 + S3
                [-(L2 + S2 - S3) // S1, 1, -1],  # 38
                # S1*k - S2 - S3
                [-(L2 + S2 + S3) // S1, 1, 1],  # 39
                # -S1*k + S2 + S3
                [(L2 - S2 - S3) // S1, -1, -1],  # 40
                # -S1*k + S2 - S3
                [(L2 - S2 + S3) // S1, -1, 1],  # 41
                # -S1*k - S2 + S3
                [(L2 + S2 - S3) // S1, 1, -1],  # 42
                # -S1*k - S2 - S3
                [-(L2 + S2 + S3) // S1, 1, 1],  # 43

                # S1 + S2*k + S3
                [-1, -(L2 - S1 - S3) // S2, -1],  # 44
                # S1 + S2*k - S3
                [-1, -(L2 - S1 + S3) // S2, 1],  # 45
                # S1 - S2*k + S3
                [-1, (L2 - S1 - S3) // S2, -1],  # 46
                # S1 - S2*k - S3
                [-1, (L2 - S1 + S3) // S2, 1],  # 47
                # -S1 + S2*k + S3
                [1, -(L2 + S1 - S3) // S2, -1],  # 48
                # -S1 + S2*k - S3
                [1, -(L2 + S1 + S3) // S2, 1],  # 49
                # -S1 - S2*k + S3
                [1, (L2 + S1 - S3) // S2, -1],  # 50
                # -S1 - S2*k - S3
                [1, -(L2 + S1 + S3) // S2, 1],  # 51

                # S1 + S2 + S3*k
                [-1, -1, -(L2 - S1 - S2) // S3],  # 52
                # S1 + S2 - S3*k
                [-1, -1, (L2 - S1 - S2) // S3],  # 53
                # S1 - S2 + S3*k
                [-1, 1, -(L2 - S1 + S2) // S3],  # 54
                # S1 - S2 - S3*k
                [-1, 1, (L2 - S1 + S2) // S3],  # 55
                # -S1 + S2 + S3*k
                [1, -1, -(L2 + S1 - S2) // S3],  # 56
                # -S1 + S2 - S3*k
                [1, -1, (L2 + S1 - S2) // S3],  # 57
                # -S1 - S2 + S3*k
                [1, 1, -(L2 + S1 + S2) // S3],  # 58
                # -S1 - S2 - S3*k
                [1, 1, (L2 + S1 + S2) // S3],  # 59
            ],
            [
                # движение в правую сторону через оборот (L1 + N)
                # проход по S1
                [a3[2][0], a2[2][0], a1[2][9]],         # 0
                # проход по S2
                [a3[2][0], a2[2][5], a1[2][0]],         # 1
                # проход по S3
                [a3[2][1], a2[2][0], a1[2][0]],         # 2

                # проход по S2 не доходя, по S1 доходя
                [a3[2][0], a2[2][5], a1[2][7]],         # 3
                # проход по S2 переходя, по S1 возвращаясь
                [a3[2][0], a2[2][6], -a1[2][8]],        # 4
                # проход по S3 не доходя, по S1 доходя
                [a3[2][1], a2[2][0], a1[2][5]],         # 5
                # проход по S3 переходя, по S1 возвращаясь
                [a3[2][2], a2[2][0], -a1[2][6]],        # 6
                # проход по S3 не доходя, по S2 доходя
                [a3[2][1], a2[2][1], a1[2][0]],         # 7
                # проход по S3 переходя, по S2 возвращаясь
                [a3[2][2], -a2[2][3], a1[2][0]],        # 8

                # проход по S3 не доходя, по S2 не доходя, по S1 доходя
                [a3[2][1], a2[2][1], a1[2][1]],         # 9
                # проход по S3 не доходя, по S2 переходя, по S1 возвращаясь
                [a3[2][1], a2[2][2], -a1[2][2]],        # 10
                # проход по S3 переходя, по S2 не доходя, по S1 доходя
                [a3[2][2], -a2[2][3], -a1[2][3]],       # 11
                # проход по S3 переходя, по S2 переходя, по S1 возвращаясь
                [a3[2][2], -a2[2][4], a1[2][4]],        # 12

                # проход по S2, переходя S3
                [-1, a2[2][7], a1[2][0]],               # 13
                # проход по S1, переходя S3
                [-1, a2[2][0], a1[2][10]],              # 14
                # проход по S1, переходя S2
                [a3[2][0], -1, a1[2][11]],              # 15

                # проход по S2 до тех пор, пока расстояние до конечного узла
                # не будет меньше, чем шаг по S3
                [1, a2[2][8], a1[2][0]],                # 16
                # проход по S1 до тех пор, пока расстояние до конечного узла
                # не будет меньше, чем шаг по S2
                [a3[2][0], 1, a1[2][12]],               # 17
                # проход по S1 до тех пор, пока расстояние до конечного узла
                # не будет меньше, чем шаг по S3
                [1, a2[2][0], a1[2][13]],               # 18

                # проход по S2 до тех пор, пока расстояние до конечного узла
                #  не будет меньше, чем шаг по S3 в обратную сторону
                [-1, a2[2][9], a1[2][0]],               # 19
                # проход по S1 до тех пор, пока расстояние до конечного узла
                #  не будет меньше, чем шаг по S2 в обратную сторону
                [a3[2][0], -1, a1[2][14]],              # 20
                # проход по S1 до тех пор, пока расстояние до конечного узла
                #  не будет меньше, чем шаг по S3 в обратную сторону
                [-1, a2[2][0], a1[2][15]],              # 21

                # проход по сумме S1 + S2 + S3
                [a3[2][3], a3[2][3], a3[2][3]],         # 22
                # проход по сумме S1 - S2 + S3
                [a3[2][4], -a3[2][4], a3[2][4]],        # 23
                # проход по сумме -S1 + S2 + S3
                [-a3[2][5], a3[2][5], a3[2][5]],        # 25

                # проход по сумме S1 + S2
                [a3[2][0], a3[2][6], a3[2][6]],         # 26
                # проход по сумме S1 + S3
                [a3[2][7], a3[2][0], a3[2][7]],         # 27
                # проход по сумме S2 + S3
                [a3[2][8], a3[2][8], a3[2][0]],         # 28
                # проход по разности S3 - S2
                [a3[2][9], -a3[2][9], a3[2][0]],        # 29
                # проход по разности S3 - S1
                [a3[2][10], a3[2][0], -a3[2][10]],      # 30
                # проход по разности S2 - S1
                [a3[2][0], a3[2][11], -a3[2][11]],      # 31

                # 9, 10, 11, 12 только в другую сторону
                # проход по S3 не доходя, по S2 не доходя, по S1 доходя
                [-a3[0][1], -a2[0][1], -a1[0][1]],      # 32
                # проход по S3 не доходя, по S2 переходя, по S1 возвращаясь
                [-a3[0][1], -a2[0][2], a1[0][2]],       # 33
                # проход по S3 переходя, по S2 не доходя, по S1 доходя
                [-a3[0][2], a2[0][3], a1[0][3]],        # 34
                # проход по S3 переходя, по S2 переходя, по S1 возвращаясь
                [-a3[0][2], a2[0][4], -a1[0][4]],       # 35

                # оставшиеся случаи
                # S1*k + S2 + S3
                [(L3 - S2 - S3) // S1, 1, 1],  # 36
                # S1*k + S2 - S3
                [(L3 - S2 + S3) // S1, 1, -1],  # 37
                # S1*k - S2 + S3
                [(L3 + S2 - S3) // S1, -1, 1],  # 38
                # S1*k - S2 - S3
                [(L3 + S2 + S3) // S1, -1, -1],  # 39
                # -S1*k + S2 + S3
                [-(L3 - S2 - S3) // S1, 1, 1],  # 40
                # -S1*k + S2 - S3
                [-(L3 - S2 + S3) // S1, 1, -1],  # 41
                # -S1*k - S2 + S3
                [-(L3 + S2 - S3) // S1, -1, 1],  # 42
                # -S1*k - S2 - S3
                [(L3 + S2 + S3) // S1, -1, -1],  # 43

                # S1 + S2*k + S3
                [1, (L3 - S1 - S3) // S2, 1],  # 44
                # S1 + S2*k - S3
                [1, (L3 - S1 + S3) // S2, -1],  # 45
                # S1 - S2*k + S3
                [1, -(L3 - S1 - S3) // S2, 1],  # 46
                # S1 - S2*k - S3
                [1, -(L3 - S1 + S3) // S2, -1],  # 47
                # -S1 + S2*k + S3
                [-1, (L3 + S1 - S3) // S2, 1],  # 48
                # -S1 + S2*k - S3
                [-1, (L3 + S1 + S3) // S2, -1],  # 49
                # -S1 - S2*k + S3
                [-1, -(L3 + S1 - S3) // S2, 1],  # 50
                # -S1 - S2*k - S3
                [-1, (L3 + S1 + S3) // S2, -1],  # 51

                # S1 + S2 + S3*k
                [1, 1, (L3 - S1 - S2) // S3],  # 52
                # S1 + S2 - S3*k
                [1, 1, -(L3 - S1 - S2) // S3],  # 53
                # S1 - S2 + S3*k
                [1, -1, (L3 - S1 + S2) // S3],  # 54
                # S1 - S2 - S3*k
                [1, -1, -(L3 - S1 + S2) // S3],  # 55
                # -S1 + S2 + S3*k
                [-1, 1, (L3 + S1 - S2) // S3],  # 56
                # -S1 + S2 - S3*k
                [-1, 1, -(L3 + S1 - S2) // S3],  # 57
                # -S1 - S2 + S3*k
                [-1, -1, (L3 + S1 + S2) // S3],  # 58
                # -S1 - S2 - S3*k
                [-1, -1, -(L3 + S1 + S2) // S3],  # 59
            ],
            [
                # движение в левую сторону через оборот
                # проход по S1
                [-a3[1][0], -a2[1][0], -a1[1][9]],      # 0
                # проход по S2
                [-a3[1][0], -a2[1][5], -a1[1][0]],      # 1
                # проход по S3
                [-a3[1][1], -a2[1][0], -a1[1][0]],      # 2

                # проход по S2 не доходя, по S1 доходя
                [-a3[1][0], -a2[1][5], -a1[1][7]],      # 3
                # проход по S2 переходя, по S1 возвращаясь
                [-a3[1][0], -a2[1][6], a1[1][8]],       # 4
                # проход по S3 не доходя, по S1 доходя
                [-a3[1][1], -a2[1][0], -a1[1][5]],      # 5
                # проход по S3 переходя, по S1 возвращаясь
                [-a3[1][2], -a2[1][0], a1[1][6]],       # 6
                # проход по S3 не доходя, по S2 доходя
                [-a3[1][1], -a2[1][1], -a1[1][0]],      # 7
                # проход по S3 переходя, по S2 возвращаясь
                [-a3[1][2], a2[1][3], -a1[1][0]],       # 8

                # проход по S3 не доходя, по S2 не доходя, по S1 доходя
                [-a3[1][1], -a2[1][1], -a1[1][1]],      # 9
                # проход по S3 не доходя, по S2 переходя, по S1 возвращаясь
                [-a3[1][1], -a2[1][2], a1[1][2]],       # 10
                # проход по S3 переходя, по S2 не доходя, по S1 доходя
                [-a3[1][2], a2[1][3], a1[1][3]],        # 11
                # проход по S3 переходя, по S2 переходя, по S1 возвращаясь
                [-a3[1][2], a2[1][4], -a1[1][4]],       # 12

                # проход по S2, переходя S3
                [1, -a2[1][7], -a1[1][0]],              # 13
                # проход по S1, переходя S3
                [1, -a2[1][0], -a1[1][10]],             # 14
                # проход по S1, переходя S2
                [-a3[1][0], 1, -a1[1][11]],             # 15

                # проход по S2 до тех пор, пока расстояние до конечного узла
                # не будет меньше, чем шаг по S3
                [-1, -a2[1][8], -a1[1][0]],             # 16
                # проход по S1 до тех пор, пока расстояние до конечного узла
                # не будет меньше, чем шаг по S2
                [-a3[1][0], -1, -a1[1][12]],            # 17
                # проход по S1 до тех пор, пока расстояние до конечного узла
                # не будет меньше, чем шаг по S3
                [-1, -a2[1][0], -a1[1][13]],            # 18

                # проход по S2 до тех пор, пока расстояние до конечного узла
                #  не будет меньше, чем шаг по S3 в обратную сторону
                [1, -a2[1][9], -a1[1][0]],              # 19
                # проход по S1 до тех пор, пока расстояние до конечного узла
                #  не будет меньше, чем шаг по S2 в обратную сторону
                [-a3[1][0], 1, -a1[1][14]],             # 20
                # проход по S1 до тех пор, пока расстояние до конечного узла
                #  не будет меньше, чем шаг по S3 в обратную сторону
                [1, -a2[1][0], -a1[1][15]],             # 21

                # проход по сумме S1 + S2 + S3
                [-a3[1][3], -a3[1][3], -a3[1][3]],      # 22
                # проход по сумме S1 - S2 + S3
                [-a3[1][4], a3[1][4], -a3[1][4]],       # 23
                # проход по сумме -S1 + S2 + S3
                [a3[1][5], -a3[1][5], -a3[1][5]],       # 25

                # проход по сумме S1 + S2
                [-a3[1][0], -a3[1][6], -a3[1][6]],      # 26
                # проход по сумме S1 + S3
                [-a3[1][7], -a3[1][0], -a3[1][7]],      # 27
                # проход по сумме S2 + S3
                [-a3[1][8], -a3[1][8], -a3[1][0]],      # 28
                # проход по разности S3 - S2
                [-a3[1][9], a3[1][9], -a3[1][0]],       # 29
                # проход по разности S3 - S1
                [-a3[1][10], -a3[1][0], a3[1][10]],     # 30
                # проход по разности S2 - S1
                [-a3[1][0], -a3[1][11], a3[1][11]],     # 31

                # 9, 10, 11, 12 только в другую сторону
                # проход по S3 не доходя, по S2 не доходя, по S1 доходя
                [a3[3][1], a2[3][1], a1[3][1]],         # 32
                # проход по S3 не доходя, по S2 переходя, по S1 возвращаясь
                [a3[3][1], a2[3][2], -a1[3][2]],        # 33
                # проход по S3 переходя, по S2 не доходя, по S1 доходя
                [a3[3][2], -a2[3][3], -a1[3][3]],       # 34
                # проход по S3 переходя, по S2 переходя, по S1 возвращаясь
                [a3[3][2], -a2[3][4], a1[3][4]],        # 35

                # оставшиеся случаи
                # S1*k + S2 + S3
                [-(L4 - S2 - S3) // S1, -1, -1],  # 36
                # S1*k + S2 - S3
                [-(L4 - S2 + S3) // S1, -1, 1],  # 37
                # S1*k - S2 + S3
                [-(L4 + S2 - S3) // S1, 1, -1],  # 38
                # S1*k - S2 - S3
                [-(L4 + S2 + S3) // S1, 1, 1],  # 39
                # -S1*k + S2 + S3
                [(L4 - S2 - S3) // S1, -1, -1],  # 40
                # -S1*k + S2 - S3
                [(L4 - S2 + S3) // S1, -1, 1],  # 41
                # -S1*k - S2 + S3
                [(L4 + S2 - S3) // S1, 1, -1],  # 42
                # -S1*k - S2 - S3
                [-(L4 + S2 + S3) // S1, 1, 1],  # 43

                # S1 + S2*k + S3
                [-1, -(L4 - S1 - S3) // S2, -1],  # 44
                # S1 + S2*k - S3
                [-1, -(L4 - S1 + S3) // S2, 1],  # 45
                # S1 - S2*k + S3
                [-1, (L4 - S1 - S3) // S2, -1],  # 46
                # S1 - S2*k - S3
                [-1, (L4 - S1 + S3) // S2, 1],  # 47
                # -S1 + S2*k + S3
                [1, -(L4 + S1 - S3) // S2, -1],  # 48
                # -S1 + S2*k - S3
                [1, -(L4 + S1 + S3) // S2, 1],  # 49
                # -S1 - S2*k + S3
                [1, (L4 + S1 - S3) // S2, -1],  # 50
                # -S1 - S2*k - S3
                [1, -(L4 + S1 + S3) // S2, 1],  # 51
            ],
        ]
    )
    S = np.array(
        [
            [S3],
            [S2],
            [S1]
        ]
    )

    tbw = find_the_best_way(N, N1, N2, L, S)
    return tbw


def test_algorithm(N, N1, S1, S2, S3):
    max_d = -10e5
    for N2 in range(2, N // 2 + 2):
    # for N2 in range(44, 45):
        g = general(N2, N, N1, S1, S2, S3)
        if isinstance(g, int):
            if g == 0:
                print(f"Error in the algorithm. C({N}, {S1}, {S2}, {S3}) in "
                      f" route {N1}-{N2}.")
        else:
            # print("1-{:d}: a3 = {:d}, a2 = {:d}, a1 = {:d}.".format(N2, *g))
            pass
        len_res = np.sum(np.abs(g))
        if len_res > max_d:
            max_d = len_res
    return max_d


if __name__ == "__main__":
    csvfiles = listdir('OptCirculants')
    for csvfile in csvfiles:
        fullFileName = 'OptCirculants/' + csvfile
        with open (fullFileName, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                if row[0].startswith('Кол-во'):
                    continue
                re_finder = re.search("\d+, \d+, \d+, \d+", row[1])
                re_result = re_finder.group(0).split(',')
                N, S1, S2, S3 = map(int, re_result)
                N1 = 1
                print(f"Circulant C({N}, {S1}, {S2}, {S3}).")
                # alg_diameter = test_algorithm(N, N1, S1, S2, S3)
    # if alg_diameter != int(row[2]):
    #     print(f'Opt D = {row[2]}, alg D = {alg_diameter} in '
    #           f'circulant C({N}, {S1}, {S2}, {S3}).')

    # N, S1, S2, S3 = 100, 26, 28, 33
    # N1 = 1
    # D = test_algorithm(N, N1, S1, S2, S3)
    # print(f'Max. diameter: {D}.')
