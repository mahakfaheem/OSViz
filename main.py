import pygame
import mutex
import binary_semaphore
import sys

class VisualizationApp:
    def __init__(self):
        pygame.init()
        self.screen_width = 400
        self.screen_height = 200
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Concurrency Visualization App")

        self.mutex_button = pygame.Rect(50, 50, 150, 50)
        self.semaphore_button = pygame.Rect(200, 50, 150, 50)
        self.exit_button = pygame.Rect(275, 150, 100, 30)  # Define exit button rectangle

    def run_mutex_demo(self):
        mutex_demo = mutex.MutexDemo(self)
        mutex_demo.run()

    def run_semaphore_demo(self):
        semaphore_demo = binary_semaphore.SemaphoreDemo(self)
        semaphore_demo.run()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.mutex_button.collidepoint(event.pos):
                        self.run_mutex_demo()
                    elif self.semaphore_button.collidepoint(event.pos):
                        self.run_semaphore_demo()
                    elif self.exit_button.collidepoint(event.pos):  # Check if exit button is clicked
                        running = False

            self.screen.fill((255, 255, 255))
            pygame.draw.rect(self.screen, (0, 0, 255), self.mutex_button)
            pygame.draw.rect(self.screen, (0, 255, 0), self.semaphore_button)
            pygame.draw.rect(self.screen, (255, 0, 0), self.exit_button)  # Draw exit button in red

            font = pygame.font.SysFont(None, 21)
            text_mutex = font.render('Mutex', True, (250, 250, 250))
            text_semaphore = font.render('Binary Semaphore', True, (250, 250, 250))
            text_exit = font.render('Exit', True, (250, 250, 250))  # Render text for exit button
            self.screen.blit(text_mutex, (95, 65))
            self.screen.blit(text_semaphore, (215, 65))
            self.screen.blit(text_exit, (313, 155))  # Position exit button text

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = VisualizationApp()
    app.run()
