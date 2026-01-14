# aaa: you hhh
# you: bbb ccc
# bbb: ddd eee
# ccc: ddd eee fff
# ddd: ggg
# eee: out
# fff: out
# ggg: out
# hhh: ccc fff iii
# iii: out
with open("input.txt") as f:
    # Read the input into an adjacency list for the graph
    graph = {}
    for line in f:
        node, neighbors = line.strip().split(": ")
        graph[node] = neighbors.split(" ")

from functools import cache

# Part 1: How many different paths lead from "you" to "out"?
@cache
def count_paths(current: str, target: str) -> int:
    if current == target:
        return 1
    total_paths = 0
    for neighbor in graph.get(current, []):
        total_paths += count_paths(neighbor, target)
    return total_paths

with open("part1.txt", "w") as f:
    f.write(str(count_paths("you", "out")))

# Part 2: Find all of the paths that lead from "svr" to "out". How many of those paths visit both "dac" and "fft"?
with open("part2.txt", "w") as f:
    f.write(str(
        count_paths("svr", "dac") * count_paths("dac", "fft") * count_paths("fft", "out") +
        count_paths("svr", "fft") * count_paths("fft", "dac") * count_paths("dac", "out")
    ))
