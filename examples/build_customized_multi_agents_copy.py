"""
Filename: MetaGPT/examples/build_customized_multi_agents.py
Created Date: Wednesday, November 15th 2023, 7:12:39 pm
Author: garylin2099
"""
import asyncio
import re
import json

import fire

from metagpt.actions import Action, UserRequirement
from metagpt.logs import logger
from metagpt.roles import Role, BA, Human1, ProductManager1
from metagpt.schema import Message
from metagpt.team import Team
from metagpt.roles.business_analyst import AnalyseBusinessReq
from metagpt.roles.human1 import Human1ReviewReq

################################################
# import os
# # os.environ["OPENAI_API_KEY"]=''
# os.environ["AZURE_OPENAI_API_KEY"]=''
# os.environ["AZURE_OPENAI_ENDPOINT"]=''
# api_version="2023-05-15"

# from semantic_router import Route
# from semantic_router import RouteLayer
# from semantic_router.encoders import HuggingFaceEncoder, OpenAIEncoder
# from semantic_router.llms import AzureOpenAILLM

# def routes_setup():
#     field_sales_route = Route(
#         name="field_sales",
#         utterances=[
#             "I want to build an application to automate my sales processes,",
#             "I want to build an app to automate my sales processes,",
#             "I want to a mobile web application that provide real time updates on prices and stocks",
#             "I want to make an app that help to effortlessly manage cash collection",
#             "I want to develop a field sales mobile app",
#         ],
#     )
#     delivery_route = Route(
#         name="delivery",
#         utterances=[
#             "I want to build a mobile app for ERP that facilitates order management with delivery of items to the last mile",
#             "I want to develop an app that provide pre-assigned routes, drivers, customer priority and schedules enables a paperless order fulfilment with ability to collect payment through different payment methods",
#             "I want to develop an application that automate end-to-end Logistic processes with the Last Mile Delivery Mobile Application"
#             "I want to develop a delivery mobile app",
#         ],
#     )
#     others_route = Route(
#         name="others",
#         utterances=[
#             "I want to make a mobile app",
#             "I want to develop an app",
#         ],
#     )
#     routes = [field_sales_route, delivery_route, others_route]
#     # encoder = OpenAIEncoder()
#     encoder = HuggingFaceEncoder()

#     return routes, encoder

# llm = AzureOpenAILLM(
#   name = "gpt-35-turbo-0125",
#   openai_api_key = os.getenv("AZURE_OPENAI_API_KEY"),
#   azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
#   api_version = "2023-05-15",
# )
# routes, encoder = routes_setup()
# # rl = RouteLayer(encoder=encoder, routes=routes)
# rl = RouteLayer(encoder=encoder, routes=routes, llm=llm)
################################################


# class HumanReviewReq(Action):
#     PROMPT_TEMPLATE: str = """
#     Context: {requirement}
#     Tasks components ok? Can alter:
#     """
#     name: str = "HumanReviewReq"

#     async def run(self, requirement: str):
#         prompt = self.PROMPT_TEMPLATE.format(requirement=requirement)
#         rsp = await self._aask(prompt)
#         # ROUTER based onm rsp?

#         updated_rsp = requirement[0].content + '\n' + rsp
#         print(f"Human1 response: {updated_rsp}")

#         # test semantic route
#         print( rl("I want to make a sales app") )
#         # print( rl({updated_rsp}) )
#         return updated_rsp

# class Human1(Role):
#     name: str = "Hungry_Human"
#     profile: str = "Human1"

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self._watch([AnalyseBusinessReq])       
#         self.set_actions([Human1ReviewReq])




################################################

def parse_code(rsp):
    pattern = r"```python(.*)```"
    match = re.search(pattern, rsp, re.DOTALL)
    code_text = match.group(1) if match else rsp
    return code_text


class SimpleWriteCode(Action):
    PROMPT_TEMPLATE: str = """
    Write a python function that can {instruction}.
    Return ```python your_code_here ``` with NO other texts,
    your code:
    """
    name: str = "SimpleWriteCode"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)
        rsp = await self._aask(prompt)
        code_text = parse_code(rsp)
        return code_text


class SimpleCoder(Role):
    name: str = "Alice"
    profile: str = "SimpleCoder"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self._watch([UserRequirement])       # UserRequirement is action?
        # self._watch([Human1ReviewReq, AnalyseBusinessReq])
        self._watch([Human1ReviewReq])    
        self.set_actions([SimpleWriteCode])


class SimpleWriteTest(Action):
    PROMPT_TEMPLATE: str = """
    Context: {context}
    Write {k} unit tests using pytest for the given function, assuming you have imported it.
    Return ```python your_code_here ``` with NO other texts,
    your code:
    """

    name: str = "SimpleWriteTest"

    async def run(self, context: str, k: int = 3):
        prompt = self.PROMPT_TEMPLATE.format(context=context, k=k)

        rsp = await self._aask(prompt)

        code_text = parse_code(rsp)

        return code_text


class SimpleTester(Role):
    name: str = "Bob"
    profile: str = "SimpleTester"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([SimpleWriteTest])
        # self._watch([SimpleWriteCode])
        self._watch([SimpleWriteCode, SimpleWriteReview])  # feel free to try this too

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo

        # context = self.get_memories(k=1)[0].content # use the most recent memory as context
        context = self.get_memories()  # use all memories as context

        code_text = await todo.run(context, k=5)  # specify arguments
        msg = Message(content=code_text, role=self.profile, cause_by=type(todo))

        return msg


class SimpleWriteReview(Action):
    PROMPT_TEMPLATE: str = """
    Context: {context}
    Review the test cases and provide one critical comments:
    """

    name: str = "SimpleWriteReview"

    async def run(self, context: str):
        prompt = self.PROMPT_TEMPLATE.format(context=context)
        rsp = await self._aask(prompt)

        return rsp


class SimpleReviewer(Role):
    name: str = "Charlie"
    profile: str = "SimpleReviewer"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([SimpleWriteReview])
        self._watch([SimpleWriteTest])


##################################################################################

async def main(
    # idea: str = "write a function that calculates the product of a list",
    # The application is a web-based sales management system for field sales representatives. Only use vanilla html, css and javascript to code. It allows users to log in securely, browse and purchase products, manage customer information, and generate reports.
    idea: str = "",
    investment: float = 3.0,
    n_round: int = 5,
    add_human1: bool = True,
    add_human2: bool = False,
):
    # BA_role = BA(is_human=add_human1)
    # idea = await BA_role.run()    # need to 'watch' something for approach to work

    idea = input("Please Input your requirements for webpage:\n")
    logger.info(idea)

    team = Team()
    team.hire(
        [
            BA(),
            Human1(is_human=add_human1),
            ProductManager1(),
            # SimpleCoder(),
            # SimpleTester(),
            # SimpleReviewer(is_human=add_human2),
        ]
    )

    team.invest(investment=investment)
    team.run_project(idea)
    await team.run(n_round=n_round)


if __name__ == "__main__":
    fire.Fire(main)
    
    # # Create an event loop and run the main coroutine
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
