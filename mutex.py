import threading
import time
import pygame
import sys

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class MutexDemo:
    def __init__(self, main_app):
        pygame.init()

        self.main_app = main_app

        self.width = 800
        self.height = 500
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Mutex Demo")

        self.character_positions = [(100, 150), (300, 150), (500, 150)]
        self.character_names = ['A', 'B', 'C']  
        self.character_speed = 5

        self.mutex = threading.Lock()  # Gate
        self.locked_flags = [False] * len(self.character_positions)

        self.current_event = ""  # For storing the current event message

        self.font = pygame.font.SysFont(None, 30)
        self.small_font = pygame.font.SysFont(None, 24) 

        self.clock = pygame.time.Clock()

        self.create_threads()

    def create_threads(self):
        for i, (x, y) in enumerate(self.character_positions):
            thread = threading.Thread(target=self.thread_func, args=(i,))
            thread.daemon = True  # Set threads as daemons to allow proper termination
            thread.start()

    def thread_func(self, index):
        while True:
            with self.mutex:
                # Lock the character
                self.locked_flags[index] = True

                # Update the current event message
                self.current_event = f"Locked by {self.character_names[index]}"
                time.sleep(0.5)

                # Move the character
                self.character_positions[index] = (self.character_positions[index][0] + self.character_speed, self.character_positions[index][1])
                time.sleep(0.5)

                # Unlock the character
                self.locked_flags[index] = False

                # Update the current event message
                self.current_event = f"Released by {self.character_names[index]}"
                time.sleep(0.5)

            time.sleep(1)

    def draw_scene(self):
        self.screen.fill(WHITE)

        # Determine the color of the mutex gate based on whether it's locked
        mutex_color = GRAY if any(self.locked_flags) else GREEN

        # Draw mutex gate
        pygame.draw.rect(self.screen, mutex_color, (350, 10, 100, 50))
        self.draw_text("Mutex Gate", 380, 70)

        # Draw characters (threads) and their names
        for i, (x, y) in enumerate(self.character_positions):
            # Draw character
            pygame.draw.rect(self.screen, BLUE, (x, y, 50, 50))

            # Draw character name
            self.draw_text(self.character_names[i], x + 20, y + 20)

            # Draw lock/unlock indicator
            if self.locked_flags[i]:
                pygame.draw.rect(self.screen, RED, (x + 20, y - 30, 10, 10))  # Draw red square when locked

        # Draw the current event message
        self.draw_text(self.current_event, 10, 10)

        # Instructions for quitting and returning to main page
        self.draw_text("Press 'Q' to quit, 'R' to return to main page", 10, 470)

        # Explanation text
        explanation = [
            "Blue boxes represent threads, each running independently.",
            "Green gate represents the mutex (Mutual Exclusion) concept.",
            "Mutex ensures that only one thread can access shared resources at a time,",
            "preventing conflicts and ensuring data integrity."
        ]

        y_offset = 250
        for line in explanation:
            self.draw_text(line, 10, y_offset, color=BLACK, font=self.small_font)
            y_offset += 20

        pygame.display.flip()

    def draw_text(self, text, x, y, color=BLACK, font=None):
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_r:
                        self.main_app.run()

            # Draw scene
            self.draw_scene()
            self.clock.tick(60)

        # Quit pygame before exiting the program
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    demo = MutexDemo()
    demo.run()
