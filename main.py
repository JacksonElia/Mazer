# Maze Maker and Solver by Jackson Elia
import ctypes
import math
import random
import sys
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QBrush, QFont, QIcon, QPainter, QPen, QIntValidator
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QMainWindow, QPushButton
# Gets time, threading, and copy library from maze_funcs
from maze_funcs import *
# Gets pre-made mazes
import stored_mazes


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Maze Values
        self.maze_width = 16
        self.maze_height = 16
        self.editing = False
        self.solving = False
        # Switch is for turning tiles to walls and vice versa, start is to place the start exit for exit
        self.edit_mode = "switch"
        # Used to make sure the window doesn't update after it finds the path
        self.solved_maze_list = []
        self.static_solved_maze_list = []
        self.solved = 0

        # Window Values
        user32 = ctypes.windll.user32
        self.screen_width = user32.GetSystemMetrics(0)
        self.screen_height = user32.GetSystemMetrics(1)
        self.big_font = QFont("Helvetica", 15)
        self.big_font.setBold(True)
        self.small_font = QFont("Helvetica", 10)
        self.small_font.setBold(True)
        self.setWindowIcon(QIcon("mazer_icon.jpg"))

        # Window Widgets
        self.solve_button = QPushButton("Solve Maze", self)
        self.edit_button = QPushButton("Edit Maze", self)
        self.pick_maze_button = QPushButton("Pick Maze", self)
        self.start_button = QPushButton("Place Start", self)
        self.start_button.setStyleSheet("QPushButton {color: limeGreen};")
        self.end_button = QPushButton("Place End", self)
        self.end_button.setStyleSheet("QPushButton {color: green};")
        self.text_box_width = QLineEdit(self)
        self.text_box_height = QLineEdit(self)
        self.text_label = QLabel("", self)

        # Makes list of Maze tiles
        self.maze_list = make_maze(self.maze_width, self.maze_height)

        self.init_window()

    def init_window(self):
        """
        Makes and Sets Window Properties and Widgets
        """
        self.setWindowTitle("Mazer")
        self.solve_button.clicked.connect(self.start_thread)
        self.solve_button.setFont(self.big_font)
        self.edit_button.clicked.connect(self.edit_button_pressed)
        self.edit_button.setFont(self.big_font)
        self.pick_maze_button.clicked.connect(self.pick_maze_button_pressed)
        self.pick_maze_button.setFont(self.big_font)
        self.start_button.clicked.connect(self.start_button_pressed)
        self.start_button.setFont(self.small_font)
        self.start_button.hide()
        self.end_button.clicked.connect(self.end_button_pressed)
        self.end_button.setFont(self.small_font)
        self.end_button.hide()
        self.text_box_width.setPlaceholderText("Enter Maze Width")
        self.text_box_width.setValidator(QIntValidator())
        self.text_box_width.textEdited.connect(self.text_box_edited)
        self.text_box_height.setPlaceholderText("Enter Maze Height")
        self.text_box_height.setValidator(QIntValidator())
        self.text_box_height.textEdited.connect(self.text_box_edited)
        self.text_label.setFont(self.small_font)
        self.text_label.setWordWrap(True)
        self.text_label.setText("Press a button!")
        self.init_geometry()

        # Shows the window
        self.show()

    def init_geometry(self):
        """
        Sets up the whole gui
        """
        window_width = self.maze_width * 50 if self.maze_width * 50 >= 900 else 900
        window_height = self.maze_height * 50 + 100
        # Automatically puts the window in the middle of the screen
        self.setGeometry(int(self.screen_width / 2 - window_width / 2),
                         int(self.screen_height / 2 - window_height / 2),
                         window_width,
                         window_height)
        self.solve_button.setGeometry(20, window_height - 80, 160, 60)
        self.edit_button.setGeometry(195, window_height - 80, 160, 60)
        self.pick_maze_button.setGeometry(370, window_height - 80, 160, 60)
        self.start_button.setGeometry(20, window_height - 80, 160, 28)
        self.end_button.setGeometry(20, window_height - 49, 160, 28)
        self.text_box_width.setGeometry(545, window_height - 80, 160, 28)
        self.text_box_height.setGeometry(545, window_height - 49, 160, 28)
        self.text_label.setGeometry(720, window_height - 77, 160, 60)

    def paintEvent(self, event):
        """
        Method is called when self.update() is called. It is used to change the pixel color of the window to illustrate
        a maze
        """
        # Changes the list that the window will paint based on if the maze has been solved
        if self.solved == 1:
            # Will paint the maze the first time it has been solved
            maze_painting_list = self.solved_maze_list
            self.static_solved_maze_list = copy.deepcopy(self.solved_maze_list)
        elif self.solved >= 2:
            # Will paint the maze after it has been solved
            maze_painting_list = self.static_solved_maze_list
        else:
            # Will paint normally
            maze_painting_list = self.maze_list

        painter = QPainter(self)
        # Iterates through the maze list each tile at a time
        for row in maze_painting_list:
            for tile in row:
                match tile["tile_type"]:
                    case "wall":
                        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
                        painter.setPen(QPen(Qt.black, 1))
                    case "blank":
                        painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))
                        painter.setPen(QPen(Qt.black, 1))
                    case "path":
                        painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
                        painter.setPen(QPen(Qt.black, 1))
                    case "solving":
                        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
                        painter.setPen(QPen(Qt.red, 1))
                    case "start":
                        painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
                        painter.setPen(QPen(Qt.black, 1))
                    case "end":
                        painter.setBrush(QBrush(Qt.darkGreen, Qt.SolidPattern))
                        painter.setPen(QPen(Qt.black, 1))
                    case _:
                        print("Try checking to make sure each tile has a valid type")
                rectangle = QRect(tile["x_coord"], tile["y_coord"], 50, 50)
                painter.drawRect(rectangle)

    def mousePressEvent(self, event):
        """
        This method is called whenever the user clicks on the window. It is used to edit the maze.
        :return:
        """
        if self.editing:
            mouse_x = event.x()
            mouse_y = event.y()
            tile_x = int((mouse_x - (mouse_x % 50)) / 50)
            tile_y = int((mouse_y - (mouse_y % 50)) / 50)
            # Checks to make sure the user clicked in the maze
            if tile_x > self.maze_width - 1 or tile_y > self.maze_height - 1:
                self.text_label.setText("Click the maze!")
            else:
                # Calls the function to edit the maze where the user clicked
                edit_maze(maze_list=self.maze_list, x_coord=tile_x, y_coord=tile_y, edit_mode=self.edit_mode)
                self.edit_mode = "switch"
                self.update()

    def start_thread(self):
        """
        Creates a thread so that the maze can be updated as it is being solved
        """
        t1 = Thread(target=self.solve_button_pressed_thread)
        t1.start()

    def solve_button_pressed_thread(self):
        """
        Clears the maze and then solves it
        """
        print(self.maze_list)
        self.edit_button.setDisabled(True)
        self.solved = 0
        self.solving = True
        clear_maze(maze_list=self.maze_list)
        solve_maze(maze_list=self.maze_list, window=self)
        self.update()
        # Accounts for weird, uncommon glitch where the maze doesn't load
        sleep(.01)
        self.update()

    def edit_button_pressed(self):
        """
        Clears the maze and then opens the edit options.
        :return:
        """
        self.solved = 0
        self.editing = not self.editing
        # Changes the GUI based on if the user is editing or not
        if self.editing:
            self.edit_button.setText("Editing...")
            self.solve_button.hide()
            self.start_button.show()
            self.end_button.show()
            self.edit_mode = "switch"
        else:
            self.edit_button.setText("Edit Maze")
            self.solve_button.show()
            self.start_button.hide()
            self.end_button.hide()
        self.text_label.setText("Press a button!")
        clear_maze(maze_list=self.maze_list)
        self.update()
        
    def pick_maze_button_pressed(self):
        """
        Loads a maze from stored_mazes.py
        """
        self.solved = 0
        # Makes sure the same maze isn't picked twice
        random_maze_num = random.randrange(len(stored_mazes.stored_mazes))
        while True:
            if random_maze_num == stored_mazes.picked_maze:
                random_maze_num = random.randrange(len(stored_mazes.stored_mazes))
            else:
                self.maze_list = copy.deepcopy(stored_mazes.stored_mazes[random_maze_num])
                stored_mazes.picked_maze = random_maze_num
                break
        self.maze_width = len(self.maze_list[0])
        self.maze_height = len(self.maze_list)
        self.init_geometry()
        self.update()

    def start_button_pressed(self):
        """
        Makes it so the next time the user clicks a border, it will become the start of the maze
        """
        self.edit_mode = "start"
        self.text_label.setText("Click the maze to place the start.")

    def end_button_pressed(self):
        """
        Makes it so the next time the user clicks a border, it will become the end of the maze
        """
        self.edit_mode = "end"
        self.text_label.setText("Click the maze to place the end.")

    def text_box_edited(self):
        """
        Is called when a text box is changed, sets the size of the maze and does formatting for the window to match it
        """
        # Makes sure dumbasses like Brenton can't break the program by trying to have negative rows
        self.text_box_width.setText(self.text_box_width.text().replace('-', ''))
        self.text_box_height.setText(self.text_box_height.text().replace('-', ''))
        if self.text_box_width.text() == "":
            self.maze_width = 16
        elif int(self.text_box_width.text()) * 50 > self.screen_width:
            self.maze_width = math.floor(self.screen_width / 50)
        else:
            self.maze_width = int(self.text_box_width.text())
        if self.text_box_height.text() == "":
            self.maze_height = 16
        elif int(self.text_box_height.text()) * 50 > self.screen_height:
            self.maze_height = math.floor((self.screen_height - 150) / 50)
        else:
            self.maze_height = int(self.text_box_height.text())
        self.init_geometry()
        self.maze_list = make_maze(self.maze_width, self.maze_height)
        self.update()


# PyQt5 window setup
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
