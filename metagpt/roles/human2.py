#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/5/2 10:00
@Author  : ed
@File    : human2.py
@Modified By: 
"""

from metagpt.roles.role import Role
from metagpt.utils.common import any_to_name

from metagpt.schema import Message
from metagpt.const import MESSAGE_ROUTE_TO_NONE
from metagpt.logs import logger

from metagpt.actions.review_by_human2 import Human2ReviewReq
from metagpt.actions import WriteTasks

# from metagpt.roles import Engineer
from metagpt.roles import Engineer1
from metagpt.roles.project_manager1 import ProjectManager1 

class Human2(Role):
    """
    Represents a Human2 role responsible for reviewing Tasks output from ProjectManager1.

    Attributes:
        name (str): Name of the Human2.
        profile (str): Role profile, default is 'Human2'.
        goal (str): Goal of the human2
        constraints (str): Constraints or limitations for the human2.
    """

    name: str = "Hairy_Human2"
    profile: str = "Human2"
    goal: str = "review Tasks output from ProjectManager1"
    constraints: str = "utilize the same language as the user requirements for seamless communication"
    todo_action: str = ""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.set_actions([Human2ReviewReq])
        self._watch([WriteTasks])       
        


    async def _act(self) -> Message:
        (user_satisfaction, requirement) = await self.rc.todo.run(self.rc.history)
        print("RETURNED...")
        print(f"{user_satisfaction=}")
        print(f"{requirement=}")

        if user_satisfaction=="Satisfied":
            msg = Message(content=requirement, cause_by=Human2ReviewReq, send_to=Engineer1)
            self.rc.env.publish_message(msg)    # ProjectManager1 subscribes to this message
            logger.info(f"USER SATISIFED, Hairy_Human2 publish_message to Engineer1: {msg}..")

        elif user_satisfaction=="Not Satisfied":
            msg = Message(content=requirement, cause_by=Human2ReviewReq, send_to=ProjectManager1)
            self.rc.env.publish_message(msg)    # Engineer subscribes to this message
            logger.info(f"USER NOT SATISIFED, Hairy_Human2 publish_message to ProjectManager1: {msg}..")

        # logger.info(f"Hairy_Human2 publish_message: {msg}..")

        return Message(content="dummy message", cause_by=Human2ReviewReq, send_to=MESSAGE_ROUTE_TO_NONE) # Since the messages have been sent, returning an empty message.


