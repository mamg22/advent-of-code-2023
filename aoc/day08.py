from enum import Enum
import itertools
import math

class Direction(Enum):
    left = 'L'
    right = 'R'


class Node:
    def __init__(self, name: str, left: str, right: str):
        self.name = name
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"Node({self.name}, ({self.left}, {self.right}))"


def extract_info(data: list[str]) -> tuple[list[str], dict[str, Node]]:
    instructions_str: str = data[0]
    node_list: list[str] = data[2:]

    instructions: list[str] = list(instructions_str)

    nodes: dict[Node] = {}
    for node_line in node_list:
        node_name, node_leaves = node_line.split(" = ")
        left_node, right_node = node_leaves.strip("()").split(", ")

        nodes[node_name] = Node(node_name, left_node, right_node)
    
    return instructions, nodes


def next_node(nodes: list[Node], current_node: Node, direction: str):
    if direction == Direction.left.value:
        return nodes[current_node.left]
    elif direction == Direction.right.value:
        return nodes[current_node.right]
    else:
        raise ValueError(f"Invalid Direction {direction}")


def solve_part1(data: list[str]) -> int:
    instructions, nodes = extract_info(data)

    current_node = nodes['AAA']
    steps = 0
    for direction in itertools.cycle(instructions):
        current_node = next_node(nodes, current_node, direction)
        steps += 1

        if current_node.name == 'ZZZ':
            break
    
    return steps


def solve_part2(data: list[str]) -> int:
    instructions, nodes = extract_info(data)

    starting_points = filter(lambda node_name: node_name.endswith('A'), nodes)

    branches = [nodes[start] for start in starting_points]
    branch_steps = []

    for branch in branches:
        steps = 0
        
        for direction in itertools.cycle(instructions):
            branch = next_node(nodes, branch, direction)
            steps += 1

            if branch.name.endswith('Z'):
                branch_steps.append(steps)
                break
    
    return math.lcm(*branch_steps)


def main():
    with open("input/day08.txt", 'r') as data_file:
        data: list[str] = data_file.read().splitlines()

    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))


if __name__ == '__main__':
    main()