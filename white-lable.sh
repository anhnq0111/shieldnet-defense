#!/bin/bash

# White-label script to rebrand wazuh -> shieldnet-defend
# Replacement rules (order matters; more specific first):
#   wazuh-  -> shieldnet-defend-   (suffix dash)
#   wazuh_  -> shieldnet_defend_   (suffix underscore)
#   -wazuh  -> -shieldnet-defend   (prefix dash)
#   _wazuh  -> _shieldnet_defend   (prefix underscore)
#   wazuh*  -> shieldnet*          (wildcard/glob pattern)
#   wazuh   -> shieldnetdefend     (catch-all)
# Same logic for WAZUH and Wazuh. packages.wazuh.com and libwazuhext.so are preserved.

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
        ! -name ".gitmodules" \
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
                # Use .bak and remove: portable on both macOS (BSD sed) and Linux (GNU sed)
                sed -i.bak "s|${search}|${replace}|g" "$file" && rm -f "$file.bak"
                echo -e "  ${GREEN}Updated: ${file}${NC}"
            fi
        fi
    done
}

# Apply name replacement rules (suffix, then prefix, then catch-all)
transform_name_lower() { echo "$1" | sed 's/wazuh-/shieldnet-defend-/g' | sed 's/wazuh_/shieldnet_defend_/g' | sed 's/-wazuh/-shieldnet-defend/g' | sed 's/_wazuh/_shieldnet_defend/g' | sed 's/wazuh/shieldnetdefend/g'; }
transform_name_upper() { echo "$1" | sed 's/WAZUH-/SHIELDNET-DEFEND-/g' | sed 's/WAZUH_/SHIELDNET_DEFEND_/g' | sed 's/-WAZUH/-SHIELDNET-DEFEND/g' | sed 's/_WAZUH/_SHIELDNET_DEFEND/g' | sed 's/WAZUH/SHIELDNETDEFEND/g'; }
transform_name_cap()   { echo "$1" | sed 's/Wazuh-/ShieldnetDefend-/g' | sed 's/Wazuh_/ShieldnetDefend_/g' | sed 's/-Wazuh/-ShieldnetDefend/g' | sed 's/_Wazuh/_ShieldnetDefend/g' | sed 's/Wazuh/ShieldnetDefend/g'; }

# Function to rename files containing 'wazuh' in their name
rename_files() {
    echo -e "${YELLOW}Renaming files containing 'wazuh'...${NC}"
    
    # Process deepest files first; apply rules: wazuh- -> shieldnet-defend-, wazuh_ -> shieldnet_defend_, -wazuh -> -shieldnet-defend, _wazuh -> _shieldnet_defend, wazuh -> shieldnetdefend
    find "$TARGET_DIR" -depth -type f \
        ! -path "*/.git/*" \
        ! -path "*/node_modules/*" \
        -name "*wazuh*" \
        -print0 2>/dev/null | while IFS= read -r -d '' file; do
        dir=$(dirname "$file")
        basename=$(basename "$file")
        newname=$(transform_name_lower "$basename")
        if [ "$basename" != "$newname" ]; then
            mv "$file" "$dir/$newname"
            echo -e "  ${GREEN}Renamed: ${basename} -> ${newname}${NC}"
        fi
    done
    
    find "$TARGET_DIR" -depth -type f \
        ! -path "*/.git/*" \
        ! -path "*/node_modules/*" \
        -name "*WAZUH*" \
        -print0 2>/dev/null | while IFS= read -r -d '' file; do
        dir=$(dirname "$file")
        basename=$(basename "$file")
        newname=$(transform_name_upper "$basename")
        if [ "$basename" != "$newname" ]; then
            mv "$file" "$dir/$newname"
            echo -e "  ${GREEN}Renamed: ${basename} -> ${newname}${NC}"
        fi
    done
    
    find "$TARGET_DIR" -depth -type f \
        ! -path "*/.git/*" \
        ! -path "*/node_modules/*" \
        -name "*Wazuh*" \
        -print0 2>/dev/null | while IFS= read -r -d '' file; do
        dir=$(dirname "$file")
        basename=$(basename "$file")
        newname=$(transform_name_cap "$basename")
        if [ "$basename" != "$newname" ]; then
            mv "$file" "$dir/$newname"
            echo -e "  ${GREEN}Renamed: ${basename} -> ${newname}${NC}"
        fi
    done
}

