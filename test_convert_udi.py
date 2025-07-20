from pathlib import Path
import json

from convert_udi import udi_to_image

spec = {
    "source": {"name": "donors", "source": "./data/example_donors.csv"},
    "representation": {
        "mark": "point",
        "mapping": [
            {"encoding": "y", "field": "height", "type": "quantitative"},
            {"encoding": "x", "field": "weight", "type": "quantitative"},
            {"encoding": "size", "field": "age", "type": "quantitative"},
        ],
    },
}

udi_to_image(spec, "donors.png",debug=True)   # → PNG file beside the script