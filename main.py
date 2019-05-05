#!/usr/bin/env python 
#-*- coding: utf-8 -*-

from kivy.app import App
from kivy.core.window import Window

from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty, ListProperty
from kivy.graphics import Color
from kivy.utils import get_random_color

from kivy.vector import Vector
from kivy.clock import Clock

from kivy.config import Config
from kivy.resources import resource_add_path

import random
import time

from controller.logic import *

class Tile(Widget):
    rgb = ListProperty(3*[0])
    width = NumericProperty(0)
    height = NumericProperty(0)
    def __init__(self,size,color,**kwargs):
        super(Tile, self).__init__(**kwargs)
        self.rgb = color
        self.width = float(size)
        self.height = float(size)

class Game(Widget):
    def __init__(self,**kwargs):
        super(Game, self).__init__(**kwargs)
        self.width = Window.size[0]-200
        self.height = Window.size[1]-self.width
        print(Window.size)
        tile_size = float(self.width/8)
        self.board = self.generate_board(tile_size)
        self.figures_location = [[None] * 8 for i in range(8)]
        self.setup_game()

    def setup_game(self):
        self.setup_board("white")
        self.setup_board("black")

    def parse_pos_to_numbers(self,pos):
        alpha_numbers = "abcdefgh"
        numeric_numbers = "12345678"
        print(pos)
        return alpha_numbers.index(pos[0].lower()),numeric_numbers.index(pos[1])

    def parse_number_to_pos(self,number):
        numeric = "12345678"
        alpha = "abcdefgh"
        try:
            return alpha.index(number.lower())
        except:
            return numeric[number]
    def get_tile_from_board(self,pos):
        x = pos[0]
        y = pos[1]
        print(self.board[x][y].children)
        try:
            return self.board[x][y]
        except:
            return None
    def sync_pos(self,figure,new_pos):
        old_x = figure.board_pos[0]
        old_y = figure.board_pos[1]
        self.figures_location[old_x][old_y] = None
        
        new_x = new_pos[0]
        new_y = new_pos[1]
        print(len(self.figures_location))
        for i in range(8):
            print(len(self.figures_location[i]))
        self.figures_location[new_x][new_y] = figure

    def get_figure_from_board(self,pos):
        x = pos[0]
        y = pos[1]
        try:
            return self.figures_location[x][y]
        except:
            return None

    def add_to_board(self,figure,pos):
        x = pos[0]
        y = pos[1]
        self.figures_location[x][y] = figure
        self.add_widget(figure)

    def setup_board(self,color):
        addendum = ""
        if(color == "white"):
            addendum = "1"
            #knight&queen
            self.add_figure_to_board("Queen",color,"D"+addendum)
            self.add_figure_to_board("King",color,"E"+addendum)
            #pawns
            for row in "ABCDEFGH":
                self.add_figure_to_board("Pawn",color,row+"2")
        else:
            addendum = "8"
            #knight&queen
            self.add_figure_to_board("Queen",color,"E"+addendum)
            self.add_figure_to_board("King",color,"D"+addendum)
            for row in "ABCDEFGH":
                self.add_figure_to_board("Pawn",color,row+"7")

        #2xtowers
        self.add_figure_to_board("Rook",color,"a"+addendum)
        self.add_figure_to_board("Rook",color,"h"+addendum)

        #2xknights
        self.add_figure_to_board("Knight",color,"b"+addendum)
        self.add_figure_to_board("Knight",color,"g"+addendum)
        #2xbishop
        self.add_figure_to_board("Bishop",color,"c"+addendum)
        self.add_figure_to_board("Bishop",color,"f"+addendum)
        
    def add_figure_to_board(self,name,color,_alpha_pos):
        pos = self.parse_pos_to_numbers(_alpha_pos)
        figure = {}
        if name == "King":
            figure = King(self,color,pos)
        elif name == "Queen":
            figure = Queen(self,color,pos)
        elif name == "Pawn":
            figure = Pawn(self,color,pos)
        elif name == "Rook":
            figure = Rook(self,color,pos)
        elif name == "Knight":
            figure = Knight(self,color,pos)
        elif name == "Bishop":
            figure = Bishop(self,color,pos)
        else:
            return
        self.add_to_board(figure,pos) 
    def place_on_center(self,figure,pos):
        center_pos = self.get_center_of_tile(pos)
        x = center_pos[0]-figure.size[0]/2
        y = center_pos[1]-figure.size[1]/2
        figure.pos = x, y

    def get_center_of_tile(self,pos):
        print(pos)
        x=pos[0]
        y=pos[1]
        tile = self.board[x][y]
        x_pos = tile.x
        y_pos = tile.y
        #print(tile.size)
        x_pos += tile.size[0] / 2
        y_pos += tile.size[1] / 2
        return x_pos,y_pos

    def generate_board(self,tile_size):
        #setup random fields/ maybe with fixxed pattern
        board = []
        for x in range(0,8):
            row = []
            for y in range(0,8):
                color = 3*[(x+y)%2]
                column_tile = Tile(tile_size,color)
                column_tile.x = tile_size*x#+(x*100)
                column_tile.y = tile_size*y#+(y*100)
                symbol = self.parse_number_to_pos(x)+\
                        self.parse_number_to_pos(y)
                column_tile.text = symbol
                row.append(column_tile)
                self.add_widget(column_tile)
            board.append(row)
        return board
    
    def update(self,dt):
        pass

class ChessApp(App):
    def __init__(self,**kwargs):
        super(ChessApp, self).__init__(**kwargs)
        self.width = Window.size[0]
        self.height = Window.size[1]

    def build(self):
        print("window size: " + str(Window.size))
        print("one field has size: " + str(Window.size[0]/8)+ "px")
        game = Game()
        #game.color_red(count=5)
        Clock.schedule_interval(game.update,1.0/60)
        return game

def config(width,height):
    Config.set('graphics', 'resizable', False)
    Config.set('graphics', 'width', width)
    Config.set('graphics', 'height', height)
    resource_add_path("./modell")
    resource_add_path("./view/standard_theme/figures")
    Window.size=(width,height)
    #Window.fullscreen = True

if __name__ == '__main__':
    config(800,800)
    ChessApp().run()