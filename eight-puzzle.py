import heapq
import time
import threading
from copy import deepcopy as dcp

file = input()
f = open(file,"r")
tmp = f.readline()
n = len(tmp.split())
matrix = (tmp + f.read()).split()
name = "Nazeri"

class node:
    def __init__(self):
        self.arr = []
        self.score = 0
        self.star = (-1,-1)
        self.swap = 0

    def print(self):
        for i in self.arr:
            for j in i:
                print(j,end=" ")
            print()
    
    def copy(self):
        b = node()
        b.arr = self.arr.copy()
        return b
    
    def __eq__(self, other):
        return (self.score > other.score)

    def __lt__(self, other):
        return (self.score < other.score)

    def __gt__(self, other):
        return (self.score > other.score)

    def write(self):
        f = open(f'Log_{file[:-4]}_{name}.txt', "a")
        for i in self.arr:
            for j in i:
                f.write(f"{j}")
                f.write(" ")
            f.write('\n')
        f.write('\n')
        f.close()

def is_seen(a: node, b: node):
    for i in range(n):
        for j in range(n):
            if a.arr[i][j] != b.arr[i][j] :
                return False     
    return True

def swap(s: node, direction: int):
    star_x = s.star[0]
    star_y = s.star[1]
    if direction == 0 :
        if star_y == 0 :
            s.swap = 1
            return s
        tmp = s.arr[star_x][star_y]
        s.arr[star_x][star_y] = s.arr[star_x][star_y-1]
        s.arr[star_x][star_y-1] = tmp
    elif direction == 1 :
        if star_x == n-1 :
            s.swap = 1
            return s
        tmp = s.arr[star_x][star_y]
        s.arr[star_x][star_y] = s.arr[star_x+1][star_y]
        s.arr[star_x+1][star_y] = tmp
    elif direction == 2 :
        if star_y == n-1 :
            s.swap = 1
            return s
        tmp = s.arr[star_x][star_y]
        s.arr[star_x][star_y] = s.arr[star_x][star_y+1]
        s.arr[star_x][star_y+1] = tmp
    else:
        if star_x == 0 :
            s.swap = 1
            return s
        tmp = s.arr[star_x][star_y]
        s.arr[star_x][star_y] = s.arr[star_x-1][star_y]
        s.arr[star_x-1][star_y] = tmp
    return s

def check(state: node):
    flag = True
    for i in range(n):
        for j in range(n):
            if '*' in state.arr[i][j]:
                state.star = (i , j)
                if flag == False:
                    return False
            if final.arr[i][j] != state.arr[i][j] :
                flag =  False
    return flag

def check_thread(a: node, b: node):
    tmp = node()
    for i in seen:
        if is_seen(b,i):
            tmp = dcp(i)
            return (tmp,True)
    for j in seen_thread:
        if is_seen(a,j):
            tmp = dcp(j)
            return (tmp,True)
    return (tmp,False)

def cal_score3(state: node, nn: int):
    res = 0
    if nn:
        for i in range(n):
            for j in range(n):
                if '*' in state.arr[i][j]:
                    continue
                tmp = dic_final[state.arr[i][j]]
                res += abs(tmp[0]-i)+abs(tmp[1]-j)
    else:
        for i in range(n):
            for j in range(n):
                if '*' in state.arr[i][j]:
                    continue
                tmp = dic_start[state.arr[i][j]]
                res += abs(tmp[0]-i)+abs(tmp[1]-j)
    state.score = res

def cal_score(state: node, nn: int):
    res = 0
    if nn:
        for i in range(n):
            for j in range(n):
                if '*' in state.arr[i][j]:
                    continue
                if state.arr[i][j] == final.arr[i][j]:
                    if i == 0 or i == n-1 or j == 0 or j == n-1:
                        res -= 3
                    else:
                        res -= 2
                else:
                    tmp = dic_final[state.arr[i][j]]
                    res += abs(tmp[0]-i)+abs(tmp[1]-j)
    else:
        for i in range(n):
            for j in range(n):
                if '*' in state.arr[i][j]:
                    continue
                if state.arr[i][j] == first.arr[i][j]:
                    if i == 0 or i == n-1 or j == 0 or j == n-1:
                        res -= 3
                    else:
                        res -= 2
                else:
                    tmp = dic_start[state.arr[i][j]]
                    res += abs(tmp[0]-i)+abs(tmp[1]-j)
    state.score = res

