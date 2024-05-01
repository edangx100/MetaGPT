#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 14:43
@Author  : alexanderwu
@File    : __init__.py
"""

from metagpt.roles.role import Role
from metagpt.roles.architect import Architect
from metagpt.roles.architect1 import Architect1

from metagpt.roles.project_manager import ProjectManager
from metagpt.roles.project_manager1 import ProjectManager1 

from metagpt.roles.product_manager import ProductManager
from metagpt.roles.product_manager1 import ProductManager1

from metagpt.roles.engineer import Engineer
from metagpt.roles.engineer1 import Engineer1

from metagpt.roles.qa_engineer import QaEngineer
from metagpt.roles.searcher import Searcher
from metagpt.roles.sales import Sales

from metagpt.roles.business_analyst import BA
from metagpt.roles.human1 import Human1
from metagpt.roles.human2 import Human2


__all__ = [
    "Role",
    "Architect",
    "ProjectManager",
    "ProductManager",
    "Engineer",
    "QaEngineer",
    "Searcher",
    "Sales",
    "BA",
    "Human1",
    "Human2"
    "ProductManager1",
    "Architect1",
    "ProjectManager1",
    "Engineer1",
]
