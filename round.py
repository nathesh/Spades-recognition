from cardrecognition import get_cards
from helper import letter_to_suit, letter_to_number
# from collections import namedtuple


class Round:

    used_cards = {}
    unavailable_suits = {1: [], 2: [], 3: [], 4: []}
    spades_broken = False
    bids = []

    def __init__(self):
        self.round_cards = {}
        self.round_suit = None

    def start(self, player_num):

        self._get_bids()

        cards_played = []
        for i in range(4):

            player_num = (player_num + i) % 4 if (player_num + i) != 4 else 4
            print "Player {0} please play your card".format(player_num)

            #case if more than necessary cards played or (*, *) is returned
            while len(cards_played) <= (i + 1):
                cards_played = get_cards()

            card = self._get_new_card(cards_played)

            if card.suit == '*' or card.num == '*':
                print "can't recognize card, restarting round"
                return 0
            elif self._invalid_play(card, player_num):
                    print "Invalid Move, 40pt Penalty, Ending play"
                    return 0
            else:
                self.round_cards[card] = player_num
                Round.used_cards[card] = True
                print "Player {0} played {1} of {2}".format(
                    player_num, letter_to_suit[card.suit],
                    letter_to_number[card.number])

        return self._round_winner(cards_played)

    def _get_new_card(self, cards_played):
        for i in len(cards_played):
            if not self.round_cards.containsKey(cards_played[i]):
                return cards_played[i]

    def _invalid_play(self):
        # Check if player played a valid suit
        # Check if the first player played spades when spades was not broken
        # Check if a used card was played
        return

    def _round_winner(self):
        #use variable player_num as first player to determine who won
        #return player numer
        return

    def _get_bids(self):
        for i in range(4):
            print 'Player {0} enter bid'.format(i + 1)
            bid = raw_input()
            while not bid.isdigit():
                print 'Please enter a number'
                bid = raw_input()
            Round.bids.append(bid)
