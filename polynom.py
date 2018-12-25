import time
from pprint import pprint

N, S1, S2, S3 = 25, 6, 7, 10
S1 = S1 % N
S2 = S2 % N
S3 = S3 % N

if all([S1, S2, S3]) == 0:
    assert "Error!"
    print("Error!")
    exit(-1)

N1 = 1
min_coeffs = tuple()
all_coeffs = list()

print(f'Circulant C({N}; {S1}, {S2}, {S3}).')
start_time = time.time()
for N2 in range(1, N // 2 + 2):
    L = abs(N2 - N1)
    min_sum = 10e+5
    for z in range(-(N // S3), N // S3 + 1):
        for y in range(-(N // S2), N // S2 + 1):
            for x in range(-(N // S1), N // S1 + 1):
                dot_sum = S1*x + S2*y + S3*z
                if dot_sum < 0:
                    dot_sum += N
                if (N1 + dot_sum) % N == N2:
                    if abs(x) + abs(y) + abs(z) < min_sum:
                        min_sum = abs(x) + abs(y) + abs(z)
                        min_coeffs = (x, y, z)
    # print(f"1-{N2} --> a1 = %d, a2 = %d, a3 = %d." % min_coeffs)
    all_coeffs.append(min_coeffs)
# print('--- %f seconds ---' % (time.time() - start_time))

min_all_tups = 10e5
max_all_tups = -10e5
for tup in all_coeffs:
    min_tup = min(tup)
    max_tup = max(tup)
    if min_tup < min_all_tups:
        min_all_tups = min_tup
    if max_tup > max_all_tups:
        max_all_tups = max_tup

# print('Min: {:d}, Max: {:d}.'.format(min_all_tups, max_all_tups))

extension_all_coeffs = list()

def negate_tuple(tmp: tuple) -> tuple:
    """
    Reversing tuple values.
    """
    return -tmp[0], -tmp[1], -tmp[2]

for t in all_coeffs:
    extension_all_coeffs.append(negate_tuple(t))

if N % 2 == 0:
    extension_all_coeffs.pop(-1)

extension_all_coeffs.pop(0)
extension_all_coeffs.reverse()
all_coeffs.extend(extension_all_coeffs)

for i, el in enumerate(all_coeffs):
    print(f"1-{i+1} --> a1 = %d, a2 = %d, a3 = %d." % el)
