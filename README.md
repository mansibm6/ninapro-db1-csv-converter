# NinaPro DB1 CSV generator

Converts DB1 MAT files to one CSV containing ten EMG channels, 22 glove channels, and six metadata/label columns.

## Setup and execution

Use Python 3.11 and a separate virtual environment for this project. Run commands from this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python check_inputs.py
python ninapro_db1_to_csv_generator.py /path/to/mat-files --output Ninapro_DB1.csv
```

On Windows, activate with `.venv\Scripts\activate`. For notebooks, select this environment’s kernel and execute from the top in a fresh kernel. The first code cell exposes `INPUT_PATHS` where old machine-specific paths existed. `PROJECT_DATA_DIR` changes the base for those configured paths; remaining relative paths use the notebook working directory.

## Inputs

No fixed external dataset is required for the default entry point. See the notes below for bundled files or command-line input requirements.

## Outputs

Ninapro_DB1.csv, retaining the legacy CSV index column.

## Implementation and limitations

Supply a directory of .mat files on the command line. Required arrays: emg N×10, glove N×22, exercise, stimulus, restimulus, repetition, rerepetition, subject. Metadata may be scalar or contain exactly N samples. Misaligned/nonfinite arrays are rejected instead of silently truncated. Files are processed in sorted order.

## Verification

The workspace regression suite checks source/notebook validity and selected behavior with bundled or synthetic inputs. Full experiment training and historical metric reproduction are not implied. See the workspace `REFACTOR_REPORT.md` for exact test coverage and unresolved runtime requirements.

## Original authors

- [@mansibm6](https://www.github.com/mansibm6)

## Original references

These links were retained from the original project notes; availability and licensing must be checked by the person obtaining the data.

- https://www.github.com/mansibm6
- https://www.kaggle.com/datasets/mansibmursalin/ninapro-db1-full-dataset
