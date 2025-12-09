# 7,1
# 11,1
# 11,7
# 9,7
# 9,5
# 2,5
# 2,3
# 7,3
with open("input.txt") as f:
    # Read the input into a list of (x, y) tuples
    points: list[tuple[int, int]] = []
    for line in f.readlines():
        x, y = map(int, line.strip().split(','))
        points.append((x, y))

# Part 1: Using two tiles as opposite corners, what is the largest area of any rectangle you can make?
def part1(points: list[tuple[int, int]]) -> int:
    max_area = 0
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            max_area = max(max_area, area)
    return max_area

with open("part1.txt", "w") as f:
    f.write(str(part1(points)))

# Part 2: Build the convex hull of the points. 
# Now using two tiles as opposite corners, what is the largest area of any rectangle you can make 
# such that the rectangle is fully contained within the convex hull?

# Too tired to implement computational geometry myself, so using external library instead
from shapely import Polygon
def part2(points: list[tuple[int, int]]) -> int:
    max_area = 0
    n = len(points)
    polygon = Polygon(points)
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            min_x = min(x1, x2)
            max_x = max(x1, x2)
            min_y = min(y1, y2)
            max_y = max(y1, y2)
            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if area <= max_area:
                continue
            rect_corners = [(min_x, min_y), (min_x, max_y), (max_x, max_y), (max_x, min_y)]
            rectangle = Polygon(rect_corners)
            if polygon.contains(rectangle):
                max_area = area
    return max_area

with open("part2.txt", "w") as f:
    f.write(str(part2(points)))