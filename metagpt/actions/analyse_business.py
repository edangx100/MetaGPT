#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/26 17:46
@Author  : ed
@File    : analyse_business.py
"""
from metagpt.actions import Action


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
    I need a business requirement document for my web application designed for following description between triple backticks:
    ```{instruction}```

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
