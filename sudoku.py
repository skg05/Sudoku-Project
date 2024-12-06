import pygame
from sudoku_generator import *
from board import Board


class GameUI:
    """Handles rendering and interaction for game screens."""

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.button_font = pygame.font.Font(None, 30)

    def draw_start_screen(self):
        """Draws the game start screen with difficulty buttons."""
        self.screen.fill("white")
        title = self.font.render("Welcome to Sudoku!", True, "black")
        self.screen.blit(title, (150, 50))

        difficulties = ["Easy", "Medium", "Hard"]
        for idx, difficulty in enumerate(difficulties):
            btn = pygame.Rect(200, 150 + idx * 100, 200, 50)
            pygame.draw.rect(self.screen, "blue", btn)
            text = self.font.render(difficulty, True, "white")
            self.screen.blit(text, (btn.x + 50, btn.y + 10))

        pygame.display.update()
        return difficulties

    def draw_end_screen(self, message):
        """Displays the end screen with a message."""
        self.screen.fill("white")
        text = self.font.render(message, True, "black")
        self.screen.blit(text, (150, 250))
        pygame.display.update()
        pygame.time.wait(3000)

    def draw_ui_buttons(self):
        """Draws the buttons below the board."""
        buttons = {"Reset": (50, 620), "Restart": (250, 620), "Exit": (450, 620)}
        for text, (x, y) in buttons.items():
            btn = pygame.Rect(x, y, 120, 40)
            pygame.draw.rect(self.screen, "gray", btn)
            label = self.button_font.render(text, True, "white")
            self.screen.blit(label, (x + 20, y + 10))

        pygame.display.update()
        return buttons


def main():
    pygame.init()
    screen = pygame.display.set_mode((603, 700))  # Extra space for buttons
    pygame.display.set_caption("Sudoku Game")
    clock = pygame.time.Clock()

    ui = GameUI(screen)
    running = True
    difficulty = None

    # Game start screen
    while running:
        difficulties = ui.draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                for idx, level in enumerate(difficulties):
                    btn = pygame.Rect(200, 150 + idx * 100, 200, 50)
                    if btn.collidepoint(event.pos):
                        difficulty = level.lower()
                        running = False

    # Start game
    board = Board(603, 603, screen, difficulty)
    screen.fill("white")  # Clear start screen before showing the board
    play_game(board, screen, ui, difficulty)


def play_game(board, screen, ui, difficulty):
    """Main gameplay loop."""
    running = True
    sketch = False
    ui.draw_ui_buttons()

    board.draw()
    board.fill_board()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y > 603:  # Check if clicking buttons below the board
                    if 50 <= x <= 170 and 620 <= y <= 660:  # Reset button
                        board.reset_to_original()
                        board.draw()
                        ui.draw_ui_buttons()
                    elif 250 <= x <= 370 and 620 <= y <= 660:  # Restart button
                        main()  # Restart the game
                    elif 450 <= x <= 570 and 620 <= y <= 660:  # Exit button
                        pygame.quit()
                        return
                elif board.original_board[y // 67][x // 67] == 0:
                    board.select(x // 67, y // 67)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    sketch = True
                if pygame.K_1 <= event.key <= pygame.K_9:
                    num = event.key - pygame.K_0
                    if sketch:
                        board.sketch(num)
                        sketch = False
                    else:
                        board.place_number(num)

        if board.is_full():
            if board.check_board():
                ui.draw_end_screen("You Win!")
            else:
                ui.draw_end_screen("Game Over!")
            return

        pygame.display.update()


if __name__ == "__main__":
    main()

