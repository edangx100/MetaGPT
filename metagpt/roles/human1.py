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

from metagpt.roles.business_analyst import AnalyseBusinessReq

################################################
import os


from semantic_router import Route
from semantic_router import RouteLayer
from semantic_router.encoders import HuggingFaceEncoder, OpenAIEncoder
from semantic_router.llms import AzureOpenAILLM

def routes_setup():
    field_sales_route = Route(
        name="field_sales",
        utterances=[
            "I want to build an application to automate my sales processes,",
            "I want to build an app to automate my sales processes,",
            "I want to a mobile web application that provide real time updates on prices and stocks",
            "I want to make an app that help to effortlessly manage cash collection",
            "I want to develop a field sales mobile app",
        ],
    )
    delivery_route = Route(
        name="delivery",
        utterances=[
            "I want to build a mobile app for ERP that facilitates order management with delivery of items to the last mile",
            "I want to develop an app that provide pre-assigned routes, drivers, customer priority and schedules enables a paperless order fulfilment with ability to collect payment through different payment methods",
            "I want to develop an application that automate end-to-end Logistic processes with the Last Mile Delivery Mobile Application"
            "I want to develop a delivery mobile app",
        ],
    )
    others_route = Route(
        name="others",
        utterances=[
            "I want to make a mobile app",
            "I want to develop an app",
        ],
    )
    routes = [field_sales_route, delivery_route, others_route]
    # encoder = OpenAIEncoder()
    encoder = HuggingFaceEncoder()

    return routes, encoder

llm = AzureOpenAILLM(
  name = "gpt-35-turbo-0125",
  openai_api_key = os.getenv("AZURE_OPENAI_API_KEY"),
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
  api_version = "2023-05-15",
)
routes, encoder = routes_setup()
# rl = RouteLayer(encoder=encoder, routes=routes)
rl = RouteLayer(encoder=encoder, routes=routes, llm=llm)
################################################

class Human1ReviewReq(Action):
    PROMPT_TEMPLATE: str = """
    Context: {requirement}
    Tasks components ok? Can alter:
    """
    name: str = "HumanReviewReq"

    async def run(self, requirement: str):
        prompt = self.PROMPT_TEMPLATE.format(requirement=requirement)
        rsp = await self._aask(prompt)
        # ROUTER based on rsp?

        updated_rsp = requirement[0].content + '\n' + rsp
        print(f"Human1 response: {updated_rsp}")

        # test semantic route
        print( rl("I want to make a sales app") )
        # print( rl({updated_rsp}) )
        return updated_rsp

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
        self._watch([AnalyseBusinessReq])       
        self.set_actions([Human1ReviewReq])

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
