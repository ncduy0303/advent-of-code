import re

# [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
# [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
# [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}

# Part 1: Find the fewest numbers needed to reach the target xor sum
with open("input.txt") as f:
    # Convert the input into a list of tuples of (target xor sum, list of numbers)
    # The target xor sum is represented as binary string where '#' is 1 and '.' is 0 (in reverse order)
    data = []
    for line in f:
        pattern = re.search(r'\[([.#]+)\]', line)
        assert pattern is not None
        binary_str = pattern.group(1).replace('#', '1').replace('.', '0')
        target_xor = int(binary_str[::-1], 2)

        groups = re.findall(r'\((?:\d+,?)+\)', line)
        number_list = []
        for g in groups:
            bits = list(map(int, g[1:-1].split(',')))
            number = sum(1 << pos for pos in bits)
            number_list.append(number)

        data.append((target_xor, number_list))

def part1(data: list[tuple[int, list[int]]]) -> int:
    total_count = 0
    for target_xor, number_list in data:
        dp = {0: 0}  # xor_sum -> min count
        for number in number_list:
            new_dp = dp.copy()
            for xor_sum, count in dp.items():
                new_xor = xor_sum ^ number
                if new_xor not in new_dp or new_dp[new_xor] > count + 1:
                    new_dp[new_xor] = count + 1
            dp = new_dp
        assert target_xor in dp
        total_count += dp[target_xor]
    return total_count
    
with open("part1.txt", "w") as f:
    f.write(str(part1(data)))

# Part 2: Find the fewest numbers needed to reach the target array
with open("input.txt") as f:
    # Convert the input into a list of tuples of (target array sum, list of arrays)
    # For example, the target array sum is {3,5,4,7}, meaning the target value is [3,5,4,7]
    # Each array in the list is represented as a one-hot encoded integer, where the i-th bit is 1 if the i-th element is present
    # Each array in the list can be used multiple times, so we need to find the minimum count of arrays to reach the target array sum
    
    # Model the problem as ILP and solve using gurobi

    import gurobipy as gp
    from gurobipy import GRB

    data = []
    for line in f:
        pattern = re.search(r'\{([\d,]+)\}', line)
        assert pattern is not None
        target_values = list(map(int, pattern.group(1).split(',')))
        target_len = len(target_values)

        groups = re.findall(r'\((?:\d+,?)+\)', line)
        array_list = []
        for g in groups:
            bits = list(map(int, g[1:-1].split(',')))
            array = [0] * target_len
            for pos in bits:
                array[pos] = 1
            array_list.append(array)

        data.append((target_values, array_list))

def part2(data: list[tuple[list[int], list[list[int]]]]) -> int:
    total_count = 0
    for target_values, array_list in data:
        target_len = len(target_values)
        num_arrays = len(array_list)

        model = gp.Model()
        x = model.addVars(num_arrays, vtype=GRB.INTEGER, name="x")

        # Constraints: for each position in the target array, ensure the sum matches the target value
        for j in range(target_len):
            model.addConstr(
                gp.quicksum(array_list[i][j] * x[i] for i in range(num_arrays)) == target_values[j],
                name=f"c{j}"
            )

        # Objective: minimize the total count of arrays used
        model.setObjective(gp.quicksum(x[i] for i in range(num_arrays)), GRB.MINIMIZE)

        model.optimize()

        assert model.status == GRB.OPTIMAL
        total_count += int(model.objVal)
    return total_count

with open("part2.txt", "w") as f:
    f.write(str(part2(data)))