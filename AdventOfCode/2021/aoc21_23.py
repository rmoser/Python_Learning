# Advent of Code
year = 2021
day = 23

import numpy as np
import aocd
import enum
import itertools

DEBUG = False

texta = """
#############
#.....D.C...#
###A#B#.#.###
  #A#B#C#D#
  #########
"""

text0 = """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########d
"""
text1 = aocd.get_data(day=day, year=year)

text2 = """
#############
#...........#
###D#C#A#B###
  #D#C#B#A#
  #D#B#A#C#
  #B#C#D#A#
  #########
 """

cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

HOME_ROW = frozenset([2, 3, 4, 5])
HOME_COL = frozenset([3, 5, 7, 9])

HOME_A = frozenset(itertools.product(HOME_ROW, [3]))
HOME_B = frozenset(itertools.product(HOME_ROW, [5]))
HOME_C = frozenset(itertools.product(HOME_ROW, [7]))
HOME_D = frozenset(itertools.product(HOME_ROW, [9]))

HOME = HOME_A | HOME_B | HOME_C | HOME_D
HOME_LIST = (HOME_A, HOME_A, HOME_B, HOME_B, HOME_C, HOME_C, HOME_D, HOME_D)
HOME_COL_LIST = (3, 3, 5, 5, 7, 7, 9, 9)
OTHER_HOMEY = (1, 0, 3, 2, 5, 4, 7, 6)
STAGES = frozenset(itertools.product([1], [1, 2, 4, 6, 8, 10, 11]))
ALL = HOME | STAGES | frozenset([(1, 3), (1, 5), (1, 7), (1, 9)])
EMPTY = frozenset([(3, 0), (3, 1), (4, 0), (4, 1), (3, 11), (3, 12), (4, 11), (4, 12)])


class Player(enum.IntEnum):
    A0 = 0
    A1 = 1
    B0 = 2
    B1 = 3
    C0 = 4
    C1 = 5
    D0 = 6
    D1 = 7


def bold(text):
    return '\033[1m' + text + '\033[0m' + '\0'


def show(moves):

    s = ''
    current_pos = set(moves[:, 0, 0])
    for r in range(5):
        s += '\n'
        for c in range(13):
            # print(r, c, end=' ')
            if (r, c) in ALL:
                if (r, c) in current_pos:
                    p = np.where([moves[i, 0, 0] == (r, c) for i in range(8)])[0][0]
                    # print(f"Player {p}: {Player(p)} at pos: {r, c} {len(s)}")
                    is_bold = Player(p).name[1] == '1'

                    if is_bold:
                        s += bold(Player(p).name[0])
                    else:
                        s += Player(p).name[0]
                else:
                    s += '.'
                    # print('floor ', len(s))
            elif r in (3, 4) and c in (0, 1, 11, 12):
                # print('corner ', len(s))
                s += ' '
            else:
                # print('wall ', len(s))
                s += '#'
    print(s)


def make_move(player: Player, move, moves, do_move=True):
    player = Player(player)
    global DEBUG
    debug = DEBUG

    if move in set(moves[:, 0, 0]):  # Target space occupied
        return False,

    pos = moves[player, 0, 0]  # Current pos
    remaining_moves = (moves[player, :, 0].astype(bool) == False).sum()

    if debug:
        print(f"{remaining_moves} moves remaining.")
    if remaining_moves == 0:
        if debug:
            print('No moves')
        return False,

    #
    # Check for valid end positions
    #
    # All valid moves target a new column
    if move[1] == pos[1]:
        if debug:
            print('Same column')
        return False,

    # All valid moves between HOME and STAGES target a new row
    if (move in HOME) != (pos in HOME):
        if move[0] == pos[0]:
            if debug:
                print(f'Same row')
            return False,

    if remaining_moves == 1:
        # Must go home
        if tuple(move) not in HOME_LIST[player]:
            if debug:
                print(f'Last move not to my Home')
            return False,

        # Home must be empty or occupied by a friend
        r, c = move
        me = player.name
        friend = Player[me[0] + str(1-int(me[1]))]
        other_home_pos = (2 + int(r == 2), c)
        if debug:
            print("Home target: ", friend, other_home_pos)
        if other_home_pos in set(moves[:, 0, 0]) and moves[friend, 0, 0] != other_home_pos:
            if debug:
                print(f'Last move to occupied Home')
            return False,  # That's NOT my friend

    if remaining_moves == 2:
        if tuple(move) not in STAGES | HOME_LIST[player]:
            if debug:
                print(f'Invalid target pos')
            return False,

    # Check for someone blocking the path:
    path = []
    if pos in HOME:  # Move up to STAGES row
        path += [(r, pos[1]) for r in range(pos[0]-1, 0, -1)]
    # Move across to target col
    d = 1 if pos[1] < move[1] else -1  # Direction: 1 or -1
    # Move across to target col
    path += [(1, c) for c in range(pos[1]+d, move[1]+d, d)]
    # Move down to my home
    if move in HOME_LIST[player]:
        path += [(r, move[1]) for r in range(2, move[0]+1)]

    if debug:
        print(f"Path from {pos} to {move}: {path}")
    if any(t in set(moves[:, 0, 0]) for t in path):
        if debug:
            print(f'Path blocked')
        return False,

    # Valid move
    if do_move:
        m = 4 - remaining_moves
        moves[player, m, 0] = tuple(move)
        moves[player, m, 1] = cost[player.name[0]] * len(path)
        moves[player, 0, 0] = tuple(move)
        moves[player, 0, 1] = moves[player, 1:4, 1].sum()
        # Record any first move that lands in the proper home
        if m == 2 and tuple(move) in HOME_LIST[player]:
            moves[player, 3, 0] = tuple(move)
            # No cost for this "move"

    return True, path


