import random
import numpy as np
import copy

colors = ['red', 'blue', 'green', 'yellow']
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
special_cards = ['Skip', 'Reverse', 'DrawTwo']
wilds = ['Wild', 'WildFour']
deck = [f"{color} {number}" for color in colors for number in numbers] + [f"{color} {special_card}" for color in colors for special_card in special_cards] 


def has_won(hand):
    return not bool(hand)

def is_valid(card):
    top_card = discard_pile[-1]

    if card.split()[0] == 'Wild' or card.split()[0] == 'WildFour':
        return True

    if card.split()[0] == top_card.split()[0] and card.split()[1] in special_cards:
        return True

    if not card.split()[1] in special_cards and (card.split()[0] == top_card.split()[0] or card.split()[1] == top_card.split()[1]):
        return True

    return card.split()[0] == top_card.split()[0] or card.split()[1] == top_card.split()[1]

def play_card(card, hand):
    global discard_pile
    global current_player

    if card is not None:
        if card.split()[0] == 'Wild':
            change_color(card)
        elif card.split()[0] == 'WildFour':
            drawfour()
        elif is_valid(card) and card in hand:
            if card.split()[1] == 'Skip':
                print("Opponent's move skipped.")
            elif card.split()[1] == 'Reverse':
                print("Reversed.")
            elif card.split()[1] == 'DrawTwo':
                draw_two_and_skip(current_player)

            hand.remove(card)
            discard_pile.append(card)

            if card.split()[1] not in ['Skip', 'Reverse', 'DrawTwo', 'Wild', 'WildFour']:
                current_player = 'agent' if current_player == 'user' else 'user'
        else:
            print(f"Invalid move. {current_player.capitalize()} must play a valid card.")
    else:
        print("Invalid move. Please enter a valid card.")

def change_color(card):
    global current_player
    global agent_hand

    if current_player == 'user':
        selected_color = input("Enter the color you want: ").lower()
        card = f"{selected_color} Wild"
        second_card = get_user_input()
        ss = second_card
        if second_card.split()[0] == selected_color or second_card.split()[1] == selected_color:
            discard_pile[-1] = ss
            current_player = 'agent' if current_player == 'user' else 'user'
        else:
            print("Invalid move. The color of the second card does not match the selected color.")
            change_color(card)
    else:
        discard_pile[-1] = agent_hand[1]

def drawfour():
    global current_player
    global agent_hand

    next_player = 'agent' if current_player == 'user' else 'user'
    print(f"{next_player.capitalize()} must draw four cards from the pile and skip their turn.")

    for _ in range(4):
        if current_player == 'user':
            agent_hand.append(deck.pop())
        else:
            user_hand.append(deck.pop())

    if current_player == 'user':
        selected_color = input("Enter the color you want: ").lower()
        card = f"{selected_color} Wild"
        second_card = get_user_input()
        ss = second_card
        if second_card.split()[0] == selected_color or second_card.split()[1] == selected_color:
            discard_pile[-1] = ss
            current_player = 'agent' if current_player == 'user' else 'user'
        else:
            print("Invalid move. The color of the second card does not match the selected color.")
            change_color(card)
    else:
        discard_pile[-1] = agent_hand[1]

def draw_two_and_skip(current_player):
    next_player = 'agent' if current_player == 'user' else 'user'
    print(f"{next_player.capitalize()} must draw two cards from the pile and skip their turn.")

    for _ in range(2):
        if current_player == 'user':
            agent_hand.append(deck.pop())
        else:
            user_hand.append(deck.pop())

    current_player = 'agent' if current_player == 'agent' else 'user'

def get_user_input():
    try:
        selected_card = input(
            "Your turn! Enter the color and value of the card you want to play (e.g., red 3 or red Draw Two), or type 'draw' to draw a card: ")
        return selected_card
    except ValueError:
        print("Invalid input. Please enter the color and value separated by a space or type 'draw'.")
        return get_user_input()

def agent_turn():
    global current_player

    if current_player == 'agent':
        wild_draw_four_moves = [card for card in agent_hand if 'WildFour' in card]
        if wild_draw_four_moves:
            selected_card = wild_draw_four_moves[0]
        else:
            same_color_special_moves = [card for card in agent_hand if card.split()[1] in ['DrawTwo', 'Reverse', 'Skip'] and card.split()[0] == discard_pile[-1].split()[0]]
            if same_color_special_moves:
                selected_card = same_color_special_moves[0]
            else:
                if discard_pile and agent_hand:
                    same_color_moves = [card for card in agent_hand if card.split()[0] == discard_pile[-1].split()[0]]
                    if same_color_moves:
                        selected_card = same_color_moves[0]
                    else:
                        same_number_moves = [card for card in agent_hand if card.split()[1] == discard_pile[-1].split()[1]]
                        if same_number_moves:
                            selected_card = same_number_moves[0]
                        else:
                            selected_card = None
                else:
                    selected_card = None

        if selected_card:
            if 'Wild' in selected_card:
                selected_color = random.choice(colors)
                selected_card = f"{selected_color} Wild"
            print(f"{current_player.capitalize()} played: {selected_card}")
            play_card(selected_card, agent_hand)
        else:
            drawn_card = deck.pop()
            print(f"{current_player.capitalize()} drew a card: {drawn_card}")
            agent_hand.append(drawn_card)
            current_player = 'user'




def user_turn():
    global current_player
    if current_player == 'user':
        selected_card = get_user_input()

        if selected_card.lower() == 'draw':
            drawn_card = deck.pop()
            print(f"{current_player.capitalize()} drew a card: {drawn_card}")
            user_hand.append(drawn_card)
            current_player = 'agent' if current_player == 'user' else 'user'
        elif is_valid(selected_card):
            play_card(selected_card, user_hand)
        else:
            while not is_valid(selected_card):
                print(
                    f"Invalid move. {current_player.capitalize()} must play a valid card or type 'draw' to draw a card.")
                selected_card = get_user_input()

def play_uno_game():
    global current_player

    while True:
        print("\n" + "=" * 30)
        print(f"Top Card on Discard Pile: {discard_pile[-1]}")
        print(f"User Hand: {user_hand}")
        print(f"Agent Hand: {agent_hand}")

        if current_player == 'user':
            user_turn()
        else:
            agent_turn()

        if has_won(user_hand):
            print("Congratulations! You have won!")
            break
        elif has_won(agent_hand):
            print("Agent has won. Better luck next time!")
            break

random.shuffle(deck)

discard_pile = [deck.pop(random.randint(0, len(deck) - 1))]
user_hand = random.sample(deck, 7)
agent_hand = random.sample(deck, 7)
current_player = 'user'

play_uno_game()


