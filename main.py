"""
    Code for analysing archer's body posture
"""
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from optitrack.geometry import *
import optitrack.csv_reader as csv

from analyse_feet import analyse_feet
from analyse_hips import analyse_hips
from analyse_shoulder import analyse_shoulder

from utils import user_message, ask_yesno
from utils import get_bones_position, show_animation, body_edges


user_message(f"Welcome to anaylsis of archer body posture 🧍", "archery")

show_plots = ask_yesno("See the plots during the analysis...? ")

analyse_shoulder(show_plots);
analyse_feet(show_plots);
analyse_hips(show_plots);


# # filename = "data/Training_Recording.csv"
# filename = "data/Wrong_Foot_Position.csv"
# # filename = "data/Wrong_Hips_Position.csv"
# # filename = "data/Wrong_Hips_Position_2.csv"
# # filename = "data/Wrong_Hips_Position_3.csv"
# # filename = "data/Wrong_Shoulder_Position.csv"

# # Read the file.
# take = csv.Take().readCSV(filename)

# # Print out some statistics
# # print("Found rigid bodies:", take.rigid_bodies.keys())
# # print("\n")

# print(len(take.rigid_bodies.keys()))

# # Process the first rigid body into a set of planes.
# bodies = take.rigid_bodies

# # for now:
# xaxis = [1,0,0]
# yaxis = [0,1,0]

# #--- GENERAL OPTIONS ---#

# body_edges, bones_pos, _ = get_bones_position(take)

# colors = [[1, 0, 0] for i in range(len(body_edges))]

# show_animation(take, bones_pos, body_edges, colors)
