from cardrecognition import get_cards
from helper import letter_to_suit, letter_to_number
# from collections import namedtuple


class Round:

    used_cards = {}
    unavailable_suits = {1: [], 2: [], 3: [], 4: []} # assume this for the each player... 
    spades_broken = False
    bids = []
    card_values = {'A': 14, 'K': 13, 'Q':12, 'J':11}

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
            elif self._invalid_play(card,player_num,self.round_suit is None ):
                    print "Invalid Move, 40pt Penalty, Ending play"
                    return 0
            else:
                self.round_cards[card] = player_num
                if self.round_suit is None 
                    self.round_suit = letter_to_suit[card.suit]
                    print "The suit of the Round is ",letter_to_suit[card.suit]
                if letter_to_suit[card.suit] == "Spades" && !Round.spades_broken
                    print "Spades is Broken!"
                if self.round_suit != letter_to_suit[card.suit]
                    print "Player {0} doesn't have {1}".format(player_num,self.round_suit)
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

    def _invalid_play(self,card,player_num,check_spades):
        # Check if player played a valid suit ?! Can't check this he might not have suit.
        # Check if the first player played spades when spades was not broken
        # Check if a used card was played
        # 
        if letter_to_suit[card.suit] in Round.unavailable_suits[player_num]
            return True
        if check_spades && letter_to_suit[card.suit] == "Spades"
            print "Played Spades"
            return True
        if Round.used_cards[card] 
            return True
        return false 


    def _round_winner(self):
        #use variable player_num as first player to determine who won
        #return player numer
        for i in range(10): # This needs to be added somewhere else 
            Round.card_values[str(i+1)] = i+1
        maxcard_player = -1;
        maxcard = -1 # Need to change this
        check_spade = False  
        for card in self.round_cards:
            cardnum = Round.card_values[card.number]
            if card.suit == self.round_suit:
                maxcard = max(cardnum,maxcard)
                maxcard_player = self.round_cards[card] if maxcard < cardnum else maxcard_player
            if card.suit == "S":
                maxcard = cardnum if !check_spade else max(maxcard,cardnum)
                if !check_spade:
                    maxcard_player = maxcard_player if cardnum < maxcard else  self.round_cards[cardnum]
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
