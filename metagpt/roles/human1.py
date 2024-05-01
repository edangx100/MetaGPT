#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/25 14:43
@Author  : ed
@File    : human1.py
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

from metagpt.roles import BA
from metagpt.roles.product_manager1 import ProductManager1       # from metagpt.roles? circular import issue?


# class Human1ReviewReq(Action):
#     PROMPT_TEMPLATE: str = """
#     Context: {requirement}
#     Tasks components ok? Can alter:
#     """
#     name: str = "HumanReviewReq"

#     async def run(self, requirement: str):
#         prompt = self.PROMPT_TEMPLATE.format(requirement=requirement)
#         rsp = await self._aask(prompt)
#         # ROUTER based on rsp?

#         # updated_rsp = requirement[0].content + '\n' + rsp
#         """
#         Context: [Human: Build a web-based field sales management application for field sales representatives. 
#         It allows users to log in securely, browse and purchase products, manage customer information, and generate reports. Only use vanilla html, css and javascript to code., user: {
#         "ProjectDescription": "Developing a web-based field sales management application for field sales representatives using vanilla HTML, CSS, and JavaScript, with Dynamics 365 Business Central as the backend.",
#         """
#         updated_rsp = requirement[1].content + '\n' + rsp
#         print(f"Human1 response: {updated_rsp}")

#         # test semantic route
#         print( rl("I want to make a sales app") )
#         # print( rl({updated_rsp}) )
#         return updated_rsp



class Human1(Role):
    """
    Represents a Human role responsible for reviewing Business Requirements output from BA.

    Attributes:
        name (str): Name of the Human1.
        profile (str): Role profile, default is 'Human1'.
        goal (str): Goal of the human1
        constraints (str): Constraints or limitations for the human.
    """

    name: str = "Hungry_Human1"
    profile: str = "Human1"
    goal: str = "review Business Requirements output from Business Analyst"
    constraints: str = "utilize the same language as the user requirements for seamless communication"
    todo_action: str = ""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.set_actions([Human1ReviewReq])
        self._watch([AnalyseBusinessReq])       
        


    async def _act(self) -> Message:
        (user_satisfaction, requirement) = await self.rc.todo.run(self.rc.history)
        print("RETURNED...")
        print(f"{user_satisfaction=}")
        print(f"{requirement=}")

        if user_satisfaction=="Satisfied":
            msg = Message(content=requirement, cause_by=Human1ReviewReq, send_to=ProductManager1)
            self.rc.env.publish_message(msg)    # ProductManager1 subscribes to this message
            logger.info(f"USER SATISIFED, Hungry_Human1 publish_message to ProductManager1: {msg}..")

        elif user_satisfaction=="Not Satisfied":
            msg = Message(content=requirement, cause_by=Human1ReviewReq, send_to=BA)
            self.rc.env.publish_message(msg)    # Business Analyst subscribes to this message
            logger.info(f"USER NOT SATISIFED, Hungry_Human1 publish_message to Business Analyst: {msg}..")

        # self.rc.env.publish_message(msg)    # Human Agent subscribes to this message
        # logger.info(f"Hungry_Human1 publish_message: {msg}..")

        return Message(content="dummy message", cause_by=Human1ReviewReq, send_to=MESSAGE_ROUTE_TO_NONE) # Since the messages have been sent, returning an empty message.


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
