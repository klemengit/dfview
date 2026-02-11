import pandas as pd

import dfview


def test_version():
    assert dfview.__version__ == "0.1.0"


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
    test_version()
    test_import()
    test_show_returns_html()
    test_show_contains_data()
    test_show_max_rows()
    test_show_has_filter_dropdowns()
    test_show_has_sort_arrows()
