import glob
import os
import sys
import importlib
import itertools
import time
from goboard import GomokuGameHandler
# from goboard.judge import Win, Lose
from goboard.exception import Win, Lose
from goboard.logger import log
import inspect
import json
import pickle


class referee:
    def __init__(self, file_path='./ai'):
        self.file_path = file_path
        self.ailist = [os.path.splitext(os.path.basename(path))[0] for path in glob.glob(self.file_path + "/*.py")]
        self.ailist = ['ai.' + str(x) for x in self.ailist]
        for module in self.ailist:
            try:
                module_obj = importlib.import_module(module)
                # create a global object containging our module
                globals()[module] = module_obj
                # because we want to import using a variable, do it this way

            except ImportError:
                sys.stderr.write("ERROR: missing python module: " + module + "\n")
                sys.exit(1)

    def competitors(self):
        return [competitor.split('.')[1] for competitor in self.ailist]

    def Round_robin(self):
        return list(itertools.combinations(self.ailist, r=2))

    def palyerName(self, classObj):
        path = inspect.getfile(classObj.__class__)
        name = os.path.splitext(os.path.basename(path))[0]
        return name

    def finalScore(self):
        pass


# TODO: combine gameBlackFirst and gameWhiteFirst
def gameBlackFirst(black_player, white_player, referee):
    with GomokuGameHandler(black_player, white_player, board_size=(13, 13)) as (black_round, white_round, board):
        for _ in range(11 * 11 // 2):
            try:
                black_round()
                # time.sleep(0.3)
                white_round()
                # time.sleep(0.3)
            except Win as e:
                log('[end game] %s' % e)
                # time.sleep(10)
                if e.winner == black_round.player:
                    return (referee.palyerName(black_round.player), referee.palyerName(white_round.player),
                            black_round.time_remaining, white_round.time_remaining)
                else:
                    return (referee.palyerName(white_round.player), referee.palyerName(black_round.player),
                            black_round.time_remaining, white_round.time_remaining)

            except Lose as e:
                log('[end game] %s' % e)
                # time.sleep(10)
                if e.loser == black_round.player:
                    return (referee.palyerName(white_round.player), referee.palyerName(black_round.player),
                            black_round.time_remaining, white_round.time_remaining)
                else:
                    return (referee.palyerName(black_round.player), referee.palyerName(white_round.player),
                            black_round.time_remaining, white_round.time_remaining)


def gameWhiteFirst(black_player, white_player, referee):
    with GomokuGameHandler(black_player, white_player, board_size=(13, 13)) as (black_round, white_round, board):

        for _ in range(11 * 11 // 2):
            try:
                white_round()
                # time.sleep(0.3)
                black_round()
                # time.sleep(0.3)
            except Win as e:
                log('[end game] %s' % e)
                # time.sleep(10)
                if e.winner == black_round.player:
                    return (referee.palyerName(black_round.player), referee.palyerName(white_round.player),
                            black_round.time_remaining, white_round.time_remaining)
                else:
                    return (referee.palyerName(white_round.player), referee.palyerName(black_round.player),
                            black_round.time_remaining, white_round.time_remaining)

            except Lose as e:
                log('[end game] %s' % e)
                # time.sleep(10)
                if e.loser == black_round.player:
                    return (referee.palyerName(white_round.player), referee.palyerName(black_round.player),
                            black_round.time_remaining, white_round.time_remaining)
                else:
                    return (referee.palyerName(black_round.player), referee.palyerName(white_round.player),
                            black_round.time_remaining, white_round.time_remaining)


if __name__ == '__main__':
    judge = referee()
    schedule = judge.Round_robin()
    print(schedule)
    # TODO: When exception occur write down the schedule
    # player1 = globals()[schedule[0][0]].Ai
    # player2 = globals()[schedule[0][1]].Ai
    #
    # black_player = player1("black", board_size=(13, 13))
    # white_player = player2("white", board_size=(13, 13))
    # # print(black_player)
    #
    # a = gameBlackFirst(black_player, white_player)
    # print(a,  '---')

    # result = []
    # for idx, game in enumerate(schedule):
    #     player1 = globals()[game[0]].Ai
    #     player2 = globals()[game[1]].Ai
    #     print(player1, player2, '--')
    #     temp_result = []
    #     for i in range(2):
    #         black_player = player1('black', board_size=(13, 13))
    #         white_player = player2('white', board_size=(13, 13))
    #         a = gameBlackFirst(black_player, white_player, judge)
    #         temp_result.append(a)
    #         b = gameWhiteFirst(black_player, white_player, judge)
    #         temp_result.append(b)
    #     with open('result.json', 'a') as file:
    #         json.dump(temp_result, file)
    #         file.write("\n")
    #     # TODO: use klepto
    #     result.append(temp_result)
    # with open('result.pickle', 'wb') as file:
    #     pickle.dump(result, file)
    # print(result)

    result = {}
    for idx, game in enumerate(schedule):
        player1 = globals()[game[0]].Ai
        player2 = globals()[game[1]].Ai
        print(player1, player2, '--')
        black_player = player1('black', board_size=(13, 13))
        white_player = player2('white', board_size=(13, 13))
        temp_result = []
        for i in range(2):
            a = gameBlackFirst(black_player, white_player, judge)
            temp_result.append(a)
            b = gameWhiteFirst(black_player, white_player, judge)
            temp_result.append(b)
        with open('result.json', 'a') as file:
            json.dump(temp_result, file)
            file.write("\n")
        # TODO: use klepto

        result[(game[0].split('.')[1], game[1].split('.')[1])] = temp_result
    with open('result.pickle', 'wb') as file:
        pickle.dump(result, file)
    print(result)

    # result.append(a)
    # print(a)
    # a=name_of_function(player1)
    # print(type(player1).__class__.__name__)
    # result = pk(player, white)
    # print(result)