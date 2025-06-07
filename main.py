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

from utils import show_message, ask_yesno, show_anim

show_message(f"Welcome to anaylsis of archer body posture 🧍", "archery")

show_plots = ask_yesno("See the plots during the analysis...? ")

analyse_shoulder(show_plots);
analyse_feet(show_plots);
analyse_hips(show_plots);

visualize_animat = ask_yesno("Do you want to see the animation? ")
if visualize_animat:
    filename = "data/Training_Recording.csv"
    show_anim(filename)
    filename = "data/Wrong_Foot_Position.csv"
    show_anim(filename)
    filename = "data/Wrong_Hips_Position.csv"
    show_anim(filename)
    filename = "data/Wrong_Hips_Position_3.csv"
    show_anim(filename)
    filename = "data/Wrong_Shoulder_Position.csv"
    show_anim(filename)
