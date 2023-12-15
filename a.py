import subprocess
import os

# Clone the repository
subprocess.run(["git", "clone", "https://github.com/neerajlifechange/Neeraj-Only.git"])

# Change to the repository directory
os.chdir("Neeraj-Only")

# Give execution permission to install_brave.sh
subprocess.run(["chmod", "+x", "Brave.sh"])

# Run install_brave.sh
subprocess.run(["./Brave.sh"])
