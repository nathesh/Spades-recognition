

suit = {
    'S': 'Spades',
    'C': 'Clubs',
    'D': 'Diamonds',
    'H': 'Hearts'
}

number = {
    'A': 'Ace',
    '2': 'Two',
    '3': 'Three',
    '4': 'Four',
    '5': 'Five',
    '6': 'Six',
    '7': 'Seven',
    '8': 'Eight',
    '9': 'Nine',
    '10': 'Ten',
    'J': 'Jack',
    'Q': 'Queen',
    'K': 'King'
}


def letter_to_suit(letter):
    return suit[letter]


def letter_to_numer(letter):
    return number[letter]

