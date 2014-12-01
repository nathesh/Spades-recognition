from cardrecognition import get_cards
from helper import letter_to_suit, letter_to_number
# from collections import namedtuple
# Note that 1 and 3 are a team and 2 and 4 are team


class Round:

    used_cards = {}
    unavailable_suits = {1: [], 2: [], 3: [], 4: []}  # assume this for the each player...
    spades_broken = False
    bids = []
    card_values = {'A': 14, 'K': 13, 'Q': 12, 'J': 11}

    def __init__(self):
        self.round_cards = {}
        self.round_suit = None

    def start(self, player_num, first_round):

        if first_round == 1:
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
            elif self._invalid_play(card, player_num, self.round_suit is None):
                    print "Invalid Move, 40pt Penalty, Ending play"
                    return 0
            else:
                self.round_cards[card] = player_num
                if not self.round_suit:
                    self.round_suit = letter_to_suit[card.suit]
                    print "The suit of the Round is ", letter_to_suit[card.suit]
                if letter_to_suit[card.suit] == "Spades" and not Round.spades_broken:
                    print "Spades is Broken!"
                if self.round_suit != letter_to_suit[card.suit]:
                    print "Player {0} doesn't have {1}".format(player_num, self.round_suit)
                    Round.unavailable_suits[player_num].append(letter_to_suit[card.suit])
                Round.used_cards[card] = True
                print "Player {0} played {1} of {2}".format(
                    player_num, letter_to_suit[card.suit],
                    letter_to_number[card.number])

        return self._round_winner(cards_played)

    def _get_new_card(self, cards_played):
        for i in len(cards_played):
            if not self.round_cards.containsKey(cards_played[i]):
                return cards_played[i]

    def _invalid_play(self, card, player_num, check_spades):
        # Check if player played a valid suit ?! Can't check this he might not have suit.
        # Check if the first player played spades when spades was not broken
        # Check if a used card was played
        if letter_to_suit[card.suit] in Round.unavailable_suits[player_num]:
            return True
        if check_spades and letter_to_suit[card.suit] == "Spades":
            print "Played Spades"
            return True
        if Round.used_cards[card]:
            return True
        return False

    def _round_winner(self):
        #use variable player_num as first player to determine who won
        #return player numer
        for i in range(10):  # This needs to be added somewhere else
            Round.card_values[str(i + 1)] = i + 1
        maxcard_player = -1
        maxcard = -1  # Need to change this
        check_spade = False
        for card in self.round_cards:
            cardnum = Round.card_values[card.number]
            if card.suit == self.round_suit:
                maxcard = max(cardnum, maxcard)
                maxcard_player = self.round_cards[card] if maxcard < cardnum else maxcard_player
            if card.suit == "S":
                maxcard = cardnum if not check_spade else max(maxcard, cardnum)
                if not check_spade:
                    maxcard_player = maxcard_player if cardnum < maxcard else self.round_cards[cardnum]
                else:
                    maxcard_player = self.round_cards[cardnum]

        return maxcard_player

    def _get_bids(self):
        for i in range(4):
            print 'Player {0} enter bid'.format(i + 1)
            bid = raw_input()
            while not bid.isdigit():
                print 'Please enter a number'
                bid = raw_input()
            Round.bids.append(bid)

if __name__ == '__main__':
    Rounds = Round()
    wins = {1: 0, 2: 0, 3: 0, 4: 0}
    Points_A = 0
    Points_B = 0
    bags_A = 0
    bags_B = 0
    while(Points_A or Points_B < 500):
        for Hand in range(13):
            player_num = Hand % 4 + 1
            winner = Round.start(player_num, Hand + 1)
            wins[winner] = wins[winner] + 1
        Combined_bid_A = Rounds.bids[0] + Rounds.bids[2]
        Combined_bid_B = Rounds.bids[1] + Rounds.bids[3]
        Combined_tricks_A = wins[0] + wins[2]
        Combined_tricks_B = wins[1] + wins[3]

        # For Team A Calculation
        if Combined_bid_A > Combined_tricks_A:
            Points_A -= Combined_bid_A * 10
        if Combined_bid_A <= Combined_tricks_A:
            Points_A += Combined_bid_A * 10 + (Combined_tricks_A - Combined_bid_A)
            bags_A = (Combined_tricks_A - Combined_bid_A)
        if Rounds.bids[0] == 0:
            Points_A = Points_A + 100 if wins[0] == 0 else Points_A - 100
        if Rounds.bids[2] == 0:
            Points_A = Points_A + 100 if wins[2] == 0 else Points_A - 100
        if bags_A >= 10:
            Points_A -= 100
            bags_A -= 10

        # For Team B Calculation
        if Combined_bid_B > Combined_tricks_B:
            Points_B -= Combined_bid_B * 10
        if Combined_bid_B <= Combined_tricks_B:
            Points_B += Combined_bid_B * 10 + (Combined_tricks_B - Combined_bid_B)
            bags_B = Combined_tricks_B - Combined_bid_B
        if Rounds.bids[0] == 0:
            Points_B = Points_B + 100 if wins[1] == 0 else Points_B - 100
        if Rounds.bids[2] == 0:
            Points_B = Points_B + 100 if wins[3] == 0 else Points_B - 100
        if bags_B >= 10:
            Points_B -= 100
            bags_B -= 10
