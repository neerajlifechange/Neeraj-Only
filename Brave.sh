#!/bin/bash

# Install curl
sudo apt-get install -y curl

# Download the Brave browser keyring
sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg

# Add Brave browser repository to sources.list.d
echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" | sudo tee /etc/apt/sources.list.d/brave-browser-release.list

# Update package list
sudo apt-get update

# Install Brave browser
sudo apt-get install -y brave-browser

# Install Python packages
pip install playwright
playwright install
pip install getindianname
