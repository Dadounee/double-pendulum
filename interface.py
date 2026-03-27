from tkinter import *
from tkinter import ttk

# definition de la taille de l'ecran (a modifier si differant)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
"""
FIRST_P_LENGTH = BASE_LENGTH
SECOND_P_LENGTH = BASE_LENGTH
FIRST_P_WIDTH = int(WIDTH * PENDULUM_WIDTH_RATIO)
SECOND_P_WIDTH = int(WIDTH * PENDULUM_WIDTH_RATIO)


FIRST_P_THETA = 0 # math.pi/90
SECOND_P_THETA = 0 # math.pi/180

FIRST_P_MASS = 1
SECOND_P_MASS = 1
FIRST_THETA_DOT = 0
SECOND_THETA_DOT = 0

FIRST_P_COLOR = (255, 255, 255)
SECOND_P_COLOR = (255, 255, 255)

DAMPING_FACTOR = 0.5
"""
class Data:

    def __init__(self, loss_factor: float = 1.0):

        self.simulation_state = 0

        # simulation vars
        self.loss_factor = loss_factor
        self.first_pend_th = 0.0
        self.second_pend_th = 0.0

        # tkinter vars
        self.__window = Tk()
        self.simulation_start = Button(
                font=('Arial', SCREEN_HEIGHT // 135),
                text="start simulation",
                activebackground="#808080",
                command=self.start_sim
                )
        self.entries = {
            "loss factor": Entry(
                font=('Arial', SCREEN_HEIGHT // 135),
                width=3
                ),
            "theta 1": Entry(
                font=('Arial', SCREEN_HEIGHT // 135),
                width=15
            ),
            "theta 2": Entry(
                font=('Arial', SCREEN_HEIGHT // 135),
                width=15
            )
        }
        self.labels = {
            "loss factor": Label(
                font=('Arial', SCREEN_HEIGHT // 135),
                text="Energy loss"
                ),
            "1": Label(
                font=('Arial', SCREEN_HEIGHT // 135),
                text="First Pendulum"
            ),
            "2": Label(
                font=('Arial', SCREEN_HEIGHT // 135),
                text="Second Pendulum"
            ),
            "theta": Label(
                font=('Arial', SCREEN_HEIGHT // 135),
                text="Pendulum theta (rad)"
            )
        }

    def start_sim(self):
        
        self.simulation_state = 1
        packed_data = {
            "energy loss": self.loss_factor,
            "thetha 1": self.first_pend_th,
            "thetha 2": self.second_pend_th
        }
        return packed_data
    
    # sortie de focus
    def loss_factor_focusout(self, event):

        new_value = self.entries["loss factor"].get()
        if (new_value == ""):
            self.entries["loss factor"].insert(0, f"{self.loss_factor}")
            return
        try:
            self.loss_factor = float(new_value)
        except ValueError:
            # en cas d'erreur on remet l'ancienne valeur
            self.entries["loss factor"].delete(0, len(new_value))
            self.entries["loss factor"].insert(0, f"{self.loss_factor}")

    def first_theta_focusout(self, event):

        new_value = self.entries["theta 1"].get()
        if (new_value == ""):
            self.entries["theta 1"].insert(0, f"{self.first_pend_th}")
            return
        try:
            self.first_pend_th = float(new_value)
        except ValueError:
            # en cas d'erreur on remet l'ancienne valeur
            self.entries["theta 1"].delete(0, len(new_value))
            self.entries["theta 1"].insert(0, f"{self.first_pend_th}")

    def second_theta_focusout(self, event):

        new_value = self.entries["theta 2"].get()
        if (new_value == ""):
            self.entries["theta 2"].insert(0, f"{self.second_pend_th}")
            return
        try:
            self.second_pend_th = float(new_value)
        except ValueError:
            # en cas d'erreur on remet l'ancienne valeur
            self.entries["theta 2"].delete(0, len(new_value))
            self.entries["theta 2"].insert(0, f"{self.second_pend_th}")
        
    # fonctions membre
    def insert_base_values(self) -> None:

        self.entries["loss factor"].insert(0, f"{self.loss_factor}")
        self.entries["loss factor"].bind("<FocusOut>", self.loss_factor_focusout)

        self.entries["theta 1"].insert(0, f"{self.first_pend_th}")
        self.entries["theta 1"].bind("<FocusOut>", self.first_theta_focusout)

        self.entries["theta 2"].insert(0, f"{self.second_pend_th}")
        self.entries["theta 2"].bind("<FocusOut>", self.second_theta_focusout)

###############################################################################################################################################################################################
###############################################################################################################################################################################################

    def value_interface(self) -> None:

        # definition de la taille de la fenetre et de son titre
        self.__window.geometry(f"{SCREEN_WIDTH // 3}x{SCREEN_HEIGHT // 3}")
        self.__window.title("Value list")

        
        self.insert_base_values()

        self.labels["theta"].place(x=SCREEN_WIDTH // 48, y=SCREEN_HEIGHT // 27)
        self.labels["loss factor"].place(x=25, y=0)
        self.entries["loss factor"].place(x=0, y=0)


        self.labels["1"].place(x=2 * SCREEN_WIDTH // 24, y=SCREEN_HEIGHT // 54)
        self.entries["theta 1"].place(x= 2 * SCREEN_WIDTH // 24, y=SCREEN_HEIGHT // 27)
        self.labels["2"].place(x=5 * SCREEN_WIDTH // 24, y=SCREEN_HEIGHT // 54)
        self.entries["theta 2"].place(x=5 * SCREEN_WIDTH // 24, y=SCREEN_HEIGHT // 27)

        self.simulation_start.place(x=SCREEN_WIDTH // 3.7, y=SCREEN_HEIGHT // 3.5)
        # boucle principale (interne a tkinter)
        self.__window.mainloop()

if __name__ == "__main__":
    simulation_data = Data()

    simulation_data.value_interface()
