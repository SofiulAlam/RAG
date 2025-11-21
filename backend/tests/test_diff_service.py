import pytest
from app.services.diff_service import DiffService


def test_generate_file_diff():
    """Test generating diff for a single file"""
    service = DiffService()

    old_content = """def hello():
    print("Hello")
"""

    new_content = """def hello():
    print("Hello, World!")
"""

    diff = service.generate_file_diff(
        path="test.py",
        old_content=old_content,
        new_content=new_content
    )

    assert diff.path == "test.py"
    assert diff.additions > 0
    assert diff.deletions > 0
    assert "Hello, World!" in diff.diff


def test_detect_new_file():
    """Test detecting a new file"""
    service = DiffService()

    diff = service.generate_file_diff(
        path="new_file.py",
        old_content="",
        new_content="print('Hello')"
    )

    assert diff.is_new is True
    assert diff.is_deleted is False


def test_detect_deleted_file():
    """Test detecting a deleted file"""
    service = DiffService()

    diff = service.generate_file_diff(
        path="deleted.py",
        old_content="print('Goodbye')",
        new_content=""
    )

    assert diff.is_deleted is True
    assert diff.is_new is False


def test_generate_changeset():
    """Test generating a changeset"""
    service = DiffService()

    changes = {
        "file1.py": {
            "old": "old content",
            "new": "new content"
        },
        "file2.py": {
            "old": "",
            "new": "brand new file"
        }
    }

    changeset = service.generate_changeset(changes)

    assert len(changeset.files) == 2
    assert changeset.total_additions > 0
    assert "2 file" in changeset.summary


def test_validate_locked_files():
    """Test locked file validation"""
    service = DiffService()

    changes = {
        "unlocked.py": {"old": "old", "new": "new"},
        "locked.py": {"old": "old", "new": "modified"},
    }

    changeset = service.generate_changeset(changes)
    validation = service.validate_locked_files(
        changeset,
        locked_files=["locked.py"]
    )

    assert validation["valid"] is False
    assert "locked.py" in validation["violations"]


def test_apply_changeset():
    """Test applying a changeset"""
    service = DiffService()

    changes = {
        "file1.py": {"old": "old", "new": "new1"},
        "file2.py": {"old": "old", "new": "new2"},
        "file3.py": {"old": "old", "new": "new3"},
    }

    changeset = service.generate_changeset(changes)

    # Apply only selected files
    result = service.apply_changeset(
        changeset,
        selected_files=["file1.py", "file2.py"]
    )

    assert len(result) == 2
    assert "file1.py" in result
    assert "file2.py" in result
    assert "file3.py" not in result
