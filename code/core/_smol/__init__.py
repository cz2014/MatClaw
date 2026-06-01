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
"""Vendored subset of smolagents 1.24.0 (Apache-2.0), owned by MatClaw.

Copied from the upstream ``smolagents`` package and pruned / edited in place; see
``PROVENANCE.md`` for the source version and the list of local patches. This is
first-party code now -- edit it directly, do NOT re-pull from PyPI.

Only the subset MatClaw uses is re-exported here for ``from core._smol import X``;
submodules (``core._smol.models``, ``core._smol.memory``, ...) expose the rest.
"""
__version__ = "1.24.0+matclaw"

from .agents import (
    CodeAgent,
    FinalAnswerPromptTemplate,
    ManagedAgentPromptTemplate,
    PlanningPromptTemplate,
    PromptTemplates,
)
from .local_python_executor import LocalPythonExecutor
from .memory import ActionStep, AgentMemory, PlanningStep, SystemPromptStep, Timing
from .models import CODEAGENT_RESPONSE_FORMAT, ChatMessage, LiteLLMModel, MessageRole
from .monitoring import AgentLogger, LogLevel, TokenUsage
from .tools import Tool, tool
from .utils import AgentError

__all__ = [
    "CodeAgent",
    "PromptTemplates",
    "FinalAnswerPromptTemplate",
    "ManagedAgentPromptTemplate",
    "PlanningPromptTemplate",
    "LocalPythonExecutor",
    "ActionStep",
    "PlanningStep",
    "SystemPromptStep",
    "AgentMemory",
    "Timing",
    "TokenUsage",
    "LiteLLMModel",
    "ChatMessage",
    "MessageRole",
    "CODEAGENT_RESPONSE_FORMAT",
    "AgentLogger",
    "LogLevel",
    "Tool",
    "tool",
    "AgentError",
]
