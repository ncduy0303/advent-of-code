import sys
import numpy as np
import gurobipy as gp
from gurobipy import GRB

# 0:
# ###
# ##.
# ##.

# 1:
# ###
# ##.
# .##

# 2:
# .##
# ###
# ##.

# 3:
# ##.
# ###
# ##.

# 4:
# ###
# #..
# ###

# 5:
# ###
# .#.
# ###

# 4x4: 0 0 0 0 2 0
# 12x5: 1 0 1 0 2 2
# 12x5: 1 0 1 0 3 2
with open("input.txt") as f:
    sections = f.read().strip().split("\n\n")
    
    shapes = {}
    regions = []
    
    # Parse Shapes
    # Shapes are in the first N blocks, regions are the last block
    # We'll iterate through sections and identify them by content
    for section in sections:
        lines = section.strip().split('\n')
        header = lines[0]
        
        if ':' in header and not 'x' in header.split(':')[0]: 
            # It's a shape (e.g. "0:")
            shape_id = int(header.split(':')[0])
            grid = []
            for line in lines[1:]:
                row = [1 if c == '#' else 0 for c in line.strip()]
                grid.append(row)
            shapes[shape_id] = np.array(grid, dtype=int)
            
        elif 'x' in header.split(':')[0]: 
            # It's a list of regions (e.g. "12x5: ...")
            # This block might have multiple lines
            for line in lines:
                parts = line.split(':')
                dims = parts[0].split('x')
                width, height = int(dims[0]), int(dims[1])
                
                counts = list(map(int, parts[1].strip().split()))
                regions.append({
                    'width': width,
                    'height': height,
                    'counts': counts # counts[i] is number of shape i needed
                })
                
def get_unique_orientations(shape_grid: np.ndarray) -> list[np.ndarray]:
    """
    Generates all unique orientations (rotations/flips) of a shape.
    Returns a list of numpy arrays.
    """
    orientations = []
    seen = set()
    
    # Base shape
    base = shape_grid
    
    # 2 flips (original and flipped)
    flips = [base, np.flipud(base)]
    
    for f in flips:
        current = f
        for _ in range(4): # 4 rotations
            # Trim the shape to minimal bounding box (remove empty rows/cols)
            # though input implies standard shapes are usually tight.
            # Convert to tuple to hash
            h_tuple = tuple(map(tuple, current))
            if h_tuple not in seen:
                seen.add(h_tuple)
                orientations.append(current)
            current = np.rot90(current)
            
    return orientations

def solve_region(shapes: dict[int, np.ndarray], region_width: int, region_height: int, counts: list[int]) -> bool:
    """
    Returns True if the region can be tiled by the requested counts of shapes.
    """
    model = gp.Model("ChristmasTrees")
    model.setParam('OutputFlag', 0) # Silence output
    
    # 1. Precompute all valid placements (variables)
    # A placement is defined by: (shape_id, orientation_idx, row, col)
    
    placements = [] # List of (shape_id, grid_mask_coords)
    # grid_mask_coords is a list of (r,c) tuples that this placement covers
    
    # We only care about shapes that are actually requested (count > 0)
    for s_id, count in enumerate(counts):
        if count == 0:
            continue
            
        if s_id not in shapes:
            continue # Should not happen based on problem description
            
        shape_vars = get_unique_orientations(shapes[s_id])
        
        for shape_grid in shape_vars:
            h, w = shape_grid.shape
            
            # Sliding window over the region
            for r in range(region_height - h + 1):
                for c in range(region_width - w + 1):
                    # Calculate covered cells
                    covered_cells = []
                    for sr in range(h):
                        for sc in range(w):
                            if shape_grid[sr, sc] == 1:
                                covered_cells.append((r + sr, c + sc))
                    
                    placements.append({
                        'shape_id': s_id,
                        'cells': covered_cells
                    })

    # 2. Create Variables
    # x[i] = 1 if placement i is used
    x = model.addVars(len(placements), vtype=GRB.BINARY, name="x")
    
    # 3. Constraint: No Overlap
    # Map each grid cell to the list of placements that cover it
    grid_to_placements = {} # (r,c) -> list of placement indices
    
    for idx, p in enumerate(placements):
        for cell in p['cells']:
            if cell not in grid_to_placements:
                grid_to_placements[cell] = []
            grid_to_placements[cell].append(idx)
            
    for cell, placement_indices in grid_to_placements.items():
        model.addConstr(gp.quicksum(x[i] for i in placement_indices) <= 1, 
                        name=f"cell_{cell}")
        
    # 4. Constraint: Shape Counts
    # For each shape ID, sum of selected placements must equal required count
    placement_indices_by_shape = {}
    for idx, p in enumerate(placements):
        s_id = p['shape_id']
        if s_id not in placement_indices_by_shape:
            placement_indices_by_shape[s_id] = []
        placement_indices_by_shape[s_id].append(idx)
        
    for s_id, count in enumerate(counts):
        if count > 0:
            if s_id in placement_indices_by_shape:
                model.addConstr(gp.quicksum(x[i] for i in placement_indices_by_shape[s_id]) == count,
                                name=f"count_shape_{s_id}")
            else:
                # If we need a shape but have no valid placements for it (e.g. too big), infeasible
                return False

    # 5. Solve
    model.optimize()

    # Print the number of constraints and variables and trials
    print(f"Region {region_width}x{region_height} with counts {counts}:")
    print(f"Variables: {model.NumVars}, Constraints: {model.NumConstrs}")
    
    if model.Status == GRB.OPTIMAL:
        return True
    return False

with open("part1.txt", "w") as f:
    total = sum(1 for region in regions if solve_region(shapes, region['width'], region['height'], region['counts']))
    f.write(f"{total}\n")