from typing import List

# Convert the compressed string to the uncompressed format
def uncompressed(s: str) -> List[int]:
    arr = []
    flip = True
    idx = 0
    for c in s:
        arr.append([idx if flip else -1] * int(c))
        flip = not flip
        if flip:
            idx += 1
    return [item for sublist in arr for item in sublist]

with open("input.txt", "r") as f:
    arr = list(uncompressed(f.read()))

l, r = 0, len(arr) - 1
while l < r:
    # Increase l until it points to '-1'
    while l < r and arr[l] != -1:
        l += 1
    # Decrease r until it points to a non '-1' character
    while l < r and arr[r] == -1:
        r -= 1
    # Swap the characters at l and r
    arr[l], arr[r] = arr[r], arr[l]
    l += 1
    r -= 1

ans = 0
for i in range(len(arr)):
    ans += i * arr[i] if arr[i] != -1 else 0

with open("part1.txt", "w") as f:
    f.write(str(ans))

# Part 2: Swap whole blocks of characters instead of individual characters
with open("input.txt", "r") as f:
    arr = list(uncompressed(f.read()))

r = len(arr) - 1
while r >= 0:
    # Decrease r until it points to a non '-1' character
    while r >= 0 and arr[r] == -1:
        r -= 1
    if r < 0:
        break
    nr = r
    # Decrease nr until it points to different character
    while nr >= 0 and arr[nr] == arr[r]:
        nr -= 1

    need = r - nr
    # Find the first empty block of characters
    l = 0
    while l < nr:
        # Increase l until it points to '-1'
        while l <= nr and arr[l] != -1:
            l += 1
        if l > nr:
            break
        nl = l
        # Increase nl until it points to a non '-1' character
        while nl < r and arr[nl] == -1:
            nl += 1
        free = nl - l
        # Swap arr[l:l+need] and arr[nr+1:r+1] if need <= free
        if need <= free:
            arr[l:l+need], arr[nr+1:r+1] = arr[nr+1:r+1], arr[l:l+need]
            break
        else:
            l = nl

    r = nr

ans = 0
for i in range(len(arr)):
    ans += i * arr[i] if arr[i] != -1 else 0

with open("part2.txt", "w") as f:
    f.write(str(ans))