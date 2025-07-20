from udi_grammar_py.spec import Chart
from udi_grammar_py.helpers import Op
import json

# This is a example of how to use the udi-grammar-py library to create a chart.

# Build most of the spec with udi-grammar-py
def usecase1_chart():
    chart = (
        Chart()
        .source("dicom", "https://neural-science.s3.us-east-1.amazonaws.com/usecase_col.csv")
        .groupby(["PatientAge", "Modality", "PatientSex"])
        .rollup('count', count=Op.count())
        .mark("bar")
        .x(field="PatientAge", type="nominal")
        .y(field="count", type="quantitative")
        .color(field="PatientSex", type="nominal")
    )

    # Convert to dict and patch the rollup
    spec = chart.to_dict()
    for t in spec["transformation"]:
        if "rollup" in t and isinstance(t["rollup"], str):
            t["rollup"] = {"count": {"op": "count"}}

    # Add column encoding manually for faceting by Modality
    spec["representation"]["mapping"].append({
        "encoding": "column",
        "field": "Modality",
        "type": "nominal"
    })

    print(json.dumps(spec, indent=2)) 


def usecase2_chart():
    # Example: Studies by StudyDate and Modality, colored by Manufacturer
    chart = (
        Chart()
        .source("dicom", "https://neural-science.s3.us-east-1.amazonaws.com/usecase_col.csv")
        .groupby(["StudyDate", "Modality", "Manufacturer"])
        .rollup('count', count=Op.count())
        .mark("bar")
        .x(field="StudyDate", type="nominal")
        .y(field="count", type="quantitative")
        .color(field="Manufacturer", type="nominal")
    )

    spec = chart.to_dict()
    for t in spec["transformation"]:
        if "rollup" in t and isinstance(t["rollup"], str):
            t["rollup"] = {"count": {"op": "count"}}

    print(json.dumps(spec, indent=2)) 

    spec = chart.to_dict()
    for t in spec["transformation"]:
        if "rollup" in t and isinstance(t["rollup"], str):
            t["rollup"] = {"count": {"op": "count"}}

    print(json.dumps(spec, indent=2))

if __name__ == "__main__":
    usecase1_chart()