#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/5/2 15:04
@Author  : ed
@File    : project_manager1.py
"""

from metagpt.actions import WriteTasks
from metagpt.actions.design_api import WriteDesign
from metagpt.roles.role import Role

from metagpt.actions.review_by_human2 import Human2ReviewReq


class ProjectManager1(Role):
    """
    Represents a Project Manager1 role responsible for overseeing project execution and team efficiency.

    Attributes:
        name (str): Name of the project manager1.
        profile (str): Role profile, default is 'Project Manager1'.
        goal (str): Goal of the project manager1.
        constraints (str): Constraints or limitations for the project manager1.
    """

    name: str = "Eve"
    profile: str = "Project Manager1"
    goal: str = (
        "break down tasks according to PRD/technical design, generate a task list, and analyze task "
        "dependencies to start with the prerequisite modules"
    )
    constraints: str = "use same language as user requirement"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.set_actions([WriteTasks])
        self._watch([WriteDesign, Human2ReviewReq])
