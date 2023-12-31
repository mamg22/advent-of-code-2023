from abc import ABC, abstractmethod
from collections.abc import Sequence
from collections import Counter, deque
from functools import reduce
from itertools import chain, count
from math import lcm
import operator
from typing import Optional, Self


class Pulse:
    value: bool
    source: 'Module'
    target: 'Module'

    def __init__(self: Self, value: bool, source: 'Module', target: 'Module'):
        self.value = value
        self.source = source
        self.target = target
    
    def __repr__(self: Self) -> str:
        class_name = self.__class__.__name__

        return f"{class_name}({self.value}, source={self.source}, target={self.target})"


class Module(ABC):
    name: str
    outputs: list[Self]
    inputs: list[Self]

    def __init__(self: Self, name: str) -> None:
        self.name = name
        self.outputs = []
        self.inputs = []


    def add_output(self: Self, output: Self) -> None:
        self.outputs.append(output)
    

    def add_input(self: Self, source: Self) -> None:
        self.inputs.append(source)

    @abstractmethod
    def dispatch_pulse(self: Self, pulse: Pulse) -> list[Pulse]:
        raise NotImplementedError()

    
    def __repr__(self: Self) -> str:
        return f"{self.__class__.__name__}({self.name})"


class Broadcaster(Module):
    def dispatch_pulse(self: Self, pulse: Pulse) -> list[Pulse]:
        return [Pulse(pulse.value, self, output) for output in self.outputs]
    

class FlipFlop(Module):
    state: bool

    def __init__(self: Self, name: str) -> None:
        super().__init__(name)
        self.state = False
    

    def dispatch_pulse(self: Self, pulse: Pulse) -> list[Pulse]:
        if pulse.value:
            return []
        else:
            self.state = not self.state
            return [Pulse(self.state, self, output) for output in self.outputs]
    

class Conjunction(Module):
    input_memory: dict[str, bool]

    def __init__(self: Self, name: str) -> None:
        super().__init__(name)
        self.input_memory = {}


    def add_input(self: Self, source: Self) -> None:
        super().add_input(source)
        self.input_memory[source.name] = False

    
    def dispatch_pulse(self: Self, pulse: Pulse) -> list[Pulse]:
        self.input_memory[pulse.source.name] = pulse.value

        pulse_value = not all(self.input_memory.values())

        return [Pulse(pulse_value, self, output) for output in self.outputs]


class Button(Module):
    def dispatch_pulse(self: Self, pulse: Pulse) -> list[Pulse]:
        raise RuntimeError(f"{self.__class__.__name__} cannot handle pulses")


class Sink(Module):
    def dispatch_pulse(self: Self, pulse: Pulse) -> list[Pulse]:
        return []


def parse_input(data: Sequence[str]) -> dict[str, Module]:
    descriptions = {
        name: outputs.split(", ")
        for name, outputs
        in map(lambda elem: elem.split(" -> "), data)
    }

    modules: dict[str, Module] = {}

    for description in chain(descriptions.keys(), *descriptions.values()):
        module_name = description.lstrip("%&")

        if description.startswith('%'):
            modules[module_name] = FlipFlop(module_name)
        elif description.startswith('&'):
            modules[module_name] = Conjunction(module_name)
        elif description == 'broadcaster':
            modules[module_name] = Broadcaster(module_name)
        else:
            modules.setdefault(module_name, Sink(module_name))
    

    for name, outputs in descriptions.items():
        module = modules[name.lstrip("%&")]

        for output in outputs:
            target = modules[output]
            module.add_output(target)
            target.add_input(module)


    
    return modules


def solve_part1(data: Sequence[str]) -> int:
    modules = parse_input(data)

    pulse_count = Counter()

    for _ in range(1000):
        pulse_queue: deque[Pulse] = deque()
        pulse_queue.append(Pulse(False, Button('button'), modules['broadcaster']))

        while pulse_queue:
            pulse = pulse_queue.popleft()

            pulse_count[pulse.value] += 1

            pulse_queue.extend(pulse.target.dispatch_pulse(pulse))

    return reduce(operator.mul, pulse_count.values())


def solve_part2(data: Sequence[str]) -> int:
    modules = parse_input(data)

    rx_conjunction = modules['rx'].inputs[0]
    targets: dict[str, Optional[int]] = {module.name: None for module in rx_conjunction.inputs}

    for i in count(1):
        pulse_queue: deque[Pulse] = deque()
        pulse_queue.append(Pulse(False, Button('button'), modules['broadcaster']))

        while pulse_queue:
            pulse = pulse_queue.popleft()

            if pulse.value and pulse.source.name in targets and not targets[pulse.source.name]:
                targets[pulse.source.name] = i

            pulse_queue.extend(pulse.target.dispatch_pulse(pulse))
        
        if all(targets.values()):
            return lcm(*targets.values())
        
    raise RuntimeError("Unreachable")

def main() -> None:
    with open("input/day20.txt", 'r') as data_file:
        data: list[str] = data_file.read().splitlines()

    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))


if __name__ == '__main__':
    main()
