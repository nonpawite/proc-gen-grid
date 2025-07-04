import random
import sys
from typing import Tuple

from PyQt6.QtGui import QColor, QPen, QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, \
    QVBoxLayout


class DungeonWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Constants
        self.GRID_SIZE = 20
        self.CELL_SIZE = 30
        self.NUM_ROOMS = 5
        self.MIN_ROOM_SIZE = 3
        self.MAX_ROOM_SIZE = 6

        # Initialize grid
        self.grid = [[0 for _ in range(self.GRID_SIZE)] for _ in
                     range(self.GRID_SIZE)]
        self.rooms = []

        # Set fixed size for the widget
        self.setFixedSize(self.GRID_SIZE * self.CELL_SIZE,
                          self.GRID_SIZE * self.CELL_SIZE)

        # Generate initial dungeon
        self.generate_dungeon()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw grid
        for y in range(self.GRID_SIZE):
            for x in range(self.GRID_SIZE):
                if self.grid[y][x] == 1:
                    painter.fillRect(
                        x * self.CELL_SIZE,
                        y * self.CELL_SIZE,
                        self.CELL_SIZE,
                        self.CELL_SIZE,
                        QColor(100, 100, 100)
                        # Gray color for rooms and corridors
                    )
                # Draw cell borders
                painter.setPen(QPen(QColor(0, 0, 0), 1))
                painter.drawRect(
                    x * self.CELL_SIZE,
                    y * self.CELL_SIZE,
                    self.CELL_SIZE,
                    self.CELL_SIZE
                )

    def generate_room(self) -> Tuple[int, int, int, int]:
        """Generate a random room with random position and size"""
        width = random.randint(self.MIN_ROOM_SIZE, self.MAX_ROOM_SIZE)
        height = random.randint(self.MIN_ROOM_SIZE, self.MAX_ROOM_SIZE)
        x = random.randint(1, self.GRID_SIZE - width - 1)
        y = random.randint(1, self.GRID_SIZE - height - 1)
        return (x, y, width, height)

    def is_room_valid(self, room: Tuple[int, int, int, int]) -> bool:
        """Check if a room overlaps with existing rooms"""
        x, y, w, h = room
        # Add padding of 1 cell around room
        for i in range(y - 1, y + h + 1):
            for j in range(x - 1, x + w + 1):
                if i < 0 or i >= self.GRID_SIZE or j < 0 or j >= self.GRID_SIZE:
                    return False
                if self.grid[i][j] == 1:
                    return False
        return True

    def place_room(self, room: Tuple[int, int, int, int]):
        """Place a room in the grid"""
        x, y, w, h = room
        for i in range(y, y + h):
            for j in range(x, x + w):
                self.grid[i][j] = 1

    def generate_corridor(self, room1: Tuple[int, int, int, int],
                          room2: Tuple[int, int, int, int]):
        """Generate a corridor between two rooms"""
        # Get center points of rooms
        x1 = room1[0] + room1[2] // 2
        y1 = room1[1] + room1[3] // 2
        x2 = room2[0] + room2[2] // 2
        y2 = room2[1] + room2[3] // 2

        # Create L-shaped corridor
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.grid[y1][x] = 1
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.grid[y][x2] = 1

    def generate_dungeon(self):
        """Generate a new dungeon"""
        # Clear grid
        self.grid = [[0 for _ in range(self.GRID_SIZE)] for _ in
                     range(self.GRID_SIZE)]
        self.rooms = []

        # Generate rooms
        attempts = 0
        while len(self.rooms) < self.NUM_ROOMS and attempts < 100:
            room = self.generate_room()
            if self.is_room_valid(room):
                self.place_room(room)
                self.rooms.append(room)
            attempts += 1

        # Generate corridors
        for i in range(len(self.rooms) - 1):
            self.generate_corridor(self.rooms[i], self.rooms[i + 1])

        self.draw_dungeon()

    def draw_dungeon(self):
        """Request a repaint of the widget"""
        self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Procedural Dungeon Generator")

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create dungeon widget
        self.dungeon_widget = DungeonWidget()
        layout.addWidget(self.dungeon_widget)

        # Create generate button
        generate_button = QPushButton("Generate New Dungeon")
        generate_button.clicked.connect(self.regenerate_dungeon)
        layout.addWidget(generate_button)

        # Set window size
        self.adjustSize()

    def regenerate_dungeon(self):
        self.dungeon_widget.generate_dungeon()
        self.dungeon_widget.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
