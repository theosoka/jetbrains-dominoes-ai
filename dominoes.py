import random


# INTERFACE

def print_menu():
    print(f'''======================================================================
Stock size: {len(stock_pieces)} 
Computer pieces: {len(computer_pieces)}''', end='\n\n')
    print_domino_snake()
    print('\n\nYour pieces:')
    for i in range(0, len(player_pieces)):
        print(f'{i + 1}:{player_pieces[i]}')
    print(f'\nStatus: {statuses.get(status)}')


def print_domino_snake():
    if len(domino_snake) < 7:
        for domino in domino_snake:
            print(domino, end='')
    else:
        for j in range(0, 3):
            print(domino_snake[j], end='')
        print('...', end='')
        for j in range(len(domino_snake) - 3, len(domino_snake)):
            print(domino_snake[j], end='')


def print_pieces(pieces):
    for j in range(0, len(pieces)):
        print(f'{j + 1}:{pieces[j]}')


# CHECKING THE MOVE

def correct_input_format(n):
    if not n.isdigit() or abs(int(n)) > len(player_pieces):
        if abs(int(n)) > len(player_pieces):
            print('Invalid input. Please try again.')
            return False
        if n.startswith('-') and n[1:].isdigit():
            return True
        print('Invalid input. Please try again.')
        return False
    return True


def legal_input(n, pieces):
    if n > 0:
        if domino_snake[len(domino_snake) - 1][1] in pieces[n - 1]:
            return True
    elif n < 0:
        if domino_snake[0][0] in pieces[-n - 1]:
            return True
    elif n == 0:
        return True
    else:
        return False


def check_orientation(n, pieces, side):
    if side == 'left':
        if domino_snake[0][0] != pieces[-n - 1][1]:
            pieces[-n - 1][0], pieces[-n - 1][1] = pieces[-n - 1][1], pieces[-n - 1][0]
    elif side == 'right':
        if domino_snake[len(domino_snake) - 1][1] != pieces[n - 1][0]:
            pieces[n - 1][0], pieces[n - 1][1] = pieces[n - 1][1], pieces[n - 1][0]


# MOVING

def make_move_player(n):
    if n == 0:
        skip_move(player_pieces)
    else:
        insert_piece(player_pieces, n)


def make_move_computer():
    n = choose_best()
    if n == 0:
        skip_move(computer_pieces)
    else:
        insert_piece(computer_pieces, n)


def make_move():
    if status == 3:
        move = input()
        if not correct_input_format(move):
            make_move()
        else:
            move = int(move)
            if not legal_input(move, player_pieces):
                print('Illegal move. Please try again.')
                make_move()
            else:
                make_move_player(move)
    elif status == 4:
        make_move_computer()
        input()


def proceed_move(n):
    if status == 3:
        make_move_player(n)
    elif status == 4:
        make_move_computer()


def skip_move(pieces):
    if len(stock_pieces) == 0:
        change_status()
        make_move()
    choice = random.choice(stock_pieces)
    if pieces == computer_pieces:
        update_count(choice)
    pieces.append(choice)
    stock_pieces.remove(choice)


def insert_piece(pieces, piece):
    """
    :param pieces: computer_pieces or player_pieces
    :param piece: int n
    :return:
    """
    if pieces == player_pieces:
        update_count(player_pieces[abs(piece) - 1])
    side = 'right' if piece > 0 else 'left'
    if side == 'right':
        check_orientation(piece, pieces, side)
        domino_snake.append(pieces[piece - 1])
        pieces.remove(pieces[piece - 1])
    elif side == 'left':
        check_orientation(piece, pieces, side)
        domino_snake.insert(0, pieces[-piece - 1])
        pieces.remove(pieces[-piece - 1])


# MISC

def difference(list1, list2):
    list_difference = list1[:]
    for item in list1:
        if item in list2:
            list_difference.remove(item)
    return list_difference


def change_status():
    if len(player_pieces) == 0:
        return 0
    if len(computer_pieces) == 0:
        return 1
    if domino_snake[0][0] == domino_snake[len(domino_snake) - 1][1] and sum(
            [e.count(domino_snake[0][0]) for e in domino_snake]) == 8:
        return 2
    if status == 3:
        return 4
    if status == 4:
        return 3


def choose_first_player():
    player_weights = [a[0] + a[0] for a in player_pieces]
    computer_weights = [a[0] + a[0] for a in computer_pieces]
    player_max = max(player_weights)
    computer_max = max(computer_weights)
    if player_max > computer_max:
        update_count(player_pieces[player_weights.index(player_max)])
        domino_snake.append(player_pieces[player_weights.index(player_max)])
        player_pieces.remove(player_pieces[player_weights.index(player_max)])
        return 4
    else:
        update_count(computer_pieces[computer_weights.index(computer_max)])
        domino_snake.append(computer_pieces[computer_weights.index(computer_max)])
        computer_pieces.remove(computer_pieces[computer_weights.index(computer_max)])
        return 3


# AI

'''
The primary objective of the AI is to determine which domino is the least favorable and then get rid of it. 
To reduce your chances of skipping a turn, you must increase the diversity of your pieces. 
For example, it's unwise to play your only domino that has a 3, unless there's nothing else that can be done. 
Using this logic, the AI will evaluate each domino in possession, based on the rarity. 
Dominoes with rare numbers will get lower scores, while dominoes with common numbers will get higher scores.

    - Count the number of 0's, 1's, 2's, etc., in your hand, and in the snake.
    - Each domino in your hand receives a score equal to the sum of appearances of each of its numbers.

The AI will now attempt to play the domino with the largest score, 
trying both the left and the right sides of the snake. 
If the rules prohibit this move, the AI will move down the score list and try another domino.
The AI will skip the turn if it runs out of options.
'''


def update_count(piece):
    count[piece[0]] += 1
    count[piece[1]] += 1


def start_count():
    for piece in computer_pieces:
        update_count(piece)


def pieces_order():
    return sorted(count, key=count.get, reverse=True)


def find_pieces(value):
    result = list()
    for i in range(0, len(computer_pieces)):
        if value in computer_pieces[i]:
            result.append(i + 1)
    return result


def choose_best():
    for value in pieces_order():  # pieces order is a list [6 0 2...] where 6,0,2 are domino values sorted descending
        for piece in find_pieces(value):
            if legal_input(piece, computer_pieces):
                return piece
            if legal_input(-piece, computer_pieces):
                return -piece
    return 0


# VARIABLES FOR PLAYING

statuses = {0: 'The game is over. You won!', 1: 'The game is over. The computer won!',
            2: 'The game is over. It\'s a draw!',
            3: 'It\'s your turn to make a move. Enter your command.',
            4: 'Computer is about to make a move. Press Enter to continue...'}
count = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
stock_pieces = [[a, b] for a in range(0, 7) for b in range(0 + a, 7)]
domino_snake = list()

computer_pieces = random.sample(stock_pieces, 7)
stock_pieces = difference(stock_pieces, computer_pieces)

player_pieces = random.sample(stock_pieces, 7)
stock_pieces = difference(stock_pieces, player_pieces)

status = choose_first_player()

start_count()

# THE GAME

while status > 2:
    print_menu()
    make_move()
    status = change_status()
print_menu()
