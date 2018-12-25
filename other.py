import csv
from os import listdir
import re


def general_fun(N2, N, S1, S2, S3):
    N1 = 1
    L_1 = min(N - N2 + N1, N2 - N1)
    spin = 1 if N2 <= (N + 1) // 2 else -1

    a30 = 0  # не шаг. никуда по S3
    a31 = L_1 // S3  # недошаг. по S3
    a32 = L_1 // S3 + 1  # перешаг. по S3
    a33 = L_1 // S3 + 2  # двойной перешаг. по S3

    L21 = L_1 % S3
    L22 = S3 - L_1 % S3

    a20 = 0  # не шаг. никуда по S2
    a21 = L21 // S2  # недошаг. по S2 после недошаг. по S3
    a22 = L21 // S2 + 1  # перешаг. по S2 после недошаг. по S3
    a23 = L22 // S2  # недошаг. по S2 после перешаг. по S3
    a24 = L22 // S2 + 1  # перешаг. по S2 после перешаг. по S3

    a25 = L_1 // S2
    a26 = L_1 // S2 + 1
    a27 = L_1 // S2 + 2

    L31 = L21 % S2
    L32 = S2 - L21 % S2
    L33 = L22 % S2
    L34 = S2 - L22 % S2

    a10 = 0  # не шаг. никуда по S1
    a11 = L31 // S1  # дошаг. по S1 после недошаг. по S3 и недошаг. по S2
    a12 = L32 // S1  # дошаг. по S1 после недошаг. по S3 и перешаг. по S2
    a13 = L33 // S1  # дошаг. по S1 после перешаг. по S3 и недошаг. по S2
    a14 = L34 // S1  # дошаг. по S1 после перешаг. по S3 и перешаг. по S2

    a15 = L21 // S1  # дошаг. по S1 после недошаг. по S3 и не шаг.  по S2
    a16 = L22 // S1  # дошаг. по S1 после перешаг. по S3 и не шаг.  по S2

    a17 = L_1 % S2 // S1  # дошаг. по S1 и не шаг. по S3 после недошаг. по S2
    a18 = (S2 - L_1 % S2) // S1  # дошаг. по S1 и не шаг. по S3 после 
    # перешаг. по S2

    a19 = L_1 // S1  # дошаг. по S1 и не шаг. по S2 и не шаг. по S3

    a110 = ((S2 - L_1 % S2) + S2) // S1  # дошаг. по S1 после двойного 
    # перешаг. по S2
    a111 = ((S3 - L_1 % S3) + S3) // S1  # дошаг. по S1 после двойного 
    # перешаг. по S3

    L1 = a31*S3 + a21*S2 + a11*S1
    L2 = a31*S3 + a22*S2 - a12*S1
    L3 = a32*S3 + a23*S2 + a13*S1
    L4 = a32*S3 - a24*S2 + a14*S1
    L5 = a31*S3 + a20*S2 + a15*S1
    L6 = a32*S3 + a20*S2 - a16*S1
    L7 = a30*S3 + a25*S2 + a17*S1
    L8 = a30*S3 + a26*S2 - a18*S1

    L9 = a31*S3 + a20*S2 + a10*S1
    L10 = a30*S3 + a25*S2 + a10*S1
    L11 = a30*S3 + a20*S2 + a19*S1

    L12 = a31*S3 + a22*S2 + a12*S1  # L2 только a12 с плюсом
    L13 = a32*S3 + a24*S2 + a14*S1  # L4 только a24 с плюсом
    L14 = a32*S3 + a20*S2 + a16*S1  # L6 только a16 с плюсом
    L15 = a30*S3 + a26*S2 + a18*S1  # L8 только a18 с плюсом

    L16 = a30*S3 + a27*S2 - a110*S1
    L17 = a33*S3 + a20*S2 - a111*S1

    # L18 = -a31*S3 + a20*S2 + a10*S1  # движение влево
    # L19 = -a32*S3 + a20*S2 + a10*S1
    # L20 = a30*S3 - a21*S2 + a10*S1
    # L21 = a30*S3 - a22*S2 + a10*S1

    results = list()

    # sums = [L1, L2, L3, L4, L5, L6, L7, L8, L9, L10, L11, L12, L13, L14,
    #         L15, L16, L17]

    if L1 == L_1:
        if L1 < 0:
            L1 = L1 + N
        if L1 > N:
            L1 = L1 % N
    if L2 == L_1:
        if L2 < 0:
            L2 = L2 + N
        if L2 > N:
            L2 = L2 % N
    if L3 == L_1:
        if L3 < 0:
            L3 = L3 + N
        if L_1 > N:
            L3 = L3 % N
    if L4 == L_1:
        if L4 < 0:
            L4 = L4 + N
        if L4 > N:
            L4 = L4 % N
    if L5 == L_1:
        if L5 < 0:
            L5 = L5 + N
        if L5 > N:
            L5 = L5 % N
    if L6 == L_1:
        if L6 < 0:
            L6 = L6 + N
        if L6 > N:
            L6 = L6 % N
    if L7 == L_1:
        if L7 < 0:
            L7 = L7 + N
        if L7 > N:
            L7 = L7 % N
    if L8 == L_1:
        if L8 < 0:
            L8 = L8 + N
        if L8 > N:
            L8 = L8 % N
    if L9 == L_1:
        if L9 < 0:
            L9 = L9 + N
        if L9 > N:
            L9 = L9 % N
    if L10 == L_1:
        if L10 < 0:
            L10 = L10 + N
        if L9 > N:
            L10 = L10 % N
    if L11 == L_1:
        if L11 < 0:
            L11 = L11 + N
        if L11 > N:
            L11 = L11 % N
    if L12 == L_1:
        if L12 < 0:
            L12 = L12 + N
        if L12 > N:
            L12 = L12 % N
    if L13 == L_1:
        if L13 < 0:
            L13 = L13 + N
        if L13 > N:
            L13 = L13 % N
    if L14 == L_1:
        if L14 < 0:
            L14 = L14 + N
        if L14 > N:
            L14 = L14 % N
    if L15 == L_1:
        if L15 < 0:
            L15 = L15 + N
        if L15 > N:
            L15 = L15 % N
    if L16 == L_1:
        if L16 < 0:
            L16 = L16 + N
        if L16 > N:
            L16 = L16 % N
    if L17 == L_1:
        if L17 < 0:
            L17 = L17 + N
        if L17 > N:
            L17 = L17 % N

    if L1 == L_1:
        results.append((spin*a31, spin*a21, spin*a11, "L1"))
    if L2 == L_1:
        results.append((spin*a31, spin*a22, -spin*a12, "L2"))
    if L3 == L_1:
        results.append((spin*a32, spin*a23, spin*a13, "L3"))
    if L4 == L_1:
        results.append((spin*a32, -spin*a24, spin*a14, "L4"))
    if L5 == L_1:
        results.append((spin*a31, spin*a20, spin*a15, "L5"))
    if L6 == L_1:
        results.append((spin*a32, spin*a20, -spin*a16, "L6"))
    if L7 == L_1:
        results.append((spin*a30, spin*a25, spin*a17, "L7"))
    if L8 == L_1:
        results.append((spin*a30, spin*a26, -spin*a18, "L8"))
    if L9 == L_1:
        results.append((spin*a31, spin*a20, spin*a10, "L9"))
    if L10 == L_1:
        results.append((spin*a30, spin*a25, spin*a10, "L10"))
    if L11 == L_1:
        results.append((spin*a30, spin*a20, spin*a19, "L11"))
    if L12 == L_1:
        results.append((spin*a31, spin*a22, spin*a12, "L12"))
    if L13 == L_1:
        results.append((spin*a32, spin*a24, spin*a14, "L13"))
    if L14 == L_1:
        results.append((spin*a32, spin*a20, spin*a16, "L14"))
    if L15 == L_1:
        results.append((spin*a30, spin*a26, spin*a18, "L15"))
    if L16 == L_1:
        results.append((spin*a30, spin*a27, -spin*a110, "L16"))
    if L17 == L_1:
        results.append((spin*a33, spin*a20, -spin*a111, "L17"))

    L_2 = max(N - N2 + N1, N2 - N1)

    a30 = 0
    a31 = L_2 // S3
    a32 = L_2 // S3 + 1
    a33 = L_2 // S3 + 2

    L21 = L_2 % S3
    L22 = S3 - L_2 % S3

    a20 = 0
    a21 = L21 // S2
    a22 = L21 // S2 + 1
    a23 = L22 // S2
    a24 = L22 // S2 + 1

    a25 = L_2 // S2
    a26 = L_2 // S2 + 1
    a27 = L_2 // S2 + 2

    L31 = L21 % S2
    L32 = S2 - L21 % S2
    L33 = L22 % S2
    L34 = S2 - L22 % S2

    a10 = 0
    a11 = L31 // S1
    a12 = L32 // S1
    a13 = L33 // S1
    a14 = L34 // S1

    a15 = L21 // S1
    a16 = L22 // S1

    a17 = L_2 % S2 // S1
    a18 = (S2 - L_2 % S2) // S1

    a19 = L_2 // S1

    a110 = ((S2 - L_2 % S2) + S2) // S1
    a111 = ((S3 - L_2 % S3) + S3) // S1

    L18 = a31*S3 + a21*S2 + a11*S1
    L19 = a31*S3 + a22*S2 - a12*S1
    L20 = a32*S3 + a23*S2 + a13*S1
    L21 = a32*S3 - a24*S2 + a14*S1
    L22 = a31*S3 + a20*S2 + a15*S1
    L23 = a32*S3 + a20*S2 - a16*S1
    L24 = a30*S3 + a25*S2 + a17*S1
    L25 = a30*S3 + a26*S2 - a18*S1

    L26 = a31*S3 + a20*S2 + a10*S1
    L27 = a30*S3 + a25*S2 + a10*S1
    L28 = a30*S3 + a20*S2 + a19*S1

    L29 = a31*S3 + a22*S2 + a12*S1
    L30 = a32*S3 + a24*S2 + a14*S1
    L31 = a32*S3 + a20*S2 + a16*S1
    L32 = a30*S3 + a26*S2 + a18*S1

    L33 = a30*S3 + a27*S2 - a110*S1
    L34 = a33*S3 + a20*S2 - a111*S1

    if L18 == L_2:
        if L18 < 0:
            L18 = L18 + N
        if L18 > N:
            L18 = L18 % N
    if L19 == L_2:
        if L19 < 0:
            L19 = L19 + N
        if L19 > N:
            L19 = L19 % N
    if L20 == L_2:
        if L20 < 0:
            L20 = L20 + N
        if L20 > N:
            L20 = L20 % N
    if L21 == L_2:
        if L21 < 0:
            L21 = L21 + N
        if L21 > N:
            L21 = L21 % N
    if L22 == L_2:
        if L22 < 0:
            L22 = L22 + N
        if L22 > N:
            L22 = L22 % N
    if L23 == L_2:
        if L23 < 0:
            L23 = L23 + N
        if L23 > N:
            L23 = L23 % N
    if L24 == L_2:
        if L24 < 0:
            L24 = L24 + N
        if L24 > N:
            L24 = L24 % N
    if L25 == L_2:
        if L25 < 0:
            L25 = L25 + N
        if L25 > N:
            L25 = L25 % N
    if L26 == L_2:
        if L26 < 0:
            L26 = L26 + N
        if L26 > N:
            L26 = L26 % N
    if L27 == L_2:
        if L27 < 0:
            L27 = L27 + N
        if L27> N:
            L27 = L27 % N
    if L28 == L_2:
        if L28 < 0:
            L28 = L28 + N
        if L28 > N:
            L28 = L28 % N
    if L29 == L_2:
        if L29 < 0:
            L29 = L29 + N
        if L29 > N:
            L29 = L29 % N
    if L30 == L_2:
        if L30 < 0:
            L30 = L30 + N
        if L30 > N:
            L30 = L30 % N
    if L31 == L_2:
        if L31 < 0:
            L31 = L31 + N
        if L31 > N:
            L31 = L31 % N
    if L32 == L_2:
        if L32 < 0:
            L32 = L32 + N
        if L32 > N:
            L32 = L32 % N
    if L33 == L_2:
        if L33 < 0:
            L33 = L33 + N
        if L33 > N:
            L33 = L33 % N
    if L34 == L_2:
        if L34 < 0:
            L34 = L34 + N
        if L34 > N:
            L34 = L34 % N

    if L18 == L_2:
        results.append((-spin*a31, -spin*a21, -spin*a11, "L18"))
    if L19 == L_2:
        results.append((-spin*a31, -spin*a22, spin*a12, "L19"))
    if L20 == L_2:
        results.append((-spin*a32, -spin*a23, -spin*a13, "L20"))
    if L21 == L_2:
        results.append((-spin*a32, spin*a24, -spin*a14, "L21"))
    if L22 == L_2:
        results.append((-spin*a31, -spin*a20, -spin*a15, "L22"))
    if L23 == L_2:
        results.append((-spin*a32, -spin*a20, spin*a16, "L23"))
    if L24 == L_2:
        results.append((-spin*a30, -spin*a25, -spin*a17, "L24"))
    if L25 == L_2:
        results.append((-spin*a30, -spin*a26, spin*a18, "L25"))
    if L26 == L_2:
        results.append((-spin*a31, -spin*a20, -spin*a10, "L26"))
    if L27 == L_2:
        results.append((-spin*a30, -spin*a25, -spin*a10, "L27"))
    if L28 == L_2:
        results.append((-spin*a30, -spin*a20, -spin*a19, "L28"))
    if L29 == L_2:
        results.append((-spin*a31, -spin*a22, -spin*a12, "L29"))
    if L30 == L_2:
        results.append((-spin*a32, -spin*a24, -spin*a14, "L30"))
    if L31 == L_2:
        results.append((-spin*a32, -spin*a20, -spin*a16, "L31"))
    if L32 == L_2:
        results.append((-spin*a30, -spin*a26, -spin*a18, "L32"))
    if L33 == L_2:
        results.append((-spin*a30, -spin*a27, spin*a110, "L33"))
    if L34 == L_2:
        results.append((-spin*a33, -spin*a20, spin*a111, "L34"))

    # выбор налучшего результата
    def find_the_best_tuple(tup_list: list):
        def abs_sum(x):
            return sum(map(abs, x))

        min_sum = 10e5
        result_tup = tuple()
        for tup in tup_list:
            tup_abs_sum = abs_sum(tup[:-1])
            if tup_abs_sum < min_sum:
                min_sum = tup_abs_sum
                result_tup = tup

        return result_tup


    the_best_res = find_the_best_tuple(results)
    # print(str(N2) + ' ' + str(the_best_res))

    return the_best_res[:-1]


