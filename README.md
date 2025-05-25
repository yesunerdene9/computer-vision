# computer-vision

# Analysing archer's body posture with Motion Capture System

The repository for the project of the course Computer Vision [[140266](https://unitn.coursecatalogue.cineca.it/insegnamenti/2024/50540_644803_89473/2011/50540/10117?annoOrdinamento=2011)] at University of Trento. This project used OptiTrafk motion capture system to analyse the body posture of the archer to detect wrong body posture during the aiming phase with purpose of improving the shooring and prevent from injuries caused by wrong body posture.

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
# Please, make sure you have Python 3 and PIP
python3 main.py
```

# What does the project do?

# Data collection

Following are the aiming phase of the archer, including the correct and wrong body postures

| <div style="text-align: center"><img src="assets/gifs/Training_Recording.gif" width="300"/><br/>Correct Posture</div> |
|------------------------------------------------------------------------------------------|



| <div style="text-align: center"><img src="assets/gifs/Wrong_Hips_Position.gif" width="300"/><br/>Wrong hips posture</div>  | <div style="text-align: center"><img src="assets/gifs/Wrong_Hips_Position.gif" width="300"/><br/>Wrong hips posture</div> |
|------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|


| <div style="text-align: center"><img src="assets/gifs/Wrong_Shoulder_Position.gif" width="300"/><br/>Wrong shoulder posture</div> |<div style="text-align: center"><img src="assets/gifs/Wrong_Foot_Position.gif" width="300"/><br/>Wrong feet distance posture</div> |
|------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|



<!-- 
| ![](assets/gifs/Training_Recording.gif) | ![](assets/gifs/Wrong_Hips_Position.gif) | ![](assets/gifs/Wrong_Shoulder_Position.gif) | ![](assets/gifs/Wrong_Foot_Position.gif) |
|-----------------------------------------|------------------------------------------|----------------------------------------------|------------------------------------------| -->