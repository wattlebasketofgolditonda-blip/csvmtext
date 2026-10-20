import csvsum


def write_csv(tmp_path, text):
    path = tmp_path / "data.csv"
    path.write_text(text, encoding="utf-8")
    return str(path)


def test_stats_basic(tmp_path, capsys):
    path = write_csv(tmp_path, "name,amount\na,10\nb,20\nc,30\n")
    csvsum.main(["stats", path, "amount"])
    out = capsys.readouterr().out
    assert "count: 3" in out
    assert "sum: 60.0" in out
    assert "median: 20.0" in out


def test_top_orders_highest_first(tmp_path, capsys):
    path = write_csv(tmp_path, "name,amount\na,10\nb,30\nc,20\n")
    csvsum.main(["top", path, "amount", "--n", "2"])
    lines = capsys.readouterr().out.strip().splitlines()
    assert lines == ["30.0  b", "20.0  c"]


def test_stats_missing_file_prints_one_line_error_and_exits_1(tmp_path, capsys):
    missing = str(tmp_path / "nothing.csv")
    try:
        csvsum.main(["stats", missing, "amount"])
    except SystemExit as exc:
        assert exc.code == 1
    else:
        raise AssertionError("missing file should exit non-zero")
    err = capsys.readouterr().err
    assert err.startswith("csvsum:")
    assert "nothing.csv" in err
    assert "Traceback" not in err


def test_top_missing_file_also_exits_cleanly(tmp_path, capsys):
    missing = str(tmp_path / "nothing.csv")
    try:
        csvsum.main(["top", missing, "amount"])
    except SystemExit as exc:
        assert exc.code == 1
    err = capsys.readouterr().err
    assert err.startswith("csvsum:")
