How to Run the Code
-------------------
This guide will help you run the provided code efficiently. Please follow the instructions carefully to ensure proper functionality.

#Prerequisites
- Python must be installed on your system.

- Ensure you have the required Python libraries installed. You can install any missing libraries using `pip install <library_name>`.
 "Here are the lists of Libraries that require you to install first"
  1> pip install screeninfo,  # from screeninfo import get_monitors  # Import get_monitors to fetch monitor information
  2> pip install numpy,       # import numpy as np # For numerical operations and data manipulation
  3> pip install sounddevice, # import sounddevice as sd # For recording audio using various audio devices
  4> pip install soundfile,   # import soundfile as sf # For reading and writing sound files
  5> pip install pynput,      # from pynput import keyboard # To capture keyboard inputs
  6> pip install datetime,    # import datetime # For handling date and time operations, such as timestamps
  7> pip install mss          # from mss import mss  # Import mss to efficiently capture screenshots on multiple operating systems"

- VSCode or any other Python-capable IDE is recommended for executing these scripts.

Step-by-Step Instructions
1. Initial Setup:
   - Open the project folder in VSCode or your chosen IDE.

2. Running the Scripts:
   - Backdoor.py: This script should be run first. It acts as a client trying to connect to the server.
   - Server.py: After running `Backdoor.py`, launch `Server.py`. This script sets up the server that listens for connections from the client.

3. Execution Methods:
   - You can run each script (`Backdoor.py` or `Server.py`) in separate terminals. One can be in VSCode's terminal, and the other can be in CMD or PowerShell.
   - Use the command: `python.exe {file_path}` to run each script. Replace `{file_path}` with the actual path to `Backdoor.py` or `Server.py`.

4. Configuration Settings:
   - Both scripts are configured to use the IP address `127.0.0.1` and port `5555`. These settings can be found in:
     - `Backdoor.py` lines 35-50: The function to establish a connection uses `s.connect(('127.0.0.1', 5555))`.
     - `Server.py` line 114: The server binding is set with `sock.bind(('0.0.0.0', 5555))`.
   - Important: If you change the IP address or port in one script, you must make a corresponding change in the other script to ensure they can connect successfully.

5. Testing Environment:
   - The default setup uses localhost (`127.0.0.1`) for testing. If your testing scenario requires a different setup, adjust the IP addresses and ports as described above.

6. Enjoy Testing!
   - Once everything is set up and running, you can test the functionalities as intended.

Additional Notes:
- Keep your system's firewall and security settings in check as they might block connections between the scripts.
- Regularly update your Python and libraries to the latest versions to avoid any compatibility issues.

Thank you for using our system. We hope your testing goes smoothly!
