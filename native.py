import csv
from os import listdir
import re


def native(N, S1, S2, S3, N1, N2):
    current = [N1]
    current2 = [N1]
    current3 = [N1]
    current4 = [N1]

    S32 = S3 - S2
    S31 = S3 - S1
    S21 = S2 - S1

    def find_min_L(N1, N2):
        L1 = N2 - N1 if N2 - N1 > 0 else N1 - N2
        L2 = N - (N2 - N1) if N2 - N1 > 0 else N - (N1 - N2)
        return min(L1, L2)

    L = find_min_L(N1, N2)
    L_copy = L
    L2 = N - L
    L2_copy = L2

    def find_opt_mod(L, S1, S2, S3, N, N1, N2, mainDir=None):
        if N1 + L == N or N1 - L == 0:
            if N1 + L == N:
                spin = 1
            else:
                spin = -1
        else:
            if abs(N2 - ((N1 + L) % N)) < abs(N2 - ((N1 - L) % N)):
                spin = 1
            else:
                spin = -1

        if L % S3 == 0:
            N1 = N1 + spin * S3
            name = S3
        elif L % S2 == 0:
            N1 = N1 + spin * S2
            name = S2
        elif L % S1 == 0:
            N1 = N1 + spin * S1
            name = S1
        else:
            if N1 + spin * mainDir > 0:
                N1 = N1 + spin * mainDir
            else:
                N1 = N + N1 + spin * mainDir
            name = mainDir

        N1 = N1 % N if N1 > N else N1
        N1 = N1 + N if N1 < 0 else N1
        N1 = N if N1 == 0 else N1
        return N1, name

    while N1 != N2:
        if L // S3 > 0:
            N1, name_S = find_opt_mod(L, S1, S2, S3, N, N1, N2, mainDir=S3)
        elif L % S32 == 0 or L % S31 == 0:
            N1, name_S = find_opt_mod(L, S1, S2, S3, N, N1, N2, mainDir=S3)
        elif L // S2 > 0:
            N1, name_S = find_opt_mod(L, S1, S2, S3, N, N1, N2, mainDir=S2)
        elif L % S21 == 0:
            N1, name_S = find_opt_mod(L, S1, S2, S3, N, N1, N2, mainDir=S2)
        elif L // S1 > 0:
            N1, name_S = find_opt_mod(L, S1, S2, S3, N, N1, N2, mainDir=S1)
        else:
            N1, name_S = find_opt_mod(L, S1, S2, S3, N, N1, N2, mainDir=S1)

        if N1 in current:
            if name_S == S1:
                N1 = N1 - S1 + S2
            elif name_S == S2:
                N1 = N1 - S2 + S3
            elif name_S == S3:
                N1 = N1 - S3 + S1

        L = find_min_L(N1, N2)

        current.append(N1)

    # def find_opt_mod_2(L, S1, S2, S3, N, N1, N2, mainDir=None):


    N1 = current2[0]

    while N1 != N2:
        if L2 // S3 > 0:
            N1, name_S = find_opt_mod(L2, S1, S2, S3, N, N1, N2, mainDir=S3)
        elif L2 % S32 == 0 or L2 % S31 == 0:
            N1, name_S = find_opt_mod(L2, S1, S2, S3, N, N1, N2, mainDir=S3)
        elif L2 // S2 > 0:
            N1, name_S = find_opt_mod(L2, S1, S2, S3, N, N1, N2, mainDir=S2)
        elif L2 % S21 == 0:
            N1, name_S = find_opt_mod(L2, S1, S2, S3, N, N1, N2, mainDir=S2)
        elif L2 // S1 > 0:
            N1, name_S = find_opt_mod(L2, S1, S2, S3, N, N1, N2, mainDir=S1)
        else:
            N1, name_S = find_opt_mod(L2, S1, S2, S3, N, N1, N2, mainDir=S1)

        if N1 in current2:
            if name_S == S1:
                N1 = N1 - S1 + S2
            elif name_S == S2:
                N1 = N1 - S2 + S3
            elif name_S == S3:
                N1 = N1 - S3 + S1

        L2 = find_min_L(N1, N2)

        current2.append(N1)

    N1 = current3[0]
    L = L_copy
    flag3 = True
    while flag3 and N1 != N2:
        # move to the right
        if L % S3 == 0:
            N1 = N1 + S3
        elif L % S2 == 0:
            N1 = N1 + S2
        elif L % S1 == 0:
            N1 = N1 + S1
        else:
            flag3 = False

        N1 = N1 % N if N1 > N else N1
        N1 = N1 + N if N1 < 0 else N1
        N1 = N if N1 == 0 else N1

        L = abs(N2 - N1)
        if N1 not in current3:
            current3.append(N1)
        else:
            break

    N1 = current4[0]
    flag4 = True
    L2 = L2_copy
    while flag4 and N1 != N2:
        # move to the left
        if L2 % S3 == 0:
            N1 = N1 - S3
        elif L2 % S2 == 0:
            N1 = N1 - S2
        elif L2 % S1 == 0:
            N1 = N1 - S1
        else:
            flag4 = False

        N1 = N1 % N if N1 > N else N1
        N1 = N1 + N if N1 < 0 else N1
        N1 = N if N1 == 0 else N1

        L2 = abs(N2 - N1)

        if N1 not in current4:
            current4.append(N1)
        else:
            break

    if current3[-1] != N2:
        current3.clear()
    if current4[-1] != N2:
        current4.clear()

    def len_not_empty(x: list):
        return len(x) if len(x) >= 1 else 10e5
    result_list = min(current, current2, current3, current4, key=len_not_empty)

    return result_list


def find_max_length(lst: list):
    return len(max(lst, key=len))

if __name__ == "__main__":
    N, S1, S2, S3 = 100, 4, 18, 19
    N1 = 1
    # all_routes = list()
    #
    # for N2 in range(2, N + 1):
    #     routes = native(N, S1, S2, S3, N1, N2)
    #     print(N2)
    #     print(routes)
    #     all_routes.append(routes)
    #
    # max_length = find_max_length(all_routes)
    # print('D = {:d}.'.format(max_length))

    N2 = 13
    routes = native(N, S1, S2, S3, N1, N2)
    print(N2)
    print(routes)


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
    #             N1 = 1
    #             print(f"Circulant C({N}, {S1}, {S2}, {S3}).")
    #             all_routes = list()
    #             for N2 in range(2, N + 1):
    #                 routes = native(N, S1, S2, S3, N1, N2)
    #                 if len(routes) == 0:
    #                     print("Error in the algorithm. "
    #                           f"Circulant C({N}, {S1}, {S2}, {S3}).")
    #                 print(N2)
    #                 print(routes)
    #                 all_routes.append(routes)
    #             max_length = find_max_length(all_routes)
