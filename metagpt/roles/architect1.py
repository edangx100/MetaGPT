#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/5/2 14:43
@Author  : ed
@File    : architect1.py
"""

from metagpt.actions import WritePRD, WritePRD1
from metagpt.actions.design_api import WriteDesign
from metagpt.roles.role import Role


class Architect1(Role):
    """
    Represents an Architect role in a software development process.

    Attributes:
        name (str): Name of the architect.
        profile (str): Role profile, default is 'Architect1'.
        goal (str): Primary goal or responsibility of the architect1.
        constraints (str): Constraints or guidelines for the architect1.
    """

    name: str = "Bob"
    profile: str = "Architect1"
    goal: str = "design a concise, usable, complete software system"
    constraints: str = (
        "make sure the architecture is simple enough and use  appropriate open source "
        "libraries. Use same language as user requirement"
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Initialize actions specific to the Architect1 role
        self.set_actions([WriteDesign])

        # Set events or actions the Architect1 should watch or be aware of
        self._watch({WritePRD1})
