# ur-protective-stop-recorder
Python program to trigger recording for a camera when Protective Stops occurs. Video recording is set to 10s pre-Protective Stop, 5s post-Protective Stop. Duration is adjustable at the  

1. Install python via Microsoft Store
2. (Recommended) Set-up Python Virtual Environment
   Example: python -m venv env
  - cd path/to/folder > *environment_name*/Scripts/activate
    - If above has Policy Errors, copy-paste the following "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process" and try again.
    - Once activated, we will install the dependency needed for this project.
    - Type in Command Prompt "pip install opencv-python"
    - Setup of Virtual Environment for this project is done. 
4. Change Robot IP Address in cam_capture.py to be the same IP as robot (Line 7) [As of 15/5/25]
5. Use Command Prompt,
  - Run virtual environement (Follow steps similar to Point 2. just without "pip install opencv-python" command
  - Run python script: cd path/to/folder > type "python cam_capture.py"

## FOR TESTING PURPOSES
Use 'c' as keypress to Unlock Protective Stop and play program.

Note_1: Recording timestamp is based on the time Robot encounters a Protective stop. 
Note_2: Program can automatically detect if robot is cb-series or e-series.  
Note_3: Program is currently only programmed for Protective Stops and not other Stops.  
Note_4: Program was tested with only 1 camera. There might be issues potential issues to automatically detect the desired camera, if device has multiple cameras  
