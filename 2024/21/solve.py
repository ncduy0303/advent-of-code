from collections import deque, defaultdict
from typing import Tuple
from functools import cache

with open("input.txt") as f:
    queries = f.read().splitlines()

# Total number of states is about 5 x 5 x 11 x 10^3 = 275000 with 5 edges per state

# Define a map of transitions
dir2dir = {
    "^": {
        ">": "A",
        "v": "v",
    },
    "A": {
        "<": "^",
        "v": ">",
    },
    "<": {
        ">": "v",
    },
    "v": {
        "<": "<",
        "^": "^",
        ">": ">",
    },
    ">": {
        "<": "v",
        "^": "A",
    },
}
dir2key = {
    "0": {
        "^": "2",
        ">": "A",
    },
    "A": {
        "<": "0",
        "^": "3",
    },
    "1": {
        "^": "4",
        ">": "2",
    },
    "2": {
        "<": "1",
        "v": "0",
        ">": "3",
        "^": "5",
    },
    "3": {
        "<": "2",
        "v": "A",
        "^": "6",
    },
    "4": {
        "^": "7",
        ">": "5",
        "v": "1",
    },
    "5": {
        "<": "4",
        "v": "2",
        ">": "6",
        "^": "8",
    },
    "6": {
        "<": "5",
        "v": "3",
        "^": "9",
    },
    "7": {
        ">": "8",
        "v": "4",
    },
    "8": {
        "<": "7",
        "v": "5",
        ">": "9",
    },
    "9": {
        "<": "8",
        "v": "6",
    },
}

# BFS from the initial state
start = ("A", "A", "A", "")
dist = {start: 0}
que = deque([start])

def add_state(old_state: Tuple[str, str, str, str], new_state: Tuple[str, str, str, str]) -> None:
    if new_state not in dist:
        dist[new_state] = dist[old_state] + 1
        que.append(new_state)

while que:
    state = que.popleft()

    # <^>v transitions
    for k, v in dir2dir[state[0]].items():
        new_state = (v, state[1], state[2], state[3])
        add_state(state, new_state)

    # A transitions
    if state[0] != "A":
        if state[0] in dir2dir[state[1]]:
            new_state = (state[0], dir2dir[state[1]][state[0]], state[2], state[3])
        # print(state, new_state)
        add_state(state, new_state)
    elif state[1] != "A":
        if state[1] in dir2key[state[2]]:
            new_state = (state[0], state[1], dir2key[state[2]][state[1]], state[3])
            add_state(state, new_state)
    elif state[2] != "A":
        if len(state[3]) < 3:
            new_state = (state[0], state[1], state[2], state[3] + state[2])
            add_state(state, new_state)

# Find the answer
ans = 0
for query in queries:
    num = query[:3]
    ans += (dist[("A", "A", "A", num)] + 1) * int(num)

with open("part1.txt", "w") as f:
    f.write(str(ans))


# Part 2: Now there are 25 directional keyboards in between
# Change approach: instead of exhausing search from start, 
# just simulate each digit of the query directly 
# (note that it is optimal to always move either horizontally or vertically first before moving the other direction)
dir2pos = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}
key2pos = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}
all_moves = defaultdict(list)
for d1, p1 in dir2pos.items():
    for d2, p2 in dir2pos.items():
        if p1[0] == p2[0]:
            all_moves[(d1, d2)].append((">" if p2[1] > p1[1] else "<") * abs(p2[1] - p1[1]))
        elif p1[1] == p2[1]:
            all_moves[(d1, d2)].append(("v" if p2[0] > p1[0] else "^") * abs(p2[0] - p1[0]))
        else:
            if d1 == "<":
                all_moves[(d1, d2)].append(">" * (p2[1] - p1[1]) + "^" * (p1[0] - p2[0]))
            elif d2 == "<":
                all_moves[(d1, d2)].append("v" * (p2[0] - p1[0]) + "<" * (p1[1] - p2[1]))
            else:
                all_moves[(d1, d2)].append((">" if p2[1] > p1[1] else "<") * abs(p2[1] - p1[1]) + ("v" if p2[0] > p1[0] else "^") * abs(p2[0] - p1[0]))
                all_moves[(d1, d2)].append(("v" if p2[0] > p1[0] else "^") * abs(p2[0] - p1[0]) + (">" if p2[1] > p1[1] else "<") * abs(p2[1] - p1[1]))
        
for k1, p1 in key2pos.items():
    for k2, p2 in key2pos.items():
        if p1[0] == p2[0]:
            all_moves[(k1, k2)].append((">" if p2[1] > p1[1] else "<") * abs(p2[1] - p1[1]))
        elif p1[1] == p2[1]:
            all_moves[(k1, k2)].append(("v" if p2[0] > p1[0] else "^") * abs(p2[0] - p1[0]))
        else:
            if k1 in "0A" and k2 in "147":
                all_moves[(k1, k2)].append("^" * (p1[0] - p2[0]) + (">" if p2[1] > p1[1] else "<") * abs(p2[1] - p1[1]))
            elif k2 in "0A" and k1 in "147":
                all_moves[(k1, k2)].append(">" * (p2[1] - p1[1]) + "v" * (p2[0] - p1[0]))
            else:
                all_moves[(k1, k2)].append((">" if p2[1] > p1[1] else "<") * abs(p2[1] - p1[1]) + ("v" if p2[0] > p1[0] else "^") * abs(p2[0] - p1[0]))
                all_moves[(k1, k2)].append(("v" if p2[0] > p1[0] else "^") * abs(p2[0] - p1[0]) + (">" if p2[1] > p1[1] else "<") * abs(p2[1] - p1[1]))

@cache
def backtrack(seq: str, level: int) -> str:
    if level == 26:
        return len(seq)
    res = 0
    for i, c in enumerate(seq):
        moves = all_moves[("A" if i == 0 else seq[i - 1], c)]
        assert len(moves) == 1 or len(moves) == 2
        if len(moves) == 1:
            res += backtrack(moves[0] + "A", level + 1)
        else:
            res += min(backtrack(moves[0] + "A", level + 1), backtrack(moves[1] + "A", level + 1))
    return res

ans = 0
for query in queries:
    num = int(query[:3])
    ans += backtrack(query, 0) * num

with open("part2.txt", "w") as f:
    f.write(str(ans))