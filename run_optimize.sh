#!/bin/bash

# Check if a CSV file is provided
if [ -z "$1" ]; then
  echo "Usage: ./run_optimize.sh <path_to_csv_file>"
  echo "Example: ./run_optimize.sh my_images.csv"
  exit 1
fi

CSV_FILE="$1"

# Check if the CSV file exists
if [ ! -f "$CSV_FILE" ]; then
    echo "Error: File '$CSV_FILE' not found!"
    exit 1
fi

echo "=========================================="
echo "Starting Image Optimization Workflow"
echo "Using CSV: $CSV_FILE"
echo "=========================================="

echo "[1/3] Resizing images (process_images.py)..."
python3 process_images.py "$CSV_FILE"
if [ $? -ne 0 ]; then
    echo "Error running process_images.py"
    exit 1
fi

echo "[2/3] Copying remaining images (copy_remaining_images.py)..."
python3 copy_remaining_images.py "$CSV_FILE"
if [ $? -ne 0 ]; then
    echo "Error running copy_remaining_images.py"
    exit 1
fi

echo "[3/3] Generating final CSV (generate_final_csv.py)..."
python3 generate_final_csv.py "$CSV_FILE"
if [ $? -ne 0 ]; then
    echo "Error running generate_final_csv.py"
    exit 1
fi

echo "=========================================="
echo "Optimization Complete!"
echo "Check the 'NEWUP' folder and 'final_images_paths.csv'."
echo "=========================================="
