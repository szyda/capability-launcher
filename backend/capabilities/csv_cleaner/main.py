import csv
import io


def run(inputs: dict) -> dict:
    raw_csv = inputs.get('csv', '')
    rows = list(csv.reader(io.StringIO(raw_csv)))

    cleaned_rows = []
    seen = set()
    removed_blank_rows = 0
    for row in rows:
        if not row or all(cell.strip() == '' for cell in row):
            removed_blank_rows += 1
            continue

        normalized = [cell.strip() for cell in row]
        key = tuple(normalized)
        if key in seen:
            continue
        seen.add(key)
        cleaned_rows.append(normalized)

    if not cleaned_rows:
        return {'rows': 0, 'columns': [], 'cleaned_rows': [], 'removed_blank_rows': removed_blank_rows, 'duplicate_rows_removed': 0}

    columns = cleaned_rows[0]
    return {
        'rows': len(cleaned_rows) - 1,
        'columns': columns,
        'cleaned_rows': cleaned_rows[1:],
        'removed_blank_rows': removed_blank_rows,
        'duplicate_rows_removed': len(rows) - len(cleaned_rows) - removed_blank_rows,
    }
