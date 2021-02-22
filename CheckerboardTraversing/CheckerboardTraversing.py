#Author:Martin Hubata

from tkinter import *
import time

#Class used both for graphics and algorithms
class check:
    def __init__(self):
        #Graphics attributes
        self.color = ""
        self.special_color = ""
        self.rectangle = None
        self.text = ""
        self.text_box = None

        #Alghoritm attributes
        self.visited = False
        self.reachable = 0

    #Returns the color that should be displayed
    def visible_color(self):
        if self.special_color != "":
            return self.special_color
        return self.color



class MainWindow:
    def __init__(self):

        self.check_size = 40
        self.check_count = 16
        self.knight = (0, 0)
        self.moves = [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]
        self.target_distance = 0
        self.clickable_canvas = True
        self.symmetry = True

        self.root = Tk()
        self.root.state("zoomed")
        self.root.title("CheckerboardTraversing")

        #TBD pevná velikost
        self.canvas = Canvas(self.root, width = self.check_size*self.check_count, height = self.check_size*self.check_count, highlightthickness = 0)
        self.canvas.grid(column = 0, columnspan = 6, row = 2, padx = 10, pady = 10)
        self.canvas.bind("<Button-1>", self.knight_move)
        self.canvas.bind("<Button-3>", self.add_move)

        self.create_board(self.canvas)

        self.b1 = Button(self.root, text="traverse", command=self.button_traverse)
        self.b1.grid(column = 0, row = 1)

        self.entry1 = Entry(self.root, width = 5)
        self.entry1.grid(column = 1, row = 0)
        self.b2 = Button(self.root, text="reach", command=self.button_reach)
        self.b2.grid(column = 1, row = 1)

        self.b3 = Button(self.root, text="reset", command=self.button_reset)
        self.b3.grid(column = 2, row = 1)
        self.b3["state"] = "disabled"

        self.b4 = Button(self.root, text="change boardsize", command=self.button_size)
        self.b4.grid(column = 3, row = 1)

        self.check1 = Checkbutton(self.root, text = "Symmetry mode", command=self.symmetry_change)
        self.check1.select()
        self.check1.grid(column = 4, row = 1)

        self.paint_knight()
        self.board_paint()

        self.root.mainloop()    


    #Creates the board, assigns base colors and canvas references to checks
    def create_board(self, canvas):
        self.board = [[check() for i in range(self.check_count)] for k in range(self.check_count)]
        #Assigns base (white/black) colors to checks
        for i in range(self.check_count):
            for k in range(self.check_count):
                if (i+k)%2==0:
                    self.board[i][k].color = "white"
                else:
                    self.board[i][k].color = "gray"
        #Creates canvas rectangles and textboxes, assigns their references to respective checkboxes
        for i in range(self.check_count):
            for k in range(self.check_count):
                x1 = i*self.check_size
                y1 = k*self.check_size
                x2 = x1 + self.check_size
                y2 = y1 + self.check_size
                self.board[i][k].rectangle = self.canvas.create_rectangle((x1, y1, x2, y2), fill = self.board[i][k].color, outline = self.board[i][k].color)
                self.board[i][k].text_box = self.canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text = self.board[i][k].text)



    #Changes the visible properites of all checks to the currently saved properties - either with or without special colors
    def board_paint(self):
        for i in range(self.check_count):
            for k in range(self.check_count):
                self.canvas.itemconfig(self.board[i][k].rectangle, fill = self.board[i][k].visible_color(), outline = self.board[i][k].visible_color())
                self.canvas.itemconfig(self.board[i][k].text_box, text = self.board[i][k].text)
        self.canvas.update()

     
    
    #Changes the knight's position, changes the respective colors of knight and his possible moves
    def knight_move(self, event):
        if self.clickable_canvas == True:
            #Uncolors the old knight and his possible moves
            self.board[self.knight[0]][self.knight[1]].special_color = ""
            for move in self.moves:
                if self.inbounds(self.knight, move):
                    self.board[self.knight[0] + move[0]][self.knight[1] + move[1]].special_color = ""

            #Calculates the position of the new knight
            self.knight = (event.x//self.check_size, event.y//self.check_size)
    
            #Uncolors the old knight and his possible moves
            self.board[self.knight[0]][self.knight[1]].special_color = "orange"
            for move in self.moves:
                if self.inbounds(self.knight, move):
                    self.board[self.knight[0] + move[0]][self.knight[1] + move[1]].special_color = "red"

            self.board_paint()

    #Add or deletes a move
    def add_move(self, event):
        if self.clickable_canvas == True:
            #Calculates the new moves relative position
            relative_x = event.x//self.check_size - self.knight[0]
            relative_y = event.y//self.check_size - self.knight[1]
            new_move = (relative_x, relative_y)

            #If it's a non-move, stops
            if new_move == (0, 0):
                return

            #If it's already a move, deletes it and uncolors it
            if (new_move in self.moves):
                self.unpaint_knight()
                if self.symmetry == False:
                    self.moves.remove(new_move)
                else:
                    if (new_move[0], new_move[1]) in self.moves:
                        self.moves.remove((new_move[0], new_move[1]))
                    if (-1 * new_move[0], new_move[1]) in self.moves:
                        self.moves.remove((-1 * new_move[0], new_move[1]))
                    if (new_move[0], -1 * new_move[1]) in self.moves:
                        self.moves.remove((new_move[0], -1 * new_move[1]))
                    if (-1 * new_move[0], -1 * new_move[1]) in self.moves:
                        self.moves.remove((-1 * new_move[0], -1 * new_move[1]))
                    if (new_move[1], new_move[0]) in self.moves:
                        self.moves.remove((new_move[1], new_move[0]))
                    if (-1 * new_move[1], new_move[0]) in self.moves:
                        self.moves.remove((-1 * new_move[1], new_move[0]))
                    if (new_move[1], -1 * new_move[0]) in self.moves:
                        self.moves.remove((new_move[1], -1 * new_move[0]))
                    if (-1 * new_move[1], -1 * new_move[0]) in self.moves:
                        self.moves.remove((-1 * new_move[1], -1 * new_move[0]))
            #Adds the move and colors it
            else:
                if self.symmetry == False:
                    self.moves.append(new_move)
                else:
                    if not (new_move[0], new_move[1]) in self.moves:
                        self.moves.append((new_move[0], new_move[1]))
                    if not (-1 * new_move[0], new_move[1]) in self.moves:
                        self.moves.append((-1 * new_move[0], new_move[1]))
                    if not (new_move[0], -1 * new_move[1]) in self.moves:
                        self.moves.append((new_move[0], -1 * new_move[1]))
                    if not (-1 * new_move[0], -1 * new_move[1]) in self.moves:
                        self.moves.append((-1 * new_move[0], -1 * new_move[1]))
                    if not (new_move[1], new_move[0]) in self.moves:
                        self.moves.append((new_move[1], new_move[0]))
                    if not (-1 * new_move[1], new_move[0]) in self.moves:
                        self.moves.append((-1 * new_move[1], new_move[0]))
                    if not (new_move[1], -1 * new_move[0]) in self.moves:
                        self.moves.append((new_move[1], -1 * new_move[0]))
                    if not (-1 * new_move[1], -1 * new_move[0]) in self.moves:
                        self.moves.append((-1 * new_move[1], -1 * new_move[0]))

            self.paint_knight()

            self.board_paint()


    
    #Checks if move relative to a position is inbounds (inside the board)
    def inbounds(self, position, move):
        if((0 <= position[0] + move[0] <= self.check_count - 1) and (0 <= position[1] + move[1] <= self.check_count - 1)):
            return True
        else:
            return False



    #Checks if every check is reachable from the knight's position
    def reachable(self):
        reachable_checks = 0
    
        #Uses BFS to traverse all of the reachable checks SUS
        queue = [self.knight]
        while len(queue) > 0 and reachable_checks != self.check_count * self.check_count:
            current_position = queue.pop(0)
            if self.board[current_position[0]][current_position[1]].visited == False:
                self.board[current_position[0]][current_position[1]].visited = True
                reachable_checks += 1
                for move in self.moves:
                    if self.inbounds(current_position, move) and self.board[current_position[0] + move[0]][current_position[1] + move[1]].visited == False:
                        queue.append((current_position[0] + move[0], current_position[1] + move[1]))

        return reachable_checks == self.check_count * self.check_count

    #Traverses the checkerboard using DFS, passes current position and number of current move
    def traversing(self, position, order):
        self.board[position[0]][position[1]].visited = True

        #Stop condition
        if order == self.check_count ** 2 - 1:
            self.board[position[0]][position[1]].text = str(order)
            return True

        #Decreases counter for every checker reachable by a single move
        for move in self.moves:
            if self.inbounds(position, move):
                self.board[position[0] + move[0]][position[1] + move[1]].reachable -= 1
    
        #Orders moves (Warnsdorff rule)
        ordered_moves = []
        for move in self.moves:
            if self.inbounds(position, move):
                ordered_moves.append(move)
        ordered_moves = sorted(ordered_moves, key=lambda current_move: self.board[position[0] + current_move[0]][position[1] + current_move[1]].reachable)

        #Tries ordered moves
        for move in ordered_moves:
            if self.board[position[0] + move[0]][position[1] + move[1]].visited == False and self.traversing((position[0] + move[0], position[1] + move[1]), order + 1):
                self.board[position[0]][position[1]].text = str(order)
                return True

        #Increases counter, because of backtracking
        for move in self.moves:
            if self.inbounds(position, move):
                self.board[position[0] + move[0]][position[1] + move[1]].reachable += 1

        self.board[position[0]][position[1]].visited = False

        return False


    def spread_general(self):
        print("new")
        queue = [(self.knight, 0), (None, None)]
        while len(queue) > 0 and queue != [(None, None)]:
            print(queue)
            current_position, current_distance = queue.pop(0)
            if current_position == None:
                for i in range(self.check_count):
                    for k in range(self.check_count):
                        print(self.board[i][k].visited, end=" ")
                        self.board[i][k].visited = False
                        
                    print()
                queue.append((None, None))
            else:
                if current_distance == self.target_distance:
                    self.board[current_position[0]][current_position[1]].special_color = "blue"
                else:
                    for move in self.moves:
                        if self.inbounds(current_position, move) and self.board[current_position[0] + move[0]][current_position[1] + move[1]].visited == False:
                            queue.append(((current_position[0] + move[0], current_position[1] + move[1]), current_distance + 1))
                            self.board[current_position[0] + move[0]][current_position[1] + move[1]].visited = True
                

    #Solves click on traverse button
    def button_traverse(self):
        self.reset_attributes()
        if self.reachable():
            self.clickable_canvas = False
            self.disable_buttons()
            self.reset_attributes()
            for i in range(self.check_count):
                for k in range(self.check_count):
                    self.board[i][k].visited = False
                    for move in self.moves:
                        if self.inbounds((i, k), move):
                            self.board[i + move[0]][k + move[1]].reachable += 1
            self.traversing(self.knight, 0)
            self.board_paint()
        else:
            PopupMessage("Warning", "Some checks can't be reached")


    def button_reach(self):
        try:
            self.target_distance = int(self.entry1.get())
        except:
            PopupMessage("Warning", "Not a number")
            return

        self.clickable_canvas = False
        self.disable_buttons()

        self.reset_attributes()

        self.spread_general()

        self.board_paint()
   
    #Solves click on reset button
    def button_reset(self):
        self.reset_attributes()
        self.paint_knight()
        self.board_paint()
    
        self.clickable_canvas = True
        self.enable_buttons()

    def button_size(self):
        PopupInput("Input", "Input a number between 1 and 16 inclusive", self)



    def paint_knight(self):
        self.board[self.knight[0]][self.knight[1]].special_color = "orange"
        for move in self.moves:
            if self.inbounds(self.knight, move):
                self.board[self.knight[0] + move[0]][self.knight[1] + move[1]].special_color = "red"

    def unpaint_knight(self):
        self.board[self.knight[0]][self.knight[1]].special_color = ""
        for move in self.moves:
            if self.inbounds(self.knight, move):
                self.board[self.knight[0] + move[0]][self.knight[1] + move[1]].special_color = ""



    def enable_buttons(self):
        self.b1["state"] = "normal"
        self.entry1["state"] = "normal"
        self.b2["state"] = "normal"
        self.b3["state"] = "disabled"
        self.b4["state"] = "normal"
        self.check1["state"] = "normal"

    def disable_buttons(self):
        self.b1["state"] = "disabled"
        self.entry1["state"] = "disabled"
        self.b2["state"] = "disabled"
        self.b3["state"] = "normal"
        self.b4["state"] = "disabled"
        self.check1["state"] = "disabled"



    def reset_attributes(self):
        for i in range(self.check_count):
            for k in range(self.check_count):
                self.board[i][k].text = ""
                self.board[i][k].special_color = ""
                self.board[i][k].visited = False
                self.board[i][k].reachable = 0 

    def resize_board(self, new_size):
        self.check_count = new_size
        self.canvas.delete("all")
        self.canvas.config(width = self.check_size*self.check_count, height = self.check_size*self.check_count)
        self.create_board(self.canvas)
        self.knight = (0, 0)
        for move in [x for x in self.moves]:
            if abs(move[0]) >= self.check_count or abs(move[1]) >= self.check_count:
                self.moves.remove(move)
        self.paint_knight()
        self.board_paint()

    def symmetry_change(self):
        if self.symmetry == False:
            self.symmetry = True
            for move in [x for x in self.moves]:
                if not (move[0], move[1]) in self.moves:
                    self.moves.append((move[0], move[1]))
                if not (-1 * move[0], move[1]) in self.moves:
                    self.moves.append((-1 * move[0], move[1]))
                if not (move[0], -1 * move[1]) in self.moves:
                    self.moves.append((move[0], -1 * move[1]))
                if not (-1 * move[0], -1 * move[1]) in self.moves:
                    self.moves.append((-1 * move[0], -1 * move[1]))
                if not (move[1], move[0]) in self.moves:
                    self.moves.append((move[1], move[0]))
                if not (-1 * move[1], move[0]) in self.moves:
                    self.moves.append((-1 * move[1], move[0]))
                if not (move[1], -1 * move[0]) in self.moves:
                    self.moves.append((move[1], -1 * move[0]))
                if not (-1 * move[1], -1 * move[0]) in self.moves:
                    self.moves.append((-1 * move[1], -1 * move[0]))
            self.paint_knight()
            self.board_paint()
        else:
            self.symmetry = False

class PopupMessage:
    #Disables main window and displays a popup window with given text
    def __init__(self, title, text):
        self.popup = Toplevel()
        self.popup.title(title)
        self.popup.grab_set()
        self.label1 = Label(self.popup, text=text)
        self.label1.pack(side=TOP, fill="x")
        self.b1 = Button(self.popup, text="OK", command = self.popup.destroy)
        self.b1.pack()
        self.popup.mainloop()

class PopupInput:
    #Disables main window and displays a popup window with given text and input box
    def __init__(self, title, text, parent):
        self.parent = parent
        self.popup = Toplevel()
        self.popup.title("Input")
        self.popup.grab_set()
        self.label = Label(self.popup, text=text)
        self.label.pack(side=TOP, fill="x")
        self.entry = Entry(self.popup)
        self.entry.pack(side = TOP, anchor = NW)
        self.b = Button(self.popup, text="OK", command = self.try_input)
        self.b.pack()
        self.popup.mainloop()

    def try_input(self):
        try:
            self.check_count = int(self.entry.get())
        except:
            PopupMessage("Warning", "Not a number")
            return
        if 1 <= int(self.entry.get()) <= 16:
            self.parent.resize_board(int(self.entry.get()))
            self.popup.destroy()
        else:
            PopupMessage("Warning", "Number not in range")

MainWindow()

