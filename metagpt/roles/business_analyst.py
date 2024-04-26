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

################################################

# class AnalyseBusinessReq(Action):
#     PROMPT_TEMPLATE: str = """
#     You are a Business Analyst now. 
#     Break the following requirements in component tasks {instruction}.
#     Respond in bullet points
#     """
#     name: str = "AnalyseBusinessReq"

#     async def run(self, instruction: str):
#         prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)
#         rsp = await self._aask(prompt)
#         return rsp

class AnalyseBusinessReq(Action):

    PROMPT_TEMPLATE: str = """
    You are a Business Analyst now. 
    I need a business requirement document for my App designed for following description between triple backticks:
    ```{instruction}```
    This app has Dynamics 365 Business Central (BC365) as backend.

    Suggest the business requirement for the app. 
    Arrange it such that it is easy for me to modify the business logic for any part if it is wrong. 
    Be as detailed as possible.

    Response in JSON format like following:
    {json_eg}
    """
    name: str = "AnalyseBusinessReq"

    async def run(self, instruction: str):
        jsonstring = """{
            "ProjectDescription": "Developing a comprehensive field sales application to streamline sales processes and enhance efficiency for field sales representatives.",
            "BusinessRequirements": {
                "BR1": "The application should allow field sales representatives to view and manage their assigned leads, contacts, and accounts.",
                "BR2": "Integration with the company's CRM system to synchronize data in real-time and ensure consistency across platforms."
            },
            "UserStories": {
                "US1": "As a field sales representative, I want to be able to easily access and update lead information while on the go.",
                "US2": "As a sales manager, I want to view real-time updates on my team's activities and performance."
            },
            "UserJourney": {
                "UJ1": "Field sales representative logs into the application using their credentials and accesses their dashboard.",
                "UJ2": "The representative views their assigned leads and selects a lead to update its status and details."
            }
        }"""
        clean_jsonstring = jsonstring.replace('\\n', ' ')
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction, json_eg=clean_jsonstring)
        rsp = await self._aask(prompt)
        return rsp


# class BA(Role):
#     name: str = "Bala_BA"
#     profile: str = "Business Analyst"

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self._watch([UserRequirement, HumanReviewReq])       # UserRequirement is action?, remove this statement -> same result? yes
#         # self._watch([UserRequirement,]) 
#         self.set_actions([AnalyseBusinessReq])

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

        # self.set_actions([AnalyseBusinessReq, PrepareDocuments, WritePRD])
        self.set_actions([AnalyseBusinessReq])
        # self._watch([UserRequirement, PrepareDocuments, HumanReviewReq])       # UserRequirement is action?, remove this statement -> same result? yes
        self._watch([UserRequirement]) 
        
        # self.todo_action = any_to_name(PrepareDocuments)    # ?

    async def _act(self) -> Message:
        subtask = await self.rc.todo.run(self.rc.history)
        self.rc.env.publish_message(Message(content=subtask, cause_by=AnalyseBusinessReq)) # Human Agent subscribes to this type of message
        return Message(content="dummy message", send_to=MESSAGE_ROUTE_TO_NONE) # Since the messages have been sent, returning an empty message is sufficient.


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


