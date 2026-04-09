from tkinter import *
from tkinter import ttk
from simulation import *

# definition de la taille de l'ecran (a modifier si different)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
"""
FIRST_P_LENGTH = BASE_LENGTH
SECOND_P_LENGTH = BASE_LENGTH
FIRST_P_WIDTH = int(WIDTH * PENDULUM_WIDTH_RATIO)
SECOND_P_WIDTH = int(WIDTH * PENDULUM_WIDTH_RATIO)

Vitesse_angulaire = []
FIRST_P_THETA = 0 # math.pi/180
SECOND_P_THETA = 0 # math.pi/180


FIRST_P_MASS = 1
SECOND_P_MASS = 1
FIRST_THETA_DOT = 0
SECOND_THETA_DOT = 0

FIRST_P_COLOR = (255, 255, 255)
SECOND_P_COLOR = (255, 255, 255)

 = 2
"""
class Data:

    def __init__(self, amortissement: float = 1.0):

        self.simulation_state = 0

        # simulation vars
        self.amortissement = amortissement
        self.max_angle = 35
        self.gravity = 9.81

        # données des pendules
        self.first_pend_th = 90
        self.first_pend_mass = 1
        self.second_pend_th = 0
        self.second_pend_mass = 1

        # tkinter vars
        self.__window = Tk()
        self.simulation_start = Button(
            font=('Arial', SCREEN_HEIGHT // 135),
            text="start simulation",
            activebackground="#808080",
            command=self.start_sim
        )
        self.graph_plot = BooleanVar()
        self.modified_gravity = BooleanVar()

        # ###############################################
        # ##        Tkinter entrées utilisateur        ##
        # ###############################################

        self.entries = {
            "amortissement": Entry(
                font=('Arial', SCREEN_HEIGHT // 135),
                width=3
                ),
            "max_angle": Entry(
                font=('Arial', SCREEN_HEIGHT // 135),
                width=3
                ),
            "gravity": Entry(
                font=('Arial', SCREEN_HEIGHT // 135),
                width=5
                ),
            "theta 1": Entry(
                font=('Arial', SCREEN_HEIGHT // 135),
                width=15
            ),
            "mass 1": Entry(
                font=('Arial', SCREEN_HEIGHT // 135),
                width=15
            ),
            "theta 2": Entry(
                font=('Arial', SCREEN_HEIGHT // 135),
                width=15
            ),
            "mass 2": Entry(
                font=('Arial', SCREEN_HEIGHT // 135),
                width=15
            ),
        }

        # ###############################################
        # ##        Tkinter zones de texte             ##
        # ###############################################

        self.labels = {
            "titre": Label(
                font=('Times New Roman', SCREEN_HEIGHT // 27),
                text="Double pendule"
                ),
            "amortissement": Label(
                font=('Arial', SCREEN_HEIGHT // 135),
                text="Amortissement"
                ),
            "max_angle": Label(
                font=('Arial', SCREEN_HEIGHT // 135),
                text="Difference max d'angle (deg)"
                ),
            "gravity": Label(
                font=('Arial', SCREEN_HEIGHT // 135),
                text="Gravité"
                ),
            "1": Label(
                font=('Arial', SCREEN_HEIGHT // 135),
                text="First Pendulum"
            ),
            "2": Label(
                font=('Arial', SCREEN_HEIGHT // 135),
                text="Second Pendulum (deg)"
            ),
            "theta": Label(
                font=('Arial', SCREEN_HEIGHT // 135),
                text="Pendulum theta (deg)"
            ),
            "masse": Label(
                font=('Arial', SCREEN_HEIGHT // 135),
                text="masse des pendules"
            )
        }

        # ###############################################
        # ##             Tkinter checkbox              ##
        # ###############################################

        self.checkboxes = {
            "graph": Checkbutton(
                font=('Arial', SCREEN_HEIGHT // 135),
                text="Afficher le graphe",
                variable=self.graph_plot
            ),
            "gravity": Checkbutton(
                font=('Arial', SCREEN_HEIGHT // 135),
                text="Utiliser une gravité personnalisée",
                variable=self.modified_gravity,
                command=self.personnalised_gravity
            )
        }

# #################################################################################################
# ####                                                                                         ####
# ####                             Lancement de la simulation                                  ####
# ####                                                                                         ####
# #################################################################################################

    def focusout_trigger(self):

        # on trigger tous les focusout pour etre sur que toutes les valeurs soient bonnes et actualisées correctement
        self.amortissement_focusout(0)
        self.max_angle_focusout(0)
        self.gravity_focusout(0)
        self.first_theta_focusout(0)
        self.first_mass_focusout(0)
        self.second_theta_focusout(0)
        self.second_mass_focusout(0)

    def start_sim(self):

        self.focusout_trigger()
        self.simulation_state = 1

        # on instancie notre simulation et lui donnont les valeurs a utiliser
        simulation = Sim()
        simulation.get_data(
            amortissement=self.amortissement,
            max_angle=self.max_angle,
            gravity=self.gravity,
            thetha1=self.first_pend_th,
            mass1=self.first_pend_mass,
            thetha2=self.second_pend_th,
            graph=self.graph_plot.get(),
            mass2=self.second_pend_mass
        )
        simulation.simulation()
    
# #################################################################################################
# ####                                                                                         ####
# ####                                    Sortie de focus                                      ####
# ####                                                                                         ####
# #################################################################################################
    
    def amortissement_focusout(self, event):

        new_value = self.entries["amortissement"].get()
        if (new_value == ""):
            self.entries["amortissement"].insert(0, f"{self.amortissement}")
            return
        try:
            self.amortissement = float(new_value)
        except ValueError:
            # en cas d'erreur on remet l'ancienne valeur
            self.entries["amortissement"].delete(0, len(new_value))
            self.entries["amortissement"].insert(0, f"{self.amortissement}")

    def max_angle_focusout(self, event):

        new_value = self.entries["max_angle"].get()
        if (new_value == ""):
            self.entries["max_angle"].insert(0, f"{self.max_angle}")
            return
        try:
            self.max_angle = int(new_value)
        except ValueError:
            # en cas d'erreur on remet l'ancienne valeur
            self.entries["max_angle"].delete(0, len(new_value))
            self.entries["max_angle"].insert(0, f"{self.max_angle}")

    def gravity_focusout(self, event):

        new_value = self.entries["gravity"].get()
        if (new_value == ""):
            self.entries["gravity"].insert(0, f"{self.gravity}")
            return
        try:
            self.gravity = float(new_value)
        except ValueError:
            # en cas d'erreur on remet l'ancienne valeur
            self.entries["gravity"].delete(0, len(new_value))
            self.entries["gravity"].insert(0, f"{self.gravity}")

    def first_theta_focusout(self, event = 0):

        new_value = self.entries["theta 1"].get()
        if (new_value == ""):
            self.entries["theta 1"].insert(0, f"{self.first_pend_th}")
            return
        try:
            self.first_pend_th = int(new_value)
            if self.first_pend_th >= 360:
                self.first_pend_th %= 360
                self.entries["theta 1"].delete(0, len(new_value))
                self.entries["theta 1"].insert(0, f"{self.first_pend_th}")

        except ValueError:
            # en cas d'erreur on remet l'ancienne valeur
            self.entries["theta 1"].delete(0, len(new_value))
            self.entries["theta 1"].insert(0, f"{self.first_pend_th}")

    def first_mass_focusout(self, event):

        new_value = self.entries["mass 1"].get()
        if (new_value == ""):
            self.entries["mass 1"].insert(0, f"{self.first_pend_mass}")
            return
        try:
            self.first_pend_mass = int(new_value)
            if self.first_pend_mass - self.second_pend_mass >= 99 or self.first_pend_mass <= 0:
                self.first_pend_mass = self.second_pend_mass + 98
                self.entries["mass 1"].delete(0, len(new_value))
                self.entries["mass 1"].insert(0, f"{self.first_pend_mass}")

        except ValueError:
            # en cas d'erreur on remet l'ancienne valeur
            self.entries["mass 1"].delete(0, len(new_value))
            self.entries["mass 1"].insert(0, f"{self.first_pend_mass}")

    def second_theta_focusout(self, event):

        new_value = self.entries["theta 2"].get()
        if (new_value == ""):
            self.entries["theta 2"].insert(0, f"{self.second_pend_th}")
            return
        try:
            self.second_pend_th = int(new_value)
            if self.second_pend_th >= 360:
                self.second_pend_th %= 360
                self.entries["theta 2"].delete(0, len(new_value))
                self.entries["theta 2"].insert(0, f"{self.second_pend_th}")
        except ValueError:
            # en cas d'erreur on remet l'ancienne valeur
            self.entries["theta 2"].delete(0, len(new_value))
            self.entries["theta 2"].insert(0, f"{self.second_pend_th}")

    def second_mass_focusout(self, event):

        new_value = self.entries["mass 2"].get()
        if (new_value == ""):
            self.entries["mass 2"].insert(0, f"{self.second_pend_mass}")
            return
        try:
            self.second_pend_mass = int(new_value)
            if self.second_pend_mass - self.first_pend_mass >= 54 or self.second_pend_mass <= 0:
                self.second_pend_mass = self.first_pend_mass + 53
                self.entries["mass 2"].delete(0, len(new_value))
                self.entries["mass 2"].insert(0, f"{self.second_pend_mass}")
        except ValueError:
            # en cas d'erreur on remet l'ancienne valeur
            self.entries["mass 2"].delete(0, len(new_value))
            self.entries["mass 2"].insert(0, f"{self.second_pend_th}")
        
# #################################################################################################
# ####                                                                                         ####
# ####                          Affichage des barres d'input                                   ####
# ####                                                                                         ####
# #################################################################################################

    def insert_base_values(self) -> None:

        # ici sont placées les valeurs par defaut de la simulation dans la bulle de texte

        self.entries["amortissement"].insert(0, f"{self.amortissement}")
        self.entries["amortissement"].bind("<FocusOut>", self.amortissement_focusout)

        self.entries["max_angle"].insert(0, f"{self.max_angle}")
        self.entries["max_angle"].bind("<FocusOut>", self.max_angle_focusout)

        self.entries["gravity"].insert(0, f"{self.gravity}")
        self.entries["gravity"].bind("<FocusOut>", self.gravity_focusout)

        self.entries["theta 1"].insert(0, f"{self.first_pend_th}")
        self.entries["theta 1"].bind("<FocusOut>", self.first_theta_focusout)

        self.entries["mass 1"].insert(0, f"{self.first_pend_mass}")
        self.entries["mass 1"].bind("<FocusOut>", self.first_mass_focusout)

        self.entries["theta 2"].insert(0, f"{self.second_pend_th}")
        self.entries["theta 2"].bind("<FocusOut>", self.second_theta_focusout)

        self.entries["mass 2"].insert(0, f"{self.second_pend_mass}")
        self.entries["mass 2"].bind("<FocusOut>", self.second_mass_focusout)

# #################################################################################################
# ####                                                                                         ####
# ####                             Interface de statistiques                                   ####
# ####                                                                                         ####
# #################################################################################################

    def value_interface(self) -> None:

        # definition de la taille de la fenetre et de son titre
        self.__window.geometry(f"{SCREEN_WIDTH // 3}x{SCREEN_HEIGHT // 3}")
        self.__window.title("Value list")

        self.insert_base_values()

        
        # informations generales
        self.labels["titre"].place(x=SCREEN_WIDTH // 96, y=0)
        self.labels["theta"].place(x=SCREEN_WIDTH // 48, y=SCREEN_HEIGHT // 27 + 4 * SCREEN_HEIGHT // 54)
        self.labels["masse"].place(x=SCREEN_WIDTH // 48, y=SCREEN_HEIGHT // 27 + 5 * SCREEN_HEIGHT // 54)
        
        # #############################################################
        # ## Affichage des variables de la simulation (gravité, ...) ##
        # #############################################################
        self.labels["amortissement"].place(x=SCREEN_WIDTH // 4 + 3 * SCREEN_HEIGHT // 135, y=SCREEN_HEIGHT // 480)
        self.entries["amortissement"].place(x=SCREEN_WIDTH // 4, y=SCREEN_HEIGHT // 480)

        self.labels["max_angle"].place(x=SCREEN_WIDTH // 4 + 3 * SCREEN_HEIGHT // 135, y=SCREEN_HEIGHT // 480 + 2 * SCREEN_HEIGHT // 135)
        self.entries["max_angle"].place(x=SCREEN_WIDTH // 4, y=SCREEN_HEIGHT // 480 + 2 * SCREEN_HEIGHT // 135)

        self.labels["gravity"].place(x=SCREEN_WIDTH // 4 + 5 * SCREEN_HEIGHT // 135, y=SCREEN_HEIGHT // 480 + 4 * SCREEN_HEIGHT // 135)
        self.entries["gravity"].place(x=SCREEN_WIDTH // 4, y=SCREEN_HEIGHT // 480 + 4 * SCREEN_HEIGHT // 135)

        # ###############################################
        # ##          Affichage des Checkbox           ##
        # ###############################################
        self.checkboxes["graph"].place(x=SCREEN_WIDTH // 256, y=SCREEN_HEIGHT // 4)
        self.checkboxes["graph"].select()

        self.checkboxes["gravity"].place(x=SCREEN_WIDTH // 256, y=SCREEN_HEIGHT // 4 + 2 * SCREEN_HEIGHT // 135)
        self.personnalised_gravity()

        # ###############################################
        # ##   Affichage des infos du premier pendule  ##
        # ###############################################
        self.labels["1"].place(x=2 * SCREEN_WIDTH // 24, y=SCREEN_HEIGHT // 27 + 3 * SCREEN_HEIGHT // 54)
        self.entries["theta 1"].place(x=2 * SCREEN_WIDTH // 24, y=SCREEN_HEIGHT // 27 + 4 * SCREEN_HEIGHT // 54)
        self.entries["mass 1"].place(x=2 * SCREEN_WIDTH // 24, y=SCREEN_HEIGHT // 27 + 5 * SCREEN_HEIGHT // 54)

        # ###############################################
        # ##  Affichage des infos du deuxieme pendule  ##
        # ###############################################
        self.labels["2"].place(x=5 * SCREEN_WIDTH // 24, y=SCREEN_HEIGHT // 27 + 3 * SCREEN_HEIGHT // 54)
        self.entries["theta 2"].place(x=5 * SCREEN_WIDTH // 24, y=SCREEN_HEIGHT // 27 + 4 * SCREEN_HEIGHT // 54)
        self.entries["mass 2"].place(x=5 * SCREEN_WIDTH // 24, y=SCREEN_HEIGHT // 27 + 5 * SCREEN_HEIGHT // 54)

        ## bouton de lancement de la simulation
        self.simulation_start.place(x=SCREEN_WIDTH // 3.7, y=SCREEN_HEIGHT // 3.5)

        # boucle principale (interne a tkinter)
        self.__window.mainloop()

# #################################################################################################
# ####                                                                                         ####
# ####                                         Autres                                          ####
# ####                                                                                         ####
# #################################################################################################

    def personnalised_gravity(self):
        if self.modified_gravity.get():
            self.entries["gravity"].configure(state="normal")
        else:
            to_remove = self.entries["gravity"].get()
            self.gravity = 9.81
            self.entries["gravity"].delete(0, len(to_remove))
            self.entries["gravity"].insert(0, f"{self.gravity}")
            self.entries["gravity"].configure(state="readonly")


if __name__ == "__main__":

    simulation_data = Data()

    simulation_data.value_interface()

