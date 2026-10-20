"""csvsum - tiny command-line tool for summarising a numeric CSV column."""
import argparse
import csv
import statistics
import sys


def read_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def column_values(rows, column):
    return [float(row[column]) for row in rows]


def cmd_stats(args):
    rows = read_rows(args.file)
    values = column_values(rows, args.column)
    print(f"count: {len(values)}")
    print(f"sum: {sum(values)}")
    print(f"mean: {statistics.mean(values)}")
    print(f"median: {statistics.median(values)}")


def cmd_top(args):
    rows = read_rows(args.file)
    values = column_values(rows, args.column)
    label_key = list(rows[0].keys())[0]
    ranked = sorted(zip(values, (r[label_key] for r in rows)), reverse=True)
    for value, label in ranked[: args.n]:
        print(f"{value}  {label}")


def build_parser():
    parser = argparse.ArgumentParser(prog="csvsum", description="Summarise a numeric CSV column.")
    sub = parser.add_subparsers(dest="command", required=True)

    stats = sub.add_parser("stats", help="show count, sum, mean and median")
    stats.add_argument("file", help="path to the CSV file")
    stats.add_argument("column", help="name of the colum to summarise")
    stats.set_defaults(func=cmd_stats)

    top = sub.add_parser("top", help="show the highest values in a column")
    top.add_argument("file", help="path to the CSV file")
    top.add_argument("column", help="name of the column to rank")
    top.add_argument("--n", type=int, default=3, help="how many rows to show (default 3)")
    top.set_defaults(func=cmd_top)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        args.func(args)
    except FileNotFoundError as exc:
        print(f"csvsum: {exc.strerror}: {exc.filename}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
