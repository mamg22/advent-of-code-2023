from collections.abc import Sequence
import operator
from typing import Callable, Self, Optional, NamedTuple, TypeAlias


COMPARE_FUNCS = {
    '>': operator.gt,
    '<': operator.lt,
}


Part: TypeAlias = dict[str, int]


class Rule:
    class RuleCondition(NamedTuple):
        category: str
        compare: Callable[[int, int], bool]
        argument: int

        def __repr__(self):
            return f"{self.category}({self.compare.__name__}){self.argument}"


    target: str
    condition: Optional[RuleCondition]


    def __init__(self: Self, step_str: str) -> None:
        if ':' not in step_str:
            self.target = step_str
            self.condition = None
        else:
            condition_str, target = step_str.split(':')

            category = condition_str[0]
            compare = COMPARE_FUNCS[condition_str[1]]
            argument = int(condition_str[2:])

            self.target = target
            self.condition = self.RuleCondition(category, compare, argument)
    
    def __repr__(self: Self) -> str:
        if self.condition:
            return f"{self.__class__.__name__}({repr(self.condition)}:{self.target})"
        else:
            return f"{self.__class__.__name__}({self.target})"

    def apply(self: Self, part: dict[str, int]) -> Optional[str]:
        if self.condition:
            applicable = self.condition.compare(part[self.condition.category], self.condition.argument)
            return self.target if applicable else None 
        else:
            return self.target


class Workflow:
    name: str
    rules: Sequence[Rule]

    def __init__(self: Self, name: str, rules: Sequence[Rule]) -> None:
        self.name = name
        self.rules = rules
    
    def __repr__(self: Self) -> str:
        return f"{self.__class__.__name__}({self.name}: {self.rules})"
    
    def apply(self: Self, part: dict[str, int]):
        for rule in self.rules:
            if target := rule.apply(part):
                return target
        else:
            raise ValueError("Invalid workflow")


def split_data(data: Sequence[str]) -> tuple[Sequence[str], Sequence[str]]:
    split_point = data.index('')

    workflow_data = data[:split_point]
    part_data = data[split_point + 1:]

    return workflow_data, part_data


def parse_workflow(line: str) -> Workflow:
    body_start = line.index('{')
    name, body = line[:body_start], line[body_start + 1:-1]

    rules = [Rule(statement) for statement in body.split(',')]

    return Workflow(name, rules)


def parse_part(line: str) -> Part:
    body = line[1:-1].split(',')

    part = {
        category: int(value)
        for category, value
        in map(lambda e: e.split('=', 1), body)
    }
    
    return part


def parse_data(data: Sequence[str]) -> tuple[dict[str, Workflow], list[Part]]:
    workflow_data, part_data = split_data(data)

    workflows = {
        workflow.name: workflow
        for workflow
        in map(parse_workflow, workflow_data)
    }
    parts = [parse_part(line) for line in part_data]  

    return workflows, parts


def process_part(part: Part, workflows: dict[str, Workflow]) -> str:
    next_workflow = 'in'

    while next_workflow in workflows:
        workflow = workflows[next_workflow]
        next_workflow = workflow.apply(part)

    return next_workflow

def solve_part1(data: Sequence[str]) -> int:
    workflows, parts = parse_data(data)

    total = 0
    for part in parts:
        result = process_part(part, workflows)
        if result == 'A':
            total += sum(part.values())

    return total


class Interval:
    low: Part
    high: Part
    target: str

    def __init__(self, low: Part, high: Part, target: str) -> None:
        self.low = low
        self.high = high
        self.target = target


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.low)}, {repr(self.high)}, {repr(self.target)})"


def sum_accepted(interval: Interval) -> int:
    size = 1
    for a, b in zip(interval.low.values(), interval.high.values()):
        size *= b - a + 1
    
    return size


def solve_part2(data: Sequence[str]) -> int:
    workflows, _ = parse_data(data)

    intervals = [
        Interval(
            {"x": 1, "m": 1, "a": 1, "s": 1},
            {"x": 4000, "m": 4000, "a": 4000, "s": 4000},
            'in'
        )
    ]

    total = 0

    while intervals:
        interval = intervals.pop()

        if interval.target in ('A', 'R'):
            if interval.target == 'A':
                total += sum_accepted(interval)

            continue

        workflow = workflows[interval.target]

        for rule in workflow.rules:
            if not rule.condition:
                intervals.append(Interval(interval.low, interval.high, rule.target))
                break

            midpoint_low = interval.high.copy()
            midpoint_high = interval.low.copy()

            if rule.condition.compare is operator.lt:
                midpoint_low[rule.condition.category] = rule.condition.argument - 1
                midpoint_high[rule.condition.category] = rule.condition.argument

                intervals.append(Interval(interval.low, midpoint_low, rule.target))
                interval.low = midpoint_high
            else:
                midpoint_low[rule.condition.category] = rule.condition.argument
                midpoint_high[rule.condition.category] = rule.condition.argument + 1

                intervals.append(Interval(midpoint_high, interval.high, rule.target))
                interval.high = midpoint_low

    return total


def main() -> None:
    with open("input/day19.txt", 'r') as data_file:
        data: list[str] = data_file.read().splitlines()

    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))


if __name__ == '__main__':
    main()