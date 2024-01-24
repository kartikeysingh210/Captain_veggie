import random
from Captain import Captain
from Rabbit import Rabbit
from Veggie import Veggie
import pickle
import csv

class GameEngine:
    NUMBER_OF_VEGGIES = 30
    NUMBER_OF_RABBITS = 5
    HIGH_SCORE_FILE = "highscore.data"

    def __init__(self):
        self._field = None
        self._rabbits = []
        self._captain = None
        self._possible_veggies = []
        self._score = 0

    def _get_random_empty_location(self):
        while True:
            row = random.randint(0, len(self._field) - 1)
            col = random.randint(0, len(self._field[0]) - 1)
            if self._field[row][col] is None:
                return row, col

    def _file_exists(self, file_name):
        try:
            with open(file_name, 'rb'):
                pass
            return True
        except FileNotFoundError:
            return False

    def init_veggies(self):
        veggie_file = input("Enter the name of the veggie CSV file: ")

        while not self._file_exists(veggie_file):
            veggie_file = input("File not found. Enter a valid veggie CSV file: ")

        with open(veggie_file, 'r') as file:
            csv_reader = csv.reader(file)

            # Find the line with numeric size information
            size_line = next((line for line in csv_reader if line[0].lower() == 'field size'), None)

            if size_line is None or len(size_line) != 3:
                print("Error: Invalid format for size information in the CSV file.")
                # Handle the error appropriately (e.g., ask the user to check the file)
                return

            num_rows, num_cols = int(size_line[1]), int(size_line[2])

            self._field = [[None for _ in range(num_cols)] for _ in range(num_rows)]

            # Skip the size line and read veggie data
            next(csv_reader)

            for veggie_data in csv_reader:
                veggie_name, veggie_symbol, veggie_points = veggie_data[0], veggie_data[1], int(veggie_data[2])
                self._possible_veggies.append(Veggie(veggie_name, veggie_symbol, veggie_points))

            for _ in range(self.NUMBER_OF_VEGGIES):
                row, col = self._get_random_empty_location()
                veggie = random.choice(self._possible_veggies)
                self._field[row][col] = veggie

    def init_captain(self):
        row, col = self._get_random_empty_location()
        self._captain = Captain(row, col)

    def init_rabbits(self):
        for _ in range(self.NUMBER_OF_RABBITS):
            row, col = self._get_random_empty_location()
            self._rabbits.append(Rabbit(row, col))
            self._field[row][col] = self._rabbits[-1]

    def initialize_game(self):
        self.init_veggies()
        self.init_captain()
        self.init_rabbits()

    def remaining_veggies(self):
        count = 0
        for row in self._field:
            for cell in row:
                if isinstance(cell, Veggie):
                    count += 1
        return count

    def intro(self):
        print("Welcome to Captain Veggie Game!")
        print("The rabbits have invaded Captain Veggie's field.")
        print("Your goal is to harvest as many vegetables as possible before they are consumed by the leporine menace.")
        print("Captain Veggie can move around the field and attempt to harvest vegetables by moving on top of them.")
        print("Rabbits will also randomly hop about, consuming any vegetables they land on.")
        print("The game continues until all the vegetables have been removed from the field.")
        print("\nList of possible vegetables:")
        for veggie in self._possible_veggies:
            print(veggie)
        print(f"\nCaptain Veggie's symbol: {self._captain.get_symbol()}")
        print(f"Rabbit's symbol: {self._rabbits[0].get_symbol()}")

    def print_field(self):
        print("##" + "#" * (len(self._field[0]) * 2 - 1) + "##")
        for row in self._field:
            print("#", end=" ")
            for cell in row:
                if cell is None:
                    print(" ", end=" ")
                else:
                    print(cell.get_symbol(), end=" ")
            print("#")
        print("##" + "#" * (len(self._field[0]) * 2 - 1) + "##")

    def get_score(self):
        return self._score

    def move_rabbits(self):
        for rabbit in self._rabbits:
            self._move_creature(rabbit)

    def move_cpt_vertical(self, movement):
        row, col = self._captain.get_x(), self._captain.get_y()
        new_row = row + movement

        if 0 <= new_row < len(self._field) and self._field[new_row][col] is None:
            self._move_captain_common(new_row, col)
        elif 0 <= new_row < len(self._field) and isinstance(self._field[new_row][col], Veggie):
            veggie = self._field[new_row][col]
            print(f"Delicious vegetable found: {veggie.get_name()}! Score +{veggie.get_points()}")
            self._captain.add_veggie(veggie)
            self._score += veggie.get_points()
            self._move_captain_common(new_row, col)
        elif 0 <= new_row < len(self._field) and isinstance(self._field[new_row][col], Rabbit):
            print("Oops! You stepped on a rabbit. Be careful!")
        else:
            print("Invalid move. Captain cannot move there.")

    def move_cpt_horizontal(self, movement):
        row, col = self._captain.get_x(), self._captain.get_y()
        new_col = col + movement

        if 0 <= new_col < len(self._field[0]) and self._field[row][new_col] is None:
            self._move_captain_common(row, new_col)
        elif 0 <= new_col < len(self._field[0]) and isinstance(self._field[row][new_col], Veggie):
            veggie = self._field[row][new_col]
            print(f"Delicious vegetable found: {veggie.get_name()}! Score +{veggie.get_points()}")
            self._captain.add_veggie(veggie)
            self._score += veggie.get_points()
            self._move_captain_common(row, new_col)
        elif 0 <= new_col < len(self._field[0]) and isinstance(self._field[row][new_col], Rabbit):
            print("Oops! You stepped on a rabbit. Be careful!")
        else:
            print("Invalid move. Captain cannot move there.")

    def _move_captain_common(self, new_row, new_col):
        row, col = self._captain.get_x(), self._captain.get_y()
        self._captain.set_x(new_row)
        self._captain.set_y(new_col)
        self._field[new_row][new_col] = self._captain
        self._field[row][col] = None

    def move_captain(self):
        direction = input("Enter the direction to move Captain (W/A/S/D): ").lower()

        if direction == 'w':
            self.move_cpt_vertical(-1)
        elif direction == 's':
            self.move_cpt_vertical(1)
        elif direction == 'a':
            self.move_cpt_horizontal(-1)
        elif direction == 'd':
            self.move_cpt_horizontal(1)
        else:
            print("Invalid input. Please enter W, A, S, or D.")
    def _move_creature(self, creature):
        current_row, current_col = creature.get_x(), creature.get_y()
        new_row, new_col = self._get_random_empty_location()

        self._field[current_row][current_col] = None
        self._field[new_row][new_col] = creature
        creature.set_x(new_row)
        creature.set_y(new_col)
    
    def game_over(self):
        print("Game Over!")
        print("Vegetables harvested by Captain Veggie:")
        for veggie in self._captain.get_veggies_collected():
            print(veggie.get_name())
        print(f"Player's score: {self._score}")
    
    def high_score(self):
        high_scores = []

        try:
            with open(self.HIGH_SCORE_FILE, 'rb') as file:
                high_scores = pickle.load(file)
        except FileNotFoundError:
            pass  # File does not exist yet, ignore and continue

        initials = input("Enter your initials (max 3 characters): ")[:3]

        player_score = (initials, self._score)

        if not high_scores:
            high_scores.append(player_score)
        else:
            index_to_insert = 0
            for i, (_, score) in enumerate(high_scores):
                if player_score[1] > score:
                    index_to_insert = i + 1
                    break
            high_scores.insert(index_to_insert, player_score)

        print("\nHigh Scores:")
        for i, (initials, score) in enumerate(high_scores, start=1):
            print(f"{i}. {initials}: {score}")

        with open(self.HIGH_SCORE_FILE, 'wb') as file:
            pickle.dump(high_scores, file)

# Example usage:
# game_engine = GameEngine()
# game_engine.initialize_game()
# game_engine.intro()
# game_engine.print_field()
# game_engine.move_captain()
# game_engine.game_over()
# game_engine.high_score()
