"""
Agent System - Sub-agent spawning and management
"""

import asyncio
import uuid
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from yanzhiti.core.tool import Tool, ToolContext, ToolResult
from yanzhiti.types import AssistantMessage, Message, UserMessage


class AgentState(str, Enum):
    """Agent state"""

    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentConfig(BaseModel):
    """Configuration for an agent"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "sub-agent"
    description: str = ""
    parent_id: str | None = None
    max_turns: int = 10
    tools: list[str] = Field(default_factory=list)
    state: AgentState = AgentState.IDLE
    metadata: dict[str, Any] = Field(default_factory=dict)


class Agent:
    """
    A sub-agent that can execute tasks independently
    """

    def __init__(
        self,
        config: AgentConfig,
        query_engine: Any,  # QueryEngine or LocalQueryEngine
    ):
        self.config = config
        self.query_engine = query_engine
        self.messages: list[Message] = []
        self.result: AssistantMessage | None = None

    async def run(self, task: str) -> AssistantMessage:
        """
        Run the agent with a task
        """
        self.config.state = AgentState.RUNNING

        try:
            # Add task as user message
            self.messages.append(UserMessage(content=task))

            # Process through query engine
            response = await self.query_engine.query(task)

            self.result = response
            self.config.state = AgentState.COMPLETED
            return response

        except Exception as e:
            self.config.state = AgentState.FAILED
            raise e

    async def pause(self):
        """Pause agent execution"""
        self.config.state = AgentState.PAUSED

    async def resume(self):
        """Resume agent execution"""
        self.config.state = AgentState.RUNNING

    def get_status(self) -> dict[str, Any]:
        """Get agent status"""
        return {
            "id": self.config.id,
            "name": self.config.name,
            "state": self.config.state.value,
            "messages": len(self.messages),
            "has_result": self.result is not None,
        }


class AgentRegistry:
    """
    Registry for managing multiple agents
    """

    def __init__(self):
        self.agents: dict[str, Agent] = {}

    def register(self, agent: Agent) -> str:
        """Register an agent"""
        self.agents[agent.config.id] = agent
        return agent.config.id

    def unregister(self, agent_id: str):
        """Unregister an agent"""
        if agent_id in self.agents:
            del self.agents[agent_id]

    def get(self, agent_id: str) -> Agent | None:
        """Get an agent by ID"""
        return self.agents.get(agent_id)

    def list_all(self) -> list[Agent]:
        """List all agents"""
        return list(self.agents.values())

    def clear(self):
        """Clear all agents"""
        self.agents.clear()


class AgentTool(Tool):
    """
    Tool for spawning and managing sub-agents
    """

    def __init__(self, query_engine: Any):
        super().__init__(
            name="agent",
            description="Spawn a sub-agent to handle a complex task autonomously",
        )
        self.query_engine = query_engine
        self.registry = AgentRegistry()

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["spawn", "status", "list", "stop"],
                    "description": "Action to perform",
                },
                "task": {
                    "type": "string",
                    "description": "Task for the agent to execute (required for spawn)",
                },
                "agent_id": {
                    "type": "string",
                    "description": "Agent ID (for status/stop actions)",
                },
                "name": {
                    "type": "string",
                    "description": "Name for the spawned agent",
                },
                "max_turns": {
                    "type": "integer",
                    "description": "Maximum turns for the agent",
                },
            },
            "required": ["action"],
        }

    async def execute(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        from yanzhiti.types import ToolResultStatus

        action = input_data["action"]

        try:
            if action == "spawn":
                # Spawn a new agent
                task = input_data.get("task")
                if not task:
                    return ToolResult(
                        status=ToolResultStatus.ERROR,
                        error="Task is required for spawn action",
                    )

                # Create agent config
                config = AgentConfig(
                    name=input_data.get("name", "sub-agent"),
                    max_turns=input_data.get("max_turns", 10),
                )

                # Create and register agent
                agent = Agent(config, self.query_engine)
                self.registry.register(agent)

                # Run agent in background
                asyncio.create_task(agent.run(task))

                return ToolResult(
                    status=ToolResultStatus.SUCCESS,
                    output=f"Spawned agent {config.id} with task: {task[:50]}...",
                    metadata={"agent_id": config.id, "status": agent.get_status()},
                )

            elif action == "status":
                agent_id = input_data.get("agent_id")
                if not agent_id:
                    return ToolResult(
                        status=ToolResultStatus.ERROR,
                        error="agent_id is required for status action",
                    )

                agent = self.registry.get(agent_id)
                if not agent:
                    return ToolResult(
                        status=ToolResultStatus.ERROR,
                        error=f"Agent not found: {agent_id}",
                    )

                return ToolResult(
                    status=ToolResultStatus.SUCCESS,
                    output=f"Agent {agent_id} status: {agent.config.state.value}",
                    metadata=agent.get_status(),
                )

            elif action == "list":
                agents = self.registry.list_all()
                status_list = [agent.get_status() for agent in agents]

                return ToolResult(
                    status=ToolResultStatus.SUCCESS,
                    output=f"Found {len(agents)} agents",
                    metadata={"agents": status_list},
                )

            elif action == "stop":
                agent_id = input_data.get("agent_id")
                if not agent_id:
                    return ToolResult(
                        status=ToolResultStatus.ERROR,
                        error="agent_id is required for stop action",
                    )

                agent = self.registry.get(agent_id)
                if not agent:
                    return ToolResult(
                        status=ToolResultStatus.ERROR,
                        error=f"Agent not found: {agent_id}",
                    )

                await agent.pause()
                self.registry.unregister(agent_id)

                return ToolResult(
                    status=ToolResultStatus.SUCCESS,
                    output=f"Stopped and removed agent {agent_id}",
                )

            else:
                return ToolResult(
                    status=ToolResultStatus.ERROR,
                    error=f"Unknown action: {action}",
                )

        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Error in agent tool: {str(e)}",
            )


class ForkTool(Tool):
    """
    Tool for forking the current conversation into a sub-agent
    """

    def __init__(self, query_engine: Any):
        super().__init__(
            name="fork",
            description="Fork current conversation into a sub-agent",
        )
        self.query_engine = query_engine

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "Task for the forked agent",
                },
                "context": {
                    "type": "string",
                    "description": "Additional context to pass",
                },
            },
            "required": ["task"],
        }

    async def execute(
        self,
        input_data: dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        from yanzhiti.types import ToolResultStatus

        task = input_data["task"]
        additional_context = input_data.get("context", "")

        try:
            # Create forked agent
            config = AgentConfig(
                name="forked-agent",
                parent_id="main",
            )

            agent = Agent(config, self.query_engine)

            # Build full task with context
            full_task = f"{task}\n\nContext: {additional_context}" if additional_context else task

            # Run agent synchronously and get result
            result = await agent.run(full_task)

            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output=result.content,
                metadata={"agent_id": config.id, "state": agent.config.state.value},
            )

        except Exception as e:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Error forking agent: {str(e)}",
            )