def cal_score3_2(state: node):
    res = 0
    for i in range(n):
        for j in range(n):
            if '*' in state.arr[i][j]:
                continue
            if state.arr[i][j] == final.arr[i][j]:
                res -= abs(n-2)
            else:
                tmp = dic_final[state.arr[i][j]]
                res += abs(tmp[0]-i)*1.1+abs(tmp[1]-j)
    state.score = res

def dgstr(state: node, seen: list, pre_nodes: list, thread_num: int):
    if thread_num:
        if check(state):
            return True
    else:
        flag = False
        for i in range(n):
            for j in range(n):
                if '*'in state.arr[i][j]:
                    state.star = (i,j)
                    flag = True
                    break
            if flag:
                break

    for i in range(4):
        new_state = dcp(state)
        new_state = swap(new_state, i)
        if new_state.swap == 1:
            continue
        flag = False
        for z in seen :
            if is_seen(z,new_state):
                flag = True
                break
            
        if flag == True:
            continue

        cal_score(new_state, thread_num)

        if thread_num:
            heapq.heappush(q,(new_state.score, new_state))            
        else:
            heapq.heappush(q_thread,(new_state.score, new_state))
        tmp = (state, new_state)
        pre_nodes.append(tmp)
    
    if thread_num:
        return False

def find_pre(s: node, pre_nodes: list):
    for i in pre_nodes:
        if is_seen(i[1],s):
            return i[0]

first = node()
final = node()

pre_nodes = []
seen = []
q = []
dic_final = {}

for i in range(n):
    tmp_arr = []
    for j in range(n):
        tmp_arr.append(matrix.pop(0))
    first.arr.append(tmp_arr.copy())

tmp_arr = []
for i in range(n):
    tmp_arr = []
    for j in range(n):
        tmp_arr.append(matrix.pop(0))
    final.arr.append(tmp_arr.copy())

for i in range(n):
    for j in range(n):
        dic_final[final.arr[i][j]] = (i, j)

cal_score(first, 1)
heapq.heappush(q,(first.score,first))

# Dijkstra starts here
st = time.time()
while q.count:
    new_state = node()
    new_state = heapq.heappop(q)
    seen.append(new_state[1])

    tmp = dgstr(new_state[1], seen, pre_nodes, 1)
    if tmp:
        break

current_state = final
res = []
while(1):
    current_state = find_pre(current_state, pre_nodes)
    if is_seen(first , current_state):
        break
    res.append(current_state)

# end of process
# save to a file
et = time.time()

f = open(f'Log_{file[:-4]}_{name}.txt', "w")
f.write(f"{file} \n \n")
f.write(f"Dijkstra: \n")
f.write(f"time {et - st}\n")
f.write(f"Act {len(res)}\n\n")
f.close()
for i in range(len(res)-1,-1,-1):
    res[i].write()

###########################
# bidirectional starts here

found = node()
dic_start = {}
q_thread = []
seen_thread = []
pre_nodes_thread = []

for i in range(n):
    for j in range(n):
        dic_start[first.arr[i][j]] = (i, j)

cal_score(final, 0)
heapq.heappush(q_thread,(final.score,final))
heapq.heappush(q,(first.score,first))

st = time.time()
while q.count != 0 and q_thread.count != 0:
    new_state = node()
    new_state = heapq.heappop(q)

    new_state_2 = node()
    new_state_2 = heapq.heappop(q_thread)

    seen.append(new_state[1])
    seen_thread.append(new_state_2[1])

    tmp = check_thread(new_state[1], new_state_2[1])
    if tmp[1]:
        found = tmp[0]
        break

    x = threading.Thread(target=dgstr, args=(new_state_2[1], seen_thread, pre_nodes_thread, 0,))
    x.start()  
    tmp = dgstr(new_state[1], seen, pre_nodes, 1)
    x.join()

current_state = found
res = []
if is_seen(found,first) != True:
    while(1):
        current_state = find_pre(current_state, pre_nodes)

        if is_seen(first , current_state):
            break
        res.append(current_state)

    res.reverse()
    if is_seen(found,final) != True:
        res.append(found)


if is_seen(found,final) != True:
    current_state = found
    while(1):
        current_state = find_pre(current_state, pre_nodes_thread)

        if is_seen(final , current_state):
            break
        res.append(current_state)

# end of process
# save to a file
et = time.time()

f = open(f'Log_{file[:-4]}_{name}.txt', "a")
f.write(f"Bidirectional: \n")
f.write(f"time {et - st}\n")
f.write(f"Act {len(res)}\n\n")
f.close()
for i in range(len(res)):
    res[i].write()
