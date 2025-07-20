# Quick start demo for udi-grammar-py
# pip install udi-grammar-py
from udi_grammar_py import Chart, Op

spec = (
    Chart()
    .source("samples", "./data/example_samples.csv")
    .groupby(["organ", "organ_condition"])
    .rollup({"count": Op.count()})
    .mark("bar")
    .x(field="organ", type="nominal")
    .y(field="count", type="quantitative")
    .color(field="organ_condition", type="nominal")
    .to_json(pretty=True)
)

print(spec) 