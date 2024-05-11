import pygame
import threading
import time
import sys
import mutex
import binary_semaphore  
from counter_semaphore import CounterSemaphoreDemo
from monitor import MonitorDemo

class VisualizationApp:
    def __init__(self):
        pygame.init()
        self.screen_width = 400
        self.screen_height = 200
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Concurrency Visualization App")

        self.mutex_button = pygame.Rect(50, 50, 150, 50)
        self.semaphore_button = pygame.Rect(200, 50, 150, 50)
        self.counter_semaphore_button = pygame.Rect(50, 110, 300, 50)
        self.monitor_button = pygame.Rect(50, 170, 300, 50)  # Add button for monitor demo
        self.exit_button = pygame.Rect(275, 230, 100, 30)

    def run_mutex_demo(self):
        mutex_demo = mutex.MutexDemo(self)
        mutex_demo.run()

    def run_semaphore_demo(self):
        semaphore_demo = binary_semaphore.SemaphoreDemo(self)
        semaphore_demo.run()

    def run_counter_semaphore_demo(self):
        counter_semaphore_demo = CounterSemaphoreDemo(self)
        counter_semaphore_demo.run()

    def run_monitor_demo(self): 
        monitor_demo = MonitorDemo(self)
        monitor_demo.run()

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
                    elif self.counter_semaphore_button.collidepoint(event.pos):
                        self.run_counter_semaphore_demo()
                    elif self.monitor_button.collidepoint(event.pos):  # Check if monitor button is clicked
                        self.run_monitor_demo()
                    elif self.exit_button.collidepoint(event.pos):
                        running = False

            self.screen.fill((255, 255, 255))
            pygame.draw.rect(self.screen, (0, 0, 255), self.mutex_button)
            pygame.draw.rect(self.screen, (0, 255, 0), self.semaphore_button)
            pygame.draw.rect(self.screen, (255, 165, 0), self.counter_semaphore_button)
            pygame.draw.rect(self.screen, (66, 77, 88), self.monitor_button)  
            pygame.draw.rect(self.screen, (255, 0, 0), self.exit_button)

            font = pygame.font.SysFont(None, 21)
            text_mutex = font.render('Mutex', True, (250, 250, 250))
            text_semaphore = font.render('Binary Semaphore', True, (250, 250, 250))
            text_counter_semaphore = font.render('Counter Semaphore', True, (250, 250, 250))
            text_monitor = font.render('Monitor', True, (250, 250, 250))  # Render text for monitor button
            text_exit = font.render('Exit', True, (250, 250, 250))
            self.screen.blit(text_mutex, (95, 65))
            self.screen.blit(text_semaphore, (215, 65))
            self.screen.blit(text_counter_semaphore, (85, 125))
            self.screen.blit(text_monitor, (120, 185))  # Position monitor button text
            self.screen.blit(text_exit, (313, 235))

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = VisualizationApp()
    app.run()
