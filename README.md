### Computer Vision 2025

# Analysing archer's body posture with Motion Capture System

The repository for the project of the course Computer Vision [[140266](https://unitn.coursecatalogue.cineca.it/insegnamenti/2024/50540_644803_89473/2011/50540/10117?annoOrdinamento=2011)] at University of Trento. This project used OptiTrack motion capture system to analyse the body posture of the archer to detect wrong body posture during the aiming phase with purpose to improve the shooting and prevent from injuries caused by wrong body posture.

## Installation & Run

```bash
# Clone the Repository
git clone https://github.com/yesunerdene9/computer-vision.git
```

```bash
# Navigate to the project root
cd computer-vision
```

```bash
# Install Dependencies
pip install -r requirements.txt
```

#### Run the project

```bash
# Please, make sure you have Python 3 and pip
python3 main.py
```

# What does the project do?

# Data collection

Following are the aiming phase of the archer, including the correct and wrong body postures

| <div style="text-align: center"><img src="assets/gifs/Training_Recording.gif" width="350"/><br/>Correct Body Posture</div> | <div style="text-align: center"><img src="assets/gifs/Training_Recording_3D.gif" width="350"/><br/>Correct Body Posture in 3D</div> |
|------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|



| <div style="text-align: center"><img src="assets/gifs/Wrong_Hips_Position.gif" width="350"/><br/>Wrong Hips Posture tilt to the Left</div>  | <div style="text-align: center"><img src="assets/gifs/Wrong_Hips_Position_3.gif" width="350"/><br/>Wrong Hips Posture Tilt to the Right</div> |
|------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|


| <div style="text-align: center"><img src="assets/gifs/Wrong_Shoulder_Position.gif" width="350"/><br/>Wrong Shoulder Raise Posture</div> |<div style="text-align: center"><img src="assets/gifs/Wrong_Foot_Position.gif" width="350"/><br/>Wrong Distance between posture</div> |
|------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|



<!-- 
| ![](assets/gifs/Training_Recording.gif) | ![](assets/gifs/Wrong_Hips_Position.gif) | ![](assets/gifs/Wrong_Shoulder_Position.gif) | ![](assets/gifs/Wrong_Foot_Position.gif) |
|-----------------------------------------|------------------------------------------|----------------------------------------------|------------------------------------------| -->


## Results

| <div style="text-align: center"><img src="output/result.png" style="width: 100%;"/><br/>The result of the analysis highlights the <br/>significant difference between the reference correct and incorrect body postures</div> |
|------------------------------------------------------------------------------------------|


| <div style="text-align: center"><img src="output/shoulder/plots/Shoulder_raise_angle_combined_plot.png" style="width: 100%;"/><br/>Shoulder Raise Angle comparison</div> |
|------------------------------------------------------------------------------------------|

| <div style="text-align: center"><img src="output/feet/plots/Feet_distance_combined_plot.png" style="width: 100%;"/><br/>Feet Distance comparison</div> |
|------------------------------------------------------------------------------------------|

| <div style="text-align: center"><img src="output/hips/plots/hips_drop/Hips_drop_combined_plot.png" style="width: 100%;"/><br/>Hips Drop comparison</div> |
|------------------------------------------------------------------------------------------|

| <div style="text-align: center"><img src="output/hips/plots/leg_tilt/Back_leg_tilt_combined_plot.png" style="width: 100%;"/><br/>Back Leg Tilt Angle comparison</div> |
|------------------------------------------------------------------------------------------|

| <div style="text-align: center"><img src="output/hips/plots/spine_tilt/Spine_tilt_combined_plot.png" style="width: 100%;"/><br/>Spine Tilt Angle comparison</div> |
|------------------------------------------------------------------------------------------|

| <div style="text-align: center"><img src="output/hips/plots/hips_raise/Hips_raise_combined_plot.png" style="width: 100%;"/><br/>Hips Raise Angle comparison</div> |
|------------------------------------------------------------------------------------------|


