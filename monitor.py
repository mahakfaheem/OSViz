import threading
import time
import pygame
import sys

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)

class MonitorDemo:
    def __init__(self, main_app=None):  # Accept main_app as an argument
        pygame.init()

        # Store the main_app instance
        self.main_app = main_app

        # Set up Pygame window
        self.width = 800
        self.height = 500
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Monitor Demo")

        # Define room positions, dimensions, and names
        self.room_info = [
            {"name": "Room A", "position": (100, 150)},
            {"name": "Room B", "position": (300, 150)},
            {"name": "Room C", "position": (500, 150)}
        ]
        self.room_size = (100, 100)

        # Initialize monitor lock
        self.monitor_lock = threading.Lock()

        # Initialize flags to track locked rooms
        self.locked_flags = [False] * len(self.room_info)

        # Initialize flags to track executing threads
        self.executing_threads = [False] * len(self.room_info)

        # Initialize clock for controlling frame rate
        self.clock = pygame.time.Clock()

        # Initialize condition variable
        self.shared_var = 0

        # Initialize the monitor gate color
        self.monitor_gate_color = GREEN

        # Initialize current event message
        self.current_event = ""

    def create_threads(self):
        # Start a thread for each room
        for i, room in enumerate(self.room_info):
            thread = threading.Thread(target=self.thread_func, args=(i,))
            thread.daemon = True
            thread.start()

    def thread_func(self, index):
        while True:
            with self.monitor_lock:
                # Simulate activity in the room
                self.locked_flags[index] = True
                self.executing_threads[index] = True
                self.current_event = f"Thread {chr(65 + index)} is executing the critical section."

                # Keep executing until shared variable reaches 5
                while self.shared_var < 5:
                    # Increment shared variable
                    self.shared_var += 1
                    time.sleep(1)  # Simulate activity

                # Reset shared variable
                self.shared_var = 0

                # Change monitor gate color to yellow when thread A is executing
                if index == 0:
                    self.monitor_gate_color = YELLOW
                else:
                    self.monitor_gate_color = GREEN

            # Simulate signaling another thread
            self.current_event = f"Thread {chr(65 + index)} is signaling another thread."

            time.sleep(1)  # Simulate idle time

            # Reset thread state
            self.executing_threads[index] = False
            self.locked_flags[index] = False

    def draw_scene(self):
        self.screen.fill(WHITE)

        # Draw monitor gate
        monitor_gate_rect = pygame.Rect(350, 50, 100, 30)
        pygame.draw.rect(self.screen, self.monitor_gate_color, monitor_gate_rect)

        # Draw rooms
        for i, room in enumerate(self.room_info):
            x, y = room["position"]
            room_rect = pygame.Rect(x, y, *self.room_size)
            pygame.draw.rect(self.screen, BLUE, room_rect)

            # Draw thread label
            thread_label = chr(65 + i)
            label_font = pygame.font.SysFont(None, 24)
            label_render = label_font.render(thread_label, True, BLACK)
            label_position = (x + 10, y + 10)
            self.screen.blit(label_render, label_position)

            # Draw lock indicator 
            lock_color = RED if self.locked_flags[i] else GREEN
            lock_radius = 10
            lock_center = (x + self.room_size[0] - lock_radius - 5, y + 5 + lock_radius)
            pygame.draw.circle(self.screen, lock_color, lock_center, lock_radius)

            # Draw executing thread indicator (red dot)
            if self.executing_threads[i]:
                pygame.draw.circle(self.screen, RED, (x + self.room_size[0] // 2, y + self.room_size[1] // 2), 5)

        # Draw shared variable
        var_text = f"Condition Variable: {self.shared_var}"
        var_font = pygame.font.SysFont(None, 24)
        var_render = var_font.render(var_text, True, BLACK)
        self.screen.blit(var_render, (10, self.height - 30))

        # Draw current event message 
        event_message = self.current_event
        event_font = pygame.font.SysFont(None, 24)
        event_render = event_font.render(event_message, True, BLACK)
        event_position = (self.width - event_render.get_width() - 10, 10)
        self.screen.blit(event_render, event_position)

        # Explanation
        explanation_text = [
            "Thread Coordination:",
            "Threads coordinate actions by signaling each other.",
            "One thread may signal another when a resource is available(when a certain condition is met).",
            "Encapsulation:",
            "Rooms encapsulate critical sections and synchronization mechanisms."
        ]
        explanation_font = pygame.font.SysFont(None, 24)
        y_offset = 250
        for line in explanation_text:
            text_render = explanation_font.render(line, True, BLACK)
            self.screen.blit(text_render, (10, y_offset))
            y_offset += 30

        # Instructions for quitting and returning to the main page
        instruction_text = "Press 'Q' to quit, 'R' to return to main page"
        instruction_font = pygame.font.SysFont(None, 24)
        instruction_render = instruction_font.render(instruction_text, True, BLACK)
        self.screen.blit(instruction_render, (10, self.height - 60))

        pygame.display.flip()

    def run(self):
        self.create_threads()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_r:
                        if self.main_app:  # Check if main_app is not None
                            self.main_app.run()  # Call the run method of the main_app instance

            # Draw scene
            self.draw_scene()
            self.clock.tick(60)  

        # Quit pygame before exiting the program
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # Create an instance of MonitorDemo and pass the main_app instance
    demo = MonitorDemo(main_app=None)
    demo.run()
