# Modules
import pygame
import math
import matplotlib.pyplot as plt
import numpy as np
# Constants
BG_COLOR = (26, 180, 250)
FULLSCREEN = True
DEFAULT_WIDTH = 1000
DEFAULT_HEIGHT = 600
FPS = 60
# Pendulum constants
GRAVITY = 9.81

# Pendulum class
class Pendulum:
    def __init__(self, length, theta, mass, color, width, x_pos, y_pos):
        self.length = length
        self.width = width
        self.theta = theta
        self.mass = mass
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.end_x = self.x_pos + self.length * math.sin(self.theta)
        self.end_y = self.y_pos + self.length * math.cos(self.theta)

    def update_position(self, theta):
        self.theta = theta
        self.end_x = self.x_pos + self.length * math.sin(self.theta)
        self.end_y = self.y_pos + self.length * math.cos(self.theta)

    def draw(self, screen, rad):
        pygame.draw.line(screen, self.color, (self.x_pos, self.y_pos), (self.end_x, self.end_y), self.width)
        self.circ = pygame.draw.circle(screen, self.color, (self.end_x, self.end_y), rad)

class Sim:
    def __init__(self):
    
        # Init
        pygame.init()

        self.WIDTH = pygame.display.Info().current_w if FULLSCREEN == True else DEFAULT_WIDTH
        self.HEIGHT = pygame.display.Info().current_h if FULLSCREEN == True else DEFAULT_HEIGHT
        # Clock
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), vsync=1)
        self.running = True

        # Base pendulum parameters
        self.BASE_LENGTH = int(self.WIDTH * 0.1)
        self.PENDULUM_WIDTH_RATIO = 0.002
        self.BOB_RADIUS = int(self.WIDTH * 0.01)

        # Pendulum parameters
        self.FIRST_P_LENGTH = self.BASE_LENGTH
        self.SECOND_P_LENGTH = self.BASE_LENGTH
        self.FIRST_P_WIDTH = int(self.WIDTH * self.PENDULUM_WIDTH_RATIO)
        self.SECOND_P_WIDTH = int(self.WIDTH * self.PENDULUM_WIDTH_RATIO)

        # angle des 2 pendules (en degré)
        self.FIRST_P_THETA = math.pi / 2
        self.SECOND_P_THETA = 0 # math.pi/180

        self.FIRST_P_MASS = 1
        self.SECOND_P_MASS = 1
        self.FIRST_THETA_DOT = 0
        self.SECOND_THETA_DOT = 0

        self.FIRST_P_COLOR = (255, 255, 255)
        self.SECOND_P_COLOR = (255, 255, 255)

        # Epuisement
        self.DAMPING_FACTOR = 1.0001
        self.ANGLE_ACCEL = 35*math.pi/180

    # a modifier
    def compute_accelerations(self, theta1, theta2, theta1_dot, theta2_dot):
        if 270*math.pi/180 <= theta1 <= self.ANGLE_ACCEL:
            theta1ddot = theta2_ddot
        num1 = (2 * self.FIRST_P_MASS + self.SECOND_P_MASS) * math.sin(theta1) * -GRAVITY 
        num2 = -self.SECOND_P_MASS * GRAVITY * math.sin(theta1 - 2 * theta2)
        num3 = -2 * math.sin(theta1 - theta2) * self.SECOND_P_MASS
        num4 = theta2_dot ** 2 * self.SECOND_P_LENGTH + theta1_dot ** 2 * self.FIRST_P_LENGTH * math.cos(theta1 - theta2)
        den = self.FIRST_P_LENGTH * (2 * self.FIRST_P_MASS + self.SECOND_P_MASS - self.SECOND_P_MASS * math.cos(2 * theta1 - 2 * theta2))
        theta1_ddot = ((num1 + num2 + num3 * num4) / den)
        num5 = 2 * math.sin(theta1 - theta2)
        num6 = (theta1_dot ** 2 * self.FIRST_P_LENGTH * (self.FIRST_P_MASS + self.SECOND_P_MASS))
        num7 = GRAVITY * (self.FIRST_P_MASS + self.SECOND_P_MASS) * math.cos(theta1)
        num8 = theta2_dot ** 2 * self.SECOND_P_LENGTH * self.SECOND_P_MASS * math.cos(theta1 - theta2)
        den2 = self.SECOND_P_LENGTH * (2 * self.FIRST_P_MASS + self.SECOND_P_MASS - self.SECOND_P_MASS * math.cos(2 * theta1 - 2 * theta2))
        theta2_ddot = (num5 * (num6 + num7 + num8)) / den2
        # if theta1 >= self.ANGLE_ACCEL:
        #    theta2_ddot += 2

        return theta1_ddot, theta2_ddot

    # a modifier
    def rk4_step(self, damping, theta1, theta2, theta1_dot, theta2_dot, dt):
        # Initial accelerations
        a1, b1 = self.compute_accelerations(theta1, theta2, theta1_dot, theta2_dot)
        
        # Compute k1
        k1_theta1_dot = dt * a1
        k1_theta2_dot = dt * b1
        k1_theta1 = dt * theta1_dot
        k1_theta2 = dt * theta2_dot
        
        # Compute k2
        a2, b2 = self.compute_accelerations(theta1 + 0.5 * k1_theta1, theta2 + 0.5 * k1_theta2, theta1_dot + 0.5 * k1_theta1_dot, theta2_dot + 0.5 * k1_theta2_dot)
        k2_theta1_dot = dt * a2
        k2_theta2_dot = dt * b2
        k2_theta1 = dt * (theta1_dot + 0.5 * k1_theta1_dot)
        k2_theta2 = dt * (theta2_dot + 0.5 * k1_theta2_dot)

        # Compute k3
        a3, b3 = self.compute_accelerations(theta1 + 0.5 * k2_theta1, theta2 + 0.5 * k2_theta2, theta1_dot + 0.5 * k2_theta1_dot, theta2_dot + 0.5 * k2_theta2_dot)
        k3_theta1_dot = dt * a3
        k3_theta2_dot = dt * b3
        k3_theta1 = dt * (theta1_dot + 0.5 * k2_theta1_dot)
        k3_theta2 = dt * (theta2_dot + 0.5 * k2_theta2_dot)

        # Compute k4
        a4, b4 = self.compute_accelerations(theta1 + k3_theta1, theta2 + k3_theta2, theta1_dot + k3_theta1_dot, theta2_dot + k3_theta2_dot)
        k4_theta1_dot = dt * a4
        k4_theta2_dot = dt * b4
        k4_theta1 = dt * (theta1_dot + k3_theta1_dot)
        k4_theta2 = dt * (theta2_dot + k3_theta2_dot)

        # Final values
        new_theta1_dot = theta1_dot + (1/6) * (k1_theta1_dot + 2*k2_theta1_dot + 2*k3_theta1_dot + k4_theta1_dot)
        new_theta2_dot = theta2_dot + (1/6) * (k1_theta2_dot + 2*k2_theta2_dot + 2*k3_theta2_dot + k4_theta2_dot)
        new_theta1 = theta1 + (1/6) * (k1_theta1 + 2*k2_theta1 + 2*k3_theta1 + k4_theta1)
        new_theta2 = theta2 + (1/6) * (k1_theta2 + 2*k2_theta2 + 2*k3_theta2 + k4_theta2)
        
        # Damping
        new_theta1_dot *= damping
        new_theta2_dot *= damping
        
        return new_theta1, new_theta2, new_theta1_dot, new_theta2_dot

    def dist(x1, y1, x2, y2):
        return ((x2 - x1) ** 2 - (y2 -y1) ** 2)
    
    def energie_cinetique(self, l1, l2, theta1, theta2, theta1_dot, theta2_dot):

        I11 = (self.FIRST_P_MASS + self.SECOND_P_MASS) * l1**2
        I22 = self.SECOND_P_MASS * l2**2
        I12 = self.SECOND_P_MASS * l1 * l2 * np.cos(theta1 - theta2)

        return (0.5 * (I11 * theta1_dot**2 +2 * I12 * theta1_dot * theta2_dot + I22 * theta2_dot**2))
    
    def simulation(self):
        pendulum_1 = Pendulum(self.FIRST_P_LENGTH, self.FIRST_P_THETA, self.FIRST_P_MASS, self.FIRST_P_COLOR, self.FIRST_P_WIDTH, self.WIDTH /2, self.HEIGHT/2)
        pendulum_2 = Pendulum(self.SECOND_P_LENGTH, self.SECOND_P_THETA, self.SECOND_P_MASS, self.SECOND_P_COLOR, self.SECOND_P_WIDTH, pendulum_1.end_x, pendulum_1.end_y)
        VARTHETA = [] #récupère toutes les valeurs de theta1 sur une période de 3-4 tours
        KINETIK = []
        POSITION_LIMIT = int(FPS * 2)
        TRAIL_SIZE = int(self.WIDTH * 0.005)
        ENABLE_TRAIL = True

        while self.running:
            for event in pygame.event.get():
                mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    self.running = False

            dt = 0.28
            self.FIRST_P_THETA, self.SECOND_P_THETA, self.FIRST_THETA_DOT, self.SECOND_THETA_DOT = self.rk4_step(self.DAMPING_FACTOR, self.FIRST_P_THETA, self.SECOND_P_THETA, self.FIRST_THETA_DOT, self.SECOND_THETA_DOT, dt)
            pendulum_1.update_position(self.FIRST_P_THETA)
            pendulum_2.x_pos, pendulum_2.y_pos = pendulum_1.end_x, pendulum_1.end_y
            pendulum_2.update_position(self.SECOND_P_THETA)
            self.screen.fill(BG_COLOR)
            pendulum_1.draw(self.screen, self.BOB_RADIUS)
            pendulum_2.draw(self.screen, self.BOB_RADIUS)
            VARTHETA.append(pendulum_1.theta)
            KINETIK.append(self.energie_cinetique(self.FIRST_P_LENGTH, self.SECOND_P_LENGTH, pendulum_1.theta, pendulum_2.theta, self.FIRST_THETA_DOT, self.SECOND_THETA_DOT))
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

        # recup tt pr plot
        plt.figure(1)           
        plt.xlabel('theta')
        plt.ylabel("vitesse angulaire")
        plt.title(f"Vitesse angulaire en fonction de l'angle avec une accélération pour à theta = {self.ANGLE_ACCEL}°")
        plt.plot(VARTHETA, KINETIK, 'r-')              #on trace la vitesse angulaire en fonction de la position
        plt.show()



if (__name__ == '__main__'):
    sim = Sim()
    sim.simulation()