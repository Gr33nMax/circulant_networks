import time
import os
import re
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from scipy.optimize import curve_fit
from math import gcd


# matplotlib global settings
plt.rcParams["font.family"] = "Times New Roman"


def check_node(num_nodes: int, node: int) -> int:
    """
    Check the validity of the node.
    Each node can't be less or equal 0 or 
    greater than the number of nodes.
    """
    if node <= 0:
        node += num_nodes
    if node > num_nodes:
        node %= num_nodes
    return node


def find_min_len(tlst: list) -> (int, int):
    """
    This function finds minimal distances to the end node.
    """
    min_t_high   = 10e5
    min_t_low    = 10e5
    sec_arg_low  = 0
    sec_arg_high = 0
    for t in tlst:
        if t[2] == "high":
            if t[0] < min_t_high:
                min_t_high = t[0]
                sec_arg_high = t[1]
        else:
            if t[0] < min_t_low:
                min_t_low = t[0]
                sec_arg_low = t[1]

    if min_t_high == 10e5:
        return min_t_low, sec_arg_low

    if min_t_low < min_t_high:
        return min_t_low, sec_arg_low

    return min_t_high, sec_arg_high


def calc_L(N: int, N1: int, N2: int) -> list:
    L = [
        min(abs(N2 - N1), N - abs(N2 - N1)),
        max(abs(N2 - N1), N - abs(N2 - N1)),
        N + min(abs(N2 - N1), N - abs(N2 - N1)),
        N + max(abs(N2 - N1), N - abs(N2 - N1)),
    ]
    return L

