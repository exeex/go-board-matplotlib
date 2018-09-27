#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
import math
from .goboard import GoBoard


class Point:
    def __init__(self, x, y):
        """
        棋盤座標和像素座標轉換
        """
        self.x = x
        self.y = y
        self.pixel_x = 30 + 30 * self.x
        self.pixel_y = 30 + 30 * self.y


class BoardCanvas(tk.Canvas):
    # 棋盤繪製
    def __init__(self, board: GoBoard, master=None, height=0, width=0):
        tk.Canvas.__init__(self, master, height=height, width=width)
        self.board = board
        self.chess_board_points = [[None for i in range(self.board.size_x)] for j in range(self.board.size_y)]
        self.init_chess_board_points()  # 畫點
        self.init_chess_board_canvas()  # 畫棋盤
        self.clicked = False
        self.put_temp = (0, 0)

    def init_chess_board_points(self):
        """
        生成棋盤點,並且對應到像素座標
        保存到 chess_board_points 屬性
        """
        for i in range(self.board.size_x):
            for j in range(self.board.size_y):
                self.chess_board_points[i][j] = Point(i, j)  # 轉換棋盤座標像素座標

    def init_chess_board_canvas(self):
        """
        初始化棋盤
        """

        for i in range(self.board.size_x):  # 直線
            self.create_line(self.chess_board_points[i][0].pixel_x, self.chess_board_points[i][0].pixel_y,
                             self.chess_board_points[i][self.board.size_x - 1].pixel_x,
                             self.chess_board_points[i][self.board.size_x - 1].pixel_y)

        for j in range(self.board.size_y):  # 橫線
            self.create_line(self.chess_board_points[0][j].pixel_x, self.chess_board_points[0][j].pixel_y,
                             self.chess_board_points[self.board.size_x - 1][j].pixel_x,
                             self.chess_board_points[self.board.size_x - 1][j].pixel_y)

        for i in range(self.board.size_x):  # 交點橢圓
            for j in range(self.board.size_y):
                r = 1
                self.create_oval(self.chess_board_points[i][j].pixel_x - r, self.chess_board_points[i][j].pixel_y - r,
                                 self.chess_board_points[i][j].pixel_x + r, self.chess_board_points[i][j].pixel_y + r)

    def put_stone_on_gui(self, i, j, color):
        if color == 'k':
            color = 'black'
        elif color == 'w':
            color = 'white'
        self.create_oval(self.chess_board_points[i][j].pixel_x - 10,
                         self.chess_board_points[i][j].pixel_y - 10,
                         self.chess_board_points[i][j].pixel_x + 10,
                         self.chess_board_points[i][j].pixel_y + 10, fill=color)
        tk.Canvas.update(self)

    def click_listener(self, event):  # click關鍵字重複

        """
        監聽滑鼠事件,根據滑鼠位置判斷落點
        """
        if not self.clicked:
            for i in range(self.board.size_x):
                for j in range(self.board.size_y):
                    square_distance = math.pow((event.x - self.chess_board_points[i][j].pixel_x), 2) + math.pow(
                        (event.y - self.chess_board_points[i][j].pixel_y), 2)
                    # 計算滑鼠的位置和點的距離
                    # 距離小於14的點

                    if square_distance <= 200 and not self.board.is_collision(i, j):  # 合法落子位置
                        # set clicked and write put stone position to put_temp
                        self.clicked = True
                        self.put_temp = (i, j)


class BoardFrame(tk.Frame):
    def __init__(self, board: GoBoard, master=None):
        tk.Frame.__init__(self, master)
        self.chess_board_label_frame = tk.LabelFrame(self, text="Chess Board", padx=5, pady=5)
        self.board_canvas = BoardCanvas(board, self.chess_board_label_frame, height=500, width=480)
        self.board_canvas.bind('<Button-1>', self.board_canvas.click_listener)
        self.chess_board_label_frame.pack()
        self.board_canvas.pack()