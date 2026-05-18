#!/bin/bash

# Check if input file is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="${INPUT_FILE%.txt}.json"

# Initialize JSON
echo "{" > "$OUTPUT_FILE"

# Process each line
counter=0
while IFS= read -r line; do
    # Skip empty lines
    if [ -z "$line" ]; then
        continue
    fi
    
    # Extract requirement number and text
    if [[ "$line" =~ ^REQ-([0-9]+):[[:space:]]*(.*)$ ]]; then
        req_num="${BASH_REMATCH[1]}"
        req_text="${BASH_REMATCH[2]}"
        
        # Escape special characters for JSON
        req_text="${req_text//\\/\\\\}"  # Backslash
        req_text="${req_text//\"/\\\"}"  # Double quote
        req_text="${req_text//$'\n'/\\n}"  # Newlines (though not expected in single lines)
        
        # Add comma for all but first entry
        if [ $counter -gt 0 ]; then
            echo "," >> "$OUTPUT_FILE"
        fi
        
        # Write key-value pair
        printf "  \"REQ-%s\": \"%s\"" "$req_num" "$req_text" >> "$OUTPUT_FILE"
        
        ((counter++))
    fi
done < "$INPUT_FILE"

# Close JSON
echo "" >> "$OUTPUT_FILE"
echo "}" >> "$OUTPUT_FILE"

echo "Conversion complete! Output saved to: $OUTPUT_FILE"
echo "Total requirements processed: $counter"
