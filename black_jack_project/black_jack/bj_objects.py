import random

RANKS = {
    'Ace'   : {'rank' : 13, 'bj_hard_val' : 1,  'bj_soft_val' : 11, 'shorthand' : 'A'},
    'King'  : {'rank' : 12, 'bj_hard_val' : 10, 'bj_soft_val' : 10, 'shorthand' : 'K'},
    'Queen' : {'rank' : 11, 'bj_hard_val' : 10, 'bj_soft_val' : 10, 'shorthand' : 'Q'},
    'Jack'  : {'rank' : 10, 'bj_hard_val' : 10, 'bj_soft_val' : 10, 'shorthand' : 'J'},
    'Ten'   : {'rank' : 9,  'bj_hard_val' : 10, 'bj_soft_val' : 10, 'shorthand' : 'T'},
    'Nine'  : {'rank' : 8,  'bj_hard_val' : 9,  'bj_soft_val' : 9,  'shorthand' : '9'},
    'Eight' : {'rank' : 7,  'bj_hard_val' : 8,  'bj_soft_val' : 8,  'shorthand' : '8'},
    'Seven' : {'rank' : 6,  'bj_hard_val' : 7,  'bj_soft_val' : 7,  'shorthand' : '7'},
    'Six'   : {'rank' : 5,  'bj_hard_val' : 6,  'bj_soft_val' : 6,  'shorthand' : '6'},
    'Five'  : {'rank' : 4,  'bj_hard_val' : 5,  'bj_soft_val' : 5,  'shorthand' : '5'},
    'Four'  : {'rank' : 3,  'bj_hard_val' : 4,  'bj_soft_val' : 4,  'shorthand' : '4'},
    'Three' : {'rank' : 2,  'bj_hard_val' : 3,  'bj_soft_val' : 3,  'shorthand' : '3'},
    'Two'   : {'rank' : 1,  'bj_hard_val' : 2,  'bj_soft_val' : 2,  'shorthand' : '2'},
}

SUITS = [
    "Spade",
    "Club",
    "Heart",
    "Diamond",
]

class Card:
    def __init__(self, _rank, _suit):
        self.rank = _rank
        self.suit = _suit

    def __str__(self):
        outStr = RANKS[self.rank]['shorthand']
        if self.suit == "Spade":
            outStr = outStr + "♠"
        elif self.suit == "Club":
            outStr = outStr + "♣"
        elif self.suit == "Heart":
            outStr = outStr + "♥"
        elif self.suit == "Diamond":
            outStr = outStr + "♦"

        return outStr

    @property
    def soft_value(self):
        return RANKS[self.rank]['bj_soft_val']

    @property
    def hard_value(self):
        return RANKS[self.rank]['bj_hard_val']

class Shoe:
    def __init__(self, num_decks=1):
        self.draw_stack = []
        self.discard_stack = []

        for deck in range(0, num_decks):
            for suit in SUITS:
                for rank in RANKS:
                    self.draw_stack.append(Card(rank, suit))

    def rebuild(self, shoe_dict):
        self.draw_stack = []
        self.discard_stack = []
        for c in shoe_dict['draw_stack']:
            self.draw_stack.append(Card(c['rank'], c['suit']))
        for c in shoe_dict['discard_stack']:
            self.discard_stack.append(Card(c['rank'], c['suit']))

        return self

    def shuffle(self):
        self.draw_stack.extend(self.discard_stack)
        self.discard_stack.clear()

        random.shuffle(self.draw_stack)
        return self

    def draw(self):
        return self.draw_stack.pop(0)

    def discard(self, cards_list):
        self.discard_stack.extend(cards_list)
        return self

    def print_draw_stack(self):
        draw_arr = []
        for c in self.draw_stack:
            draw_arr.append(c.__str__())
        print(draw_arr)
        return

class Hand:
    def __init__(self, dealer=False):
        self.cards = []
        self.facedown_card = None
        self.dealer = dealer

    def __str__(self):
        outStr = ""
        if self.facedown_card:
            outStr = outStr + "## "
        for card in self.cards:
            outStr = outStr + str(card) + " "
        return outStr

    @property
    def soft_value(self):
        value = 0
        for c in self.cards:
            # Ace Check
            if c.soft_value == 11:
                if value > 10:
                    value += c.hard_value
                else:
                    value += c.soft_value
            else:
                value += c.soft_value
        return value

    @property
    def hard_value(self):
        value = 0
        for c in self.cards:
            value += c.hard_value
        return value

    @property
    def final_value(self):
        return self.soft_value if self.soft_value <= 21 else self.hard_value

    def rebuild(self, hand_dict):
        self.cards = []
        for c in hand_dict['cards']:
            self.cards.append(Card(c['rank'], c['suit']))
        self.facedown_card = None if hand_dict['facedown_card'] == None else Card(hand_dict['facedown_card']['rank'], hand_dict['facedown_card']['suit'])
        self.dealer = hand_dict['dealer']

        return self

    def print_value(self):
        if (self.hard_value != self.soft_value) and (self.soft_value < 21):
            print(str(self.hard_value) + "/" + str(self.soft_value))
        elif (self.soft_value == 21):
            print(str(self.soft_value))
        else:
            print(str(self.hard_value))

    def draw_card(self, game_shoe, facedown=False):
        if facedown:
            self.facedown_card = game_shoe.draw()
        else:
            self.cards.append(game_shoe.draw())
        return self

if __name__ == "__main__":
    my_shoe = Shoe(1)

    print(my_shoe.draw_stack[0].soft_value)
    print(my_shoe.draw_stack[0].hard_value)