# UDI Grammar DICOM Workflow Demo

This project demonstrates a complete workflow for extracting DICOM metadata, generating UDI grammar specifications, and visualizing the results using the UDI grammar system. For a full demonstration, see the [workflow demo notebook](udi_grammar_workflow_demo.ipynb).

## Features
- Extracts metadata from DICOM (.dcm) files into a CSV with customizable columns
- Generates UDI grammar JSON specifications from the CSV using Python
- Renders UDI grammar specs to images automatically
- Provides a Jupyter notebook for an interactive, end-to-end demo
- Optionally, interact with the official UDI web editor directly from the notebook

## Requirements
- Python 3.8+
- See `requirements.txt` for all dependencies

## Installation
1. Clone this repository
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. (Optional) Install Playwright browsers:
   ```sh
   playwright install chromium
   ```

## Usage
### 1. Extract DICOM Metadata
Use the provided script or the Jupyter notebook to extract metadata from your DICOM files:
```python
from read_dicom_metadata import extract_usecase_columns
extract_usecase_columns('/path/to/dicom_dir', 'usecase_col.csv')
```

### 2. Generate UDI Grammar Spec
Use the notebook or `udi_grammar_usecase.py` to generate a UDI grammar JSON spec from the CSV.

### 3. Render UDI Spec to Image
Use the notebook or `udi_grammar_wrapper.py` to render the spec to a PNG image:
```python
from udi_grammar_wrapper import udi_to_png
import asyncio
asyncio.run(udi_to_png(spec, 'output.png'))
```

### 4. Interactive Jupyter Notebook
Open `udi_grammar_workflow_demo.ipynb` for a step-by-step, interactive workflow:
- Extract metadata
- Generate and view UDI spec
- Render and display the chart image
- Optionally, use the embedded UDI web editor for interactive exploration

### 5. UDI Web Editor (Optional)
You can also use the official UDI web editor directly from the notebook (see the last cell in the demo notebook) or at:
https://hms-dbmi.github.io/udi-grammar/#/Editor

## Project Structure
- `read_dicom_metadata.py` — Extracts DICOM metadata to CSV
- `udi_grammar_usecase.py` — Example: Generate UDI grammar spec from CSV
- `udi_grammar_wrapper.py` — Renders UDI grammar spec to PNG using Playwright
- `udi_grammar_workflow_demo.ipynb` — Jupyter notebook for the full workflow
- `requirements.txt` — All required Python dependencies
- `usecase_col.csv` — Example output CSV (generated)

## License
MIT License

## Acknowledgments
- [pydicom](https://pydicom.github.io/)
- [udi-grammar-py](https://github.com/hms-dbmi/udi-grammar-py)
- [UDI Grammar Web Editor](https://hms-dbmi.github.io/udi-grammar/#/Editor) 