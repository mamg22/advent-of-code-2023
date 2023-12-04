from functools import reduce

class Card:
    def __init__(self, card_id: int, winners: set[int], numbers: set[int]):
        self.card_id = card_id
        self.winners = winners
        self.numbers = numbers
        self.instances = 1
    
    def add_copies(self, copies=1):
        self.instances += copies

def extract_card_info(data: list[str]) -> list[Card]:
    cards = []
    for line in data:
        line = line.strip()
        card_meta, card_contents = line.split(": ")
        card_number = int(card_meta.split()[1])

        card_winners = {int(num) for num in card_contents.split(" | ")[0].split()}
        card_numbers = {int(num) for num in card_contents.split(" | ")[1].split()}

        cards.append(Card(card_number, card_winners, card_numbers))

    return cards

def solve_part1(data: list[str]):
    cards = extract_card_info(data)

    total = 0
    for card in cards:
        winning_numbers = card.winners & card.numbers

        if winners := len(winning_numbers):
            total += 2 ** (winners - 1)
    
    return total


def solve_part2(data: list[str]):
    cards = extract_card_info(data)
    for idx, card in enumerate(cards):
        winners = len(card.winners & card.numbers)

        for i in range(1, winners + 1):
            try:
                cards[idx + i].add_copies(card.instances)
            except IndexError:
                continue

    total = reduce(lambda val, card: val + card.instances, cards, 0)

    return total


def main():
    with open("input/day04.txt", 'r') as data_file:
        data: list[str] = data_file.readlines()

    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))

if __name__ == '__main__':
    main()