def fail_alg(N, N1, N2, S, prev_step, the_first=1):
    remove_pos = 0
    sl = [S[0], S[1], S[2], -S[0], -S[1], -S[2]]
    remove_flag = False
    if (-prev_step) in sl:
        remove_pos = sl.index(-prev_step)
        sl.remove(-prev_step)
        remove_flag = True

    X = [
        N1 + S[0],
        N1 + S[1],
        N1 + S[2],
        N1 - S[0],
        N1 - S[1],
        N1 - S[2]
    ]

    if remove_flag:
        X.remove(X[remove_pos])

    for idx, el in enumerate(X):
        X[idx] = check_node(N, el)

    if the_first in X:
        remove_tf_pos = X.index(the_first)
        X.remove(the_first)
        sl.remove(sl[remove_tf_pos])

    lengths = list()
    for idx, el in enumerate(X):
        lengths.append(calc_L(N, el, N2))

    min_lengths = list()
    for i, lst in enumerate(lengths):
        min_d = list()
        for d in lst:
            if d % S[2] == 0:
                min_d.append((d // S[2], sl[i], "high"))
            if d % S[1] == 0:
                min_d.append((d // S[1], sl[i], "high"))
            if d % S[0] == 0:
                min_d.append((d // S[0], sl[i], "high"))
            if d % (S[0] + S[1]) == 0:
                min_d.append((d // (S[0] + S[1]) * 2, sl[i], "low"))
            if d % (S[0] + S[2]) == 0:
                min_d.append((d // (S[0] + S[2]) * 2, sl[i], "low"))
            if d % (S[1] + S[2]) == 0:
                min_d.append((d // (S[1] + S[2]) * 2, sl[i], "low"))
            if d % (S[1] - S[0]) == 0:
                min_d.append((d // (S[1] - S[0]) * 2, sl[i], "low"))
            if d % (S[2] - S[0]) == 0:
                min_d.append((d // (S[2] - S[0]) * 2, sl[i], "low"))
            if d % (S[2] - S[1]) == 0:
                min_d.append((d // (S[2] - S[1]) * 2, sl[i], "low"))

            if d % (S[0] + S[1] + S[2]) == 0:
                min_d.append((d // (S[0] + S[1] + S[2]) * 3, sl[i], "low"))
            if S[0] + S[1] - S[2] > 0 and d % (S[0] + S[1] - S[2]) == 0:
                min_d.append((d // (S[0] + S[1] - S[2]) * 3, sl[i], "low"))
            if -S[0] - S[1] + S[2] > 0 and d % (-S[0] - S[1] + S[2]) == 0:
                min_d.append((d // (-S[0] - S[1] + S[2]) * 3, sl[i], "low"))
            if d % (S[0] - S[1] + S[2]) == 0:
                min_d.append((d // (S[0] - S[1] + S[2]) * 3, sl[i], "low"))
            if d % (-S[0] + S[1] + S[2]) == 0:
                min_d.append((d // (-S[0] + S[1] + S[2]) * 3, sl[i], "low"))

        min_lengths.append(find_min_len(min_d))

    f = 1  # for debug
    near_result = min(min_lengths, key=lambda  r: r[0])[1]
    result_generatrix = near_result
    if near_result != 0:
        result_generatrix = near_result
    else:
        if prev_step > 0:
            if S[2] in sl:
                result_generatrix = S[2]
            elif S[1] in sl:
                result_generatrix = S[1]
            elif S[0] in sl:
                result_generatrix = S[0]
        else:
            if -S[2] in sl:
                result_generatrix = -S[2]
            elif -S[1] in sl:
                result_generatrix = -S[1]
            elif -S[0] in sl:
                result_generatrix = -S[0]

    return result_generatrix


def check_generatrices(N: int, gLst: list):
    for idx, gen in enumerate(gLst):
        if gen > N:
            gen %= N
        elif gen > N // 2:
            if gLst[idx] - gen <= 0:
                continue
            else:
                gLst[idx] -= gen
    gLst = tuple(sorted(gLst))

    if gcd(gcd(gLst[0], gLst[1]), gLst[2]) != 1 and N % 2 == 0:
        return 0

    return tuple(gLst)


def start_alg(N, N1, N2, S):
    """ Запуск алгоритма для поиска маршрута из N1 в N2 """
    S = check_generatrices(N, list(S))
    if not S:
        return -1

    visited = list()
    next_step = 0
    visited.append(N1)
    # infinity_cycles = False
    num_iterations = 0
    the_first = N1
    while N1 != N2:
        num_iterations += 1
        next_step = fail_alg(N, N1, N2, S, next_step, the_first=the_first)
        N1 = check_node(N, N1 + next_step)
        if num_iterations > 10e5:
            return list()
        if N1 in visited:
            N1 = check_node(N, N1 - next_step)
            if next_step == S[0]:
                next_step = np.random.choice([S[1], S[2]])
            if next_step == S[1]:
                next_step = np.random.choice([S[2],S[0]])
            if next_step == S[2]:
                next_step = np.random.choice([S[0], S[1]])
            if next_step == -S[0]:
                next_step = np.random.choice([-S[1], -S[2]])
            if next_step == -S[1]:
                next_step = np.random.choice([-S[2], -S[0]])
            if next_step == -S[2]:
                next_step = np.random.choice([-S[0], -S[1]])
            N1 = check_node(N, N1 + next_step)
        visited.append(N1)
    return visited


def find_max_diameter(lst_lsts):
    return len(max(lst_lsts, key=len)) - 1


def read_from_csv():
    # В текущей директории должна находиться папка 'OptCirculants' c
    # csv-файлами таблиц, доступных по ссылке:
    # https://www.kaggle.com/gre3nlime/3dimensional-optimal-circulants
    """ Чтение и обработка данных из csv файлов """
    if not os.path.exists('OptCirculants'):
        print("Error! Can't find folder 'OptCirculants'!\n"
              "Please, create a folder 'OptCirculants' with Optimal "
              "Circulants (csv-files).\nDownload link: "
              "https://www.kaggle.com/gre3nlime/3dimensional-optimal-circulants")
        return False
    N1 = 1
    num_diff_diameters = 0
    num_circulant = 0
    circulant_signatures = list()
    list_diff_diameters = list()
    csvfiles = os.listdir('OptCirculants')
    errors = 0

    x = list()
    y = list()
    num_errors = 0

    num_circulants_with_s0_eq_1 = 0

    for csvfile in csvfiles:
        fullFileName = 'OptCirculants/' + csvfile
        with open (fullFileName, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                if row[0].startswith('Кол-во'):
                    continue
                if row[0].startswith('stop'):
                    break
                re_finder = re.search("\d+, \d+, \d+, \d+", row[1])
                re_result = re_finder.group(0).split(',')
                S = [0, 0, 0]
                N, S[0], S[1], S[2] = map(int, re_result)
                all_vertices_list = list()
                error_flag = False

                if S[0] == 1:
                    num_circulants_with_s0_eq_1 += 1

                for N2 in range(2, N + 1):
                    vertices = start_alg(N, N1, N2, S)
                    if not vertices:
                        errors += 1
                        error_flag = True
                    all_vertices_list.append(vertices)
                if error_flag:
                    num_errors += 4
                    continue
                if -1 in all_vertices_list:
                    continue
                max_diameter = find_max_diameter(all_vertices_list)
                opt_diameter = int(row[2])

                x.append(num_circulant)
                circulant_signatures.append(f'C({N}; {S[0]}, {S[1]}, {S[2]})')

                y.append(max_diameter - opt_diameter)

                print(f"C({N}, {S[0]}, {S[1]}, {S[2]}).")
                # print(f'D = {max_diameter}. Opt D = {opt_diameter}.')
                if max_diameter - opt_diameter != 0:
                    num_diff_diameters += 1
                    list_diff_diameters.append(max_diameter - opt_diameter)

                num_circulant += 1

    list_diff_diameters.sort(reverse=True)
    # print(f"Max diff diameters: {list_diff_diameters}")

    # plt.yticks([0, 1, 2])
    plt.plot(x, y)
    plt.grid(True)
    # plt.xticks(np.arange(0, 26), circulant_signatures, rotation=90)
    plt.xlim(5, 300)
    plt.xlabel('Количество вершин')
    plt.ylabel('D_dijkstra - D_sequent')
    plt.show()

    print('s1 = 1 in %d circulants.' % num_circulants_with_s0_eq_1)
    print('Percentage s1 = 1 to all circulants: %f.' %
          (num_circulants_with_s0_eq_1 / num_circulant))
    print('Num all diameters: %d.' % num_circulant)
    print('Num diff diameters: %d. ' % num_diff_diameters)
    print('Percentage diff. diam / num all diam: %f.' %
          (num_diff_diameters / num_circulant))
    print('Errors: %d.' % num_errors)

    return True


def launch_algorithm(start=10, end=100, S=(2, 3, 4),
                     print_graph_time=True,
                     print_graph_diameter=True,
                     draw_trend_line_time=True,
                     draw_trend_line_diameter=True):
    """
     Запуск алгоритма с отрисовкой двух графиков зависимости
        1) времени выполнения алгоритма от числа вершин;
        2) диаметра от числа вершин.
     Результаты сохраняются в текущую папку в виде изображения с названием
     'fig.png'
    """
    N1 = 1
    if start < max(S):
        print('Error! Start number of vertices must be greater than S3!')
        exit(-1)
    elif end < start:
        print('End number of vertices must be greater than Start number!')
        exit(-2)
    time_list = list()
    diameters_list = list()
    errors = 0
    num_errors = 0
    for N in range(start, end+1):
        if not check_generatrices(N, S):
            print('Error! Wrong generatrices!')
            exit(-3)
        all_vertices_list = list()
        start_time = time.time()
        error_flag = False
        num_err_N2 = 0
        for N2 in range(82, 83):
        # for N2 in range(32, 33):
            vertices = start_alg(N, N1, N2, S)
            if not vertices:
                errors += 1
                num_err_N2 = N2
                error_flag = True
                continue
            all_vertices_list.append(vertices)
        # print(len(all_vertices_list))
        if error_flag:
            num_errors += 1
            print(f'Error in circulant C({N}; {S[0]}, {S[1]}, {S[2]}). '
                  f'({N1}-{num_err_N2}).')
            continue
        diff_time = time.time() - start_time
        time_list.append(diff_time)
        # for num_v, v in enumerate(all_vertices_list):
        #     print(f'{N1}-{num_v+1}: {v}')
        max_diameter = find_max_diameter(all_vertices_list)
        diameters_list.append(max_diameter)
        # print("--- %f seconds ---" % diff_time)
        # print(f'D = {max_diameter}.')
        # print(num_errors)

    X = np.array(np.arange(start, end-errors+1))
    time_list = time_list[:X.shape[0]]
    diameters_list = diameters_list[:X.shape[0]]
    Y1 = np.array(time_list)
    Y2 = np.array(diameters_list)

    # printing graphs
    ##################################################################
    # graph 1
    if print_graph_diameter:
        pylab.plot(X, Y2)

        if draw_trend_line_diameter:
            Z2 = np.polyfit(X, Y2, 1)
            P2 = np.poly1d(Z2)
            pylab.plot(X, P2(X))

        pylab.grid()
        pylab.xlabel('Количество вершин')
        pylab.ylabel('Диаметр')
        pylab.xlim(start, end)
        # pylab.title('Зависимость диаметра от количества вершин\nдля циркулянта '
        #           f'C(N; {S[0]}, {S[1]}, {S[2]})')
        plt.savefig(fname='fig2.png')
        pylab.show()
    ##################################################################
    # graph 2
    if print_graph_time:
        plt.plot(X, Y1)
        # trend line
        if draw_trend_line_time:
            def func(x, a, b, c):
                return a * x ** 2 + b * x + c
            x = X
            y = func(x, 0.000002, 0.00001, 0.01)
            yn = y + 0.00001 * np.random.normal(size=len(x))
            popt, pcov = curve_fit(func, x, yn)
            pylab.plot(x, np.polyval(popt, x))

        pylab.grid()
        pylab.xlabel('Количество вершин')
        pylab.ylabel('Время выполнения алгоритма, с')
        pylab.xlim(start, end)
        # pylab.title('Зависимость времени выполнения алгоритма "Sequent" от\n'
        #             'количества вершин для циркулянта '
        #           f'C(N; {S[0]}, {S[1]}, {S[2]})')
        pylab.savefig(fname='fig1.png')
        pylab.show()

    ##################################################################
    # print(num_errors)

    return num_errors


def useless_function():
    pass

    # Расчеты ниже были сделаны заранее при помощи функций, которые уже
    # удалены. Здесь лишь приведены результаты и отрисовка графиков
    ########################################################

    # colors = ["peachpuff", "lightskyblue"]
    # x = ['1', '2']
    # y = [2, 18]
    # plt.ylim(0, 20)
    # plt.ylabel('Количество диаметров')
    # plt.title('Количество различных диаметров')
    # plt.annotate('2', xy=(-0.015, 2.35))
    # plt.annotate('18', xy=(0.985, 18.35))
    # plt.annotate('Total: 20', xy=(-0.35, 17))
    # plt.bar(x, y, color=colors)
    # plt.xlabel('Величина разницы D_dijkstra - D_sequent')
    # plt.show()

    ########################################################

    # x = [9, 15, 16, 21, 23, 35, 36, 49, 64, 81, 100]
    # x = list(map(str, x))
    # y = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4]
    # colors = [*['lightgreen']*4, *['mediumaquamarine']*4,
    #           *['c']*3]
    # plt.ylim(0, 4.5)
    # plt.ylabel('D - диаметр')
    # plt.xlim(-0.5, len(x)-0.5)
    # plt.bar(x, y, color=colors)
    # plt.xlabel('Количество вершин')
    # plt.show()


if __name__ == "__main__":
    # чтение данных из csv-таблиц
    read_from_csv()

    # запуск расчета зависимостей при помощи алгоритма с заданными параметрами
    # num_circulants = 0
    # num = 0
    # errors = 0
    #
    # start = 82
    # end = start

    # for a in range(10, 30):
    #     for b in range(a+1, 30):
    #         for c in range(b+1, 30):
    #             if gcd(gcd(a, b), c) != 1:
    #                 continue
    #             if not (a == 12 and b == 24 and c == 29):
    #                 continue
    #             local_num_errors = launch_algorithm(
    #                 start=start, end=end, S=(a, b, c),
    #                 print_graph_time=False,
    #                 print_graph_diameter=False,
    #                 draw_trend_line_time=False,
    #                 draw_trend_line_diameter=False)
    #             num += 1
    #             num_circulants += 1
    #             print(f'Circulant C({end}, {a}, {b}, {c}). '
    #                   f'Total checked: {num_circulants}.')

    # local_num_errors = launch_algorithm(
    #             start=24, end=36, S=(2, 3, 4),
    #             print_graph_time=False,
    #             print_graph_diameter=False,
    #             draw_trend_line_time=False,
    #             draw_trend_line_diameter=False)
    # print('Num errors: %d.' % local_num_errors)
    #             errors += local_num_errors
    #             if local_num_errors != 0:
    #                 print(f'Circulant C(N; {a}, {b}, {c})', end='')
    #                 print(' with %d errors.' % local_num_errors)
    # print(f'Number of errors: {errors}.')

    # useless_function()
    pass