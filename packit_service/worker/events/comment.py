# Copyright Contributors to the Packit project.
# SPDX-License-Identifier: MIT

"""
abstract-comment event classes.
"""
from logging import getLogger
from typing import Dict, Optional, Set

from ogr.abstract import Comment
from packit_service.service.db_triggers import (
    AddIssueDbTrigger,
    AddPullRequestDbTrigger,
)
from packit_service.worker.events.event import AbstractForgeIndependentEvent

logger = getLogger(__name__)


class AbstractCommentEvent(AbstractForgeIndependentEvent):
    def __init__(
        self,
        project_url: str,
        comment: str,
        comment_id: int,
        pr_id: Optional[int] = None,
        comment_object: Optional[Comment] = None,
    ) -> None:
        super().__init__(project_url=project_url, pr_id=pr_id)
        self.comment = comment
        self.comment_id = comment_id

        # Lazy properties
        self._comment_object = comment_object

    @property
    def comment_object(self) -> Optional[Comment]:
        raise NotImplementedError("Use subclass instead.")

    def get_dict(self, default_dict: Optional[Dict] = None) -> dict:
        result = super().get_dict()
        result.pop("_comment_object")
        return result


class AbstractPRCommentEvent(AddPullRequestDbTrigger, AbstractCommentEvent):
    def __init__(
        self,
        pr_id: int,
        project_url: str,
        comment: str,
        comment_id: int,
        commit_sha: str = "",
        comment_object: Optional[Comment] = None,
        targets_override: Optional[Set[str]] = None,
    ) -> None:
        super().__init__(
            pr_id=pr_id,
            project_url=project_url,
            comment=comment,
            comment_id=comment_id,
            comment_object=comment_object,
        )

        # Lazy properties
        self._commit_sha = commit_sha
        self._comment_object = comment_object
        self._targets_override = targets_override

    @property
    def commit_sha(self) -> str:  # type:ignore
        # mypy does not like properties
        if not self._commit_sha:
            self._commit_sha = self.project.get_pr(pr_id=self.pr_id).head_commit
        return self._commit_sha

    @property
    def comment_object(self) -> Optional[Comment]:
        if not self._comment_object:
            self._comment_object = self.project.get_pr(self.pr_id).get_comment(
                self.comment_id
            )
        return self._comment_object

    @property
    def targets_override(self) -> Optional[Set[str]]:
        if not self._targets_override:
            self._targets_override = self._get_all_failed_targets_in_pr()

        return self._targets_override

    def _get_all_failed_targets_in_pr(self) -> Optional[Set[str]]:
        targets_found: Optional[Set[str]] = None
        if "rebuild-failed" in self.comment:
            targets_found = super().get_all_build_failed_targets()
        elif "retest-failed" in self.comment:
            targets_found = super().get_all_tf_failed_targets()

        return targets_found if targets_found else None

    def get_dict(self, default_dict: Optional[Dict] = None) -> dict:
        result = super().get_dict()
        result["commit_sha"] = self.commit_sha
        result.pop("_targets_override")
        return result


class AbstractIssueCommentEvent(AddIssueDbTrigger, AbstractCommentEvent):
    def __init__(
        self,
        issue_id: int,
        repo_namespace: str,
        repo_name: str,
        project_url: str,
        comment: str,
        comment_id: int,
        tag_name: str = "",
        comment_object: Optional[Comment] = None,
    ) -> None:
        super().__init__(
            project_url=project_url,
            comment=comment,
            comment_id=comment_id,
            comment_object=comment_object,
        )
        self.issue_id = issue_id
        self.repo_namespace = repo_namespace
        self.repo_name = repo_name

        # Lazy properties
        self._tag_name = tag_name
        self._comment_object = comment_object

    @property
    def tag_name(self):
        if not self._tag_name:
            self._tag_name = ""
            if latest_release := self.project.get_latest_release():
                self._tag_name = latest_release.tag_name
        return self._tag_name

    @property
    def commit_sha(self):
        return self.tag_name

    @property
    def comment_object(self) -> Optional[Comment]:
        if not self._comment_object:
            self._comment_object = self.project.get_issue(self.issue_id).get_comment(
                self.comment_id
            )
        return self._comment_object

    def get_dict(self, default_dict: Optional[Dict] = None) -> dict:
        result = super().get_dict()
        result["tag_name"] = self.tag_name
        result["issue_id"] = self.issue_id
        return result
