import chess
import chess.pgn
import time
import sys

def findFname(input, num):
    fname = input.rstrip('.pgn').lstrip('data/')
    fname = 'results/' + fname + '_' + str(num) + '.output'
    return fname

def saveData(data, num):
    with open(findFname(sys.argv[1], num), 'w') as outfile:
        sorted_data = sorted(data, key=data.get, reverse=True)
        for r in sorted_data:
            outfile.write('{0},{1}\n'.format(r, data[r]))

pgn = open(sys.argv[1], 'r')

match = chess.pgn.read_game(pgn)
data = {}
total_games = 0
eval_games = 0
num = 0
start = time.time()

while match != None:
    node = match
    try:
        comment = node.variations[0].comment
    except:
        match = chess.pgn.read_game(pgn)
        total_games += 1
        continue

    if '%eval' not in comment:
        # There is no eval for this game, skip to next
        match = chess.pgn.read_game(pgn)
        total_games += 1
        continue

    # Game has an eval, loop through moves
    while not node.is_end():
        next_node = node.variations[0]
        if 4 in next_node.nags:
            # Check the nag set for each node for 4: the indicator for blunder
            fen = node.board().fen()
            move = node.board().san(next_node.move)
            index = str(fen) + "," + str(move)

            if index in data:
                data[index] += 1
            else:
                data[index] = 1

        node = next_node

    match = chess.pgn.read_game(pgn)
    total_games += 1
    eval_games += 1

    if eval_games % 100000 == 0:
        # Prepare to write dict to outfile
        num += 1
        saveData(data, num)
        data = {}
        print('eval = {0} : total = {1}'.format(eval_games, total_games))


print('FINAL: eval = {0} : total = {1}'.format(eval_games, total_games))

end = time.time()
t = end - start

# Prepare to write dict to outfile
num += 1

saveData(data, num)

#Save stats to the logs file
with open('logs', 'a') as outfile:
    name = sys.argv[1].rstrip('.pgn')
    name = name.lstrip('data/')
    outfile.write('{0}: eval = {1}, total = {2}, time = {3:.1f}\n'.format(name, eval_games, total_games, t))
