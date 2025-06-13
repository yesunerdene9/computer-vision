### Computer Vision 2025

# Analysing archer's body posture with Motion Capture System

The repository for the project of the course Computer Vision [[140266](https://unitn.coursecatalogue.cineca.it/insegnamenti/2024/50540_644803_89473/2011/50540/10117?annoOrdinamento=2011)] at University of Trento. 

This project analyses the fundamental body posture of an archer using MoCap technology to capture key postural parameters such as joint angles and foot distances. The aim is to provide insights that could lead to an automatic method for evaluating posture and classifying it as proper or incorrect in future work. The result of the analysis highlights a significant difference between the reference correct and incorrect body postures, showing the potential for objective classification based on measurable postural features.

The presentation video can be found [HERE](https://www.youtube.com/watch?v=LigHnNiQJhU)

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

# Implementation

## Data collection

The following images show the aiming phase of the archer, including both correct and incorrect body postures.

| <div style="text-align: center"><img src="assets/gifs/Training_Recording.gif" style="width: 100%;"/><br/>Correct Body Posture</div> | <div style="text-align: center"><img src="assets/gifs/Training_Recording_3D.gif" style="width: 100%;"/><br/>Correct Body Posture in 3D</div> |
|------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|



| <div style="text-align: center"><img src="assets/gifs/Wrong_Hips_Position.gif" style="width: 100%;"/><br/>Wrong Hips Posture tilt to the Left</div>  | <div style="text-align: center"><img src="assets/gifs/Wrong_Hips_Position_3.gif" style="width: 100%;"/><br/>Wrong Hips Posture Tilt to the Right</div> |
|------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|


| <div style="text-align: center"><img src="assets/gifs/Wrong_Shoulder_Position.gif" style="width: 100%;"/><br/>Wrong Shoulder Raise Posture</div> |<div style="text-align: center"><img src="assets/gifs/Wrong_Foot_Position.gif" style="width: 100%;"/><br/>Wrong Distance between posture</div> |
|------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|



<!-- 
| ![](assets/gifs/Training_Recording.gif) | ![](assets/gifs/Wrong_Hips_Position.gif) | ![](assets/gifs/Wrong_Shoulder_Position.gif) | ![](assets/gifs/Wrong_Foot_Position.gif) |
|-----------------------------------------|------------------------------------------|----------------------------------------------|------------------------------------------| -->

## Method
| <div style="text-align: center"><img src="docs/Training_Recording.png" style="width: 30%;"/><br/>Joints Marked with Points</div> |
|------------------------------------------------------------------------------------------|

| <div style="text-align: center"><img src="docs/Wrong_Hips_Position.png" style="width: 50%;"/><br/>Spine and Hips raising Angle</div> | <div style="text-align: center"><img src="docs/Wrong_Hips_Position_3.png" style="width: 50%;"/><br/>Leg Tilting Angle</div> |
|------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|

| <div style="text-align: center"><img src="docs/Wrong_Shoulder_Position.png" style="width: 50%;"/><br/>Shoulder Angle</div> | <div style="text-align: center"><img src="docs/Wrong_Foot_Position.png" style="width: 50%;"/><br/>Distance Between Feet and Toes </div> |
|------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|



## Results

<p align="center">
  <img src="output/result.png" width="70%">
</p>
<p align="center">
  The result of the analysis highlights the <br/>
  significant difference between the reference correct and incorrect body postures.
</p>



### Output

The resulting output is organized in following structure:

```bash
output/
├── feet/
│   ├── plots/
│   │   ├── plot1.png
│   │   └── report.pdf
│   ├── stats/
│   │   ├── plot1.png
│   │   └── plot2.png
│   └── ...
├── hips/
│   └── hips_drop/
│   └── hips_raise/
│   └── leg_tilt/
│   └── spine_tilt/
│   │   ├── ...
│   │   ├── ...
├── shoulder/
│   ├── ...
```

---



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


