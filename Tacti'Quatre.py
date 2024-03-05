from tkinter import *

class Game:
    def __init__(self, n=10, p=5):
        self.__size = n
        self.__pawn = p
        self.__board = self.newBoard()
        self.__player = 1
        self.__row = 0
        self.__col = 0
        self.__turn = 0
        self.__pion1 = Pawn(0, 0, 1)
        self.__pion2 = Pawn(0, 0, 2)
        
        self.__root = Tk()
        self.__root.title("TactiQuatre")
        
        self.__frame1 = Frame(self.__root)
        self.__frame1.config(height=self.__size * 60 + 1, width=self.__size * 60 + 1)
        self.__frame1.grid(row=0, column=0, rowspan=2)

        self.__frame2 = Frame(self.__root)
        self.__frame2.config(height=50, width=self.__size * 50 + 1)
        self.__frame2.grid(row=2, column=0)
        
        self.__frame3 = Frame(self.__root)
        self.__frame3.grid(row=1, column=1)
        
        self.__sizeScale = Scale(self.__frame3, from_=8, to=12, orient=HORIZONTAL, label="Taille du plateau", length=100)
        self.__sizeScale.set(self.__size)
        self.__sizeScale.grid(row=0, column=0)
        
        self.__nbPawn = Scale(self.__frame3, from_=4, to=6, orient=HORIZONTAL, label="Pions à aligner", length=100)
        self.__nbPawn.set(self.__pawn)
        self.__nbPawn.grid(row=3, column=0)
        
        self.__buttonValid1 = Button(self.__frame3, text='Valider', command=self.restart, width=10)
        self.__buttonValid1.grid(row=2, column=0, pady=20)
        
        self.__buttonValid2 = Button(self.__frame3, text='Valider', command=self.restart, width=10)
        self.__buttonValid2.grid(row=4, column=0, pady=20)
        
        self.__canvas = Canvas(self.__frame1)
        self.__canvas.config(width=self.__size * 60 + 1, height=self.__size * 60 + 1, highlightthickness=0, bd=0)
        self.__canvas.place(x=0, y=0)
        self.__canvas.bind('<Button-1>', self.click)
        
        self.__textPlayer = StringVar()
        self.__textPlayer.set(f"Tour du joueur {self.__player}")
        self.__text1 = Label(self.__frame2, textvariable=self.__textPlayer, fg='black', font=("Courier", 20))
        self.__text1.pack()
        
        self.display()
        self.__root.mainloop()
    
    def newBoard(self):
        return [[0] * self.__size for i in range(self.__size)]
        
    def display(self):
        self.__canvas.delete("all")
        self.displayPlayable()
        for i in range(self.__size):
            for j in range(self.__size):
                symbol = self.symbol(self.__board[i][j])
                self.__canvas.create_rectangle(j * 50, i * 50, (j+1) * 50, (i+1) * 50, fill='white', outline='black')
                # Pions
                if self.__board[i][j] == 1:
                    self.__canvas.create_oval(j * 50 + 5, i * 50 + 5, (j+1) * 50 - 5, (i+1) * 50 - 5, fill='navy')
                elif self.__board[i][j] == 2:
                    self.__canvas.create_oval(j * 50 + 5, i * 50 + 5, (j+1) * 50 - 5, (i+1) * 50 - 5, fill='gold')
                # Croix
                elif self.__board[i][j] == 3:
                    self.__canvas.create_line(j * 50 + 5, i * 50 + 5, (j+1) * 50 - 5, (i+1) * 50 - 5, fill='navy', width=3)
                    self.__canvas.create_line((j+1) * 50 - 5, i * 50 + 5, j * 50 + 5, (i+1) * 50 - 5, fill='navy', width=3)
                elif self.__board[i][j] == 4:
                    self.__canvas.create_line(j * 50 + 5, i * 50 + 5, (j+1) * 50 - 5, (i+1) * 50 - 5, fill='gold', width=3)
                    self.__canvas.create_line((j+1) * 50 - 5, i * 50 + 5, j * 50 + 5, (i+1) * 50 - 5, fill='gold', width=3)
        self.__textPlayer.set(f"Tour du joueur {self.__player}")

    def symbol(self, value):
        if value == 0:
            return '.'
        elif value == 1:
            return 'O'
        elif value == 2:
            return 'o'
        elif value == 3:
            return 'X'
        elif value == 4:
            return 'x'

    def put(self, i, j):
        if self.__board[i][j] == 0 and self.__turn < 2:
            self.__board[i][j] = self.__player
            self.__player = 3 - self.__player
            self.__turn += 1
            return True
        else:
            return False

    def possible(self, i, j):
        return 0 <= i < self.__size and 0 <= j < self.__size and self.__board[i][j] == 0 and \
               (0 <= i-2 < self.__size and 0 <= j-1 < self.__size and self.__board[i-2][j-1] == self.__player or
                0 <= i-1 < self.__size and 0 <= j-2 < self.__size and self.__board[i-1][j-2] == self.__player or
                0 <= i+1 < self.__size and 0 <= j-2 < self.__size and self.__board[i+1][j-2] == self.__player or
                0 <= i+2 < self.__size and 0 <= j-1 < self.__size and self.__board[i+2][j-1] == self.__player or
                0 <= i+2 < self.__size and 0 <= j+1 < self.__size and self.__board[i+2][j+1] == self.__player or
                0 <= i+1 < self.__size and 0 <= j+2 < self.__size and self.__board[i+1][j+2] == self.__player or
                0 <= i-1 < self.__size and 0 <= j+2 < self.__size and self.__board[i-1][j+2] == self.__player or
                0 <= i-2 < self.__size and 0 <= j+1 < self.__size and self.__board[i-2][j+1] == self.__player)

    def displayPlayable(self):
        for i in range(self.__size):
            for j in range(self.__size):
                if self.possible(i, j):
                    if self.__player == 1:
                        self.__canvas.create_oval(j * 50 + 20, i * 50 + 20, (j + 1) * 50 - 20, (i + 1) * 50 - 20, fill='navy')
                    else:
                        self.__canvas.create_oval(j * 50 + 20, i * 50 + 20, (j + 1) * 50 - 20, (i + 1) * 50 - 20, fill='gold')

    def move(self, i, j):
        if self.possible(i, j) :
            if self.__player == 1:
                row = self.__pion1.getRow()
                col = self.__pion1.getCol()
                self.__board[col][row] = 3
                self.__board[i][j] = 1
                self.__pion1.setCoordinates(i, j)
                self.__pion1.setState(1)
            else:
                row = self.__pion2.getRow()
                col = self.__pion2.getCol()
                self.__board[col][row] = 4
                self.__board[i][j] = 2
                self.__pion2.setCoordinates(i, j)
                self.__pion2.setState(2)
            self.__player = 3 - self.__player
            self.__turn += 1
            return True
        else:
            return False

    def again(self):
        for i in range(self.__size):
            for j in range(self.__size):
                if self.possible(i, j):
                    return True
        return False
    
    def checkWinner(self, player, row, col):
        # ligne
        count = 0
        for j in range(self.__size):
            if row + j < self.__size and self.__board[row + j][col] == player + 2:
                count += 1
                if count == self.__pawn:
                    return True   
        # colonne
        count = 0
        for i in range(self.__size):
            if col + i < self.__size and self.__board[row][col + i] == player + 2:
                count += 1
                if count == self.__pawn:
                    return True
        # diagonale /
        count = 0
        for i in range(-self.__pawn + 1, self.__pawn):
            if 0 <= row + i < self.__size and 0 <= col + i < self.__size and self.__board[row + i][col + i] == player + 2:
                count += 1
                if count == self.__pawn:
                    return True
        # diagonale \
        count = 0
        for i in range(-self.__pawn + 1, self.__pawn):
            if 0 <= row - i < self.__size and 0 <= col + i < self.__size and self.__board[row - i][col + i] == player + 2:
                count += 1
                if count == self.__pawn:
                    return True
        return False
                        
    def endGame(self):
        self.__canvas.delete("playable")
        answer = messagebox.askyesno("TactiQuatre", "Rejouer ?")
        if answer:
            self.restart()
        else:
            self.__root.destroy()
            
    def click(self, event):
        i = event.y // 50
        j = event.x // 50
        if self.__turn < 2:
            self.put(i, j)
            self.display()
            self.displayPlayable()
            if self.__turn == 1:
                self.__pion1.setCoordinates(i, j)
            else:
                self.__pion2.setCoordinates(i, j)
        else:
            self.move(i, j)
            self.display()
            self.displayPlayable()
            check = False
            for i in range(self.__size):
                for j in range(self.__size):
                    if self.checkWinner(self.__player, i, j):
                        check = True
            if check:
                messagebox.showinfo("TactiQuatre", f"Le joueur {self.__player} a gagné")
                self.endGame()
            if not self.again():
                messagebox.showinfo("TactiQuatre", f"Le joueur {3-self.__player} a gagné")
                self.endGame()
            
    def restart(self):
        self.__size = self.__sizeScale.get()
        self.__pawn = self.__nbPawn.get()
        self.__board = self.newBoard()
        self.__player = 1
        self.__row = 0
        self.__col = 0
        self.__turn = 0
        self.__pion1 = Pawn(0, 0, 1)
        self.__pion2 = Pawn(0, 0, 2)
        self.displayPlayable()
        self.display()
    
class Pawn:
    def __init__(self, i, j, state=0):
        self.__pawnState = state
        self.__row = j
        self.__col = i
        
    def getRow(self):
        return self.__row
    
    def getCol(self):
        return self.__col
    
    def getCoordinates(self, i, j):
        self.__row = j
        self.__col = i

    def setCoordinates(self, i, j):
        self.__row = j
        self.__col = i
        
    def getState(self):
        return self.__pawnState
        
    def setState(self, state):
        self.__pawnState = state

start = Game()
start.newBoard()