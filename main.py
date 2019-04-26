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
        self.width = Window.size[0]
        self.height = Window.size[1]-self.width
        tile_size = float(Window.size[0]/8)
        self.board = self.generate_board(tile_size)
        self.setup_board("white")
        self.setup_board("black")
    
    def setup_game(self):
        self.setup_white()
        self.setup_black()

    def setup_board(self,color):
        addendum = ""
        if(color == "white"):
            addendum = "1"
            #knight&queen
            figure = Queen(self,color,"D"+addendum)
            self.add_widget(figure)
            figure = King(self,color,"E"+addendum)
            self.add_widget(figure)
            for row in "ABCDEFGH":
                figure = Pawn(self,color,row+"2")
                self.add_widget(figure)
        else:
            addendum = "8"
            #knight&queen
            figure = Queen(self,color,"E"+addendum)
            self.add_widget(figure)
            figure = King(self,color,"D"+addendum)
            self.add_widget(figure)
            for row in "ABCDEFGH":
                figure = Pawn(self,color,row+"7")
                self.add_widget(figure)
        #2xtowers
        figure = Rook(self,color,"a"+addendum)
        self.add_widget(figure)
        figure = Rook(self,color,"h"+addendum)
        self.add_widget(figure)

        #2xknights
        figure = Knight(self,color,"b"+addendum)
        self.add_widget(figure)
        figure = Knight(self,color,"g"+addendum)
        self.add_widget(figure)

        #2xbishop
        figure = Bishop(self,color,"c"+addendum)
        self.add_widget(figure)
        figure = Bishop(self,color,"f"+addendum)
        self.add_widget(figure)
    def parse_pos_to_numbers(self,pos):
        alpha_numbers = "ABCDEFGH"
        numeric_numbers = "12345678"
        return alpha_numbers.index(pos[0]),numeric_numbers.index(pos[1])
    
    def place_on_center(self,figure,pos):
        center_pos = self.get_center_of_tile(pos)
        x = center_pos[0]-figure.size[0]/2
        y = center_pos[1]-figure.size[1]/2
        figure.pos = x, y

    def get_center_of_tile(self,pos):
        tile = self.board[pos.upper()]
        x_pos = tile.x
        y_pos = tile.y
        print(tile.size)
        x_pos += tile.size[0] / 2
        y_pos += tile.size[1] / 2
        return x_pos,y_pos

    def generate_board(self,tile_size):
        #setup random fields/ maybe with fixxed pattern
        numeric = "12345678"
        alpha = "ABCDEFGH"
        board = {}
        for x in range(0,8):
            for y in range(0,8):
                color = 3*[(x+y)%2]
                column_tile = Tile(tile_size,color)
                column_tile.x = tile_size*x#+(x*100)
                column_tile.y = tile_size*y#+(y*100)
                symbol = alpha[x]+numeric[y]

                column_tile.text = symbol

                board[symbol] = column_tile
                self.add_widget(column_tile)
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
    Window.fullscreen = True

if __name__ == '__main__':
    config(600,800)
    ChessApp().run()