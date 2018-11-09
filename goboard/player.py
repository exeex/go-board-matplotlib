from .board import Board, BoardInfo


class Player:
    def __init__(self, color="black", **kwargs):
        """
        :param board_info: A GoBoard instance.
        :param color: to tell the ai what color he is playing. "black" or "white"
         """

        self.color = color
        self.gui = None

    def get_action(self, board: BoardInfo, timeout) -> (int, int):
        """
        Implement your algorithm here.
        To get the current status of the GoBoard, you might call self.board.steps and analysis it by your ai algorithm
        Before function return, you need to call self.put(x, y) once.
        :return:
        """
        raise NotImplementedError

    def bind_gui(self, gui):
        self.gui = gui

    def after_battle(self):
        pass


class Human(Player):
    def __init__(self, color, **kwargs):
        super(Human, self).__init__(color, **kwargs)

    def get_action(self, board: Board):
        x, y = self.gui.get_put_index()
        return x, y


class Replay(Player):
    def __init__(self, color, steps, **kwargs):
        super(Replay, self).__init__(color, **kwargs)
        self.steps = steps
        self.counter = 0

    def get_action(self, board: Board, timeout):
        x, y = self.steps[self.counter]
        self.counter += 1
        return x, y
