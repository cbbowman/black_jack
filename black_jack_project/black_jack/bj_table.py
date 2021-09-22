from .bj_objects import Shoe, Hand
import math, json

# Objects on table:
# Card Shoe - Shoe Object
# Dealer Hand - Hand Object
# Player Hand(s) with Bet(s) - List of hands that the player has and associated bets. Start with 1, up to 4 via splitting.
# Side Bet(s) - List of positive integer values.
# State - Current part of the game.
#   start - Beginning of the game, pre-deal.
#   insurance - Ask for insurance bet.
#   player_turn - Player's turn to hit, stand, etc.
#   dealer_turn - Dealer's turn
#   end - End of game.

# Player hand status:
#   active - Available to take hits.
#   stand - Hand completed.
#   blackjack - Hand received blackjack (21) on the deal.
#   bust - Hand value is higher than 21.
#   win - Player hand value beats dealer hand value.
#   lose - Dealer hand value beats player hand value.
#   push - Player hand value and dealer hand value match.
class Blackjack:
    def __init__(self, game_shoe=[], dealer=None, player=[], side_bets={}, wins={}, state="start"): # Info will be stored in session data.
        # May not need to store side bets in class.
        self.shoe = game_shoe
        self.dealer = dealer
        self.player = player
        self.side_bets = side_bets
        self.wins = wins
        self.state = state

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def from_json(self, json_str):
        build_dict = json.loads(json_str)
        # Shoe
        self.shoe = Shoe().rebuild(build_dict['shoe'])
        # Dealer
        self.dealer = Hand().rebuild(build_dict['dealer'])
        # Player
        self.player = []
        for player_hand in build_dict['player']:
            self.player.append({
                'bet'    : player_hand['bet'],
                'hand'   : Hand().rebuild(player_hand['hand']),
                'status' : player_hand['status'],
            })
        # The Rest
        self.side_bets = build_dict['side_bets']
        self.wins = build_dict['wins']
        self.state = build_dict['state']

        return self

    # new_game()
    # Start a new Blackjack game with a new shoe, dealer hand, and one player hand.
    def new_game(self, main_bet, side_bets={}):
        self.state = "start"
        # Set up shoe.
        self.shoe = Shoe(6) # Standard Blackjack uses six decks.
        self.shoe.shuffle()

        # Set up hands and side bets.
        self.dealer = Hand(True)
        self.player = [{
            'bet'    : main_bet,
            'hand'   : Hand(),
            'status' : "active",
        }]

        # Deal 2 cards each.
        self.player[0]['hand'].draw_card(self.shoe)
        self.dealer.draw_card(self.shoe, True) # Dealer face down card.
        self.player[0]['hand'].draw_card(self.shoe)
        self.dealer.draw_card(self.shoe)

        # Do side bet checks here.

        # Insurance qualifier check.
        if (self.dealer.cards[0].rank == "Ace") and (self.player[0]['bet'] > 1):
            self.state = "insurance"
        # Blackjack check.
        else:
            self.blackjack_check()

        return self

    # take_insurance()
    # Handle blackjack insurance bet, equal to 1/2 main bet rounded down.
    # Pays 2 to 1 on dealer blackjack.
    def take_insurance(self):
        if self.state == "insurance":
            insurance_bet = math.floor(self.player[0]['bet'] / 2)

            if self.dealer.cards[0].soft_value + self.dealer.facedown_card.soft_value == 21: # Dealer blackjack.
                self.state = "dealer_turn"
                self.player[0]['status'] = "stand"
                self.wins['insurance'] = insurance_bet * 3 # 2 to 1
            else:
                self.blackjack_check()

        return self

    # blackjack_check()
    # Check for dealer and player blackjack.
    def blackjack_check(self):
        print(self.dealer.cards[0], self.dealer.facedown_card)
        dealer_blackjack = (self.dealer.cards[0].soft_value + self.dealer.facedown_card.soft_value == 21)
        player_blackjack = (self.player[0]['hand'].cards[0].soft_value + self.player[0]['hand'].cards[1].soft_value == 21)

        if dealer_blackjack:
            # When dealer has blackjack, go to dealer turn. Subsequent logic will determine if the player loses or pushes.
            self.player[0]['status'] = "stand"
            self.state = "dealer_turn"
        elif player_blackjack:
            # When player has blackjack and dealer doesn't, turn up dealer facedown card and go to end.
            self.player[0]['status'] = "blackjack" # Set so end of game knows to pay correctly.
            self.dealer_reveal()
            self.state = "end"
        else:
            self.state = "player_turn"

    # hit(hand_num)
    # Player hits on current hand, drawing from the shoe.
    def hit(self, hand_num):
        # Draw a card.
        self.player[hand_num]['hand'].draw_card(self.shoe)
        # Determine next course of action based on the hand value. Stand if 21, bust if hard value over 21.
        if self.player[hand_num]['hand'].final_value == 21:
            self.player[hand_num]['status'] = "stand"
        elif self.player[hand_num]['hand'].hard_value > 21:
            self.player[hand_num]['status'] = "bust"

        return self

    # stand(hand_num)
    # Player stands on current hand, freezing the value.
    def stand(self, hand_num):
        self.player[hand_num]['status'] = "stand"
        return self

    # split(hand_num)
    # Current hand is split into two hands, extra card drawn for each hand.
    # Only available when card ranks are identical, and player has less than 4 hands.
    def split(self, hand_num):
        if (len(self.player[hand_num]['hand'].cards) == 2) and (len(self.player) < 4):
            card_to_split = self.player[hand_num]['hand'].cards.pop()
            # Start new hand.
            self.player.append({
                'bet'    : self.player[hand_num]['bet'],
                'hand'   : Hand(),
                'status' : 'active',
            })
            self.player[len(self.player)-1]['hand'].cards.append(card_to_split)
            # Draw new cards for each. Auto-stand if 21.
            self.player[hand_num]['hand'].draw_card(self.shoe)
            if self.player[hand_num]['hand'].final_value == 21:
                self.player[hand_num]['status'] = "stand"
            self.player[len(self.player)-1]['hand'].draw_card(self.shoe)
            if self.player[len(self.player)-1]['hand'].final_value == 21:
                self.player[len(self.player)-1]['status'] = "stand"

        return self

    # double_down(hand_num)
    # Double the bet, draw one extra card, then stand.
    # Only available when hand has 2 cards with total value of 9, 10, or 11.
    def double_down(self, hand_num):
        if len(self.player[hand_num]['hand'].cards) == 2:
            # Double the bet.
            self.player[hand_num]['bet'] *= 2
            # Draw a card.
            self.player[hand_num]['hand'].draw_card(self.shoe)
            # Stand
            self.player[hand_num]['status'] = "stand"

        return self

    # dealer_reveal()
    # Reveal dealer face down card.
    def dealer_reveal(self):
        self.dealer.cards.insert(0, self.dealer.facedown_card)
        self.dealer.facedown_card = None
        return self

    # dealer_draw()
    # Commence the dealer's turn.
    # Dealer actions: Hit on any 16 or below, or soft 17. Stand on any 18 or above, or hard 17.
    def dealer_draw(self):
        # Determine next course of action.
        if (self.dealer.hard_value >= 17) or (self.dealer.soft_value >= 18):
            self.state = "end"
        else:
            # Draw card.
            self.dealer.draw_card(self.shoe)

        return self

    # evaluate()
    # Do all hand evaluations.
    def evaluate(self):
        dealer_bust = (self.dealer.final_value > 21)
        hand_count = 0

        for player_hand in self.player:
            hand_count += 1
            if player_hand['status'] == "blackjack":
                self.wins[f'Hand {hand_count}'] = player_hand['bet'] * 2.5 # Blackjack pays 3 to 2.
            elif player_hand['status'] == "stand":
                # Hand Wins
                if (player_hand['hand'].final_value > self.dealer.final_value) or dealer_bust:
                    player_hand['status'] = "win"
                    self.wins[f'Hand {hand_count}'] = player_hand['bet'] * 2 # Hand win pays 1 to 1.
                # Hand Push
                elif (player_hand['hand'].final_value == self.dealer.final_value):
                    player_hand['status'] = "push"
                    self.wins[f'Hand {hand_count}'] = player_hand['bet'] # Hand push returns bet.
                # Hand Loss
                else:
                    player_hand['status'] = "lose"
        
        return self

if __name__ == "__main__":
    game = Blackjack()
    game.new_game(10)
    print(game.__dict__)
    json_str = game.to_json()
    print(json_str)
    load_game = Blackjack().from_json(json_str)
    print(load_game.__dict__)
    print(load_game.to_json())