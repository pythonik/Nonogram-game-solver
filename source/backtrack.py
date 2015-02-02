#!/usr/bin/env python
import sys
import timeit
data = 'nonograms_2.txt'
show_output = True
num_of_nono_to_solve = 50
stop = []
node_count = []
def permutate(seg, space):
    if not seg or seg== [[]]:
        return [['_']*space]
    ret = []
    for x in xrange(1, space-len(seg)+2):
        for last in permutate(seg[1:], space - x):
            ret.append(['_']*x+seg[0]+last)
    return ret

def dfs(rules, tree, col_size, count):
    if not partial_check(tree, stop[0], 10):
        return False
    if len(rules) == 0:
        if check(tree, stop[0], count):
            return True
        return False
    ret = False
    for x in permutate([['*'] * i for i in rules[0]], col_size + 1 - sum(rules[0])):
        count+=1
        tree.append(x[1:])
        if dfs(list(rules[1:]), list(tree), col_size, count):
            ret = True
            break
        tree.pop()
    return ret

def convert(l):
    l.append('_')
    count = 0
    t = []
    for e in l:
        if e == '*':
            count = count + 1
        elif count > 0:
            t.append(count)
            count = 0 
    if len(t) == 0:
        t = [0]
    return t  

def partial_check(tree, constrain, row_size):
    if len(tree) == 0:
        return True
    index = 0
    new_tree = map(list, zip(*[i for i in tree]))
    for el in new_tree:
        current = [len(segment) for segment in ''.join(el).split('_') 
                                    if len(segment)>0]
        constrain_len = len(constrain[index])
        current_len = len(current)
        fail_condition_one = current_len > constrain_len
        fail_condition_three = (constrain_len == current_len) and (constrain_len == 1) and current[0]>constrain[index][0]
        if fail_condition_three or fail_condition_one:
            return False
        if current_len <= constrain_len and constrain_len > 1:
            for i,v in enumerate(current[:-1]):
                if v != constrain[index][i]:
                    return False
            if current_len > 0 and (current[current_len-1] > constrain[index][current_len-1]):
                return False
        if sum(current) > sum(constrain[index]):
            return False
        if current_len == 1 and current[0] > constrain[index][0]:
            return False
        index += 1
    return another_partial_check(tree)

def another_partial_check(tree):
    t = map(list, zip(*tree))
    for i,v in enumerate(t):
        found = False
        for v1 in stop[1][i]:
            if v1.startswith(''.join(v)):
                found = True
                break
        if not found:
            return False
    return True

def nice_print(board):
    for x in board:
        print ''.join(x)

def check(board, constrain, count):
    t = map(list, zip(*board))
    for i,row in enumerate(constrain):
        if row != convert(t[i]):
            return False
    print 'node_count:',count
    node_count.append(count)
    nice_print(board)
    return True

def plain_print(nested):
    for row in nested:
        print row

def solve(row_constrain, col_constrain, size):
    row = [map(int, row.split(' ')) for row in row_constrain]
    constrain = [map(int, col.split(' ')) for col in col_constrain]
    row_size, col_size =  size.strip().split(' ')
    s = timeit.default_timer()
    all_possible_cols = []
    for r in constrain:
        l = permutate([['*'] * i for i in r], 
                int(col_size) + 1 - sum(r))
        all_possible_cols.append(map(lambda x:''.join(x[1:]), l))
    tree = []
    try:
        stop.append(constrain)
        stop.append(all_possible_cols)
        dfs(row, tree, int(col_size), 0)
        stop.pop()
        stop.pop()
        run_time = timeit.default_timer() - s
        if show_output:
            print 'run time:', run_time
        return run_time
    except KeyboardInterrupt:
        nice_print(tree)
        sys.exit()

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
    print 'avg node count:',sum(node_count)/num_of_nono_to_solve

def main():
    with open(data, 'r') as f:
        config =filter(lambda x:not x.startswith('#'), 
                    f.readlines())
    read_board(i for i in config)
            
if __name__ == '__main__':
    main()
