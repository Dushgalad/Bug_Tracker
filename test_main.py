import Main as test


import json


def test_view_reports_empty(capsys):
    test.view_reports([])
    output = capsys.readouterr().out
    assert "No bugs reported yet." in output


def test_view_reports_with_bug(capsys):
    test.view_reports(
        [
            {
                "id": 1,
                "title": "asd",
                "description": "asd",
                "severity": "Critical",
                "status": "Resolved",
            }
        ]
    )
    output = capsys.readouterr().out
    assert "Title: asd" in output


def test_filter_reports_by_status(capsys):
    bugs = [
        {
            "id": 1,
            "title": "Crash",
            "description": "Game crashes when opening inventory",
            "severity": "Critical",
            "status": "Open",
        },
        {
            "id": 2,
            "title": "Texture",
            "description": "Character texture is missing",
            "severity": "Low",
            "status": "Resolved",
        },
    ]
    test.filtering_reports(bugs, "status", "Open")
    output = capsys.readouterr().out
    assert "Crash" in output
    assert "Texture" not in output


def test_filter_reports_by_severity(capsys):
    bugs = [
        {
            "id": 1,
            "title": "Crash",
            "description": "Game crashes when opening inventory",
            "severity": "Critical",
            "status": "Open",
        },
        {
            "id": 2,
            "title": "Texture",
            "description": "Character texture is missing",
            "severity": "Low",
            "status": "Resolved",
        },
    ]
    test.filtering_reports(bugs, "severity", "Critical")
    output = capsys.readouterr().out
    assert "Crash" in output
    assert "Texture" not in output


def test_filter_reports_by_id(capsys):
    bugs = [
        {
            "id": 1,
            "title": "Crash",
            "description": "Game crashes when opening inventory",
            "severity": "Critical",
            "status": "Open",
        },
        {
            "id": 2,
            "title": "Texture",
            "description": "Character texture is missing",
            "severity": "Low",
            "status": "Resolved",
        },
    ]
    test.filtering_reports(bugs, "id", 1)
    output = capsys.readouterr().out
    assert "Crash" in output
    assert "Texture" not in output


def test_filter_reports_no_matches(capsys):
    bugs = [
        {
            "id": 1,
            "title": "Crash",
            "description": "Game crashes when opening inventory",
            "severity": "Critical",
            "status": "Open",
        },
        {
            "id": 2,
            "title": "Texture",
            "description": "Character texture is missing",
            "severity": "Low",
            "status": "Resolved",
        },
    ]
    test.filtering_reports(bugs, "severity", "Medium")
    output = capsys.readouterr().out
    assert "No bugs match the selected filter." in output


def test_delete_bug_confirmed(monkeypatch):
    bugs = [
        {
            "id": 1,
            "title": "Crash",
            "description": "Game crashes when opening inventory",
            "severity": "Critical",
            "status": "Open",
        },
        {
            "id": 2,
            "title": "Texture",
            "description": "Character texture is missing",
            "severity": "Low",
            "status": "Resolved",
        },
    ]

    answers = iter(["1", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    result = test.delete_bug(bugs)
    assert result
    assert len(bugs) == 1
    assert bugs[0]["id"] == 2


def test_delete_bug_cancelled(monkeypatch):
    bugs = [
        {
            "id": 1,
            "title": "Crash",
            "description": "Game crashes when opening inventory",
            "severity": "Critical",
            "status": "Open",
        },
        {
            "id": 2,
            "title": "Texture",
            "description": "Character texture is missing",
            "severity": "Low",
            "status": "Resolved",
        },
    ]
    answers = iter(["1", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    result = test.delete_bug(bugs)
    assert result is False
    assert len(bugs) == 2


def test_delete_bug_empty():
    bugs = []
    result = test.delete_bug(bugs)
    assert result is False
    assert not bugs


def test_update_status_success(monkeypatch):
    bugs = [
        {
            "id": 1,
            "title": "Crash",
            "description": "Game crashes when opening inventory",
            "severity": "Critical",
            "status": "Open",
        },
        {
            "id": 2,
            "title": "Texture",
            "description": "Character texture is missing",
            "severity": "Low",
            "status": "Resolved",
        },
    ]
    answers = iter(["1", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    result = test.update_status(bugs)
    assert result
    assert bugs[0]["status"] == "In Progress"
    assert bugs[1]["status"] == "Resolved"


def test_update_status_empty():
    bugs = []
    result = test.update_status(bugs)
    assert result is False


def test_make_report(monkeypatch):
    bugs = []
    next_id = 1
    answers = iter(
        [
            "Character gets stuck after colliding with a wall",
            "After colliding with a wall, the character becomes stuck and can no longer move",
            "4",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    bug, next_id = test.make_report(next_id)
    assert bug["id"] == 1
    assert bug["severity"] == "Critical"
    assert bug["status"] == "Open"
    assert next_id == 2


def test_save_bugs(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    bugs = [
        {
            "id": 1,
            "title": "Crash",
            "description": "Game crashes when opening inventory",
            "severity": "Critical",
            "status": "Open",
        }
    ]
    next_id = 2
    result = test.save_bugs(bugs, next_id)
    assert result


def test_load_bugs(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    bugs = [
        {
            "id": 1,
            "title": "Crash",
            "description": "Game crashes when opening inventory",
            "severity": "Critical",
            "status": "Open",
        }
    ]
    result = test.save_bugs(bugs, 2)
    loaded_bugs, next_id = test.load_bugs()
    assert loaded_bugs == bugs
    assert next_id == 2
    assert result


def test_filter_invalid_severity(monkeypatch):
    answers = iter(["9", "4"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    selected_filter, selected_subfilter = test.get_filter_choice("2")
    assert selected_filter == "severity"
    assert selected_subfilter == "Critical"


def test_load_bugs_missing_key(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with open("bugs.json", "w") as file:
        json.dump({"bugs": []}, file)
    loaded_bugs, next_id = test.load_bugs()
    assert loaded_bugs is None
    assert next_id is None


def test_save_bugs_failure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    def fake_replace(source, destination):
        raise OSError("Simulated disk error")

    monkeypatch.setattr("os.replace", fake_replace)
    result = test.save_bugs([], 1)
    assert result is False


def test_load_bugs_invalid_structure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with open("bugs.json", "w") as file:
        json.dump(None, file)
    loaded_bug, next_id = test.load_bugs()
    assert loaded_bug is None
    assert next_id is None
