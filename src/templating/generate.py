from pathlib import Path
from datamodel_code_generator import InputFileType, generate
from datamodel_code_generator.model import pydantic as _dummy  # noqa: F401

SCHEMA = Path("schema/bagel_order.yaml")
OUT    = Path("generated")
GEN_TMP = Path("jinja-templates")

OUT.mkdir(exist_ok=True)
# --- API models ---
generate(
    input=SCHEMA.as_posix(),
    input_file_type=InputFileType.JsonSchema,
    output=(OUT / "api_models.py").as_posix(),
    custom_template_dir=GEN_TMP.as_posix(),
    template="io_models.py.jinja2",
)
# --- SQLModel table ---
generate(
    input=SCHEMA.as_posix(),
    input_file_type=InputFileType.JsonSchema,
    output=(OUT / "db_models.py").as_posix(),
    custom_template_dir=GEN_TMP.as_posix(),
    template="sqlmodel.py.jinja2",
)
# --- JSON schema for LLMs (verbatim copy) ---
(OUT / "llm_schema.json").write_bytes(SCHEMA.read_bytes())
print("Generated:", *OUT.iterdir(), sep="\n  ")
