# Data Quality Assessment and Visualization Tool

This repository contains tools for analyzing, visualizing, and processing insurance data for quality assessment purposes.

## Repository Structure

- `requirements.txt` - Python dependencies
- `src` - Source code directory

## Source Code Files

### `src/visualization.py`

Creates comprehensive visualizations for data quality assessment including:

- Data completeness analysis
- Insurance provider distribution
- Postal code distribution
- Gender distribution
- Age distribution
- Insurance type analysis
- Franchise value distribution

The script generates an interactive HTML report (`QA_visualization.html`) with meaningful insights for each visualization.

### `src/split.py`

Splits the main dataset by postal code into separate CSV files using multiprocessing for efficiency, storing results in the `splitted_dataset` directory.

### `src/manifest.py`

Generates a manifest file (`manifest.txt`) that contains information about each postal code group including:

- Unique dates of birth
- Total unique dates of birth
- Total records per postal code

## Setup and Usage

1. Install required dependencies:

```bash
pip install -r requirements.txt
```

2. Generate the data quality visualization:

```bash
python src/visualization.py
```

3. Split the dataset by postal code:

```bash
python src/split.py
```

4. Generate the manifest file:

```bash
python src/manifest.py
```

## Technologies Used

- Python 3
- Pandas for data manipulation
- Plotly for interactive visualizations
- NumPy for numerical operations

## Output Files

- `QA_visualization.html`: Interactive data quality assessment report with visualizations
- `manifest.txt`: Summary of dataset metrics by postal code
- `splitted_dataset/*.csv`: Individual datasets for each
