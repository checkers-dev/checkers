import re
from pathlib import Path
from py_markdown_table.markdown_table import markdown_table
from checkers.collectors import CheckCollector
from checkers.config import load_config


index_page_path = Path("docs/checks/_index.md")


def build_table():
    config = load_config()
    collector = CheckCollector(config=config)
    checks = collector.collect()
    check_data = list()
    for c in checks:
        check_name = c.check.__name__
        description = c.check.__doc__.strip()
        default_enabled = c.enabled
        if default_enabled:
            icon = "✅"
        else:
            icon = "❌"
        link = f'<a href="/docs/checks/{check_name}">Link</a>'
        check_data.append(
            {
                "Check Name": check_name,
                "Description": description,
                "Default Enabled": icon,
                "Details": link,
            }
        )
    table = markdown_table(check_data)
    table.set_params(row_sep="markdown", quote=False)
    result = table.get_markdown()
    return result


def inject_table(table: str):
    index_page = index_page_path.read_text()
    start_chars = "<!-- BEGIN_INDEX_PAGE_TABLE -->"
    end_chars = "<!-- END_INDEX_PAGE_TABLE -->"
    start_index = index_page.index(start_chars)
    end_index = index_page.rindex(end_chars) + len(end_chars)
    current_table = index_page[start_index:end_index]
    res = index_page.replace(
        current_table, start_chars + "\n" + table + "\n" + end_chars
    )
    print(res)
    index_page_path.write_text(res)


def main():
    assert index_page_path.exists(), f"No index page found at {index_page_path}"
    mdtable = build_table()
    inject_table(mdtable)


if __name__ == "__main__":
    main()
