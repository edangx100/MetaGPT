#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/29 14:43
@Author  : ed
@File    : product_manager1.py
@Modified By: 
"""

from metagpt.actions import UserRequirement, WritePRD1
from metagpt.actions.prepare_documents import PrepareDocuments
from metagpt.roles.role import Role
from metagpt.utils.common import any_to_name

# from metagpt.roles.human1 import Human1ReviewReq
from metagpt.actions.review_by_human1 import Human1ReviewReq


class ProductManager1(Role):
    """
    Represents a Product Manager role responsible for product development and management.

    Attributes:
        name (str): Name of the product manager.
        profile (str): Role profile, default is 'Product Manager'.
        goal (str): Goal of the product manager.
        constraints (str): Constraints or limitations for the product manager.
    """

    name: str = "Alice"
    profile: str = "Product Manager1"
    goal: str = "efficiently create a successful product that meets market demands and user expectations"
    constraints: str = "utilize the same language as the user requirements for seamless communication"
    todo_action: str = ""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.set_actions([PrepareDocuments, WritePRD1])
        self._watch([Human1ReviewReq, PrepareDocuments])
        self.todo_action = any_to_name(PrepareDocuments)

    async def _think(self) -> bool:
        """Decide what to do"""
        if self.git_repo and not self.config.git_reinit:
            self._set_state(1)
        else:
            self._set_state(0)
            self.config.git_reinit = False
            self.todo_action = any_to_name(WritePRD1)
        return bool(self.rc.todo)

    async def _observe(self, ignore_memory=False) -> int:
        return await super()._observe(ignore_memory=True)


    # async def _act(self) -> Message:
    #     subtask = await self.rc.todo.run(self.rc.history)
    #     msg = Message(content=subtask, cause_by=WritePRD1)
    #     logger.info(f"Alice publish_message: {msg}..")
    #     return msg
