# ur-protective-stop-recorder
Python program to trigger recording for a camera when (tentatively) Protective Stops occurs.  

1. Install python via Microsoft Store
2. (Recommended) Set-up Python Virtual Environment
3. Change Robot IP Address in cam_capture.py to be the same IP as robot (Line 7) [As of 15/5/25]
4. Use Command Prompt, run virtual environement and run python script

Note_1: Python Script can automatically detect if robot is cb-series or e-series.
Note_2: Program is currently only programmed for Protective Stops and not others
Note_3: Program was tested with only 1 camera. There might be issues potential issues to automatically detect the desired camera, if device has multiple cameras  