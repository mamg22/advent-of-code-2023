from enum import IntEnum, auto
from collections import Counter

SYMBOL_LABEL_VALUES = {
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}

def get_label_value(label: str, jokers: bool = False) -> int:
    if label.isdecimal():
        return int(label)
    elif jokers and label == 'J':
        return 1
    else:
        return SYMBOL_LABEL_VALUES[label]

class Hand:
    class Type(IntEnum):
        FiveKind = 7
        FourKind = 6
        FullHouse = 5
        ThreeKind = 4
        TwoPair = 3
        OnePair = 2
        HighCard = 1

    def __init__(self, cards, jokers):
        self.cards = cards
        self.type = self._get_type(cards, jokers)
        self.jokers = jokers
    
    def __repr__(self):
        return f"Hand({''.join(self.cards)})"

    def __gt__(self, other):
        if self.type != other.type:
            return self.type > other.type
        else:
            for my_card, their_card in zip(self.cards, other.cards):
                my_value = get_label_value(my_card, self.jokers)
                their_value = get_label_value(their_card, self.jokers)
                if my_value != their_value:
                    return my_value > their_value

    def _get_type(self, cards: list[str], jokers: bool = False):
        groups = Counter()
        for card in cards:
            groups[card] += 1
        
        # If in joker mode, and there's at least one joker but less than a full hand
        if jokers and 'J' in groups and groups['J'] != 5:
            n_jokers = groups['J']
            del groups['J']
            most_cards = max(groups, key=groups.get)
            groups[most_cards] += n_jokers

        ordered_group_lengths = sorted(list(groups.values()), reverse=True)

        match ordered_group_lengths:
            case [5]:
                return Hand.Type.FiveKind
            case [4, 1]:
                return Hand.Type.FourKind
            case [3, 2]:
                return Hand.Type.FullHouse
            case [3, 1, 1]:
                return Hand.Type.ThreeKind
            case [2, 2, 1]:
                return Hand.Type.TwoPair
            case [2, 1, 1, 1]:
                return Hand.Type.OnePair
            case [1, 1, 1, 1, 1]:
                return Hand.Type.HighCard
            case _:
                raise ValueError(f"Invalid card set {''.join(cards)}")
    
def extract_info(data: list[str], jokers: bool = False):
    info = []
    for line in data:
        hand = Hand(list(line.split()[0]), jokers)
        bid = int(line.split()[1])

        info.append((hand, bid))
    
    return info

def solve_part1(data: list[str]) -> int:
    info = extract_info(data, False)
    info.sort(key=lambda elem: elem[0])
    total = 0
    for rank, (hand, bid) in enumerate(info, 1):
        total += bid * rank

    return total

def solve_part2(data: list[str]) -> int:
    info = extract_info(data, True)
    info.sort(key=lambda elem: elem[0])
    total = 0
    for rank, (hand, bid) in enumerate(info, 1):
        total += bid * rank

    return total

def main():
    with open("input/day07.txt", 'r') as data_file:
        data: list[str] = data_file.read().splitlines()

    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))

if __name__ == '__main__':
    main()