
#from pynput import keyboard
from tkinter import  *
from tkinter import messagebox
import random
import copy

#tkinter display setup
root =Tk()
root.title('2048 GAME')
root.resizable(height = False, width = False)


#variables
#cancel_timer variable reset timer for restart and new game
global cancl_timer
global high_score,my_score,undo_my_score,undo_high_score
my_score = 0
#second minute and hour for timer stopwatch
sc = min = hr = 0
#number of rows and columns in game
rows, cols = (4, 4)


# define 2048 grid 4*4
grid = [[0 for i in range(rows)] for j in range(cols)]

#create a duplicate undo_grid for undo move that stores previous grid data
undo_grid = copy.deepcopy(grid)
# end_game flag for infinite loop
not_end = True

#whene game restart and new game starts reset all the grids and assign new two number initially  and reset  timer and score
def gird_create():
    global my_score,undo_my_score
    for i in range(rows):
       for j in range(cols):
           grid[i][j] = 0
    global sc ,min,hr,cancl_timer,undo_grid,my_score,undo_high_score
    root.after_cancel(cancl_timer)
    hr=0
    sc=0
    min =0
    my_score=0
    new_num_assign()
    new_num_assign()
    undo_grid = copy.deepcopy(grid)
    undo_my_score = 0
    score_card.config(text= "Your Score : %i" % my_score)
    undo_high_score = high_score


#before each move the states will be saved in  undo_grid for undo move
def undo_copy():
    global undo_grid,grid,my_score,undo_my_score,undo_high_score
    undo_grid = copy.deepcopy(grid)
    undo_my_score = my_score
    undo_high_func()

#when undo a move the grid will go to previous state according to undo_grid
def undo_game():
    global undo_high_score,my_score
    for i in range(rows):
        for j in range(cols):
            grid[i][j]=undo_grid[i][j]
    high_score_card.config(text="Highest Score : %i" % int(undo_high_score))
    with open("highest_score.txt", "w") as f:
        f.write(str(undo_high_score))
    score_card.config(text="Your Score : %i" % undo_my_score)
    my_score=undo_my_score
    tk_display()

#after each move if the grid dos not change from previous grid then no new number will assign to the grid
def grid_compare():
    global grid,undo_grid
    for i in range(rows):
        for j in range(cols):
            if undo_grid[i][j]!=grid[i][j]:
                return 1
    return 0

# check for end of game
# if all the cells are full and no 2048
def check_full_grid():
    zero_flag = False
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 0:
                zero_flag = True
            elif grid[i][j] == 2048:
                show_msg(0)

    if  zero_flag == False:
        show_msg(1)

#after end of game display win or Lost and ask for new game or exit
def show_msg(x):
    if x ==0:
        tk_display()

        gird_create()
        res = messagebox.askquestion('prompt', 'CONGO .YOU WIN...\nTry New Game')
        if res == 'yes':

            gird_create()
            clock()

        else:
            exit()

    else:
        tk_display()
        responce = messagebox.askquestion('prompt', 'LOST\nTry New Game')
        if responce == 'yes':
           gird_create()
           clock()

        else:
           exit()


#function for different colours for different grid elements
def colorpicker(i,j):
    if grid[i][j]==2  or grid[i][j]==512:
        return '#94d0cc'
    if grid[i][j]==4 or grid[i][j]==1024:
        return '#eec4c4'
    if grid[i][j]==8:
        return '#f29191'
    if grid[i][j]==16 or grid[i][j]==256:
        return '#d1d9d9'
    if grid[i][j]==32:
        return '#fb9300'
    if grid[i][j] == 64 :
        return '#0a81ab'
    if grid[i][j] == 0:
        return '#feffde'
    if grid[i][j] == 128:
        return '#511281'
    if grid[i][j] ==2048:
        return 'red'



# For storing
def store_high_score():
    global my_score,high_score

    if  high_score <my_score:
        with open("highest_score.txt", "w") as f:
            f.write(str(my_score))


#retrive high score
def get_high_score():
    with open("highest_score.txt", "r") as f:
        return f.read()
# display high score
def display_high_score():
    global high_score
    try:
         hs = int(get_high_score())
         high_score_card.config(text ="Highest Score : %i"%hs )

         high_score= hs

    except:
        high_score = 0
        high_score_card.config(text = "Highest Score : %i"%high_score )

    store_high_score()
def undo_high_func():
    global undo_high_score
    try:
         undo_high_score = int(get_high_score())
    except:
        undo_high_score = 0






#function for score
def cal_my_score(x):
    global my_score
    my_score = my_score+x
    score_card.config(text = "Your Score : %i"%my_score )