# Function to rename directories containing 'wazuh' in their name
rename_directories() {
    echo -e "${YELLOW}Renaming directories containing 'wazuh'...${NC}"
    
    find "$TARGET_DIR" -depth -type d \
        ! -path "*/.git/*" \
        ! -path "*/node_modules/*" \
        -name "*wazuh*" \
        -print0 2>/dev/null | while IFS= read -r -d '' dir; do
        parent=$(dirname "$dir")
        basename=$(basename "$dir")
        newname=$(transform_name_lower "$basename")
        if [ "$basename" != "$newname" ]; then
            mv "$dir" "$parent/$newname"
            echo -e "  ${GREEN}Renamed dir: ${basename} -> ${newname}${NC}"
        fi
    done
    
    find "$TARGET_DIR" -depth -type d \
        ! -path "*/.git/*" \
        ! -path "*/node_modules/*" \
        -name "*WAZUH*" \
        -print0 2>/dev/null | while IFS= read -r -d '' dir; do
        parent=$(dirname "$dir")
        basename=$(basename "$dir")
        newname=$(transform_name_upper "$basename")
        if [ "$basename" != "$newname" ]; then
            mv "$dir" "$parent/$newname"
            echo -e "  ${GREEN}Renamed dir: ${basename} -> ${newname}${NC}"
        fi
    done
    
    find "$TARGET_DIR" -depth -type d \
        ! -path "*/.git/*" \
        ! -path "*/node_modules/*" \
        -name "*Wazuh*" \
        -print0 2>/dev/null | while IFS= read -r -d '' dir; do
        parent=$(dirname "$dir")
        basename=$(basename "$dir")
        newname=$(transform_name_cap "$basename")
        if [ "$basename" != "$newname" ]; then
            mv "$dir" "$parent/$newname"
            echo -e "  ${GREEN}Renamed dir: ${basename} -> ${newname}${NC}"
        fi
    done
}

# Step 1_a: Replace packages.wazuh.com with placeholder
echo -e "\n${GREEN}Step 1_a: Preserving packages.wazuh.com with placeholder...${NC}"
replace_in_files "packages.wazuh.com" "$PACKAGE_URL_PLACEHOLDER" "Preserve package URL"

# # Step 1_b: Replace libwazuhext.so with placeholder
# echo -e "\n${GREEN}Step 1_b: Preserving libwazuhext.so with placeholder...${NC}"
# replace_in_files "libwazuhext.so" "$LIB_PLACEHOLDER" "Preserve lib so"

# Step 2: Replace lowercase (order: wazuh- then wazuh_ then wazuh)
echo -e "\n${GREEN}Step 2: Replacing lowercase 'wazuh-' -> 'shieldnet-defend-'...${NC}"
replace_in_files "wazuh-" "shieldnet-defend-" "wazuh- replacement"
echo -e "\n${GREEN}Step 2b: Replacing lowercase 'wazuh_' -> 'shieldnet_defend_'...${NC}"
replace_in_files "wazuh_" "shieldnet_defend_" "wazuh_ replacement"
echo -e "\n${GREEN}Step 2c: Replacing lowercase '-wazuh' -> '-shieldnet-defend'...${NC}"
replace_in_files "\-wazuh" "-shieldnet-defend" "-wazuh replacement"
echo -e "\n${GREEN}Step 2d: Replacing lowercase '_wazuh' -> '_shieldnet_defend'...${NC}"
replace_in_files "_wazuh" "_shieldnet_defend" "_wazuh replacement"
echo -e "\n${GREEN}Step 2e: Replacing lowercase 'wazuh*' -> 'shieldnet*'...${NC}"
replace_in_files "wazuh\*" "shieldnet*" "wazuh* wildcard replacement"
echo -e "\n${GREEN}Step 2f: Replacing lowercase 'wazuh' -> 'shieldnetdefend'...${NC}"
replace_in_files "wazuh" "shieldnetdefend" "wazuh replacement"

