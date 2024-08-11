import argparse  
import random  

# Constants  
RED_MARBLE_POINTS = 2  
BLUE_MARBLE_POINTS = 3  

# Define the game class  
class NimGame:  
    def __init__(self, num_red, num_blue, version, first_player, depth):  
        self.red_marbles = num_red  
        self.blue_marbles = num_blue  
        self.version = version  
        self.first_player = first_player  
        self.depth = depth  
        self.current_player = first_player  

    # Function to get the current player  
    def get_current_player(self):  
        return self.current_player  

    # Function to switch the player  
    def switch_player(self):  
        self.current_player = 'human' if self.current_player == 'computer' else 'computer'  

    # Function to get the available moves  
    def get_available_moves(self):  
        moves = []  
        for pile, num_marbles in [('R', self.red_marbles), ('B', self.blue_marbles)]:  
            for i in range(1, num_marbles + 1):  
                moves.append((pile, i))  
        return moves  

    # Function to make a move  
    def make_move(self, pile, num_marbles):  
        if pile == 'R':  
            self.red_marbles -= num_marbles  
        elif pile == 'B':  
            self.blue_marbles -= num_marbles  
        self.switch_player()  

    # Function to check if the game is over  
    def is_game_over(self):  
        return self.red_marbles == 0 and self.blue_marbles == 0  

    # Function to calculate the score  
    def calculate_score(self):  
        return self.red_marbles * RED_MARBLE_POINTS + self.blue_marbles * BLUE_MARBLE_POINTS  

    # Function to get the game status  
    def get_game_status(self):  
        if self.is_game_over():  
            if self.version == 'standard':  
                return 'You lose!' if self.current_player == 'human' else 'Computer loses!'  
            else:  
                return 'You win!' if self.current_player == 'human' else 'Computer wins!'  
        else:  
            return 'Game in progress'  

    # Function to display the game state  
    def display_game_state(self):  
        print(f"Red marbles: {self.red_marbles}")  
        print(f"Blue marbles: {self.blue_marbles}")  

    # Function to get the heuristic evaluation of the current state  
    def evaluate(self):  
        # Simple evaluation function based on the difference in score  
        return self.calculate_score() if self.version == 'standard' else -self.calculate_score()  

    # Function to implement the MinMax algorithm with Alpha Beta Pruning  
    def minmax(self, depth, alpha, beta, maximizing_player):  
        if depth == 0 or self.is_game_over():  
            return self.evaluate(), None  

        if maximizing_player:  
            best_value = float('-inf')  
            best_move = None  
            for move in self.get_available_moves():  
                self.make_move(*move)  
                value, _ = self.minmax(depth - 1, alpha, beta, False)  
                self.make_move(move[0], -move[1])  # Undo the move  
                if value > best_value:  
                    best_value = value  
                    best_move = move  
                alpha = max(alpha, best_value)  
                if beta <= alpha:  
                    break  
            return best_value, best_move  
        else:  
            best_value = float('inf')  
            best_move = None  
            for move in self.get_available_moves():  
                self.make_move(*move)  
                value, _ = self.minmax(depth - 1, alpha, beta, True)  
                self.make_move(move[0], -move[1])  # Undo the move  
                if value < best_value:  
                    best_value = value  
                    best_move = move  
                beta = min(beta, best_value)  
                if beta <= alpha:  
                    break  
            return best_value, best_move  

    # Function to get the computer's move  
    def get_computer_move(self):  
        if self.current_player == 'computer':  
            _, best_move = self.minmax(self.depth, float('-inf'), float('inf'), True)  
            return best_move  
        else:  
            return None  

# Function to handle human player input  
def get_human_move(game):  
    while True:  
        move = input(f"Enter your move (e.g., R2 for removing 2 red marbles, B1 for removing 1 blue marble): ").upper()  
        if len(move) == 2 and move[0] in ['R', 'B'] and move[1].isdigit():  
            pile = move[0]  
            num_marbles = int(move[1])  
            if (pile == 'R' and 1 <= num_marbles <= game.red_marbles) or (pile == 'B' and 1 <= num_marbles <= game.blue_marbles):  
                return (pile, num_marbles)  
            else:  
                print("Invalid move. Please try again.")  
        else:  
            print("Invalid move format. Please try again.")  

# Main function  
def main():  
    parser = argparse.ArgumentParser(description="Play the Red-Blue Nim Game")  
    parser.add_argument("red_marbles", type=int, help="Number of red marbles")  
    parser.add_argument("blue_marbles", type=int, help="Number of blue marbles")  
    parser.add_argument("version", choices=['standard', 'misere'], help="Game version (standard or misere)")  
    parser.add_argument("first_player", choices=['human', 'computer'], help="First player (human or computer)")  
    parser.add_argument("depth", type=int, help="Search depth for the AI (for computer player)")  
    args = parser.parse_args()  

    game = NimGame(args.red_marbles, args.blue_marbles, args.version, args.first_player, args.depth)  

    print(f"Red marbles: {game.red_marbles}")  
    print(f"Blue marbles: {game.blue_marbles}")  

    while True:  
        if game.get_current_player() == 'human':  
            move = get_human_move(game)  
        else:  
            move = game.get_computer_move()  
            if move is not None:  
                print(f"Computer removes {move[1]} {move[0]} marbles.")  

        if move is not None:  
            game.make_move(*move)  
            game.display_game_state()  
            game_status = game.get_game_status()  
            if game_status != 'Game in progress':  
                print(game_status)  
                break  
        else:  
            print("Invalid move. Game over. Computer wins!")  
            break  

if __name__ == "__main__":  
    main()
