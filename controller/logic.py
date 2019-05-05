#!/usr/bin/env python 
#-*- coding: utf-8 -*-
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Ellipse
from kivy.uix.behaviors import ButtonBehavior

class Figure(Button): 
    def __init__(self,game,pos,**kwargs):
        super(Figure, self).__init__(**kwargs)
        self.size = 30,50
        #(2, 'solid', (1,1,1,1.))
        self.game = game
        self.position_on_board(pos)
        self.bind(on_release=self.toggle_active_figure,on_press=self.click)
        
    def position_on_board(self,pos):
        self.board_pos=pos
        center_pos = self.game.get_center_of_tile(pos)
        #print("center_pos:  " + str(center_pos))
        #print("pos : " + str(pos))
        self.place_on_center(center_pos)
    
    def place_on_center(self,center_pos):
        #center_pos = self.get_center_of_tile(pos)
        x = center_pos[0]-self.size[0]/2
        y = center_pos[1]-self.size[1]/2
        self.pos = x, y
    def click(self,obj):
        remove_examples(self.game)
        print("no click implemented")
    
    def toggle_active_figure(self,obj):
        global active_figure
        try:
            active_figure
        except:
            active_figure = self.uid
            return
        if(str(active_figure)==str(self.uid)):
            del active_figure
            return
    def delete_active_figure(self):
        global active_figure
        del active_figure
    def get_active_figure(self):
        global active_figure
        try:
            return active_figure
        except:
            return None

    def move(self,obj):
        print("nothing to do here")
    def clear_examples(self,obj):
        remove_examples(self.game)

    def print_stuff(self,obj):
        print("figure "+ str(self.pos) +" pressed")

class King(Figure):
    def __init__(self,game,color,pos,**kwargs):
        super(King, self).__init__(game,pos,**kwargs)
        set_figure(self,"Knight",color)

    def get_possible_movements(self):
        pass
    def move(self,obj):
        print("moving " + str(self.text))

class Queen(Figure):
    def __init__(self,game,color,pos,**kwargs):
        super(Queen, self).__init__(game,pos,**kwargs)
        set_figure(self,"Queen",color)
    def move(self,obj):
        print("moving " + str(self.text))
    
#turm
class Rook(Figure):
    def __init__(self,game,color,pos,**kwargs):
        super(Rook, self).__init__(game,pos,**kwargs)
        set_figure(self,"Rook",color)
    def move(self,obj):
        print("moving " + str(self.text))
#läufer
class Bishop(Figure):
    def __init__(self,game,color,pos,**kwargs):
        super(Bishop, self).__init__(game,pos,**kwargs)
        set_figure(self,"Bishop",color)
    def move(self,obj):
        print("moving " + str(self.text))
#pferd
class Knight(Figure):
    def __init__(self,game,color,pos,**kwargs):
        super(Knight, self).__init__(game,pos,**kwargs)
        set_figure(self,"Knight",color)
    def move(self,obj):
        print("moving " + str(self.text))
#bauer
class Pawn(Figure):
    def __init__(self,game,color,pos,**kwargs):
        super(Pawn, self).__init__(game,pos,**kwargs)
        set_figure(self,"Pawn",color)
        self.board_pos = pos
        self.game = game
        self.moved = False

    def click(self,obj):
        remove_examples(self.game)        
        active_figure=self.get_active_figure()
        if active_figure != None:
            self.show_possible_move()
            return
        if str(active_figure) == str(self.uid):
            return
        self.show_possible_move()

    def callback_on_move(self):
        #print("callback pawn called")
        self.moved = True

    def show_possible_move(self):
        if(self.team_color == "white"):
            direction = 1
        else:
            direction = -1
        if(not self.moved and not hasattr(self.game,"examples")):
            #check for all in front of pawn
            for field in [1,2]:
                target_pos=self.board_pos[0], self.board_pos[1]+field*direction
                if(self.game.get_tile_from_board(target_pos).children != []):
                    print("tile existiert")
                    pass
                    #print("figure")
                    #print(self.game.get_tile_from_board(target_pos).children)
                draw_example(self.game,target_pos,self)
            #check two diagonals
            return
            target_pos = (self.board_pos[0]+1, self.board_pos[1]+direction)
            if(self.check_kill(target_pos)):
                draw_example(self.game,target_pos,self)
            
            target_pos=(self.board_pos[0]-1, self.board_pos[1]+direction)
            if(self.check_kill(target_pos)):
                draw_example(self.game,target_pos,self)
            # target_0_pos=self.board_pos[0], self.board_pos[1]+1*direction
            # target_1_pos=self.board_pos[0], self.board_pos[1]+2*direction
        elif(not self.moved):
            target_pos=self.board_pos[0], self.board_pos[1]+1*direction
            draw_example(self.game,target_pos,self)
    
    def check_kill(self,pos):
        #print(pos)
        target_tile = self.game.get_tile_from_board(pos)
        if(target_tile.children):
            #print("check kill true")
            return True
        else:
            #print("check kill false")
            return False      
    def move(self,obj):
        pass
class Example(Figure):
    def __init__(self,game,pos,figure,callback_function=None,**kwargs):
        super(Example, self).__init__(game,pos,**kwargs)
        set_figure(self,"example","example")
        if callback_function == None:
            self.callback_function = self.dummy
        else:
            self.callback_function = callback_function
        self.board_pos = pos
        self.group = "example"
        self.game = game
        self.referenced_figure = figure

    def click(self,obj):
        #print("referenced_figure: " + str(figure.__name__))
        remove_examples(self.game)
        print("positioning figure: " + str(self.board_pos))
        
        figure = self.referenced_figure
        figure.position_on_board(self.board_pos)
        self.callback_function()

    def dummy(self):
        print(self.board_pos)
        pass
def remove_examples(game):
    if(not hasattr(game,"examples")):
        return
    for example in game.examples:
        game.remove_widget(example)
    del game.examples

def draw_example(game,pos,figure):
    print("drawing example with: " +str(pos))
    try:
        target_pos = game.get_center_of_tile(pos)
    except:
        return
    target_pos = target_pos[0]-30/2,target_pos[1]-50/2
    example = Example(game,pos,figure,figure.callback_on_move)#
    if(hasattr(game,"examples")):
        game.examples.append(example)
    else:
        game.examples= [example]
    game.add_widget(example)
    
    #self.game.canvas.add()        
    #self.game.canvas.add()            

def set_figure(figure,name,color):
    #figure.text = name
    name = "figure"
    figure.ids["symbol"].source = color.lower()+"_"+name.lower()+".png"
    figure.team_color = color.lower()
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