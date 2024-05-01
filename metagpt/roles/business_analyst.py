#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/25 18:00
@Author  : ed
@File    : business_analyst.py
@Modified By: 
"""

from metagpt.actions import UserRequirement, WritePRD, Action
from metagpt.actions.prepare_documents import PrepareDocuments
from metagpt.roles.role import Role
from metagpt.utils.common import any_to_name

from metagpt.schema import Message
from metagpt.const import MESSAGE_ROUTE_TO_NONE
from metagpt.logs import logger

from metagpt.actions.review_by_human1 import Human1ReviewReq
from metagpt.actions.analyse_business import AnalyseBusinessReq


class BA(Role):
    """
    Represents a Business Analyst role responsible for business requirements defination.

    Attributes:
        name (str): Name of the business analyst.
        profile (str): Role profile, default is 'Business Analyst'.
        goal (str): Goal of the business analyst.
        constraints (str): Constraints or limitations for the business analyst.
    """

    name: str = "Bala_BA"
    profile: str = "Business Analyst"
    goal: str = "Prepare business requirement document for mobile application development"
    constraints: str = "utilize the same language as the user requirements for seamless communication"
    todo_action: str = ""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.set_actions([AnalyseBusinessReq])
        # self._watch([UserRequirement, PrepareDocuments, HumanReviewReq])       # UserRequirement is action?, remove this statement -> same result? yes
        self._watch([UserRequirement, Human1ReviewReq]) 
        # self._watch([UserRequirement]) 
        

    async def _act(self) -> Message:
        print("XXXX")
        print(self.rc.history)
        subtask = await self.rc.todo.run(self.rc.history)
        # msg = Message(content=subtask, cause_by=AnalyseBusinessReq, send_to="<all>")
        msg = Message(content=subtask, cause_by=AnalyseBusinessReq)
        # self.rc.env.publish_message(msg)    # Human Agent subscribes to this type of message
        logger.info(f"Bala_BA publish_message: {msg}..")
        # return Message(content="dummy message", send_to=MESSAGE_ROUTE_TO_NONE, cause_by=AnalyseBusinessReq) # Since the messages have been sent, returning an empty message is sufficient.
        return msg

    # async def _think(self) -> bool:
    #     """Decide what to do"""
    #     if self.git_repo and not self.config.git_reinit:
    #         self._set_state(1)
    #     else:
    #         self._set_state(0)
    #         self.config.git_reinit = False
    #         self.todo_action = any_to_name(WritePRD)
    #     return bool(self.rc.todo)

    # async def _observe(self, ignore_memory=False) -> int:
    #     return await super()._observe(ignore_memory=True)


