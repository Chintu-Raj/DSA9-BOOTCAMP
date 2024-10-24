import random
import time
from queue import PriorityQueue
from dataclasses import dataclass
from enum import Enum
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, 
                            QPushButton, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QSlider)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QPen

class CellType(Enum):
    EMPTY = 0
    OBSTACLE = 1
    START = 2
    END = 3
    PATH = 4
    EXPLORED = 5

@dataclass
class Cell:
    type: CellType
    f_score: float = float('inf')
    g_score: float = float('inf')
    came_from: tuple = None

class PathfindingMode(Enum):
    ASTAR = "A* Algorithm"
    DIJKSTRA = "Dijkstra's Algorithm"

class GridCell(QPushButton):
    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col
        self.setFixedSize(30, 30)
        self.setCellType(CellType.EMPTY)

    def setCellType(self, cell_type: CellType):
        self.cell_type = cell_type
        color_map = {
            CellType.EMPTY: "#FFFFFF",
            CellType.OBSTACLE: "#000000",
            CellType.START: "#00FF00",
            CellType.END: "#FF0000",
            CellType.PATH: "#0000FF",
            CellType.EXPLORED: "#FFFF00"
        }
        self.setStyleSheet(f"background-color: {color_map[cell_type]};")

class PathfindingVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('A* Pathfinding Visualizer')
        self.setGeometry(100, 100, 800, 600)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Control panel
        control_panel = QHBoxLayout()

        # Algorithm selection
        self.algo_combo = QComboBox()
        for algo in PathfindingMode:
            self.algo_combo.addItem(algo.value)
        control_panel.addWidget(self.algo_combo)

        # Reset button
        reset_btn = QPushButton("Reset Grid")
        reset_btn.clicked.connect(self.resetGrid)
        control_panel.addWidget(reset_btn)

        # Random obstacles button
        random_btn = QPushButton("Random Obstacles")
        random_btn.clicked.connect(self.generateRandomObstacles)
        control_panel.addWidget(random_btn)

        # Animation speed slider
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(50)
        control_panel.addWidget(QLabel("Animation Speed:"))
        control_panel.addWidget(self.speed_slider)

        layout.addLayout(control_panel)

        # Grid
        self.grid_size = 20
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(1)
        self.grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell = GridCell(i, j)
                cell.clicked.connect(lambda checked, row=i, col=j: self.cellClicked(row, col))
                self.grid_layout.addWidget(cell, i, j)
                self.grid[i][j] = cell

        layout.addLayout(self.grid_layout)

        # Metrics display
        self.metrics_label = QLabel()
        layout.addWidget(self.metrics_label)

        # Initialize pathfinding variables
        self.start_pos = None
        self.end_pos = None
        self.is_setting_start = True
        self.is_running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.animationStep)

    def cellClicked(self, row, col):
        if self.is_running:
            return

        cell = self.grid[row][col]

        if self.is_setting_start:
            if self.start_pos:
                self.grid[self.start_pos[0]][self.start_pos[1]].setCellType(CellType.EMPTY)
            self.start_pos = (row, col)
            cell.setCellType(CellType.START)
            self.is_setting_start = False
        else:
            if self.end_pos:
                self.grid[self.end_pos[0]][self.end_pos[1]].setCellType(CellType.EMPTY)
            self.end_pos = (row, col)
            cell.setCellType(CellType.END)
            self.is_setting_start = True

            # Start pathfinding if we have both points
            if self.start_pos and self.end_pos:
                self.startPathfinding()

    def resetGrid(self):
        self.is_running = False
        self.timer.stop()
        self.start_pos = None
        self.end_pos = None
        self.is_setting_start = True

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.grid[i][j].setCellType(CellType.EMPTY)

        self.metrics_label.setText("")

    def generateRandomObstacles(self):
        if self.is_running:
            return

        density = 0.3  # 30% obstacles
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if (i, j) != self.start_pos and (i, j) != self.end_pos:
                    if random.random() < density:
                        self.grid[i][j].setCellType(CellType.OBSTACLE)
                    else:
                        self.grid[i][j].setCellType(CellType.EMPTY)

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def get_neighbors(self, pos):
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # 4-directional movement
            new_x, new_y = pos[0] + dx, pos[1] + dy
            if (0 <= new_x < self.grid_size and 
                0 <= new_y < self.grid_size and 
                self.grid[new_x][new_y].cell_type != CellType.OBSTACLE):
                neighbors.append((new_x, new_y))
        return neighbors

    def startPathfinding(self):
        self.is_running = True
        self.path_found = False
        self.explored_cells = []
        self.final_path = []

        # Initialize algorithm data
        self.cells = [[Cell(CellType.EMPTY) for _ in range(self.grid_size)] 
                     for _ in range(self.grid_size)]

        start_cell = self.cells[self.start_pos[0]][self.start_pos[1]]
        start_cell.g_score = 0
        start_cell.f_score = self.manhattan_distance(self.start_pos, self.end_pos)

        self.open_set = PriorityQueue()
        self.open_set.put((start_cell.f_score, self.start_pos))

        # Start animation
        self.animation_step = 0
        self.timer.start(max(1, int(100 / self.speed_slider.value())))

    def animationStep(self):
        if self.open_set.empty() or self.path_found:
            self.timer.stop()
            self.is_running = False
            return

        current_f, current_pos = self.open_set.get()

        if current_pos == self.end_pos:
            self.path_found = True
            self.reconstructPath(current_pos)
            self.showMetrics()
            return

        if current_pos != self.start_pos:
            self.grid[current_pos[0]][current_pos[1]].setCellType(CellType.EXPLORED)

        for neighbor_pos in self.get_neighbors(current_pos):
            tentative_g = self.cells[current_pos[0]][current_pos[1]].g_score + 1

            if tentative_g < self.cells[neighbor_pos[0]][neighbor_pos[1]].g_score:
                self.cells[neighbor_pos[0]][neighbor_pos[1]].came_from = current_pos
                self.cells[neighbor_pos[0]][neighbor_pos[1]].g_score = tentative_g
                f_score = tentative_g + self.manhattan_distance(neighbor_pos, self.end_pos)
                self.cells[neighbor_pos[0]][neighbor_pos[1]].f_score = f_score
                self.open_set.put((f_score, neighbor_pos))

    def reconstructPath(self, current):
        path = []
        while self.cells[current[0]][current[1]].came_from is not None:
            path.append(current)
            current = self.cells[current[0]][current[1]].came_from

        path.append(self.start_pos)
        path.reverse()

        for pos in path:
            if pos != self.start_pos and pos != self.end_pos:
                self.grid[pos[0]][pos[1]].setCellType(CellType.PATH)

    def showMetrics(self):
        explored_count = sum(1 for i in range(self.grid_size) 
                            for j in range(self.grid_size) 
                            if self.grid[i][j].cell_type == CellType.EXPLORED)
        path_count = sum(1 for i in range(self.grid_size) 
                        for j in range(self.grid_size) 
                        if self.grid[i][j].cell_type == CellType.PATH)

        metrics_text = (f"Path Length: {path_count} cells\n"
                        f"Explored Nodes: {explored_count} cells")
        self.metrics_label.setText(metrics_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PathfindingVisualizer()
    window.show()
    sys.exit(app.exec())