def valid_moves(player: Player, moves):
    global DEBUG

    result = set()
    current_pos = set(moves[:, 0, 0])

    pos = moves[player, 0, 0]
    if pos == max(HOME_LIST[player]):
        # No moves needed
        if DEBUG:
            print("Already home")
        return result

    if pos == min(HOME_LIST[player]) and player_at(max(HOME_LIST[player]), moves) == OTHER_HOMEY[player]:
        # No moves needed
        if DEBUG:
            print("Already home together")
        return result

    if moves[player, 3, 0] is not None:
        # No more moves
        if DEBUG:
            print("No moves left")
        return result

    if pos in HOME:
        # Check for immediately blocked path out of home
        if (pos[0]-1, pos[1]) in set(current_pos):
            if DEBUG:
                print("Blocked in the wrong home")
            return result

        open_stages = STAGES - set(moves[:, 0, 0])
        r, c = pos
        # Scan all stages to the right until we are blocked
        blocked = False
        for i in range(c+1, 12):
            p = (1, i)
            if p not in STAGES:
                continue

            if (1, i) not in open_stages:
                blocked = True
                continue
            if blocked:
                open_stages -= set([(1, i)])

        # Scan all stages to the left until we are blocked
        blocked = False
        for i in range(c-1, 0, -1):
            p = (1, i)
            if p not in STAGES:
                continue

            if (1, i) not in open_stages:
                blocked = True
                continue
            if blocked:
                open_stages -= set([(1, i)])

        if DEBUG:
            print("Open stages:", open_stages)


        result |= open_stages

        # check for open space in my home
        open_home = HOME_LIST[player] - current_pos
        my_stages = {(1, HOME_COL_LIST[player] - 1), (1, HOME_COL_LIST[player] + 1)}
        if open_home and (my_stages & open_stages):
            # Path is open to my home's 'porch', let's see inside...
            if len(open_home) == 2:
                # Deeper spot is open so take it (and skip the shallower spot)
                result |= set([(3, HOME_COL_LIST[player])])
            elif moves[OTHER_HOMEY[player], 0, 0] in HOME_LIST[player]:
                # My homey is here already
                result |= open_home

        if DEBUG:
            print("Open home: ", open_home)

    elif pos in STAGES:
        # Only valid move is to my home
        d = 1 if pos[1] < HOME_COL_LIST[player] else -1  # Direction

        for c in range(pos[1], HOME_COL_LIST[player], d):
            if (1, c) in (current_pos - {pos}):
                if DEBUG:
                    print("Blocked from going home")
                return result

        # Path is open to my home's 'porch', let's see inside...
        open_home = HOME_LIST[player] - current_pos
        if open_home:
            if len(open_home) == 2:
                # Deeper spot is open so take it (and skip the shallower spot)
                result |= set([(3, HOME_COL_LIST[player])])
            elif moves[OTHER_HOMEY[player], 0, 0] in HOME_LIST[player]:
                # My homey is here already
                result |= open_home
        if DEBUG:
            print("open home: ", open_home)

    return result


def valid_movers(moves):
    # Who still has moves:
    movers = set([Player(i) for i in np.where(moves[:, 3, 0] == None)[0]])
    current_pos = moves[:, 0, 0]

    # Remove those who are home
    movers = set(movers)
    for p in range(8):
        if current_pos[p] in HOME_LIST[p]:
            if current_pos[p] == max(HOME_LIST[p]):
                movers -= {p}
            other_homey = Player(OTHER_HOMEY[p])
            if current_pos[other_homey] in HOME_LIST[p]:
                movers -= {p}
                movers -= {other_homey}


    # Keep those with valid moves
    movers = [p for p in movers if valid_moves(p, moves)]

    return movers


def player_at(pos, moves):
    current_pos = moves[:, 0, 0]
    if not pos in set(current_pos):
        return

    for p in range(8):
        if pos == current_pos[p]:
            return Player(p)

    return


