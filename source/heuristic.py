#!/usr/bin/env python
import sys
import timeit
import random
# configs
data = 'nonograms_2.txt'
show_output = True
num_of_nono_to_solve = 200
# when depth is 1, will switch in round-robin fashion between most constrained and most
# constraining heuristic, use other number will switch every time when 
# that number of recursions reached
depth_control = 1
'--------------------------------------------------'
heuristic_switch = []

def permutate(seg, space):
    if not seg or seg== [[]]:
        return [['_']*space]
    ret = []
    for x in xrange(1, space-len(seg)+2):
        for last in permutate(seg[1:], space - x):
            ret.append(['_']*x+seg[0]+last)
    return ret

def compare(a,b):
    for i,v in enumerate(a):
        if v != b[i]:
            return False
    return True

def propagate(a_list, size, count):
    done = False
    columns = a_list[size:]
    rows = a_list[:size]
    while not done:
        pre_col = list(columns)
        pre_row = list(rows)
        for row_index, row in enumerate(rows):
            if len(row) == 1:
                # loop through cols(each chars)
                for char_index, char in enumerate(row[0]):
                    tmp = []
                    # test if chars matchs
                    for col in columns[char_index]:
                        if col[row_index] == char:
                            tmp.append(col)
                    if len(tmp) == 0:
                        return True
                    columns[char_index] = tmp
        for col_index, col in enumerate(columns):
            if len(col) == 1:
                # loop through each chars
                for char_index, char in enumerate(col[0]):
                    tmp = []
                    # test if chars matchs
                    for row in rows[char_index]:
                        if row[col_index] == char:
                            tmp.append(row)
                    if len(tmp) == 0:
                        return True
                    rows[char_index] = tmp
        if compare(rows,pre_row) and compare(columns, pre_col):
            break

    for index, var in enumerate(a_list):
        if index>size-1:
            a_list[index] = columns[index-size]
        else:
            a_list[index] = rows[index]
    return False


def heuristic(a_list, size, condition=None, random_heuristic=False):
    """Change the random flag to use random heuristic"""
    if random_heuristic:
        return random.choice([i for i,var in enumerate(a_list) 
                                if len(var)>1])
    start = len(a_list[0])
    for i,var in enumerate(a_list):
        if len(var)>1 and condition(len(var),start) and i<size:
            start = i
    return start

def csp(a_list, size, count):
    """switch between heuristics"""
    if count - heuristic_switch[0] > depth_control:
        heuristic_switch[0] = count
        # use most constraining
        condition = lambda x,y: x>y  
    else:
        # use most contrained
        condition = lambda x,y: x<y
    index = heuristic(a_list, size, condition)
    flag = False
    for v in a_list[index]:
        a_list_copy = []
        for a_l in a_list:
            a_list_copy.append(list(a_l))
        a_list_copy[index] = [v]
        back_track = propagate(a_list_copy, size, count)
        if not back_track:
            unique = True
            for e,x in enumerate(a_list_copy):
                if len(x) > 1 and e<size:
                    unique = False
                    break
            if unique:
                if show_output:
                    nice_print(a_list_copy, size)
                return True
            flag = csp(a_list_copy, size, count+1)
            if flag:
                break
    return flag

def nice_print(board, size):
    print len(board)
    for i,x in enumerate(board):
        if i < size:
            print ''.join(x[0])

def plain_print(nested):
    for row in nested:
        print row

def solve(row_constrain, col_constrain, size):
    row = [map(int, row.split(' ')) for row in row_constrain]
    constrain = [map(int, col.split(' ')) for col in col_constrain]
    row_size, col_size =  size.strip().split(' ')
    s = timeit.default_timer()
    heuristic_switch.append(0)
    try:
        a_list = []
        for r in row:
            l = permutate([['*'] * i for i in r], 
                int(col_size) + 1 - sum(r))
            a_list.append(map(lambda x:x[1:], l))
        for r in constrain:
            l = permutate([['*'] * i for i in r], 
                int(col_size) + 1 - sum(r))
            a_list.append(map(lambda x:x[1:], l))
        csp(a_list, int(row_size), 0)
        run_time = timeit.default_timer() - s
        heuristic_switch.pop()
        if show_output:
            print 'run time:',run_time
        return run_time
    except KeyboardInterrupt:
        sys.exit()
    print 'no solution' 

def read_board(config):
    size = next(config, None)
    count = 0
    run_times = []
    while size:
        count+=1
        row, col = size.strip().split(' ')
        row_constrain, col_constrain = [], []
        for i in range(int(row)):
            row_constrain.append(next(config).strip())
        for i in range(int(col)):
            col_constrain.append(next(config).strip())
        run_times.append(solve(row_constrain, col_constrain, size))
        if show_output:
            print '---line-split----'
        size = next(config, None)
        if size == '\n':
            size = next(config, None)
        if count == num_of_nono_to_solve:
            print 'solved: %d nonos' % num_of_nono_to_solve
            break
    print 'avg run time:',sum(run_times)/num_of_nono_to_solve

def main():
    sys.setrecursionlimit(15000)
    with open(data, 'r') as f:
        config =filter(lambda x:not x.startswith('#'), 
                    f.readlines())
    read_board(i for i in config)
            
if __name__ == '__main__':
    main()