#function for displaying the grid in gui
def tk_display():
    global undo_high_score
    for i in range(4):
        for j in range(4):
            Label(root, text=grid[i][j], font="Helvatica 15", bg=colorpicker(i,j),fg = 'black',height = 3, width = 7,relief = 'solid').grid(row=i, column=j)
    display_high_score()
    #undo_high_score = get_high_score()
    store_high_score()
    display_high_score()








#define random function that produce 2 or 4 in blank cell
get_num_list = [2, 4]
def get_num():
    return random.choice(get_num_list)


# define random empty cell where random number will generate
def get_random_grid():
    return random.randrange(0, 16)


# devide the get_random_grid into row and coloum
# find blank cell and assign new number 2 or 4
def new_num_assign():

    row = get_random_grid()
    new_col = row % 4
    new_row = row // 4
    if grid[new_row][new_col] == 0:
        grid[new_row][new_col] = get_num()
    else:
        new_num_assign()

#left swip
def left_swap():
    for i in range(rows):
        temp = []
        for j in range(cols):
            if grid[i][j] != 0:
                temp.append(grid[i][j])
                grid[i][j] = 0

        for assign_num in range(len(temp)):
            grid[i][assign_num] = temp[assign_num]




# right swipe
def right_swap():

    for i in range(rows):
        temp = []
        for j in range(cols):
            if grid[i][j] != 0:
                temp.append(grid[i][j])
                grid[i][j] = 0
        for assign_num in range(len(temp)):
            grid[i][cols - len(temp) + assign_num] = temp[assign_num]




# down swipe
def down_swap():
    for j in range(rows):
        temp = []
        for i in range(cols):
            if grid[i][j] != 0:
                temp.append(grid[i][j])
                grid[i][j] = 0
        for assign_num in range(len(temp)):
            grid[rows - len(temp) + assign_num][j] = temp[assign_num]

#up swip
def up_swap():
    for j in range(rows):
        temp = []
        for i in range(cols):
            if grid[i][j] != 0:
                temp.append(grid[i][j])
                grid[i][j] = 0
        for assign_num in range(len(temp)):
            grid[assign_num][j] = temp[assign_num]


# left blending function after swip merge same number
def left_blend():
    #global swap
    for i in range(rows):
        for j in range(cols-1):
            if grid[i][j] == grid[i][j + 1] and grid[i][j] != 0:
                grid[i][j] = 2 * grid[i][j]
                grid[i][j + 1] = 0
                cal_my_score(grid[i][j])
    left_swap()


# right blending function after swip merge same number
def right_blend():
    #global swap
    for i in range(rows):
        for j in range(cols - 1, 0, -1):
            if grid[i][j] == grid[i][j - 1] and grid[i][j] != 0:
                grid[i][j] = 2 * grid[i][j]
                grid[i][j - 1] = 0
                #swap = 1
                cal_my_score(grid[i][j])
    right_swap()


# up_blend after swip merge same number
def up_blend():

    for i in range(cols):
        for j in range(rows-1):
            if grid[j][i] == grid[j + 1][i] and grid[j][i] != 0:
                grid[j][i] = 2 * grid[j][i]
                grid[j + 1][i] = 0
                cal_my_score(grid[j][i])
    up_swap()

#down blend after swip merge same number
def down_blend():

    for i in range(cols):
        for j in range(rows - 1, 0, -1):
            if grid[j][i] == grid[j - 1][i] and grid[j][i] != 0:
                grid[j][i] = 2 * grid[j][i]
                grid[j - 1][i] = 0
                cal_my_score(grid[j][i])
    down_swap()


#function for countdown or stopwatch
def clock():
    global sc , min ,hr
    sc= sc+1
    if sc==60:
        min =min+1
        sc = 0
    if min ==60:
        hr = hr+1
        min =0

    global cancl_timer
    #curr_time.config(text = hr + ":" + min + ":" + sc)
    curr_time.config(text ='%i:%i:%i'%(hr,min,sc))
    cancl_timer= curr_time.after(1000,clock)

#for restart a game or new game
def newgame():
     gird_create()
     tk_display()


     clock()

