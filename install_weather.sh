#!/bin/bash

# Define the base raw GitHub URL for the weather repository
REPO_BASE_URL="https://raw.githubusercontent.com/SJK-py/nanobot-weather/main"

# 1. Validate workspace directory by checking for 'skills' folder
if [ ! -d "skills" ]; then
    echo "Error: The 'skills' directory was not found."
    echo "This script must be executed from the root of your nanobot workspace directory."
    exit 1
fi

# 2. Create the necessary directories
echo "Creating directories..."
mkdir -p skills/weather/scripts

# Function to handle backing up and downloading files
download_file() {
    local url=$1
    local dest=$2
    local filename=$(basename "$dest")

    # 3. Rename old files with .bak extension if they already exist
    if [ -f "$dest" ]; then
        mv "$dest" "${dest}.bak"
        echo "  -> Backed up existing '$filename' to '${filename}.bak'"
    fi

    # Download the file
    echo "  -> Downloading '$filename'..."
    curl -sS -f -L "$url" -o "$dest"
    
    if [ $? -ne 0 ]; then
        echo "  -> Error: Failed to download '$filename'. Please check the URL or your network connection."
    fi
}

# 4 & 5. Download the files to their respective directories
echo "Downloading files from repository..."

# Download SKILL.md
download_file "${REPO_BASE_URL}/skills/weather/SKILL.md" "skills/weather/SKILL.md"

# Download weather.py
download_file "${REPO_BASE_URL}/skills/weather/scripts/weather.py" "skills/weather/scripts/weather.py"

# 6. Output completion message
echo ""
echo "============================================================"
echo "Installation complete! The Weather skill has been added."
echo "Your nanobot will now detect and use the weather skill."
echo "============================================================"
