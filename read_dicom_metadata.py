import os
import csv
import pydicom

# Directory containing DICOM files
DICOM_DIR = '/Users/chunwei/research/midrc-demo/downloads'
OUTPUT_CSV = 'dicom_metadata.csv'

def extract_dicom_metadata(directory, output_csv, max_files=None):
    # Get all .dcm files
    all_files = [f for f in os.listdir(directory) if f.lower().endswith('.dcm')]
    selected_files = all_files if max_files is None else all_files[:max_files]

    metadata_list = []
    all_keys = set()

    # Read metadata from each file
    for filename in selected_files:
        filepath = os.path.join(directory, filename)
        try:
            ds = pydicom.dcmread(filepath, stop_before_pixels=True)
            meta = {elem.keyword: elem.value for elem in ds.iterall() if elem.keyword}
            meta['__filename'] = filename
            metadata_list.append(meta)
            all_keys.update(meta.keys())
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    # Ensure __filename is the first column
    all_keys = sorted(k for k in all_keys if k != '__filename')
    fieldnames = ['__filename'] + all_keys

    # Write to CSV
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for meta in metadata_list:
            writer.writerow({k: meta.get(k, '') for k in fieldnames})

    print(f"Wrote metadata for {len(metadata_list)} DICOM files to {output_csv}")
    return output_csv

def extract_selected_dicom_metadata(directory, output_csv, attributes, max_files=None):
    """
    Extract only selected attributes from DICOM files and write to CSV.
    attributes: list of DICOM attribute keywords (e.g., ['PatientID', 'Modality'])
    """
    all_files = [f for f in os.listdir(directory) if f.lower().endswith('.dcm')]
    selected_files = all_files if max_files is None else all_files[:max_files]

    metadata_list = []
    for filename in selected_files:
        filepath = os.path.join(directory, filename)
        try:
            ds = pydicom.dcmread(filepath, stop_before_pixels=True)
            meta = {'__filename': filename}
            for attr in attributes:
                meta[attr] = getattr(ds, attr, '')
            metadata_list.append(meta)
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    fieldnames = ['__filename'] + list(attributes)
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for meta in metadata_list:
            writer.writerow({k: meta.get(k, '') for k in fieldnames})

    print(f"Wrote selected metadata for {len(metadata_list)} DICOM files to {output_csv}")
    return output_csv

def extract_usecase_columns(directory, output_csv='usecase_col.csv', max_files=None):
    usecase_attributes = [
        'PatientID', 'PatientName', 'PatientSex', 'PatientAge', 'PatientBirthDate',
        'StudyDate', 'StudyTime', 'StudyDescription', 'StudyInstanceUID',
        'SeriesDescription', 'SeriesNumber', 'SeriesInstanceUID',
        'Modality', 'Manufacturer', 'ManufacturerModelName', 'BodyPartExamined',
        'ProtocolName', 'AcquisitionDate', 'AcquisitionTime',
        'ImageType', 'InstanceNumber', 'Rows', 'Columns', 'PixelSpacing',
        'SliceThickness', 'PhotometricInterpretation', 'ReferringPhysicianName',
        'AccessionNumber', 'InstitutionName', 'SoftwareVersions'
    ]
    return extract_selected_dicom_metadata(directory, output_csv, usecase_attributes, max_files)

if __name__ == "__main__":
    # Full metadata extraction
    csv_path = extract_dicom_metadata(DICOM_DIR, OUTPUT_CSV)
    print("\nPreview of CSV file:")
    with open(csv_path, 'r') as f:
        for i, line in enumerate(f):
            print(line.strip())
            if i > 20:
                print("... (truncated)")
                break

    # Selected attributes extraction
    selected_attributes = ['PatientID', 'Modality', 'StudyDate', 'PatientSex']
    selected_csv = 'selected_metadata.csv'
    csv_path2 = extract_selected_dicom_metadata(DICOM_DIR, selected_csv, selected_attributes)
    print(f"\nPreview of {selected_csv}:")
    with open(csv_path2, 'r') as f:
        for i, line in enumerate(f):
            print(line.strip())
            if i > 20:
                print("... (truncated)")
                break

    # Usecase columns extraction
    usecase_csv = 'usecase_col.csv'
    csv_path3 = extract_usecase_columns(DICOM_DIR, usecase_csv)
    print(f"\nPreview of {usecase_csv}:")
    with open(csv_path3, 'r') as f:
        for i, line in enumerate(f):
            print(line.strip())
            if i > 20:
                print("... (truncated)")
                break 