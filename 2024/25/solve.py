from typing import List

W, H = 5, 7

locks = []
keys = []

with open("input.txt", "r") as f:
    # Read multiple 7 x 5 grids until EOF
    while True:
        grid = []
        for _ in range(H):
            grid.append(f.readline().strip())
        f.readline()
        if not grid[0]:
            break
        
        if grid[0] == "#" * W:
            # lock
            assert grid[-1] == "." * W
            arr = []
            for j in range(W):
                i = 0
                while grid[i][j] == "#":
                    i += 1
                arr.append(i)
            locks.append(arr)

        if grid[0] == "." * W:
            # key
            assert grid[-1] == "#" * W
            arr = []
            for j in range(W):
                i = 0
                while grid[i][j] == ".":
                    i += 1
                arr.append(H - i)
            keys.append(arr)

def check_fit(lock: List[int], key: List[int]) -> bool:
    for x, y in zip(lock, key):
        if x + y > H:
            return False
    return True

ans = 0
for lock in locks:
    for key in keys:
        if check_fit(lock, key):
            ans += 1

with open("part1.txt", "w") as f:
    f.write(str(ans))
        