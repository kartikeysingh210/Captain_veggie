from GameEngine import GameEngine

def main():
    game_engine = GameEngine()
    game_engine.initialize_game()
    game_engine.intro()

    remaining_veggies = game_engine.remaining_veggies()

    while remaining_veggies > 0:
        print(f"Remaining Veggies: {remaining_veggies}")
        print(f"Score: {game_engine.get_score()}")
        game_engine.print_field()
        game_engine.move_rabbits()
        game_engine.move_captain()  # Fixed: Call the move_captain method
        remaining_veggies = game_engine.remaining_veggies()  # Update remaining_veggies

    game_engine.game_over()
    game_engine.high_score()

if __name__ == "__main__":
    main()
