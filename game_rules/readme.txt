cards.py contains Card and Shoe classes. The Shoe constructor builds a list of cards comprised of the number of 52-card poker decks specified.

blackjack.py includes the Hand class, with specifiers for the dealer hand.

blackjack.py can be run from the command line in an environment with Python3.
It will play through a Blackjack round using a six-deck shoe.
See 'blackjack rules.txt' for information on how Blackjack is played.

Thoughts:
Information that needs to be passed to the view: Dealer hand, player hands, hand values.
This information needs to persist through player actions up until the end of the round, perhaps in the session object.
Though we'd have to be careful not to expose information not meant to be seen (e.g. cards in the shoe).
Class may therefore need updating to receive information from the front end.
Final results can then be tallied for stat boards.

Mapping cards to graphics: An identifier for the card that is simply a combination of the rank and suit. A property can be added to the Card class using existing variables if necessary.