# Step 3: Replace uppercase (order: WAZUH- then WAZUH_ then WAZUH)
echo -e "\n${GREEN}Step 3: Replacing 'WAZUH-' -> 'SHIELDNET-DEFEND-'...${NC}"
replace_in_files "WAZUH-" "SHIELDNET-DEFEND-" "WAZUH- replacement"
echo -e "\n${GREEN}Step 3b: Replacing 'WAZUH_' -> 'SHIELDNET_DEFEND_'...${NC}"
replace_in_files "WAZUH_" "SHIELDNET_DEFEND_" "WAZUH_ replacement"
echo -e "\n${GREEN}Step 3c: Replacing '-WAZUH' -> '-SHIELDNET-DEFEND'...${NC}"
replace_in_files "\-WAZUH" "-SHIELDNET-DEFEND" "-WAZUH replacement"
echo -e "\n${GREEN}Step 3d: Replacing '_WAZUH' -> '_SHIELDNET_DEFEND'...${NC}"
replace_in_files "_WAZUH" "_SHIELDNET_DEFEND" "_WAZUH replacement"
echo -e "\n${GREEN}Step 3e: Replacing 'WAZUH*' -> 'SHIELDNET*'...${NC}"
replace_in_files "WAZUH\*" "SHIELDNET*" "WAZUH* wildcard replacement"
echo -e "\n${GREEN}Step 3f: Replacing 'WAZUH' -> 'SHIELDNETDEFEND'...${NC}"
replace_in_files "WAZUH" "SHIELDNETDEFEND" "WAZUH replacement"

# Step 4: Replace capitalized (order: Wazuh- then Wazuh_ then Wazuh)
echo -e "\n${GREEN}Step 4: Replacing 'Wazuh-' -> 'Shieldnet-Defend-'...${NC}"
replace_in_files "Wazuh-" "Shieldnet-Defend-" "Wazuh- replacement"
echo -e "\n${GREEN}Step 4b: Replacing 'Wazuh_' -> 'Shieldnet_Defend_'...${NC}"
replace_in_files "Wazuh_" "Shieldnet_Defend_" "Wazuh_ replacement"
echo -e "\n${GREEN}Step 4c: Replacing '-Wazuh' -> '-Shieldnet-Defend'...${NC}"
replace_in_files "\-Wazuh" "-Shieldnet-Defend" "-Wazuh replacement"
echo -e "\n${GREEN}Step 4d: Replacing '_Wazuh' -> '_Shieldnet_Defend'...${NC}"
replace_in_files "_Wazuh" "_Shieldnet_Defend" "_Wazuh replacement"
echo -e "\n${GREEN}Step 4e: Replacing 'Wazuh*' -> 'Shieldnet*'...${NC}"
replace_in_files "Wazuh\*" "Shieldnet*" "Wazuh* wildcard replacement"
echo -e "\n${GREEN}Step 4f: Replacing 'Wazuh' -> 'ShieldnetDefend'...${NC}"
replace_in_files "Wazuh" "ShieldnetDefend" "Wazuh replacement"

# Step 5_a: Restore packages.wazuh.com from placeholder
echo -e "\n${GREEN}Step 5_a: Restoring packages.wazuh.com from placeholder...${NC}"
replace_in_files "$PACKAGE_URL_PLACEHOLDER" "packages.wazuh.com" "Restore package URL"

# # Step 5_b: Restore libwazuhext.so from placeholder
# echo -e "\n${GREEN}Step 5_b: Restoring libwazuhext.so from placeholder...${NC}"
# replace_in_files "$LIB_PLACEHOLDER" "libwazuhext.so" "Restore lib so"

# Step 6: Rename files with 'wazuh' in their name
echo -e "\n${GREEN}Step 6: Renaming files...${NC}"
rename_files

# Step 7: Rename directories with 'wazuh' in their name
echo -e "\n${GREEN}Step 7: Renaming directories...${NC}"
rename_directories

echo -e "\n${GREEN}White-label process completed!${NC}"
echo -e "${YELLOW}Please review the changes and test thoroughly.${NC}"
