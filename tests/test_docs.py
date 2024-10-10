import os
import yaml
from checkers.collectors import CheckCollector


def test_checks_have_docs_page(config, checkers_root):
    collector = CheckCollector(config=config)

    # Collect builtin check names
    builtin_checks = collector.collect_builtin_checks()
    builtin_check_names = [f.__name__ for f in builtin_checks]

    # Collect doc site pages for each check
    doc_pages = os.listdir(os.path.join(checkers_root, "docs", "checks"))
    doc_page_names = [d.replace(".md", "") for d in doc_pages]
    doc_page_names.remove("_index")  # skip the index page

    # Collect site pages defined in mkdocs.yml
    site_pages = yaml.load(
        open(os.path.join(checkers_root, "mkdocs.yml"), "r"), Loader=yaml.SafeLoader
    )
    site_doc_pages = [
        list(v.values())[0] for v in site_pages["nav"][3]["Builtin Checks"]
    ]
    site_doc_page_names = [d.split("/")[-1].replace(".md", "") for d in site_doc_pages]
    site_doc_page_names.remove("_index")  # skip the index page

    # Check all builtin checks have a doc page
    assert list(sorted(builtin_check_names)) == list(sorted(doc_page_names)), list(
        sorted(doc_page_names)
    )

    # Check all builtin checks are specified in mkdocs.yml
    assert list(sorted(builtin_check_names)) == list(sorted(site_doc_page_names))
