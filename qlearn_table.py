import random
import numpy as np
import copy

COLORS = ['red', 'blue', 'green', 'yellow']
NUMBERS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
special_cards = ['Skip', 'Reverse', 'DrawTwo']
wilds = ['Wild', 'WildFour']
DECK = [f"{color} {number}" for color in COLORS for number in numbers] + [f"{color} {special_card}" for color in COLORS for special_card in special_cards]
random.shuffle(DECK)
deck_copy = copy.copy(DECK)


def initialize_deck():
    deck = DECK.copy()
    random.shuffle(deck)
    return deck

def draw_cards(deck, num_cards):
    cards = deck[:num_cards]
    deck = deck[num_cards:]
    return deck, cards

def is_valid(card, top_card):
    return card[0] == top_card[0] or card[1] == top_card[1]

q_table = np.zeros((len(DECK), 2 * len(DECK)), dtype=float)

def update_q_table(q_table, state, action, reward, next_state):
    alpha = 0.1
    gamma = 0.9

    current_value = q_table[state, action]
    max_future_value = np.max(q_table[next_state, :])
    new_value = (1 - alpha) * current_value + alpha * (reward + gamma * max_future_value)
    q_table[state, action] = new_value

def play_episode():
    deck = initialize_deck()
    player_1_hand, deck = draw_cards(deck, 7)
    player_2_hand, deck = draw_cards(deck, 7)

    top_card, deck = draw_cards(deck, 1)

    state = DECK.index(player_1_hand[0])

    for _ in range(100):
        action = np.argmax(q_table[state, :])
        card = player_1_hand.pop(action % len(player_1_hand))

        if card.split()[1] == 'DrawTwo':
            player_2_hand, _ = draw_cards(deck, 2)
            reward = 1
        elif card.split()[0] == 'WildFour':
            player_2_hand, _ = draw_cards(deck, 4)
            reward = 1
        elif card.split()[0] == 'Wild':
          top_card = player_1_hand.pop(action % len(player_1_hand))
          reward = 1
        elif card.split()[1] == 'Skip':
            reward = 1
        elif card.split()[1] == 'Reverse':
            player_2_hand.reverse()
            reward = 1
        elif is_valid(card, top_card[0].split()[0]):
            reward = 1
            top_card = card
        else:
            reward = -1


        next_state = DECK.index(player_1_hand[0])
        update_q_table(q_table, state, action, reward, next_state)

        if not player_2_hand:
            break

        card = random.choice(player_2_hand)

        if card.split()[1] == 'DrawTwo':
            player_1_hand, _ = draw_cards(deck, 2)
            reward = 1
        elif card.split()[0] == 'WildFour':
            player_1_hand, _ = draw_cards(deck, 4)
            reward = 1
        elif card.split()[0] == 'Wild':
          top_card = player_2_hand.pop(action % len(player_2_hand))
          reward = 1
        elif card.split()[1] == 'Skip':
            reward = 1
        elif card.split()[1] == 'Reverse':
            player_1_hand.reverse()
            reward = 1
        elif is_valid(card, top_card.split()[0]):
            reward = 1
            top_card = card
        else:
            reward = -1

        state = DECK.index(card)
        next_state = DECK.index(player_1_hand[0])
        update_q_table(q_table, state, 0, reward, next_state)

    return


for _ in range(1000):
    play_episode()

print(q_table)