def test_alg(N, S1, S2, S3):
    N1 = 1
    max_D = -10e5
    success = True
    for N2 in range(2, N + 1):
        t = general_fun(N2, N, S1, S2, S3)
        if len(t) == 0:
            print(f"Error in the algorithm. C({N}, {S1}, {S2}, {S3}) in line "
                  f"{N1} --> {N2}.")
            success = False
        else:
            success = True
        # print("1 --> {:d}, a1 = {:d}, a2 = {:d}, a3 = {:d}.".format(N2, *t))
        len_the_best_res = sum(map(abs, t))
        if len_the_best_res > max_D:
            max_D = len_the_best_res
    # print("D = {:d}.".format(max_D))
    return success, max_D


if __name__ == "__main__":
    # csvfiles = listdir('OptCirculants')
    # for csvfile in csvfiles:
    #     fullFileName = 'OptCirculants/' + csvfile
    #     with open (fullFileName, 'r') as file:
    #         reader = csv.reader(file, delimiter=';')
    #         for row in reader:
    #             if row[0].startswith('Кол-во'):
    #                 continue
    #             re_finder = re.search("\d+, \d+, \d+, \d+", row[1])
    #             re_result = re_finder.group(0).split(',')
    #             N, S1, S2, S3 = map(int, re_result)
    #             # print(N, S1, S2, S3)
    #             test_res, diameter = test_alg(N, S1, S2, S3)
    #             if diameter != int(row[2]):
    #                 print(f'Opt D = {row[2]}, alg D = {diameter}.')

    res, D  = test_alg(100, 6, 23, 32)
