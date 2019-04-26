#!/usr/bin/env python 
#-*- coding: utf-8 -*-
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Ellipse

class Figure(Button):  
    def __init__(self,center_pos,**kwargs):
        super(Figure, self).__init__(**kwargs)
        self.size = 30,50
        self.place_on_center(center_pos)
        self.bind(on_release=self.move)
    
    def place_on_center(self,center_pos):
        #center_pos = self.get_center_of_tile(pos)
        print("center_pos:  " + str(center_pos))
        x = center_pos[0]-self.size[0]/2
        y = center_pos[1]-self.size[1]/2
        self.pos = x, y
    def move(self,obj):
        print("nothing to do here")

    def print_stuff(self,obj):
        print("figure "+ str(self.pos) +" pressed")

class King(Figure):
    def __init__(self,game,color,pos,**kwargs):
        center_pos = game.get_center_of_tile(pos)
        super(King, self).__init__(center_pos,**kwargs)
        self.text = "King"
        print(self.ids["symbol"].source)
        #,self.__class__.__name__ => King
        self.ids["symbol"].source = color.lower()+"_figure.png"

    def get_possible_movements(self):
        pass
    def move(self,obj):
        print("moving " + str(self.text))

class Queen(Figure):
    def __init__(self,game,color,pos,**kwargs):
        center_pos = game.get_center_of_tile(pos)
        super(Queen, self).__init__(center_pos,**kwargs)
        self.text = "Queen"
        self.ids["symbol"].source = color.lower()+"_figure.png"
        
    def move(self,obj):
        print("moving " + str(self.text))
    
#turm
class Rook(Figure):
    def __init__(self,game,color,pos,**kwargs):
        center_pos = game.get_center_of_tile(pos)
        super(Rook, self).__init__(center_pos,**kwargs)
        self.text = "Rook"
    def move(self,obj):
        print("moving " + str(self.text))
#läufer
class Bishop(Figure):
    def __init__(self,game,color,pos,**kwargs):
        center_pos = game.get_center_of_tile(pos)
        super(Bishop, self).__init__(center_pos,**kwargs)
        self.text = "Bishop"
    def move(self,obj):
        print("moving " + str(self.text))
#pferd
class Knight(Figure):
    def __init__(self,game,color,pos,**kwargs):
        center_pos = game.get_center_of_tile(pos)
        super(Knight, self).__init__(center_pos,**kwargs)
        self.text = "Knight"
    def move(self,obj):
        print("moving " + str(self.text))
#bauer
class Pawn(Figure):
    def __init__(self,game,color,pos,**kwargs):
        center_pos = game.get_center_of_tile(pos)
        super(Pawn, self).__init__(center_pos,**kwargs)
        self.text = "Pawn"
        self.alpha_numberic_pos = pos
        self.game = game
        self.not_moved = True
    def move(self,obj):
        
        with self.game.canvas:
            Color(1,0,0)
            d = 25
            print(self.alpha_numberic_pos)
            new_pos = self.alpha_numberic_pos[0]+str(int(self.alpha_numberic_pos[1])+1)
            target_pos = self.game.get_center_of_tile(new_pos)
            target_pos = target_pos[0]-15/2,target_pos[1]-15/2
            print(self.alpha_numberic_pos)
            Ellipse(pos=target_pos,size=(d,d))
        #print("moving " + str(self.color))



#Pawn
#(x,y) =>
#y+1 | y+2
#(x+1,y+1),(x-1,y-1)

#Rook
#(x,y) =>
#(x+~),(x-~),(y-~),(y+~)

#Bishop
#(x,y) =>
#(x+a,y+a) a=1|-1
#(x-a,y+a)(x+a,y-a) a=1|-1

#Knight
#(x,y) => 
#(x+1,y+2)(x-1,y+2)
#(x+1,y-2)(x-1,y-2)
#(x+2,y+1)(x-2,y+1)
#(x+2,y-1)(x-2,y-1)