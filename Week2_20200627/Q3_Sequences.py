# custom functions
def f_value(i):
    vals = []
    for j in J[i]:
        val = I_A[i] * (j*j) + I_B[i]
        vals.append(val)
    return vals

def permutation(lst):
    if len(lst) == 0:
        return []
    if len(lst) == 1:
        return [lst]

    l = []

    for i in range(len(lst)):
        m = lst[i]
        remLst = lst[:i] + lst[i + 1:]

        for p in permutation(remLst):
            l.append([m] + p)

    return l

def n_length_combo(lst, n, order_ref=False):
    if n == 0:
        return [[]]

    l = []
    for i in range(0, len(lst)):

        m = lst[i]
        if order_ref == False:
            remLst = lst[i:]
        else:
            remLst = lst[i + 1:]

        for p in n_length_combo(remLst, n - 1):
            l.append([m] + p)

    return l


# start
lines = []
count = 0
first_line = input()
first_line = [int(x) for x in first_line.split(' ')]
N = first_line[0]
M = first_line[1]
K = first_line[2]
del first_line


# input lines, varies by value of N
while (count < N):
    try:
        line = [int(x) for x in input().split(' ')]
        lines.append(line)
        count += 1
    except:
        break

I_A = [x[0] for x in lines]
I_B = [x[1] for x in lines]
I_C = [x[2] for x in lines]
J = [[a for a in range(1, x+1)] for x in I_C]
del lines


# count function values
f_values = []
for i in range(0, N):
    f_values.append(f_value(i))

del I_A, I_B, I_C, J


# make dictionary for reference
choices_sets = []
result_sets = []
i = 0
for i in range(0, len(f_values)):
    for j in range(0, len(f_values[i])):
        choices_sets.append((i,j))
        result_sets.append(f_values[i][j])

del f_values
f_value_dict = dict(zip(choices_sets, result_sets))
del choices_sets, result_sets


# list combinations
valid_sets = []
for group in n_length_combo([*f_value_dict], M):
    check_div = 0
    for set in group:
        check_div += f_value_dict[set]
    if check_div % K == 0:
        valid_sets.append(group)

del f_value_dict


# make permutations, since change order still count into valid result
valid_sets_check = []
for set in valid_sets:
    for p in permutation(set):
        valid_sets_check.append(p)

del valid_sets


# remove duplicates
final = []
for elem in valid_sets_check:
    if elem not in final:
        final.append(elem)

del valid_sets_check

print(len(final))