#function to display how to play this game on a new window
def helpme():
     help_notes ='''2048 is played on a plain 4×4 grid, with numbered tiles that slide when a player moves them using the four arrow keys.\n
     Every turn, a new tile randomly appears in an empty spot on the board with a value of either 2 or 4.\n
     Tiles slide as far as possible in the chosen direction until they are stopped by either another tile or the edge of the grid.\n
      If two tiles of the same number collide while moving, they will merge into a tile with the total value of the two tiles that collided.\n
     The resulting tile cannot merge with another tile again in the same move. \n
    If a move causes three consecutive tiles of the same value to slide together, only the two tiles farthest along the direction of motion will combine.\n
    If all four spaces in a row or column are filled with tiles of the same value, a move parallel to that row/column will combine the first two and last two.\n
     A scoreboard on the upper-right keeps track of the user's score.\n
     The user's score starts at zero, and is increased whenever two tiles combine, by the value of the new tile.\n
    The game is won when a tile with a value of 2048 appears on the board.\n
     When the player has no legal moves (there are no empty spaces and no adjacent tiles with the same value), the game ends.\n
     \n\n\n\n\nCreated by Arnab Das . 
     '''
     top =Toplevel()
     top.resizable(height=False, width=False)
     top.geometry('900x500')
     lbl = Label(top,text=help_notes,padx=50,pady=50).pack()





#up button function for move up
def up():
    undo_copy()
    up_swap()
    up_blend()
    if grid_compare():
        new_num_assign()
    check_full_grid()
    tk_display()

#down button function for move down
def down():
    undo_copy()
    down_swap()
    down_blend()
    if grid_compare():
        new_num_assign()
    check_full_grid()
    tk_display()

 #right button function for move right
def right():
    undo_copy()
    right_swap()
    right_blend()
    if grid_compare():
        new_num_assign()
    check_full_grid()
    tk_display()

 #left button function for move left
def left():
    undo_copy()
    left_swap()
    left_blend()
    if grid_compare():
        new_num_assign()
    check_full_grid()

    tk_display()






#up button function for move up
def k_up(event):
    undo_copy()
    up_swap()
    up_blend()
    if grid_compare():
        new_num_assign()
    check_full_grid()
    tk_display()

#down button function for move down
def k_down(event):
    undo_copy()
    down_swap()
    down_blend()
    if grid_compare():
        new_num_assign()
    check_full_grid()
    tk_display()

 #right button function for move right
def k_right(event):
    undo_copy()
    right_swap()
    right_blend()
    if grid_compare():
        new_num_assign()
    check_full_grid()
    tk_display()

 #left button function for move left
def k_left(event):
    undo_copy()
    left_swap()
    left_blend()
    if grid_compare():
        new_num_assign()
    check_full_grid()

    tk_display()

#create button for move or play the fame joystick
left_arrow =Button(root,text='LEFT',height = 4, width = 22,relief = 'groove',bg="#98ded9",command = left).grid(row=5,column=0,rowspan=2,columnspan=2)
right_arrow =Button(root,text='RIGHT',height = 4, width = 22,relief = 'groove',bg="#98ded9",command = right).grid(row=5,column=2,rowspan=2,columnspan=2)
up_arrow =Button(root,text='UP',height = 1, width = 15,relief = 'groove',bg="#c7ffd8",padx =5,pady=5,command = up).grid(row=5,column=1,columnspan=2)
down_arrow=Button(root,text='DOWN',height = 1, width = 15,relief = 'groove',bg="#c7ffd8",padx =5,pady=5,command = down).grid(row=6,column=1,columnspan=2)



#undo newgame help and timer button
new_game_button = Button(root,text='RESTART ',height = 3, width =10,padx = 3,command = newgame,bg="#94d0cc",relief = 'flat').grid(row = 8,column = 1)
undo = Button(root,text = 'UNDO ',height = 3, width =10,padx = 3,bg="#eec4c4",relief = 'flat',command = undo_game).grid(row = 8,column = 0)
help_button = Button(root,text='HELP',height = 3, width =10,padx = 3,bg="#f29191",relief = 'flat',command = helpme).grid(row = 8,column = 2)
curr_time = Label(root,text=" ",height = 3, width =10,padx = 3,bg="#feffde")
curr_time.grid(row = 8,column = 3)
high_score_card = Label(root,text="",height = 2,relief = 'flat', width =23,bg="#0a81ab",fg ="red")
high_score_card.grid(row = 7,column=0,columnspan=2)
score_card = Label(root,text="Your Score : 0",height = 2, width =23,relief = 'flat',bg="#511281",fg="white")
score_card.grid(row = 7,column=2,columnspan=2)


root.bind("<Up>", k_up)
root.bind("<Down>",k_down)
root.bind("<Left>",k_left)
root.bind("<Right>",k_right)

#main driver function program start from here
def main():
    new_num_assign()
    new_num_assign()
    undo_copy()
    clock()
    tk_display()




if __name__=='__main__':

    main()



def closing_game():
    #curr_time.after_cancel(clock)
    root.quit()

#when the close button is clicked it calls quit sys function otherwise tcl clock error occures
root.protocol("WM_DELETE_WINDOW",closing_game)
root.mainloop()