from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .forms import RegisterForm, LoginForm
from .bj_table import Blackjack
# Create your views here.

def register(request):
    if request.method == 'POST':
        User.objects.create_user(username = request.POST['username'],first_name=request.POST['first_name'], last_name=request.POST['last_name'],email=request.POST['email'], password=request.POST['password'])
        print(request)
        return redirect('/')
    return redirect('/')

def login_user(request):
    if request.method == 'POST':
        logged_user =authenticate(username=request.POST['username'],password=request.POST['password'])
        login(request,logged_user)
        return redirect('/')
    return redirect('/')

def logout_user(request):
    logout(request)
    return redirect('/')

# Blackjack game must be rebuilt from session data on every view.
# game_data in request.session contains the following:
#   table - Blackjack() object. See bj_table.py for details.
#   active_hand - Integer representing active player hand.
#   actions_available - List of actions available to the player, based on table.state and active_hand.

def player_turn_actions(bj_game, active_hand):
    actions = []
    if bj_game.player[active_hand]['hand'].final_value < 21:
        if not ((active_hand > 0) and (bj_game.player[active_hand]['hand'].cards[0].rank == "Ace") and (bj_game.player[active_hand]['hand'].cards[1].rank == "Ace")): # Split aces that get another ace cannot be hit, but can be split again.
            actions.append('hit')
        actions.append('stand')
        if len(bj_game.player[active_hand]['hand'].cards) == 2: # First turn on hand. Add player credit check for these.
            if (bj_game.player[active_hand]['hand'].hard_value >= 9) and (bj_game.player[active_hand]['hand'].hard_value <= 11):
                actions.append('double_down')
            if (bj_game.player[active_hand]['hand'].cards[0].rank == bj_game.player[active_hand]['hand'].cards[1].rank) and (len(bj_game.player) < 4):
                actions.append('split')
    return actions

