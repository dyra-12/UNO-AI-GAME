import random
import numpy as np
import copy


colors = ['red', 'blue', 'green', 'yellow']
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
special_cards = ['Skip', 'Reverse', 'DrawTwo']
wilds = ['Wild', 'WildFour']
deck = [f"{color} {number}" for color in colors for number in numbers] + [f"{color} {special_card}" for color in colors for special_card in special_cards] 

deck_copy = copy.copy(deck)

top_card = deck.pop(random.randint(0, len(deck) - 1))
player_hand = random.sample(deck, 7)
agent_hand = random.sample(deck, 7)
turn = 'agent'


def draw_card(deck):
    global deck_copy
    card = deck_copy.pop()
    return deck, card

def is_valid(card, top_card):


    if card.split()[0] == 'Wild' or card.split()[0] == 'WildFour':
        return True

    if card.split()[0] == top_card.split()[0] and card.split()[1] in special_cards:
        return True

    if not card.split()[1] in special_cards and (card.split()[0] == top_card.split()[0] or card.split()[1] == top_card.split()[1]):
        return True

    return card.split()[0] == top_card.split()[0] or card.split()[1] == top_card.split()[1]

def play_card(card, hand):
    global turn
    global top_card

    if card is not None:
        if card.split()[0] == 'Wild':
          change_color(card)
        elif card.split()[0] == 'WildFour':
          drawfour()

        elif card.split()[1] == 'Skip':
              print("Opponent's move skipped.")
              turn = 'agent' if turn == 'agent' else 'user'
        elif card.split()[1] == 'Reverse':
              print("Reversed.")
              turn = 'agent' if turn == 'agent' else 'user'
        elif card.split()[1] == 'DrawTwo':
              draw_two_and_skip(turn)
              turn = 'agent' if turn == 'agent' else 'user'

        hand.remove(card)
        top_card = card

        if card.split()[1] not in ['Skip', 'Reverse', 'DrawTwo']:
            turn = 'agent' if turn == 'user' else 'user'
    else:
        print("Invalid move. Please enter a valid card.")

def get_user_input():
    try:
        selected_card = input(
            "Your turn! Enter the color and value of the card you want to play (e.g., red 3 or red Draw Two), or type 'draw' to draw a card: ")
        return selected_card
    except ValueError:
        print("Invalid input. Please enter the color and value separated by a space or type 'draw'.")
        return get_user_input()

def change_color(card):
    global current_player
    global agent_hand

    if current_player == 'user':
        selected_color = input("Enter the color you want: ").lower()
        card = f"{selected_color} Wild"
        second_card = get_user_input()
        ss = second_card
        if second_card.split()[0] == selected_color or second_card.split()[1] == selected_color:
            top_card = ss
            current_player = 'agent' if current_player == 'user' else 'user'
        else:
            print("Invalid move. The color of the second card does not match the selected color.")
            change_color(card)
    else:
        top_card  = agent_hand[1]

def drawfour():
    global current_player
    global agent_hand

    next_player = 'agent' if current_player == 'user' else 'user'
    print(f"{next_player.capitalize()} must draw four cards from the pile and skip their turn.")

    for _ in range(4):
        if current_player == 'user':
            agent_hand.append(deck.pop())
        else:
            player_hand.append(deck.pop())

    if current_player == 'user':
        selected_color = input("Enter the color you want: ").lower()
        card = f"{selected_color} Wild"
        second_card = get_user_input()
        ss = second_card
        if second_card.split()[0] == selected_color or second_card.split()[1] == selected_color:
            top_card  = ss
            current_player = 'agent' if current_player == 'user' else 'user'
        else:
            print("Invalid move. The color of the second card does not match the selected color.")
            change_color(card)
    else:
        top_card  = agent_hand[1]

def draw_two_and_skip(current_player):
    global turn
    next_player = 'agent' if current_player == 'user' else 'user'
    print(f"{next_player.capitalize()} must draw two cards from the pile and skip their turn.")

    for _ in range(2):
        if current_player == 'user':
            agent_hand.append(deck.pop())
        else:
            player_hand.append(deck.pop())


def update_q_table(q_table, state, action, reward, next_state):
    alpha = 0.1
    gamma = 0.9

    current_value = q_table[state, action]
    max_future_value = np.max(q_table[next_state, :])
    new_value = (1 - alpha) * current_value + alpha * (reward + gamma * max_future_value)

    q_table[state, action] = new_value

def play_game(deck):
    global deck_copy
    global turn

    while True:
        print("\n" + "=" * 30)
        print(f"Top Card: {top_card}")
        print("User Hand:", player_hand)
        print("Agent Hand:", agent_hand)

        if turn == 'user':
            user_action = input("Your turn! Enter the card you want to play, or type 'draw' to draw a card: ")

            if user_action.lower() == 'draw':
                if not deck:
                    print("Deck is empty. Skipping turn.")
                else:
                    drawn_card = deck_copy.pop()
                    print(f"User draws: {drawn_card}")
                    player_hand.append(drawn_card)
                turn = 'agent'
            else:
                user_input = user_action.split()
                if len(user_input) == 2:
                    color, value = user_input
                    card = f"{color} {value}"
                else:
                    print("Invalid input. Try again.")
                    continue

                if is_valid(card, top_card):
                    print(f"User plays: {card}")
                    play_card(card, player_hand)
                    if not player_hand:
                        print("Congratulations! You won!")
                        break
                else:
                    print("Invalid move. Try again.")

        else:
            valid_cards = [card for card in agent_hand if is_valid(card, top_card)]
            if valid_cards:
                agent_action = np.argmax(q_table[deck.index(valid_cards[0]), :])
                agent_card = valid_cards[agent_action % len(valid_cards)]
                print(f"Agent plays: {agent_card}")
                if is_valid(agent_card, top_card):
                    play_card(agent_card, agent_hand)
                    if not agent_hand:
                        print("Agent won!")
                        break

                state = deck.index(agent_card)
                next_state = deck.index(player_hand[0] if player_hand else agent_hand[0])
                reward = 1 if not agent_hand else 0
                update_q_table(q_table, state, deck.index(agent_card), reward, next_state)
            else:
                if not deck:
                    print("Deck is empty. Skipping agent's turn.")
                else:
                    deck, agent_cards = draw_card(deck)
                    state = deck.index(agent_cards)
                    next_state = deck.index(player_hand[0] if player_hand else agent_hand[0])
                    reward = 0
                    update_q_table(q_table, state, deck.index(agent_cards), reward, next_state)

                    agent_hand.append(agent_cards)
                    print(f"Agent draws: {agent_cards}")
                    turn = 'user'

    return

play_game(deck.copy())
