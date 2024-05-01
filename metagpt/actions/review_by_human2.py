#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/5/2 09:00
@Author  : ed
@File    : review_by_human2.py
"""
from metagpt.actions import WriteTasks
from metagpt.actions import Action
from metagpt.logs import logger
# from metagpt.schema import Message
# from metagpt.const import MESSAGE_ROUTE_TO_NONE


class Human2ReviewReq(Action):
    PROMPT_TEMPLATE: str = """
    #-----------------------------------------#
    Context: {requirement}
    #-----------------------------------------#
    Hairy_Human2 Tasks components ok? Can alter:
    """

    CLASSIFY_RESPONSE_PROMPT: str = """
    You are an AI assistant in charge of classifying whether user is satisfied with defined task definition.
    Task definition had been shared with user, and user provided his/her response in text.
    Given the user response text delimited between triple backticks, your specific task is to classify whether user is satisfied or not satisfied. 
    ```{user_response}```
    Respond with "Satisfied" if user is satisfied. Respond with "Not Satisfied" if user is not satisfied.
    """

    name: str = "Human2ReviewReq"


    async def run(self, req: str):
        # test semantic route

        # logger.info(f"Human2ReviewReq req: {req=}")

        prompt = self.PROMPT_TEMPLATE.format(requirement=req[-1].content)    #! to avoid printing full conversation history
        rsp = await self._aask(prompt)

        user_response_to_classify = self.CLASSIFY_RESPONSE_PROMPT.format(user_response=rsp)
        llm_tool = self.context.llm_with_cost_manager_from_llm_config(self.config.llm)
        user_satisfaction = await llm_tool.aask(user_response_to_classify)
        logger.info(f"{user_satisfaction=}")

        if user_satisfaction=="Satisfied":
            logger.info(f"Satisfied Human2ReviewReq req[-1]: {req[-1]=}")
            # return( (user_satisfaction, req[1].content ) )
            return( (user_satisfaction, req[-1].content ) )          #!

        elif user_satisfaction=="Not Satisfied":
            # updated_req = rsp + '\n\n' + '#########' + '\n\n' + req[1].content       # need to improve prompt
            updated_req = rsp                                                          # Architect1 will feed conversation history into Architect1's llm
            return( (user_satisfaction, updated_req) ) 

        return( (user_satisfaction, req) )