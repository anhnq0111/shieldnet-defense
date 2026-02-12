#!/bin/bash

# White-label script to rebrand wazuh -> shieldnet-defend
# This script performs the following operations:
# 1. Replace packages.wazuh.com with placeholder to preserve it
# 2. Replace all wazuh variations with shieldnet-defend
# 3. Restore packages.wazuh.com from placeholder
# 4. Rename files containing 'wazuh' to 'shieldnet-defend'

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default target directory is current directory
TARGET_DIR="${1:-.}"

# Temporary placeholder for package URL
PACKAGE_URL_PLACEHOLDER="__PACKAGE_URL_PLACEHOLDER__"

# Temporary placeholder for libwazuhext.so
LIB_PLACEHOLDER="__LIB_PLACEHOLDER__"

echo -e "${GREEN}Starting white-label process...${NC}"
echo -e "${YELLOW}Target directory: ${TARGET_DIR}${NC}"

# Function to perform sed replacement on files
replace_in_files() {
    local search="$1"
    local replace="$2"
    local description="$3"
    
    echo -e "${YELLOW}Replacing: ${search} -> ${replace}${NC}"
    
    # Find all text files and perform replacement
    # Exclude .git directory, binary files, and this script itself
    find "$TARGET_DIR" -type f \
        ! -path "*/.git/*" \
        ! -path "*/node_modules/*" \
        ! -name "*.png" \
        ! -name "*.jpg" \
        ! -name "*.jpeg" \
        ! -name "*.gif" \
        ! -name "*.ico" \
        ! -name "*.pdf" \
        ! -name "*.zip" \
        ! -name "*.tar" \
        ! -name "*.gz" \
        ! -name "*.bz2" \
        ! -name "*.exe" \
        ! -name "*.dll" \
        ! -name "*.so" \
        ! -name "*.dylib" \
        ! -name "white-lable.sh" \
        -print0 2>/dev/null | while IFS= read -r -d '' file; do
        # Check if file is a text file
        if file "$file" | grep -q "text"; then
            if grep -q "$search" "$file" 2>/dev/null; then
                sed -i "s|${search}|${replace}|g" "$file"
                echo -e "  ${GREEN}Updated: ${file}${NC}"
            fi
        fi
    done
}

# Function to rename files containing 'wazuh' in their name
rename_files() {
    echo -e "${YELLOW}Renaming files containing 'wazuh'...${NC}"
    
    # Find files with 'wazuh' in name (case insensitive for finding, but rename preserving case pattern)
    # Process deepest files first to avoid path issues
    find "$TARGET_DIR" -depth -type f \
        ! -path "*/.git/*" \
        ! -path "*/node_modules/*" \
        -name "*wazuh*" \
        -print0 2>/dev/null | while IFS= read -r -d '' file; do
        dir=$(dirname "$file")
        basename=$(basename "$file")
        newname=$(echo "$basename" | sed 's/wazuh/shieldnet_defend/g')
        if [ "$basename" != "$newname" ]; then
            mv "$file" "$dir/$newname"
            echo -e "  ${GREEN}Renamed: ${basename} -> ${newname}${NC}"
        fi
    done
    
    # Also handle uppercase WAZUH in filenames
    find "$TARGET_DIR" -depth -type f \
        ! -path "*/.git/*" \
        ! -path "*/node_modules/*" \
        -name "*WAZUH*" \
        -print0 2>/dev/null | while IFS= read -r -d '' file; do
        dir=$(dirname "$file")
        basename=$(basename "$file")
        newname=$(echo "$basename" | sed 's/WAZUH/SHIELDNET_DEFEND/g')
        if [ "$basename" != "$newname" ]; then
            mv "$file" "$dir/$newname"
            echo -e "  ${GREEN}Renamed: ${basename} -> ${newname}${NC}"
        fi
    done
    
    # Handle Wazuh (capitalized) in filenames
    find "$TARGET_DIR" -depth -type f \
        ! -path "*/.git/*" \
        ! -path "*/node_modules/*" \
        -name "*Wazuh*" \
        -print0 2>/dev/null | while IFS= read -r -d '' file; do
        dir=$(dirname "$file")
        basename=$(basename "$file")
        newname=$(echo "$basename" | sed 's/Wazuh/ShieldnetDefend/g')
        if [ "$basename" != "$newname" ]; then
            mv "$file" "$dir/$newname"
            echo -e "  ${GREEN}Renamed: ${basename} -> ${newname}${NC}"
        fi
    done
}