def read_map(map):
    # row 0 is current location
    # rows 1..3 capture each location: starting, first move, second move
    moves = np.empty(shape=(8, 4, 2), dtype=object)  # move and cost for each
    for r, row in enumerate(map):
        for c, p in enumerate(row):
            pos = (r, c)
            if p in 'ABCD':
                i = int(bool(moves[Player[f'{p}0'], 0, 0]))
                moves[Player[f'{p}{i}'], 0, 0] = pos
                moves[Player[f'{p}{i}'], 1, 0] = pos
                moves[Player[f'{p}{i}'], :, 1] = 0

    # Check for happy campers:
    for p in range(8):
        pos = moves[p, 0, 0]
        if pos == max(HOME_LIST[p]):
            # Already deep in home
            moves[p, 2, 0] = pos
            moves[p, 3, 0] = pos
        elif pos in HOME_LIST[p]:
            other_player = player_at(min(HOME_LIST[p]), moves)
            if other_player == OTHER_HOMEY[p]:
                # Already deep in home
                moves[p, 2, 0] = pos
                moves[p, 3, 0] = pos

    return moves


def is_done(moves):
    if set(moves[0:2, 0, 0]) != HOME_A:
        return False
    if set(moves[2:4, 0, 0]) != HOME_B:
        return False
    if set(moves[4:6, 0, 0]) != HOME_C:
        return False
    if set(moves[6:8, 0, 0]) != HOME_D:
        return False
    return True


def path(a, b, moves):
    # walks the path from a to b ignoring player collisions
    # Check for someone blocking the path:
    result = []
    if a[1] == b[1]:
        d = 1 if b[0] > a[0] else -1
        for r in range(a[0]+d, b[0]+d, d):
            result.append((r, a[1]))
        return result

    if a in HOME:  # Move up to STAGES row
        result += [(r, a[1]) for r in range(a[0] - 1, 0, -1)]
    # Move across to target col
    d = 1 if a[1] < b[1] else -1  # Direction: 1 or -1
    # Move across to target col
    result += [(1, c) for c in range(a[1] + d, b[1] + d, d)]
    # Move down to my home
    result += [(r, b[1]) for r in range(2, b[0] + 1)]

    return result


def play(games, iters=-1, best=None):
    if isinstance(games, np.ndarray):
        games = [[games]]
    if best is None:
        # best = (5 * min_score(games[-1][-1]), None)
        best = (np.inf, None)

    while iters != 0:
        iters -= 1
        end = len(games)
        print(end)
        if end == 0:
            break

        for _ in range(end):
            g_list = games.pop(0)
            game = g_list[-1]

            # Abort bad game decisions
            if score(game) > best[0]:
                continue

            for player in valid_movers(game):
                player_moves = valid_moves(player, game)
                home_moves = player_moves & HOME_LIST[player]
                if home_moves:
                    _game = game.copy()
                    make_move(player, max(home_moves), _game)

                    _g_list = g_list.copy()
                    _g_list.append(_game)
                    if is_done(_game):
                        s = score(_game)
                        if s < best[0]:
                            best = (s, _g_list)
                            print("New best: ", best[0])
                            show(best[1][-1])
                        continue

                    if score(_game) > best[0]:
                        continue
                    games.append(_g_list)
                    continue

                # Only use the furthest stage moves
                stage_moves = [min(player_moves), max(player_moves)]
                # stage_moves = player_moves & STAGES
                for move in stage_moves:
                    _game = game.copy()
                    make_move(player, move, _game)
                    if score(_game) > best[0]:
                        continue

                    _g_list = g_list.copy()
                    _g_list.append(_game)
                    games.append(_g_list)

    return best, games


def score(game):
    return game[:, 0, 1].sum()


def min_score(game):
    s = 0
    for p in range(8):
        steps = path(game[p, 0, 0], min(HOME_LIST[p]), game)
        s += cost[Player(p).name[0]] * len(steps)
    return s


if __name__ == '__main__':
    pone = ''
    ptwo = ''

    text = text0
    text = text.strip().splitlines()

    moves = read_map(text)

    if False:
        # Generate all possible move sequences
        # Each game is a series of player, move tuples
        game = moves.copy()
        make_move(0, (1, 2), game)
        show(game)
        print(score(game))

        make_move(2, (1, 4), game)
        show(game)
        print(score(game))

        make_move(1, (1, 10), game)
        show(game)
        print(score(game))

        make_move(7, (3, 9), game)
        show(game)
        print(score(game))

        make_move(4, (3, 7), game)
        show(game)
        print(score(game))

        make_move(5, (2, 7), game)
        show(game)
        print(score(game))

        make_move(2, (3, 5), game)
        show(game)
        print(score(game))

        make_move(6, (2, 9), game)
        show(game)
        print(score(game))

        make_move(3, (2, 5), game)
        show(game)
        print(score(game))

        make_move(1, (3, 3), game)
        show(game)
        print(score(game))

        make_move(0, (2, 3), game)
        show(game)
        print(score(game))

    best, games = play(moves)
    game = best[-1][-1]
    show(moves)
    print()
    show(game)

    # show(best[1])

    pone = best[0]

    print(f"AOC {year} day {day}  Part One: {pone}")

    print(f"AOC {year} day {day}  Part Two: {ptwo}")
