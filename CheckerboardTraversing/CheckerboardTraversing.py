from tkinter import *

check_size = 40
check_count = 8
knight = (2, 2)
moves = [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]



#Class used both for graphics and algorithms
class check:
    def __init__(this):
        #Graphics attributes
        this.color = ""
        this.special_color = ""
        this.rectangle = None
        this.text = ""
        this.text_box = None

        #Alghoritm attributes
        this.visited = False
        this.reachable = 0

    #Returns the color that should be displayed
    def visible_color(this, use_special):
        if use_special and this.special_color != "":
            return this.special_color
        return this.color



#Creates the board, assigns base colors and canvas references to checks
def create_board(check_count):
    board = [[check() for i in range(check_count)] for k in range(check_count)]
    #Assigns base (white/black) colors to checks
    for i in range(check_count):
        for k in range(check_count):
            if (i+k)%2==0:
                board[i][k].color = "white"
            else:
                board[i][k].color = "gray"
    #Creates canvas rectangles and textboxes, assigns their references to respective checkboxes
    for i in range(check_count):
        for k in range(check_count):
            x1 = i*check_size
            y1 = k*check_size
            x2 = x1 + check_size
            y2 = y1 + check_size
            board[i][k].rectangle = canvas.create_rectangle((x1, y1, x2, y2), fill=board[i][k].color, outline=board[i][k].color)
            board[i][k].text_box = canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text = board[i][k].text)
    return board



#Changes the visible properites of all checks to the currently saved properties - either with or without special colors
def board_paint(special_on):
    for i in range(check_count):
        for k in range(check_count):
            canvas.itemconfig(board[i][k].rectangle, fill=board[i][k].visible_color(special_on), outline=board[i][k].visible_color(special_on))
            canvas.itemconfig(board[i][k].text_box, text = board[i][k].text)
    canvas.update()

     
    
#Changes the knight's position, changes the respective colors of knight and his possible moves
def knight_move(event):
    global knight
    global moves

    #Uncolors the old knight and his possible moves
    board[knight[0]][knight[1]].special_color = ""
    for move in moves:
        if inbounds(knight, move):
            board[knight[0] + move[0]][knight[1] + move[1]].special_color = ""

    #Calculates the position of the new knight
    knight = (event.x//check_size, event.y//check_size)
    
    #Uncolors the old knight and his possible moves
    board[knight[0]][knight[1]].special_color = "orange"
    for move in moves:
        if inbounds(knight, move):
            board[knight[0] + move[0]][knight[1] + move[1]].special_color = "red"

    board_paint(True)

#Add or deletes a move
def add_move(event):
    global knight
    global moves

    #Calculates the new moves relative position
    relative_x = event.x//check_size - knight[0]
    relative_y = event.y//check_size - knight[1]
    new_move = (relative_x, relative_y)

    #If it's a non-move, stops
    if new_move == (0, 0):
        return

    #If it's already a move, deletes it and uncolors it
    if (new_move in moves):
        moves.remove(new_move)
        board[knight[0] + relative_x][knight[1] + relative_y].special_color = ""

    #Adds the move and colors it
    else:
        moves.append(new_move)
        board[knight[0] + new_move[0]][knight[1] + new_move[1]].special_color = "red"

    board_paint(True)


    
#Checks if move relative to a position is inbounds (inside the board)
def inbounds(position, move):
    global check_count
    if((0 <= position[0] + move[0] <= check_count - 1) and (0 <= position[1] + move[1] <= check_count - 1)):
        return True
    else:
        return False



#Checks if every check is reachable from the knight's position
def reachable():
    reachable_checks = 0
    max_reachable_checks = check_count * check_count
    
    #Uses BFS to traverse all of the reachable checks
    queue = [knight]
    while len(queue) > 0 and reachable_checks != check_count * check_count:
        current_position = queue.pop(0)
        if board[current_position[0]][current_position[1]].visited == False:
            board[current_position[0]][current_position[1]].visited = True
            reachable_checks += 1
            for move in moves:
                if inbounds(current_position, move) and board[current_position[0] + move[0]][current_position[1] + move[1]].visited == False:
                    queue.append((current_position[0] + move[0], current_position[1] + move[1]))

    return reachable_checks == max_reachable_checks

#Traverses the checkerboard using DFS, passes current position and number of current move
def traversing(position, order):
    board[position[0]][position[1]].visited = True

    #Stop condition
    if order == check_count ** 2 - 1:
        board[position[0]][position[1]].text = str(order)
        return True

    #Decreases counter for every checker reachable by a single move
    for move in moves:
        if inbounds(position, move):
            board[position[0] + move[0]][position[1] + move[1]].reachable -= 1
    
    #Orders moves (Warnsdorff rule)
    ordered_moves = []
    for move in moves:
        if inbounds(position, move):
            ordered_moves.append(move)
    ordered_moves = sorted(ordered_moves, key=lambda current_move: board[position[0] + current_move[0]][position[1] + current_move[1]].reachable)

    #Tries ordered moves
    for move in ordered_moves:
        if board[position[0] + move[0]][position[1] + move[1]].visited == False and traversing((position[0] + move[0], position[1] + move[1]), order + 1):
            board[position[0]][position[1]].text = str(order)
            return True

    #Increases counter, because of backtracking
    for move in moves:
        if inbounds(position, move):
            board[position[0] + move[0]][position[1] + move[1]].reachable += 1

    board[position[0]][position[1]].visited = False

    return False



#Solves click on traverse button
def button_traverse():
    for i in range(check_count):
        for k in range(check_count):
            board[i][k].visited = False
    if reachable():
        b1["state"] = "disabled"
        b2["state"] = "normal"
        for i in range(check_count):
            for k in range(check_count):
                board[i][k].text = ""
                board[i][k].visited = False
                for move in moves:
                    if inbounds((i, k), move):
                        board[i + move[0]][k + move[1]].reachable += 1
        traversing(knight, 0)
        board_paint(False)
    else:
        popupmessage("Some checks can't be reached")

#Solves click on reset button
def button_traverse_reset():
    for i in range(check_count):
        for k in range(check_count):
            board[i][k].text = ""
            board[i][k].visited = -1
            board[i][k].reachable = 0 
    board_paint(True)
    b2["state"] = "disabled"
    b1["state"] = "normal"



#Disables main window and displays a popup window with given text
def popupmessage(text):
    popup = Toplevel()
    popup.geomtery = ("192*108 + 192*108")
    popup.title("Warning")
    popup.grab_set()
    label = Label(popup, text=text)
    label.pack(side=TOP, fill="x")
    B1 = Button(popup, text="OK", command = popup.destroy)
    B1.pack()
    popup.mainloop()



root = Tk()
root.geometry("1920x1080+0+0")
root.title("CheckerboardTraversing")

#TBD pevná velikost
canvas = Canvas(root, width = check_size*check_count, height = check_size*check_count, highlightthickness = 0)
canvas.pack(side = TOP, anchor = NW)

board = create_board(check_count)

canvas.bind("<Button-1>", knight_move)
canvas.bind("<Button-3>", add_move)

b1 = Button(root, text="traverse", command=button_traverse)
b1.pack(side = TOP, anchor = NW)
b2 = Button(root, text="reset", command=button_traverse_reset)
b2.pack(side = TOP, anchor = NW)
b2["state"] = "disabled"

board[knight[0]][knight[1]].special_color = "orange"
for move in moves:
    if inbounds(knight, move):
        board[knight[0] + move[0]][knight[1] + move[1]].special_color = "red"

board_paint(True)

root.mainloop()