# Function to rename directories containing 'wazuh' in their name
rename_directories() {
    echo -e "${YELLOW}Renaming directories containing 'wazuh'...${NC}"
    
    # Process deepest directories first
    find "$TARGET_DIR" -depth -type d \
        ! -path "*/.git/*" \
        ! -path "*/node_modules/*" \
        -name "*wazuh*" \
        -print0 2>/dev/null | while IFS= read -r -d '' dir; do
        parent=$(dirname "$dir")
        basename=$(basename "$dir")
        newname=$(echo "$basename" | sed 's/wazuh/shieldnet_defend/g')
        if [ "$basename" != "$newname" ]; then
            mv "$dir" "$parent/$newname"
            echo -e "  ${GREEN}Renamed dir: ${basename} -> ${newname}${NC}"
        fi
    done
    
    # Handle uppercase WAZUH in directory names
    find "$TARGET_DIR" -depth -type d \
        ! -path "*/.git/*" \
        ! -path "*/node_modules/*" \
        -name "*WAZUH*" \
        -print0 2>/dev/null | while IFS= read -r -d '' dir; do
        parent=$(dirname "$dir")
        basename=$(basename "$dir")
        newname=$(echo "$basename" | sed 's/WAZUH/SHIELDNET_DEFEND/g')
        if [ "$basename" != "$newname" ]; then
            mv "$dir" "$parent/$newname"
            echo -e "  ${GREEN}Renamed dir: ${basename} -> ${newname}${NC}"
        fi
    done
    
    # Handle Wazuh (capitalized) in directory names
    find "$TARGET_DIR" -depth -type d \
        ! -path "*/.git/*" \
        ! -path "*/node_modules/*" \
        -name "*Wazuh*" \
        -print0 2>/dev/null | while IFS= read -r -d '' dir; do
        parent=$(dirname "$dir")
        basename=$(basename "$dir")
        newname=$(echo "$basename" | sed 's/Wazuh/ShieldnetDefend/g')
        if [ "$basename" != "$newname" ]; then
            mv "$dir" "$parent/$newname"
            echo -e "  ${GREEN}Renamed dir: ${basename} -> ${newname}${NC}"
        fi
    done
}

# Step 1_a: Replace packages.wazuh.com with placeholder
echo -e "\n${GREEN}Step 1_a: Preserving packages.wazuh.com with placeholder...${NC}"
replace_in_files "packages.wazuh.com" "$PACKAGE_URL_PLACEHOLDER" "Preserve package URL"

# Step 1_b: Replace libwazuhext.so with placeholder
echo -e "\n${GREEN}Step 1_b: Preserving libwazuhext.so with placeholder...${NC}"
replace_in_files "libwazuhext.so" "$LIB_PLACEHOLDER" "Preserve lib so"

# Step 2: Replace all lowercase 'wazuh' with 'shieldnet-defend'
echo -e "\n${GREEN}Step 2: Replacing 'wazuh' -> 'shieldnet_defend'...${NC}"
replace_in_files "wazuh" "shieldnet_defend" "Lowercase replacement"

# Step 3: Replace all uppercase 'WAZUH' with 'SHIELDNET-DEFEND'
echo -e "\n${GREEN}Step 3: Replacing 'WAZUH' -> 'SHIELDNET_DEFEND'...${NC}"
replace_in_files "WAZUH" "SHIELDNET_DEFEND" "Uppercase replacement"

# Step 4: Replace capitalized 'Wazuh' with 'Shieldnet-Defend'
echo -e "\n${GREEN}Step 4: Replacing 'Wazuh' -> 'ShieldnetDefend'...${NC}"
replace_in_files "Wazuh" "ShieldnetDefend" "Capitalized replacement"

# Step 5_a: Restore packages.wazuh.com from placeholder
echo -e "\n${GREEN}Step 5_a: Restoring packages.wazuh.com from placeholder...${NC}"
replace_in_files "$PACKAGE_URL_PLACEHOLDER" "packages.wazuh.com" "Restore package URL"

# Step 5_b: Restore libwazuhext.so from placeholder
echo -e "\n${GREEN}Step 5_a: Restoring libwazuhext.so from placeholder...${NC}"
replace_in_files "$LIB_PLACEHOLDER" "libwazuhext.so" "Restore lib so"

# Step 6: Rename files with 'wazuh' in their name
echo -e "\n${GREEN}Step 6: Renaming files...${NC}"
rename_files

# Step 7: Rename directories with 'wazuh' in their name
echo -e "\n${GREEN}Step 7: Renaming directories...${NC}"
rename_directories

echo -e "\n${GREEN}White-label process completed!${NC}"
echo -e "${YELLOW}Please review the changes and test thoroughly.${NC}"
