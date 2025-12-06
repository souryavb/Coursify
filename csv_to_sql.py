#!/usr/bin/env python3
import csv
import sys
from pathlib import Path

# Order to respect foreign keys
TABLE_ORDER = [
    "SystemSetting",
    "Term",
    "Department",
    "DegreePrograms",
    "Requirements",
    "Student",
    "Professor",
    "Course",
    "Section",
    "DataQualityIssue",
    "StudentPlan",
    "Rating",
    "Stu_degr",
    "Course_req",
    "Course_plan",
    "Scheduled_in",
    "Flag_course",
    "Flag_section",
    "Enrollment",
    "OverrideRequest",
]

ORDER_INDEX = {name: i for i, name in enumerate(TABLE_ORDER, start=2)}  # 02, 03, ...

def csv_to_insert(csv_path: Path, table: str, out_path: Path):
    print(f"Converting {csv_path.name} -> {out_path.name}")
    with csv_path.open(newline="", encoding="utf-8") as f_in, \
         out_path.open("w", encoding="utf-8") as f_out:

        reader = csv.DictReader(f_in)
        cols = reader.fieldnames
        if not cols:
            return

        # Simple comment header
        f_out.write(f"-- Inserts for {table} generated from {csv_path.name}\n")

        for row in reader:
            values_sql = []
            for c in cols:
                v = row[c]

                # Treat empty string as NULL
                if v is None or v == "":
                    values_sql.append("NULL")
                    continue

                # Don't try to be too clever: quote everything and let MySQL cast
                v_escaped = v.replace("\\", "\\\\").replace("'", "''")
                values_sql.append(f"'{v_escaped}'")

            col_list = ", ".join(f"`{c}`" for c in cols)
            val_list = ", ".join(values_sql)
            f_out.write(f"INSERT INTO `{table}` ({col_list}) VALUES ({val_list});\n")


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 csv_to_sql.py <csv_folder> <output_folder>")
        sys.exit(1)

    csv_folder = Path(sys.argv[1])
    out_folder = Path(sys.argv[2])

    if not csv_folder.is_dir():
        print(f"CSV folder not found: {csv_folder}")
        sys.exit(1)
    out_folder.mkdir(parents=True, exist_ok=True)

    # Get all CSVs and sort by our TABLE_ORDER
    csv_files = list(csv_folder.glob("*.csv"))

    def sort_key(p: Path):
        table = p.stem
        return ORDER_INDEX.get(table, 999)  # unknown tables go last

    for csv_path in sorted(csv_files, key=sort_key):
        table = csv_path.stem
        idx = ORDER_INDEX.get(table, 99)  # default 99 if not in list
        out_path = out_folder / f"{idx:02d}_insert_{table}.sql"
        csv_to_insert(csv_path, table, out_path)


if __name__ == "__main__":
    main()
