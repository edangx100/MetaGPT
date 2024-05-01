#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/26 17:46
@Author  : ed
@File    : review_by_human1.py
"""
from metagpt.actions import Action
from metagpt.logs import logger
# from metagpt.schema import Message
# from metagpt.const import MESSAGE_ROUTE_TO_NONE


################################################
import os
# os.environ["OPENAI_API_KEY"]=''
os.environ["AZURE_OPENAI_API_KEY"]=''
os.environ["AZURE_OPENAI_ENDPOINT"]=''
api_version=""

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
    #-----------------------------------------#
    Context: {requirement}
    #-----------------------------------------#
    Hungry_Human1: Tasks components ok? Can alter:
    """

    CLASSIFY_RESPONSE_PROMPT: str = """
    You are an AI assistant in charge of classifying whether user is satisfied with defined task definition.
    Task definition had been shared with user, and user provided his/her response in text.
    Given the user response text delimited between triple backticks, your specific task is to classify whether user is satisfied or not satisfied. 
    ```{user_response}```
    Respond with "Satisfied" if user is satisfied. Respond with "Not Satisfied" if user is not satisfied.
    """

    name: str = "Human1ReviewReq"


    async def run(self, req: str):
        # test semantic route
        # print( rl("I want to make a sales app") )

        prompt = self.PROMPT_TEMPLATE.format(requirement=req[-1].content)    #! to avoid printing full conversation history
        rsp = await self._aask(prompt)

        user_response_to_classify = self.CLASSIFY_RESPONSE_PROMPT.format(user_response=rsp)
        llm_tool = self.context.llm_with_cost_manager_from_llm_config(self.config.llm)
        user_satisfaction = await llm_tool.aask(user_response_to_classify)
        logger.info(f"{user_satisfaction=}")

        if user_satisfaction=="Satisfied":
            return( (user_satisfaction, req[1].content ) )

        elif user_satisfaction=="Not Satisfied":
            # updated_req = rsp + '\n\n' + '#########' + '\n\n' + req[1].content       # need to improve prompt
            updated_req = rsp                                                          # BA will feed conversation history into BA's llm
            return( (user_satisfaction, updated_req) ) 

        return( (user_satisfaction, req) )