from cards import Card, Shoe

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
    import os, time, math

    def print_status(player_hands, dealer_hand, end=False):
        if os.name == "posix": # Mac/Linux
            os.system("clear")
        else: # Windows
            os.system("cls")
        print("DEALER")
        print(dealer_hand)
        if end:
            dealer_bust_txt = " - BUST" if dealer_hand.final_value > 21 else ""
            print(str(dealer_hand.final_value) + dealer_bust_txt)
        else:
            dealer_hand.print_value()
        print("")
        for i in range(0, len(player_hands)):
            print("PLAYER HAND " + str(i+1))
            print(player_hands[i])
            if end:
                hand_status = str(player_hands[i].final_value) + " - "
                if player_hands[i].final_value > 21:
                    hand_status = hand_status + "BUST"
                elif (player_hands[i].final_value > dealer_hand.final_value) or (dealer_hand.final_value > 21):
                    hand_status = hand_status + "WIN"
                elif player_hands[i].final_value < dealer_hand.final_value:
                    hand_status = hand_status + "LOSE"
                else:
                    hand_status = hand_status + "PUSH"
                print(hand_status)
            else:
                player_hands[i].print_value()
            print("--------------------")

        return

    my_shoe = Shoe(6)
    # my_shoe.print_draw_stack()
    my_shoe.shuffle()

    player_bet = 10 # Dummy Bet
    insurance_bet = 0
    
    player_hands = [Hand()]
    dealer_hand = Hand(True)
    player_hands[0].draw_card(my_shoe)
    dealer_hand.draw_card(my_shoe, dealer_hand.dealer) # Dealer first card, face down.
    player_hands[0].draw_card(my_shoe)
    dealer_hand.draw_card(my_shoe)
    print_status(player_hands, dealer_hand)

    game_over = False

    # Insurance Check.
    if (dealer_hand.cards[0].rank == "Ace") and (player_bet > 1):
        while 1:
            take_insurance = input("Insurance? [Y/N]: ")
            if take_insurance.upper() == "Y":
                insurance_bet = math.floor(player_bet / 2)
                break
            elif take_insurance.upper() == "N":
                break

    # Blackjack Check.
    dealer_blackjack = (dealer_hand.cards[0].soft_value + dealer_hand.facedown_card.soft_value == 21)
    player_blackjack = (player_hands[0].soft_value == 21)

    if dealer_blackjack:
        print("DEALER BLACKJACK!")
        game_over = True
    if player_blackjack:
        print("PLAYER BLACKJACK!")
        game_over = True

    player_eligible = False
    # Player Turn
    if not game_over:
        hand_num = 0
        for cur_hand in player_hands:
            hand_num += 1
        # Start Hands
            while cur_hand.hard_value < 21 and cur_hand.soft_value != 21:
            # Split Check
                split_available = (len(cur_hand.cards) == 2) and (cur_hand.cards[0].rank == cur_hand.cards[1].rank) and (len(player_hands) < 4)
                # Scenario: Ace split off, dealt card in the hand is not an ace. Automatically stand.
                if (hand_num > 1) and (cur_hand.cards[0].rank == "Ace") and (cur_hand.cards[1].rank != "Ace"):
                    player_eligible = True
                    break
                # Scenario: Aces were split, and the dealt card in the current hand was also an ace. In this case, allow an additional split, but cannot hit.
                aces_split = (len(cur_hand.cards) == 2) and (cur_hand.cards[0].rank == "Ace") and (cur_hand.cards[1].rank == "Ace") and (len(player_hands) > 1)
            # Double Down Check
                dd_available = (len(cur_hand.cards) == 2) and (cur_hand.soft_value >= 9) and (cur_hand.soft_value <= 11)
                print_status(player_hands, dealer_hand)
                print(f"Hand {hand_num} - Select")
                if not aces_split:
                    print("1: Hit")
                print("2: Stand")
                if split_available:
                    print("3: Split")
                if dd_available:
                    print("4: Double Down")
                option = input("")

                ## Hit - Add Card To Hand.
                if (option == "1") and not aces_split:
                    cur_hand.draw_card(my_shoe)
                    if cur_hand.final_value == 21:
                        player_eligible = True
                        break
                    elif cur_hand.hard_value > 21: # Bust
                        break

                ## Stand. End hand.
                elif option == "2":
                    player_eligible = True
                    break

                ## Split. Create new hand.
                elif (option == "3") and split_available:
                    # Take card out.
                    card_to_split = cur_hand.cards.pop()
                    # Start new hand.
                    player_hands.append(Hand())
                    # Draw new cards.
                    cur_hand.draw_card(my_shoe)
                    player_hands[len(player_hands)-1].cards.append(card_to_split)
                    player_hands[len(player_hands)-1].draw_card(my_shoe)

                ## Double Down. Add one card and end hand.
                elif (option == "4") and dd_available:
                    cur_hand.draw_card(my_shoe)
                    player_eligible = True
                    break

    # Dealer Turn
    ## Turn up the face down card.
    dealer_hand.cards.insert(0, dealer_hand.facedown_card)
    dealer_hand.facedown_card = None
    print_status(player_hands, dealer_hand)
    if player_eligible and not game_over:
        # Conditions to stand: Hard value is 17 or more, or soft value is between 18 and 21 when hard value is less than 17.
        while dealer_hand.hard_value <= 16 and (dealer_hand.soft_value <= 17 or dealer_hand.soft_value > 21):
            time.sleep(1)
            dealer_hand.draw_card(my_shoe)
            print_status(player_hands, dealer_hand)

    # Game End
    print_status(player_hands, dealer_hand, True)
    if insurance_bet > 0:
        if dealer_blackjack:
            print("INSURANCE WIN")
        else:
            print("INSURANCE LOSE")