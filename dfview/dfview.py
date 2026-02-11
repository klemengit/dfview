import webbrowser
import tempfile

import pandas as pd


def show(df, max_rows=None, open_browser=True):
    """Show a pandas DataFrame in a browser.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to display.
    max_rows : int, optional
        Maximum number of rows to display. If None, all rows are shown.
    open_browser : bool, optional
        If True (default), open the HTML in the default browser.

    Returns
    -------
    str
        The generated HTML string.
    """
    total_rows = df.shape[0]
    if max_rows:
        df = df.head(max_rows)

    html = _build_html(df, total_rows)

    if open_browser:
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html") as f:
            f.write(html)
            webbrowser.open(f.name)

    return html


def _build_html(df, total_rows):
    """Build the full HTML page for the DataFrame."""
    n_rows, n_cols = df.shape
    table_html = df.to_html()

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
    body {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        padding: 20px;
        background: #f8f9fa;
    }}
    .info {{ color: #666; font-size: 13px; margin-bottom: 10px; }}
    table {{
        border-collapse: collapse;
        background: white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        font-size: 13px;
        table-layout: fixed;
    }}
    thead th {{
        background: #f7f7f9;
        position: sticky;
        top: 0;
        z-index: 2;
        font-weight: 600;
        border-bottom: 2px solid #dee2e6;
        overflow: hidden;
        min-width: 60px;
        max-width: 300px;
        position: relative;
        cursor: pointer;
        user-select: none;
    }}
    thead th .sort-arrow {{
        font-size: 10px;
        margin-left: 4px;
        color: #999;
    }}
    thead th .sort-arrow.active {{
        color: #333;
    }}
    .filter-btn {{
        display: inline-block;
        background: none;
        border: 1px solid transparent;
        border-radius: 3px;
        cursor: pointer;
        font-size: 10px;
        color: #999;
        padding: 1px 4px;
        margin-left: 2px;
        vertical-align: middle;
    }}
    .filter-btn:hover {{
        color: #333;
        background: #e0e0e0;
    }}
    .filter-btn.active {{
        color: #4a90d9;
        font-weight: bold;
    }}
    .filter-dropdown {{
        position: absolute;
        min-width: 180px;
        max-width: 300px;
        background: white;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 100;
        padding: 8px;
        text-align: left;
        font-weight: normal;
        cursor: default;
    }}
    .filter-dropdown input[type="text"] {{
        width: 100%;
        box-sizing: border-box;
        padding: 4px 6px;
        border: 1px solid #ccc;
        border-radius: 3px;
        font-size: 12px;
        margin-bottom: 6px;
    }}
    .filter-dropdown input[type="text"]:focus {{
        outline: none;
        border-color: #4a90d9;
    }}
    .filter-dropdown .checkbox-list {{
        max-height: 200px;
        overflow-y: auto;
        border: 1px solid #eee;
        border-radius: 3px;
        padding: 2px 0;
    }}
    .filter-dropdown label {{
        display: block;
        padding: 3px 6px;
        font-size: 12px;
        cursor: pointer;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}
    .filter-dropdown label:hover {{
        background: #f0f4ff;
    }}
    .filter-dropdown label.select-all {{
        border-bottom: 1px solid #eee;
        margin-bottom: 2px;
        font-weight: 600;
    }}
    .resize-handle {{
        position: absolute;
        right: 0;
        top: 0;
        bottom: 0;
        width: 5px;
        cursor: col-resize;
        background: transparent;
    }}
    .resize-handle:hover,
    .resize-handle.active {{
        background: #4a90d9;
    }}
    th, td {{
        padding: 8px 14px;
        border: 1px solid #e9ecef;
        text-align: right;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 300px;
    }}
    td {{
        cursor: pointer;
    }}
    td.expanded {{
        white-space: normal;
        word-break: break-word;
        background: #fffde7;
    }}
    th:first-child, td:first-child {{
        text-align: left;
        font-weight: 500;
        background: #fafafa;
    }}
    td:first-child.expanded {{
        background: #fffde7;
    }}
    tbody tr:nth-child(even) {{ background: #f8f9fa; }}
    tbody tr:hover {{ background: #e8f4fe; }}
</style></head><body>
    <div class="info" id="info">{n_rows} rows &times; {n_cols} columns</div>
    {table_html}
    <script>
    (function() {{
        const table = document.querySelector('table');
        const thead = table.querySelector('thead');
        const tbody = table.querySelector('tbody');
        const headerRow = thead.querySelector('tr');
        const headers = headerRow.querySelectorAll('th');
        const totalRows = {total_rows};
        const shownRows = {n_rows};
        const numCols = {n_cols};
        const infoEl = document.getElementById('info');

        // Store original order
        const rows = Array.from(tbody.querySelectorAll('tr'));
        rows.forEach((row, i) => row.dataset.origIndex = i);

        // --- Sort state ---
        // 0 = original, 1 = ascending, 2 = descending
        let sortCol = -1;
        let sortDir = 0;

        function parseValue(text) {{
            const num = Number(text);
            return isNaN(num) ? text.toLowerCase() : num;
        }}

        function sortTable(colIdx, direction) {{
            const sorted = [...rows];
            if (direction === 0) {{
                sorted.sort((a, b) => a.dataset.origIndex - b.dataset.origIndex);
            }} else {{
                sorted.sort((a, b) => {{
                    const aVal = parseValue(a.children[colIdx].textContent.trim());
                    const bVal = parseValue(b.children[colIdx].textContent.trim());
                    if (aVal < bVal) return direction === 1 ? -1 : 1;
                    if (aVal > bVal) return direction === 1 ? 1 : -1;
                    return 0;
                }});
            }}
            sorted.forEach(row => tbody.appendChild(row));
            applyFilters();
        }}

        function updateSortArrows() {{
            headers.forEach((th, i) => {{
                const arrow = th.querySelector('.sort-arrow');
                if (!arrow) return;
                if (i === sortCol && sortDir === 1) {{
                    arrow.textContent = ' \\u25B2';
                    arrow.classList.add('active');
                }} else if (i === sortCol && sortDir === 2) {{
                    arrow.textContent = ' \\u25BC';
                    arrow.classList.add('active');
                }} else {{
                    arrow.textContent = '';
                    arrow.classList.remove('active');
                }}
            }});
        }}

        // --- Filter state: per-column set of checked values ---
        const colFilters = [];  // colFilters[i] = Set of checked values (null = all)
        let openDropdown = null; // currently open dropdown element
        let openDropdownCol = -1; // column index of open dropdown

        function getUniqueValues(colIdx) {{
            const vals = new Set();
            rows.forEach(row => {{
                vals.add(row.children[colIdx].textContent.trim());
            }});
            return Array.from(vals).sort((a, b) => {{
                const na = Number(a), nb = Number(b);
                if (!isNaN(na) && !isNaN(nb)) return na - nb;
                return a.localeCompare(b);
            }});
        }}

        function closeDropdown() {{
            if (openDropdown) {{
                openDropdown.remove();
                openDropdown = null;
                openDropdownCol = -1;
            }}
        }}

        function openFilterDropdown(colIdx, th) {{
            closeDropdown();
            const allValues = getUniqueValues(colIdx);

            const dd = document.createElement('div');
            dd.className = 'filter-dropdown';

            // Search input
            const search = document.createElement('input');
            search.type = 'text';
            search.placeholder = 'Search...';
            dd.appendChild(search);

            // Select All
            const selectAllLabel = document.createElement('label');
            selectAllLabel.className = 'select-all';
            const selectAllCb = document.createElement('input');
            selectAllCb.type = 'checkbox';
            selectAllCb.checked = colFilters[colIdx] === null;
            selectAllLabel.appendChild(selectAllCb);
            selectAllLabel.appendChild(document.createTextNode(' Select All'));
            dd.appendChild(selectAllLabel);

            // Checkbox list
            const listDiv = document.createElement('div');
            listDiv.className = 'checkbox-list';
            dd.appendChild(listDiv);

            function renderList(filter) {{
                listDiv.innerHTML = '';
                const cur = colFilters[colIdx];
                const filtered = filter
                    ? allValues.filter(v => v.toLowerCase().includes(filter.toLowerCase()))
                    : allValues;
                filtered.forEach(val => {{
                    const lbl = document.createElement('label');
                    const cb = document.createElement('input');
                    cb.type = 'checkbox';
                    cb.value = val;
                    cb.checked = cur === null || cur.has(val);
                    cb.addEventListener('change', () => {{
                        updateCheckedFromList(colIdx, allValues);
                    }});
                    lbl.appendChild(cb);
                    lbl.appendChild(document.createTextNode(' ' + val));
                    listDiv.appendChild(lbl);
                }});
                // Update Select All state
                const boxes = listDiv.querySelectorAll('input[type=checkbox]');
                const allChecked = Array.from(boxes).every(b => b.checked);
                selectAllCb.checked = allChecked;
            }}

            function updateCheckedFromList(ci, allVals) {{
                const boxes = listDiv.querySelectorAll('input[type=checkbox]');
                const checkedVals = new Set();
                boxes.forEach(b => {{ if (b.checked) checkedVals.add(b.value); }});
                // Also keep values not currently visible in the search that were checked
                const visibleVals = new Set(Array.from(boxes).map(b => b.value));
                if (colFilters[ci] !== null) {{
                    colFilters[ci].forEach(v => {{
                        if (!visibleVals.has(v)) checkedVals.add(v);
                    }});
                }} else {{
                    allVals.forEach(v => {{
                        if (!visibleVals.has(v)) checkedVals.add(v);
                    }});
                }}
                colFilters[ci] = checkedVals.size === allVals.length ? null : checkedVals;
                updateFilterBtn(ci);
                applyFilters();
                // Update Select All
                const allChecked = Array.from(boxes).every(b => b.checked);
                selectAllCb.checked = allChecked;
            }}

            selectAllCb.addEventListener('change', () => {{
                const boxes = listDiv.querySelectorAll('input[type=checkbox]');
                boxes.forEach(b => {{ b.checked = selectAllCb.checked; }});
                updateCheckedFromList(colIdx, allValues);
            }});

            search.addEventListener('input', () => {{
                renderList(search.value);
            }});

            renderList('');
            document.body.appendChild(dd);
            const rect = th.getBoundingClientRect();
            dd.style.left = rect.left + window.scrollX + 'px';
            dd.style.top = rect.bottom + window.scrollY + 'px';
            openDropdown = dd;
            openDropdownCol = colIdx;
            search.focus();

            // Prevent clicks inside dropdown from triggering sort
            dd.addEventListener('click', e => e.stopPropagation());
            dd.addEventListener('mousedown', e => e.stopPropagation());
        }}

        function updateFilterBtn(colIdx) {{
            const btn = headers[colIdx].querySelector('.filter-btn');
            if (!btn) return;
            if (colFilters[colIdx] === null) {{
                btn.classList.remove('active');
            }} else {{
                btn.classList.add('active');
            }}
        }}

        // Add sort arrows, filter buttons, and click handlers to headers
        headers.forEach((th, i) => {{
            colFilters.push(null); // null = all values selected

            const arrow = document.createElement('span');
            arrow.className = 'sort-arrow';
            th.appendChild(arrow);

            // Filter button
            const filterBtn = document.createElement('span');
            filterBtn.className = 'filter-btn';
            filterBtn.textContent = '\\u25BC';
            filterBtn.title = 'Filter';
            filterBtn.addEventListener('click', (e) => {{
                e.stopPropagation();
                if (openDropdown && openDropdownCol === i) {{
                    closeDropdown();
                }} else {{
                    openFilterDropdown(i, th);
                }}
            }});
            th.appendChild(filterBtn);

            // Add resize handle
            const handle = document.createElement('div');
            handle.className = 'resize-handle';
            th.appendChild(handle);

            th.addEventListener('click', (e) => {{
                if (e.target.classList.contains('resize-handle')) return;
                if (e.target.classList.contains('filter-btn')) return;
                if (sortCol === i) {{
                    sortDir = (sortDir + 1) % 3;
                }} else {{
                    sortCol = i;
                    sortDir = 1;
                }}
                updateSortArrows();
                sortTable(i, sortDir);
            }});

            // Column resize
            let startX, startW;
            handle.addEventListener('mousedown', e => {{
                e.preventDefault();
                e.stopPropagation();
                startX = e.pageX;
                startW = th.offsetWidth;
                handle.classList.add('active');

                const onMouseMove = e => {{
                    const newWidth = Math.max(60, startW + e.pageX - startX);
                    th.style.width = newWidth + 'px';
                    th.style.maxWidth = newWidth + 'px';
                    const idx = th.cellIndex;
                    document.querySelectorAll(`tbody td:nth-child(${{idx + 1}})`).forEach(td => {{
                        td.style.width = newWidth + 'px';
                        td.style.maxWidth = newWidth + 'px';
                    }});
                }};

                const onMouseUp = () => {{
                    handle.classList.remove('active');
                    document.removeEventListener('mousemove', onMouseMove);
                    document.removeEventListener('mouseup', onMouseUp);
                }};

                document.addEventListener('mousemove', onMouseMove);
                document.addEventListener('mouseup', onMouseUp);
            }});
        }});

        // Close dropdown on outside click or Escape
        document.addEventListener('click', (e) => {{
            if (openDropdown && !openDropdown.contains(e.target) && !e.target.classList.contains('filter-btn')) {{
                closeDropdown();
            }}
        }});
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') closeDropdown();
        }});

        function applyFilters() {{
            let visibleCount = 0;
            const currentRows = Array.from(tbody.querySelectorAll('tr'));

            currentRows.forEach(row => {{
                const cells = row.children;
                let match = true;
                for (let i = 0; i < cells.length; i++) {{
                    if (colFilters[i] !== null && !colFilters[i].has(cells[i].textContent.trim())) {{
                        match = false;
                        break;
                    }}
                }}
                row.style.display = match ? '' : 'none';
                if (match) visibleCount++;
            }});

            if (visibleCount === shownRows) {{
                infoEl.textContent = shownRows + ' rows \\u00D7 ' + numCols + ' columns';
            }} else {{
                infoEl.textContent = 'Showing ' + visibleCount + ' of ' + shownRows + ' rows \\u00D7 ' + numCols + ' columns';
            }}
        }}

        // --- Cell expand on click ---
        document.querySelectorAll('tbody td').forEach(td => {{
            td.addEventListener('click', e => {{
                e.stopPropagation();
                const wasExpanded = td.classList.contains('expanded');
                document.querySelectorAll('td.expanded').forEach(el => el.classList.remove('expanded'));
                if (!wasExpanded) td.classList.add('expanded');
            }});
        }});
        document.addEventListener('click', () => {{
            document.querySelectorAll('td.expanded').forEach(el => el.classList.remove('expanded'));
        }});
    }})();
    </script>
</body></html>"""