if settings.DEBUG:
    def test_page(request):
        return render(request, "test_page.html")

    def test_display(request):
        context = {}
        if 'game_data' in request.session:
            game_data = request.session['game_data']
            context['dealer_hand'] = game_data['table'].dealer
            context['active_hand'] = game_data['active_hand']
            context['player_hands'] = []
            context['player_bets'] = {}
            context['player_bets']['main'] = []
            context['player_status'] = []
            for i in game_data['table'].player:
                context['player_hands'].append(game_data['table'].player[i]['hand'])
                context['player_bets']['main'].append(game_data['table'].player[i]['bet'])
                context['player_status'].append(game_data['table'].player[i]['status'])
            if game_data['table'].state == "end":
                context['wins'] = game_data['table'].wins
            context['actions_available'] = game_data['actions_available']
        else:
            context['no_game_data'] = True
        return render(request, "table.html", context)

    # test_reset
    # Path: '/test/reset/'
    # Reset after the game ends, go to fresh table.
    def test_reset(request):
        if request.method == "POST":
            request.session.pop('game_data')
        return redirect('/test/display/')
        
    # test_new_game
    # Path: '/test/new/'
    # Start new blackjack game.
    def test_new_game(request):
        if request.method == "POST":
            if 'main_bet' in request.POST:
                main_bet = request.POST['main_bet']
            else:
                main_bet = 2

            # Set Game Data.
            game_data = {}
            game_data['table'] = Blackjack()
            game_data['table'].new_game(main_bet)

            game_data['active_hand'] = 1
            game_data['actions_available'] = []
            # Set options.
            if game_data['table'].state == 'insurance':
                game_data['active_hand'] = 0
                if (main_bet > 1): # and player has credits available.
                    game_data['actions_available'].extend(["insurance_yes", "insurance_no"])
                else:
                    game_data['table'].blackjack_check()

            # Save to session data.
            request.session['game_data'] = game_data
        
            return test_setup_game(request)
    
        return redirect('/test/display/')

    # test_hit
    # Path: /test/hit/
    # Add card to active hand.
    def test_hit(request):
        if request.method == "POST":
            game_data = request.session['game_data']

            # Do the hit.
            game_data['table'].hit(game_data['active_hand'])

            # Determine next actions.
            if game_data['table'].player[game_data['active_hand']]['status'] == "active":
                game_data['actions_available'] = player_turn_actions(game_data['table'], game_data['active_hand'])
            else: # active hand stand or bust
                # Traverse to the next active hand.
                while (game_data['table'].player[game_data['active_hand']].status != "active") and (game_data['active_hand'] < len(game_data['table'].player)):
                    game_data['active_hand'] += 1
                # Determine next available actions.
                game_data['active_hand'] += 1
                if game_data['active_hand'] == len(game_data['table'].player): # Played through all player hands.
                    game_data['actions_available'] = []
                    game_data['table'].status = "dealer_turn"
                else:
                    game_data['actions_available'] = player_turn_actions(game_data['table'], game_data['active_hand'])

            # Save to session data.
            request.session['game_data'] = game_data

        return redirect('/test/display/')

    # test_stand
    # Path: /test/stand/
    # End turn on active hand.
    def test_stand(request):
        if request.method == "POST":
            game_data = request.session['game_data']

            game_data['table'].stand(game_data['active_hand'])

            # Traverse to the next active hand.
            while (game_data['table'].player[game_data['active_hand']].status != "active") and (game_data['active_hand'] < len(game_data['table'].player)):
                game_data['active_hand'] += 1
            # Determine next available actions.
            if game_data['active_hand'] == len(game_data['table'].player): # Played through all player hands.
                game_data['actions_available'] = []
                game_data['table'].status = "dealer_turn"
            else:
                game_data['actions_available'] = player_turn_actions(game_data['table'], game_data['active_hand'])

            # Save to session data.
            request.session['game_data'] = game_data

        return redirect('/test/display/')

    # test_double_down
    # Path: /test/double_down/
    # Double the bet on the active hand, draw one card, and stand.
    def test_double_down(request):
        if request.method == "POST":
            game_data = request.session['game_data']

            # Deduct from player credit meter here.

            game_data['table'].double_down(game_data['active_hand'])

            game_data['active_hand'] += 1
            if game_data['active_hand'] == len(game_data['table'].player): # Played through all player hands.
                game_data['actions_available'] = []
                game_data['table'].status = "dealer_turn"
            else:
                game_data['actions_available'] = player_turn_actions(game_data['table'], game_data['active_hand'])

        return redirect('/test/display/')

    # test_split
    # Path: /test/split/
    # Split a pair.
    def test_split(request):
        if request.method == "POST":
            game_data = request.session['game_data']

            # Deduct from player credit meter here.

            game_data['table'].player.split(game_data['active_hand'])

            # Stand on all split aces. A split ace that gets another ace can be split again.
            for i in range(game_data['active_hand'], len(game_data['table'].player)):
                if (game_data['table'].player[i]['hand'].cards[0].rank == "Ace") and (game_data['table'].player[i]['hand'].cards[1].rank != "Ace"):
                    game_data['table'].player[i]['status'] = "stand"

            # Traverse to the next active hand.
            while (game_data['table'].player[game_data['active_hand']].status != "active") and (game_data['active_hand'] < len(game_data['table'].player)):
                game_data['active_hand'] += 1
            # Determine next available actions.
            if game_data['active_hand'] == len(game_data['table'].player): # Played through all player hands.
                game_data['actions_available'] = []
                game_data['table'].status = "dealer_turn"
            else:
                game_data['actions_available'] = player_turn_actions(game_data['table'], game_data['active_hand'])

            # Save to session data.
            request.session['game_data'] = game_data

        return redirect('/test/display/')

    # take_insurance
    # Path: /test/insurance/
    # When taking insurance.
    def test_take_insurance(request):
        if request.method == "POST":
            game_data = request.session['game_data']

            # Deduct from player credit meter here.

            game_data['table'].take_insurance()

            # Save to session data.
            request.session['game_data'] = game_data

            return test_setup_game(request)

        return redirect('/test/display/')

    # test_setup_game
    # Path: /test/setup_game/
    # Set up for the first turn.
    def test_setup_game(request):
        if request.method == "POST":
            game_data = request.session['game_data']

            game_data['table'].blackjack_check()

            if game_data['table'].state == 'player_turn':
                game_data['active_hand'] = 0
                game_data['actions_available'] = player_turn_actions(round, 0)

            if game_data['table'].state == 'dealer_turn': # Dealer blackjack, game effectively over.
                round.dealer_reveal()
                round.dealer_draw()

            if game_data['table'].state == 'end': # Will get here after dealer blackjack or player blackjack.
                round.evaluate()

            # Save to session data.
            request.session['game_data'] = game_data

        return redirect('/test/display/')