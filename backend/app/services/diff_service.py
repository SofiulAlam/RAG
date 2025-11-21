from typing import List, Dict, Optional
from difflib import unified_diff
from pydantic import BaseModel


class FileDiff(BaseModel):
    """Represents a diff for a single file"""
    path: str
    old_content: str
    new_content: str
    diff: str
    additions: int
    deletions: int
    is_new: bool = False
    is_deleted: bool = False


class ChangeSet(BaseModel):
    """Represents a set of changes across multiple files"""
    files: List[FileDiff]
    total_additions: int
    total_deletions: int
    summary: str


class DiffService:
    """Service for generating and managing code diffs"""

    def generate_file_diff(
        self,
        path: str,
        old_content: str,
        new_content: str,
    ) -> FileDiff:
        """Generate diff for a single file"""
        # Generate unified diff
        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)

        diff_lines = list(unified_diff(
            old_lines,
            new_lines,
            fromfile=f"a/{path}",
            tofile=f"b/{path}",
            lineterm=""
        ))

        diff_text = "".join(diff_lines)

        # Count additions and deletions
        additions = sum(1 for line in diff_lines if line.startswith('+') and not line.startswith('+++'))
        deletions = sum(1 for line in diff_lines if line.startswith('-') and not line.startswith('---'))

        # Determine if file is new or deleted
        is_new = old_content == ""
        is_deleted = new_content == ""

        return FileDiff(
            path=path,
            old_content=old_content,
            new_content=new_content,
            diff=diff_text,
            additions=additions,
            deletions=deletions,
            is_new=is_new,
            is_deleted=is_deleted,
        )

    def generate_changeset(
        self,
        changes: Dict[str, Dict[str, str]],
    ) -> ChangeSet:
        """
        Generate a changeset from multiple file changes

        Args:
            changes: Dict mapping file paths to {"old": old_content, "new": new_content}
        """
        file_diffs = []
        total_additions = 0
        total_deletions = 0

        for path, content in changes.items():
            file_diff = self.generate_file_diff(
                path=path,
                old_content=content.get("old", ""),
                new_content=content.get("new", ""),
            )
            file_diffs.append(file_diff)
            total_additions += file_diff.additions
            total_deletions += file_diff.deletions

        # Generate summary
        file_count = len(file_diffs)
        new_files = sum(1 for f in file_diffs if f.is_new)
        deleted_files = sum(1 for f in file_diffs if f.is_deleted)
        modified_files = file_count - new_files - deleted_files

        summary_parts = []
        if new_files:
            summary_parts.append(f"{new_files} new")
        if modified_files:
            summary_parts.append(f"{modified_files} modified")
        if deleted_files:
            summary_parts.append(f"{deleted_files} deleted")

        summary = (
            f"{file_count} file{'s' if file_count != 1 else ''} changed "
            f"({', '.join(summary_parts)}), "
            f"+{total_additions}, -{total_deletions}"
        )

        return ChangeSet(
            files=file_diffs,
            total_additions=total_additions,
            total_deletions=total_deletions,
            summary=summary,
        )

    def apply_changeset(
        self,
        changeset: ChangeSet,
        selected_files: Optional[List[str]] = None,
    ) -> Dict[str, str]:
        """
        Apply a changeset, optionally filtering by selected files

        Returns a dict mapping file paths to new content
        """
        result = {}

        for file_diff in changeset.files:
            # Skip if file not selected
            if selected_files is not None and file_diff.path not in selected_files:
                continue

            # Skip deleted files
            if not file_diff.is_deleted:
                result[file_diff.path] = file_diff.new_content

        return result

    def validate_locked_files(
        self,
        changeset: ChangeSet,
        locked_files: List[str],
    ) -> Dict[str, List[str]]:
        """
        Validate that no locked files are being modified

        Returns dict with "valid" and "violations" lists
        """
        violations = []

        for file_diff in changeset.files:
            if file_diff.path in locked_files and not file_diff.is_new:
                violations.append(file_diff.path)

        return {
            "valid": len(violations) == 0,
            "violations": violations,
        }
