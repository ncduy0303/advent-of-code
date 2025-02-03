import re
from collections import deque

class Node:
    def __init__(self, gate: str):
        self.gate = gate
        self.inputs = []
        self.input_names = []

    def add_input(self, x: int, name: str):
        self.inputs.append(x)
        self.input_names.append(name)

    def get_output(self):
        assert 1 <= len(self.inputs) <= 2

        if len(self.inputs) == 1:
            return self.inputs[0]

        if len(self.inputs) == 2:
            if self.gate == "AND":
                return self.inputs[0] & self.inputs[1]
            elif self.gate == "OR":
                return self.inputs[0] | self.inputs[1]
            elif self.gate == "XOR":
                return self.inputs[0] ^ self.inputs[1]

        assert False

initial_pattern = re.compile(r"(.+): ([01])")
gate_pattern = re.compile(r"(.+) (AND|OR|XOR) (.+) -> (.+)")

with open("input1.txt", "r") as f:
    initial_states = [initial_pattern.match(line).groups() for line in f]

with open("input2_fixed.txt", "r") as f:
    gates = [gate_pattern.match(line).groups() for line in f]

str2idx = {}
nodes = []
queue = deque()

for name, value in initial_states:
    str2idx[name] = len(str2idx)
    node = Node("INIT")
    node.add_input(int(value), name)
    nodes.append(node)
    queue.append(str2idx[name])

for in_1, gate, in_2, out in gates:
    if out not in str2idx:
        str2idx[out] = len(str2idx)
        nodes.append(Node(gate))

n = len(nodes)
adj = [[] for _ in range(n)]
for in_1, gate, in_2, out in gates:
    adj[str2idx[in_1]].append(str2idx[out])
    adj[str2idx[in_2]].append(str2idx[out])

idx2str = {v: k for k, v in str2idx.items()}

name_dct = {
    "bmc": "c01",
    "kmn": "c02",
    "shk": "c03",
    "tmr": "c04",
    "kfh": "c05",
    "rvc": "c06",
    "rgc": "c07",
    "ddq": "c08",
    "dfm": "c09",
    "cft": "c10",
    "mnh": "c11",
    "pgq": "c12",
    "pqc": "c13",
    "phn": "c14",
    "pfg": "c15",
    "bfg": "c16",
    "mtg": "c17",
    "frj": "c18",
    "gnd": "c19",
    "nnt": "c20",
    "vgj": "c21",
    "pgt": "c22",
    "ktp": "c23",
    "gvs": "c24",
    "pmm": "c25",
    "rtm": "c26",
    "vdb": "c27",
    "psj": "c28",
    "msm": "c29",
    "djr": "c30",
    "vdd": "c31",
    "chd": "c32",
    "nng": "c33",
    "rrf": "c34",
    "wpv": "c35",
    "rcd": "c36",
    "brm": "c37",
    "qwj": "c38",
    "gqg": "c39",
    "qbf": "c40",
    "bqd": "c41",
    "kmm": "c42",
    "gpq": "c43",
}
for k, v in name_dct.items():
    str2idx[v] = str2idx[k]
    idx2str[str2idx[k]] = v

while queue:
    u = queue.popleft()
    node = nodes[u]
    for v in adj[u]:
        nodes[v].add_input(node.get_output(), idx2str[u])
        if len(nodes[v].inputs) == 2:
            # Change the name of node v to the output name
            if nodes[v].input_names[0].startswith("x") or nodes[v].input_names[0].startswith("y"):
                name = f"({nodes[v].input_names[0]}_{nodes[v].gate}_{nodes[v].input_names[1]})"
                idx2str[v] = name
                str2idx[name] = v
            print(f"{nodes[v].input_names[0]} {nodes[v].gate} {nodes[v].input_names[1]} -> {idx2str[v]}")
            queue.append(v)

end_keys = [key for key in sorted(str2idx.keys()) if key.startswith("z")]
end_values = [nodes[str2idx[key]].get_output() for key in end_keys]

ans = "".join(str(x) for x in end_values)
ans = int(ans[::-1], 2)

with open("part1.txt", "w") as f:
    f.write(str(ans))

# Part 2: Find 4 pairs of wires to swap to make the binary adder works
# Use manual inspection with understanding of how the full adder circuit works

# Swap z07 with swt
# Swap z13 with pqc
# Swap z31 with bgs
# Swap x24_AND_y24 and x24_XOR_y24 (or swap rjm with wsv)

ans = ["z07", "swt", "z13", "pqc", "z31", "bgs", "rjm", "wsv"]
ans = ",".join(sorted(ans))

with open("part2.txt", "w") as f:
    f.write(ans)
