
import os
import subprocess
from config import initialize_system

def main():
    subprocess.Popen(["python", '../../SmartAccess/web_app/app.py'])
    initialize_system()

if __name__ == "__main__":
    main()
