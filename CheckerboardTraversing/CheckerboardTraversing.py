#Author:Martin Hubata
#Project: "Knight's" tour and checkerboard jumps
#Programming 1

from tkinter import *
import time

#Class used both for graphics and algorithms, represents a single check on a checkerboard
class check:
    def __init__(self):
        #---Graphics attributes---
        #Base color
        self.color = ""
        #Temporary special color
        self.special_color = ""
        #Reference to associated rectangle on canvas
        self.rectangle = None
        #Text to be displayed
        self.text = ""
        #Reference to associated text on canvas
        self.text_box = None
        #---Alghoritm attributes---
        self.visited = False
        self.reachable = 0

    #Returns the color that should be displayed
    def visible_color(self):
        if self.special_color != "":
            return self.special_color
        return self.color



#Primary window of the application
class MainWindow:
    #Constructor
    def __init__(self):
        #---Graphics attributes---
        #Size of a single check
        self.check_size = 40
        #---Other attributes---
        #Size of the board 1 to 16
        self.boardsize = 8
        #Position of the "knight"
        self.knight = (0, 0)
        #List of all currently inputted moves
        self.moves = [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]
        #Target distance for jumping through the board
        self.target_distance = 0
        #If clicking on the board should modify the position of the knight, or his possible moves
        self.modifiy_knight = True
        #Moves of the knight should be added/removed symmetrically 
        self.symmetry = True
        #It's only possible to display the knight, not modify it
        self.currently_touring = False

        #---App visuals---#
        #(Everyting is positioned using grid)
        #Primary window setup 
        self.root = Tk()
        self.root.state("zoomed")
        self.root.title("CheckerboardTraversing")
        #Canvas setup
        self.canvas = Canvas(self.root, width = self.check_size*self.boardsize, height = self.check_size*self.boardsize, highlightthickness = 0)
        self.canvas.grid(column = 0, columnspan = 6, row = 2, padx = 10, pady = 10)
        self.canvas.bind("<Button-1>", self.knight_move)
        self.canvas.bind("<Button-3>", self.add_remove_move)
        #Create a board on the canvas
        self.create_board(self.canvas)
        #Creating the UI bar
        self.b1 = Button(self.root, text="Tour the board", command=self.button_tour)
        self.b1.grid(column = 0, row = 0, padx = 10, pady = 2)

        self.entry1 = Entry(self.root, width = 5)
        self.entry1.grid(column = 1, row = 1, padx = 10, pady = 2)
        self.b2 = Button(self.root, text="Reach", command=self.button_reach)
        self.b2.grid(column = 1, row = 0, padx = 10, pady = 2)

        self.b3 = Button(self.root, text="Reset", command=self.button_reset)
        self.b3.grid(column = 2, row = 0, padx = 10, pady = 2)
        self.b3["state"] = "disabled"

        self.b4 = Button(self.root, text="Settings", command=self.button_setting)
        self.b4.grid(column = 3, row = 0, padx = 10, pady = 2)

        self.b5 = Button(self.root, text="Clear moves", command=self.button_clear_moves)
        self.b5.grid(column = 4, row = 0, padx = 10, pady = 2)

        self.check1 = Checkbutton(self.root, text = "Symmetry mode", command=self.symmetry_change)
        self.check1.select()
        self.check1.grid(column = 5, row = 0, padx = 10, pady = 2)
        
        self.paint_knight()
        self.board_paint()

        self.root.mainloop()    



    #---Board functions---
    #Creates the board as a two dimensional list of Checks, assigns base colors and canvas references to Checks
    def create_board(self, canvas):
        self.board = [[check() for i in range(self.boardsize)] for k in range(self.boardsize)]
        #Assigns base (white/black) colors to checks
        for i in range(self.boardsize):
            for k in range(self.boardsize):
                if (i+k)%2==0:
                    self.board[i][k].color = "white"
                else:
                    self.board[i][k].color = "gray"
        #Creates canvas rectangles and textboxes, assigns their references to respective checks
        for i in range(self.boardsize):
            for k in range(self.boardsize):
                x1 = i*self.check_size
                y1 = k*self.check_size
                x2 = x1 + self.check_size
                y2 = y1 + self.check_size
                self.board[i][k].rectangle = self.canvas.create_rectangle((x1, y1, x2, y2), fill = self.board[i][k].color, outline = self.board[i][k].color)
                self.board[i][k].text_box = self.canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text = self.board[i][k].text, font = ("TkDefaultFont", self.check_size//3))
    #Changes the visible properites of all checks to the currently saved properties - either with or without special colors
    def board_paint(self):
        for i in range(self.boardsize):
            for k in range(self.boardsize):
                self.canvas.itemconfig(self.board[i][k].rectangle, fill = self.board[i][k].visible_color(), outline = self.board[i][k].visible_color())
                self.canvas.itemconfig(self.board[i][k].text_box, text = self.board[i][k].text)
        self.canvas.update()

    
    
    #---Knight management---
    #Changes the knight's position, changes the respective colors of knight and his possible moves (if currently touring or in default state)
    def knight_move(self, event):
        if self.modifiy_knight == True or self.currently_touring == True:
            self.unpaint_knight()

            #Calculates the position of the new knight
            self.knight = (event.x//self.check_size, event.y//self.check_size)
    
            self.paint_knight()
            self.board_paint()
    #Adds or deletes a move when in default state
    def add_remove_move(self, event):
        if self.modifiy_knight == True:
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
        elif self.currently_touring == True:
            self.unpaint_knight()
            self.board_paint()

    def paint_knight(self):
        self.board[self.knight[0]][self.knight[1]].special_color = "orange"
        for move in self.moves:
            if self.inbounds(self.knight, move):
                self.board[self.knight[0] + move[0]][self.knight[1] + move[1]].special_color = "red"
    #Used to only erase the knight (not text for example)
    def unpaint_knight(self):
        self.board[self.knight[0]][self.knight[1]].special_color = ""
        for move in self.moves:
            if self.inbounds(self.knight, move):
                self.board[self.knight[0] + move[0]][self.knight[1] + move[1]].special_color = ""



    #---Algortihm functions---
    #-Utility-
    #Checks if move relative to a position is inside the board
    def inbounds(self, position, move):
        if((0 <= position[0] + move[0] <= self.boardsize - 1) and (0 <= position[1] + move[1] <= self.boardsize - 1)):
            return True
        else:
            return False
    #Clear the temporary graphic and algorithm properties of every check
    def reset_attributes(self):
        for i in range(self.boardsize):
            for k in range(self.boardsize):
                self.board[i][k].text = ""
                self.board[i][k].special_color = ""
                self.board[i][k].visited = False
                self.board[i][k].reachable = 0 

    #-Touring the board-
    #Checks if every check is reachable from the knight's position
    def all_reachable(self):
        reachable_checks = 0
    
        #Uses BFS to traverse all of the reachable checks SUS
        queue = [self.knight]
        while len(queue) > 0 and reachable_checks != self.boardsize * self.boardsize:
            current_position = queue.pop(0)
            if self.board[current_position[0]][current_position[1]].visited == False:
                self.board[current_position[0]][current_position[1]].visited = True
                reachable_checks += 1
                for move in self.moves:
                    if self.inbounds(current_position, move) and self.board[current_position[0] + move[0]][current_position[1] + move[1]].visited == False:
                        queue.append((current_position[0] + move[0], current_position[1] + move[1]))

        return reachable_checks == self.boardsize * self.boardsize
    #Traverses the checkerboard using DFS (implemented with recursion), writes the number of the move onto the respective check, passes the current position and number of current move
    def tour(self, position, order):
        #Kills the search after too much time passes
        if self.killswitch() == False:
            return False

        self.board[position[0]][position[1]].visited = True

        #Stop condition
        if order == self.boardsize ** 2 - 1:
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
            if self.board[position[0] + move[0]][position[1] + move[1]].visited == False and self.tour((position[0] + move[0], position[1] + move[1]), order + 1):
                self.board[position[0]][position[1]].text = str(order)
                return True

        #Increases counter, because of backtracking
        for move in self.moves:
            if self.inbounds(position, move):
                self.board[position[0] + move[0]][position[1] + move[1]].reachable += 1

        self.board[position[0]][position[1]].visited = False
        return False
    #Checks if too much time has passed
    def killswitch(self):
        if time.perf_counter() - self.start_time >= 5:
            return False
        else:
            return True

    #-Finding all checks in a given distance-
    #Searches for every check reachable in target_distance jumps using BFS
    def spread(self):
        #If the knight can't move or doesn't have to, only color the knight check
        if self.target_distance == 0 or self.moves == []:
            self.board[self.knight[0]][self.knight[1]].special_color = "blue"
            return
        #BFS (implemented with a queue) based algorithm, None pair signifies a change of distance from the start
        queue = [(self.knight, 0), (None, None)]
        while len(queue) > 0 and queue != [(None, None)]:
            current_position, current_distance = queue.pop(0)
            #If the distance from the start of currently investigated checks is about to change (compared to the previously investigated checks), 
            #resets the visited attribute and adds another None pair to signify the next distance change
            if current_position == None:
                for i in range(self.boardsize):
                    for k in range(self.boardsize):
                        self.board[i][k].visited = False
                queue.append((None, None))
            else:
                #If the current check is the right amount of jumps awaz from start, colors it
                if current_distance == self.target_distance:
                    self.board[current_position[0]][current_position[1]].special_color = "blue"
                else:
                    #Adds every check reachable from the current square and not already in the queue (controlled by the visited attribute) with the same distance to the queue
                    for move in self.moves:
                        if self.inbounds(current_position, move) and self.board[current_position[0] + move[0]][current_position[1] + move[1]].visited == False:
                            queue.append(((current_position[0] + move[0], current_position[1] + move[1]), current_distance + 1))
                            self.board[current_position[0] + move[0]][current_position[1] + move[1]].visited = True
                


    #---Button functions---
    def button_tour(self):
        self.reset_attributes()
        #Only starts the tour alghoritm if every check is reachable
        if self.all_reachable():
            self.modifiy_knight = False
            self.disable_buttons()
            self.currently_touring = True

            self.board_paint()

            #Precalculates the amount of reachable squares from every square (Warnsdorff's rule)
            self.reset_attributes()
            for i in range(self.boardsize):
                for k in range(self.boardsize):
                    self.board[i][k].visited = False
                    for move in self.moves:
                        if self.inbounds((i, k), move):
                            self.board[i + move[0]][k + move[1]].reachable += 1

            #Set's the start time
            self.start_time = time.perf_counter()   
            
            if not self.tour(self.knight, 0):
                PopupMessage("Warning", "Solution couldn't be found")
            else:
                self.board_paint()
        else:
            PopupMessage("Warning", "Some checks can't be reached")

    def button_reach(self):
        #Filter's the input
        try:
            self.target_distance = int(self.entry1.get())
        except ValueError:
            PopupMessage("Warning", "Not a number")
            return
        if self.target_distance < 0:
            PopupMessage("Warning", "Moves can't be negative")
            return

        self.modifiy_knight = False
        self.disable_buttons()

        self.reset_attributes()
        self.spread()

        self.board_paint()
   
    def button_reset(self):
        self.reset_attributes()

        self.currently_touring = False
        self.modifiy_knight = True
        self.enable_buttons()

        self.paint_knight()
        self.board_paint()

    def button_setting(self):
        PopupInput("Input", "Input a boardsize between 1 and 16 inclusive", self.boardsize, "Input a check size between 20 and 60", self.check_size, self)
    #Resizes the board with given parameters, called from input popup
    def resize_board(self, new_boardsize, new_checksize):
        self.boardsize = new_boardsize
        self.check_size = new_checksize
        self.canvas.delete("all")
        self.canvas.config(width = self.check_size*self.boardsize, height = self.check_size*self.boardsize)
        self.create_board(self.canvas)
        self.knight = (0, 0)
        for move in [x for x in self.moves]:
            if abs(move[0]) >= self.boardsize or abs(move[1]) >= self.boardsize:
                self.moves.remove(move)
        self.paint_knight()
        self.board_paint()

    def button_clear_moves(self):
        self.unpaint_knight()
        self.moves = []
        self.paint_knight()
        self.board_paint()

    #If going from asymmetry to symmetry, adds moves so they are symetric
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

    #Enables all but reset button and disables reset button
    def enable_buttons(self):
        self.b1["state"] = "normal"
        self.entry1["state"] = "normal"
        self.b2["state"] = "normal"
        self.b3["state"] = "disabled"
        self.b4["state"] = "normal"
        self.b5["state"] = "normal"
        self.check1["state"] = "normal"
    #Disables all but reset button and enables reset button
    def disable_buttons(self):
        self.b1["state"] = "disabled"
        self.entry1["state"] = "disabled"
        self.b2["state"] = "disabled"
        self.b3["state"] = "normal"
        self.b4["state"] = "disabled"
        self.b5["state"] = "disabled"
        self.check1["state"] = "disabled"   
        


#Temporarily disables parent window and displays a popup window with given title, text and a button
class PopupMessage:
    def __init__(self, title, text1):
        self.popup = Toplevel()
        self.popup.title(title)
        self.popup.grab_set()
        self.label1 = Label(self.popup, text = text1)
        self.label1.pack(side = TOP, fill = "x")
        self.b1 = Button(self.popup, text = "OK", command = self.popup.destroy)
        self.b1.pack(side = TOP)
        self.popup.mainloop()



#Temporarily disables parent window and displays a popup window with given title and two sets of text, input window and default value, and a button
#On correct input and button push calls a function of MainWindow that resizes the board
class PopupInput:
    def __init__(self, title, text1, current1, text2, current2, parent):
        self.parent = parent
        self.popup = Toplevel()
        self.popup.title("Input")
        self.popup.grab_set()
        self.label1 = Label(self.popup, text=text1)
        self.label1.pack(side=TOP, fill="x")
        self.entry1 = Entry(self.popup)
        self.entry1.pack(side = TOP)
        self.entry1.insert(END, str(current1))
        self.label2 = Label(self.popup, text=text2)
        self.label2.pack(side=TOP, fill="x")
        self.entry2 = Entry(self.popup)
        self.entry2.pack(side = TOP)
        self.entry2.insert(END, str(current2))
        self.b = Button(self.popup, text="OK", command = self.try_input)
        self.b.pack(side = TOP)
        self.popup.mainloop()

    def try_input(self):
        try:
            boardsize = int(self.entry1.get())
            check_size = int(self.entry2.get())
        except ValueError:
            PopupMessage("Warning", "Not a number")
            return

        if 1 <= boardsize <= 16 and 20 <= check_size <= 60:
            self.parent.resize_board(boardsize, check_size)
            self.popup.destroy()
        else:
            PopupMessage("Warning", "Number not in range")



MainWindow()

