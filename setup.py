import os
import re
import subprocess
import sys
import shutil

#TEXT FORMATS
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"
BOLD = "\033[1m"

EXIT_MESSAGE = f"{RED}{BOLD}Exiting...{RESET}"

def run(cmd):
    print(f"{GREEN}{BOLD}Running Command:{RESET} {cmd}")
    subprocess.check_call(cmd,shell=True)

def generateEnv():
    print(f"{BLUE}{BOLD}Creating .env file:{RESET}")
    plex_address = input(f"Enter your plex address (default: http://localhost:32400):\t")
    plex_tkn = input(f"Enter your plex token:\t")
    if(not re.match('http://(.*):32400',plex_address)):
        print(f"{RED}{BOLD}Error!{RESET} {plex_address} is not a valid format.")
        print(EXIT_MESSAGE)
        exit(1)
    
    content = "PLEX_HOST="+plex_address+"\nPLEX_TKN="+plex_tkn

    run('echo {content} > .env')

def createVenv():
    print(f"{BLUE}{BOLD}Creating a virtual environment{RESET}")
    run(f'{sys.executable} -m venv venv')

def installDependencies():
    print(f"{BLUE}{BOLD}Installing dependencies{RESET}")
    pip_path = os.path.join("venv", "Scripts" if os.name == "nt" else "bin", "pip")

    run(f'{pip_path} install -r requirements.txt')

if __name__ == "__main__":
    
    generateEnv()
    createVenv()
    installDependencies()

    print(f"{BOLD}{GREEN}Success!{RESET} Setup Complete!")
    print(f"{BOLD}{BLUE}You can now run the script as follows:{RESET}")

    if os.name == "nt":
        print("venv\\Scripts\\makeMetaData.py")
    else:
        print("source venv/bin/activate && python makeMetaData.py")


