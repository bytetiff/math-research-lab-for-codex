import pytest

from math_research_lab.script_cli import main


def test_build_notation_table_rejects_invalid_json_file(tmp_path):
    invalid = tmp_path / "symbols.json"
    invalid.write_text("{not json", encoding="utf-8")

    with pytest.raises(ValueError):
        main("build_notation_table", [str(invalid)])
