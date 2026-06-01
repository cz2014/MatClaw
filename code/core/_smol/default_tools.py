#!/usr/bin/env python
# coding=utf-8

# Copyright 2024 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Vendored default tools, trimmed in P2.

Upstream smolagents shipped a set of built-in tools here (web search, Python
interpreter, Wikipedia, speech-to-text, ...). MatClaw always constructs
``CodeAgent`` with ``add_base_tools=False`` and injects its own curated toolset,
so the only tool kept is ``FinalAnswerTool`` (which ``agents.py`` always adds).
``TOOL_MAPPING`` is empty for the same reason.
"""
from typing import Any

from .tools import Tool


class FinalAnswerTool(Tool):
    name = "final_answer"
    description = "Provides a final answer to the given problem."
    inputs = {"answer": {"type": "any", "description": "The final answer to the problem"}}
    output_type = "any"

    def forward(self, answer: Any) -> Any:
        return answer


# MatClaw always passes add_base_tools=False, so no base tools are auto-registered.
TOOL_MAPPING: dict[str, type[Tool]] = {}

__all__ = ["FinalAnswerTool", "TOOL_MAPPING"]
