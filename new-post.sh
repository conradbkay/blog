#!/bin/bash

# Check if title argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 \"Article Title\""
    echo "Example: $0 \"My New Blog Post\""
    exit 1
fi

# Get the title from arguments
TITLE="$1"

# Convert title to folder name: lowercase and replace spaces with dashes
FOLDER_NAME=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-\|-$//g')

# Get current date in YYYY-MM-DD format
CURRENT_DATE=$(date +"%Y-%m-%d")

# Create the folder
mkdir -p "drafts/$FOLDER_NAME"

# Create the index.qmd file
cat > "drafts/$FOLDER_NAME/index.qmd" << EOF
---
title: "$TITLE"
author: "Conrad Kay"
date: "$CURRENT_DATE"
draft: true
echo: false
format: "html"
categories: []
---

EOF

echo "Created new post: drafts/$FOLDER_NAME/index.qmd"
echo "Title: $TITLE"
echo "Date: $CURRENT_DATE" 