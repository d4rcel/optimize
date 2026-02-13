# Image Optimization Tools

This collection of scripts helps you resize and organize images based on a CSV file.

## Setup

1.  Ensure you have Python 3 installed.
2.  Install the required library:
    ```bash
    pip install Pillow
    ```
3.  Place your source images in the `UP` folder.

## How to Run

To run the entire optimization process with a new CSV file:

1.  Place your new CSV file in this directory (e.g., `my_new_file.csv`).
2.  Run the master script:

    ```bash
    ./run_optimize.sh my_new_file.csv
    ```

### What happens?

The script performs three steps:
1.  **Resizes Images**: Reads the CSV and resizes images marked for resizing.
2.  **Consolidates Images**: Copies all other images from `UP` to `NEWUP` (searching for them if moved/renamed).
3.  **Generates Report**: Creates `final_images_paths.csv` listing all available images in `NEWUP`.

## Manual execution (Optional)

You can also run the scripts individually:

```bash
python3 process_images.py <filename.csv>
python3 copy_remaining_images.py <filename.csv>
python3 generate_final_csv.py <filename.csv>
```

If no filename is provided, they default to `optimisation_images_titabymtn.csv`.
