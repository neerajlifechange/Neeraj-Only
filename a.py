import subprocess

# Install required packages
subprocess.run(["pip", "install", "playwright"])
subprocess.run(["pip", "install", "beautifulsoup4"])
subprocess.run(["pip", "install", "requests"])
subprocess.run(["pip", "install", "indian-names"])
subprocess.run(["playwright", "install"])
subprocess.run(["playwright", "install-deps"])

# Install required system packages
subprocess.run(["apt", "install", "firefox", "-y"])
subprocess.run(["apt", "install", "wget", "-y"])

# Download and install GeckoDriver
geckodriver_url = "https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz"
subprocess.run(["wget", geckodriver_url])
subprocess.run(["tar", "-xvzf", "geckodriver-v0.30.0-linux64.tar.gz"])
subprocess.run(["chmod", "+x", "geckodriver"])
subprocess.run(["mv", "geckodriver", "/usr/local/bin/"])
