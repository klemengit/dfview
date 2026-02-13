import os
import pandas as pd
import tempfile

import dfview



def test_import():
    import dfview

    assert True


def test_show_returns_html():
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    html = dfview.show(df, open_browser=False)
    assert "<table" in html
    assert "<thead" in html
    assert "<tbody" in html


def test_show_contains_data():
    df = pd.DataFrame({"col1": [10, 20], "col2": ["hello", "world"]})
    html = dfview.show(df, open_browser=False)
    assert "col1" in html
    assert "col2" in html
    assert "hello" in html
    assert "world" in html

def test_utf8():
    df = pd.DataFrame({"col1": [10, 20], "col2": ["živjo", "\u010d"]})
    html = dfview.show(df, open_browser=False)


    _temp_files = []
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html", encoding="utf-8") as f:
        f.write(html)
        _temp_files.append(f.name)


    for path in _temp_files:
        try:
            os.unlink(path)
        except OSError:
            pass
    _temp_files.clear()


def test_show_max_rows():
    df = pd.DataFrame({"a": range(100)})
    html = dfview.show(df, max_rows=5, open_browser=False)
    assert "5 rows" in html


def test_show_has_filter_dropdowns():
    df = pd.DataFrame({"a": [1], "b": [2]})
    html = dfview.show(df, open_browser=False)
    assert "filter-dropdown" in html
    assert "filter-btn" in html


def test_show_has_sort_arrows():
    df = pd.DataFrame({"a": [1], "b": [2]})
    html = dfview.show(df, open_browser=False)
    assert "sort-arrow" in html


if __name__ == "__main__":
    test_import()
    test_show_returns_html()
    test_show_contains_data()
    test_show_max_rows()
    test_show_has_filter_dropdowns()
    test_show_has_sort_arrows()
