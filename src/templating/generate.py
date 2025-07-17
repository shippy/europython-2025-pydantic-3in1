"""
Run:
    python generate.py
Results land in generated/api_models.py, domain.py, db_models.py, llm_schema.json
"""
from pathlib import Path
import json, yaml
from datamodel_code_generator import generate, InputFileType, DataModelType

ROOT     = Path(__file__).parent
SCHEMA   = ROOT / "schema" / "bagel_order.yaml"
OUTPUT   = ROOT / "generated"
TEMPLDIR = ROOT / "templates"

# 1) Pydantic DTOs (API) ------------------------------------------------------
generate(
    SCHEMA.read_text(),
    input_file_type=InputFileType.JsonSchema,
    output_model_type=DataModelType.PydanticV2BaseModel,
    output=OUTPUT / "api_models.py",
    custom_template_dir=TEMPLDIR / "pydantic",
)

# 2) Domain dataclass ---------------------------------------------------------
generate(
    SCHEMA.read_text(),
    input_file_type=InputFileType.JsonSchema,
    output_model_type=DataModelType.DataclassesDataclass,
    output=OUTPUT / "domain.py",
    custom_template_dir=TEMPLDIR / "dataclass",
)

# 3) SQLModel table -----------------------------------------------------------
generate(
    SCHEMA.read_text(),
    input_file_type=InputFileType.JsonSchema,
    output_model_type=DataModelType.PydanticV2BaseModel,  # we’re still hijacking BaseModel
    output=OUTPUT / "db_models.py",
    custom_template_dir=TEMPLDIR / "sqlmodel",
)

# 4) LLM schema with prompt-only descriptions --------------------------------
spec = yaml.safe_load(SCHEMA.read_text())
for prop in spec["properties"].values():
    if "x-llm-desc" in prop:
        prop["description"] = prop.pop("x-llm-desc")  # inject, drop original
(OUTPUT / "llm_schema.json").write_text(json.dumps(spec, indent=2))
print("Generated →", *OUTPUT.iterdir(), sep="\n  ")