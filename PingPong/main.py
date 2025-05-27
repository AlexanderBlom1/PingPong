import tkinter as tk
import random

# Game settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 20
PADDLE_SPEED = 20
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

class PingPong:
    def __init__(self, master):
        self.master = master
        master.title("Ping Pong Game")

        self.canvas = tk.Canvas(master, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
        self.canvas.pack()

        # Scores
        self.left_score = 0
        self.right_score = 0
        self.score_text = self.canvas.create_text(WINDOW_WIDTH//2, 30, fill="white", font=("Arial", 24),
                                                  text="0 : 0")

        # Paddles and ball
        self.left_paddle = self.canvas.create_rectangle(20, 150, 20 + PADDLE_WIDTH, 150 + PADDLE_HEIGHT, fill="white")
        self.right_paddle = self.canvas.create_rectangle(WINDOW_WIDTH - 30, 150,
                                                         WINDOW_WIDTH - 30 + PADDLE_WIDTH,
                                                         150 + PADDLE_HEIGHT, fill="white")
        self.ball = self.canvas.create_oval(WINDOW_WIDTH//2 - BALL_SIZE//2, WINDOW_HEIGHT//2 - BALL_SIZE//2,
                                            WINDOW_WIDTH//2 + BALL_SIZE//2, WINDOW_HEIGHT//2 + BALL_SIZE//2,
                                            fill="white")

        self.ball_dx = random.choice([BALL_SPEED_X, -BALL_SPEED_X])
        self.ball_dy = random.choice([BALL_SPEED_Y, -BALL_SPEED_Y])

        # Bind keys
        self.master.bind("<w>", self.move_left_paddle_up)
        self.master.bind("<s>", self.move_left_paddle_down)
        self.master.bind("<Up>", self.move_right_paddle_up)
        self.master.bind("<Down>", self.move_right_paddle_down)

        self.update()

    def move_left_paddle_up(self, event):
        self.move_paddle(self.left_paddle, -PADDLE_SPEED)

    def move_left_paddle_down(self, event):
        self.move_paddle(self.left_paddle, PADDLE_SPEED)

    def move_right_paddle_up(self, event):
        self.move_paddle(self.right_paddle, -PADDLE_SPEED)

    def move_right_paddle_down(self, event):
        self.move_paddle(self.right_paddle, PADDLE_SPEED)

    def move_paddle(self, paddle, dy):
        x1, y1, x2, y2 = self.canvas.coords(paddle)
        if y1 + dy >= 0 and y2 + dy <= WINDOW_HEIGHT:
            self.canvas.move(paddle, 0, dy)

    def update(self):
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        self.check_collision()
        self.master.after(30, self.update)

    def check_collision(self):
        ball_coords = self.canvas.coords(self.ball)
        left_coords = self.canvas.coords(self.left_paddle)
        right_coords = self.canvas.coords(self.right_paddle)

        # Top and bottom wall bounce
        if ball_coords[1] <= 0 or ball_coords[3] >= WINDOW_HEIGHT:
            self.ball_dy = -self.ball_dy

        # Left paddle collision
        if (ball_coords[0] <= left_coords[2] and
            left_coords[1] < ball_coords[3] and
            left_coords[3] > ball_coords[1]):
            self.ball_dx = abs(self.ball_dx)

        # Right paddle collision
        if (ball_coords[2] >= right_coords[0] and
            right_coords[1] < ball_coords[3] and
            right_coords[3] > ball_coords[1]):
            self.ball_dx = -abs(self.ball_dx)

        # Scoring
        if ball_coords[0] <= 0:
            self.right_score += 1
            self.reset_ball()
        elif ball_coords[2] >= WINDOW_WIDTH:
            self.left_score += 1
            self.reset_ball()

        self.canvas.itemconfig(self.score_text, text=f"{self.left_score} : {self.right_score}")

    def reset_ball(self):
        self.canvas.coords(self.ball,
                           WINDOW_WIDTH//2 - BALL_SIZE//2,
                           WINDOW_HEIGHT//2 - BALL_SIZE//2,
                           WINDOW_WIDTH//2 + BALL_SIZE//2,
                           WINDOW_HEIGHT//2 + BALL_SIZE//2)
        self.ball_dx = random.choice([BALL_SPEED_X, -BALL_SPEED_X])
        self.ball_dy = random.choice([BALL_SPEED_Y, -BALL_SPEED_Y])

if __name__ == "__main__":
    root = tk.Tk()
    game = PingPong(root)
    root.mainloop()
