"""
Task management tools
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from yanzhiti.core.tool import Tool, ToolContext, ToolInputSchema, ToolResult
from yanzhiti.types import ToolResultStatus


class Task(BaseModel):
    """Task model"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    description: Optional[str] = None
    status: str = "pending"  # pending, in_progress, completed, failed
    priority: str = "medium"  # low, medium, high, urgent
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TaskManager:
    """In-memory task manager"""

    def __init__(self):
        self._tasks: Dict[str, Task] = {}

    def create_task(self, task: Task) -> Task:
        self._tasks[task.id] = task
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)

    def list_tasks(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> List[Task]:
        tasks = list(self._tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)

    def update_task(self, task_id: str, **kwargs) -> Optional[Task]:
        task = self._tasks.get(task_id)
        if not task:
            return None

        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)

        task.updated_at = datetime.now()
        return task

    def delete_task(self, task_id: str) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False


# Global task manager
_task_manager = TaskManager()


class TaskCreateTool(Tool):
    """Tool for creating tasks"""

    def __init__(self):
        super().__init__(
            name="task_create",
            description="Create a new task",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "title": {
                    "type": "string",
                    "description": "Task title",
                },
                "description": {
                    "type": "string",
                    "description": "Task description",
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high", "urgent"],
                    "description": "Task priority (default: medium)",
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Task tags",
                },
            },
            required=["title"],
        )

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        task = Task(
            title=input_data["title"],
            description=input_data.get("description"),
            priority=input_data.get("priority", "medium"),
            tags=input_data.get("tags", []),
        )

        created_task = _task_manager.create_task(task)

        return ToolResult(
            status=ToolResultStatus.SUCCESS,
            output=f"Created task: {created_task.id}\nTitle: {created_task.title}\nPriority: {created_task.priority}",
            metadata={"task_id": created_task.id, "task": created_task.model_dump()},
        )


class TaskListTool(Tool):
    """Tool for listing tasks"""

    def __init__(self):
        super().__init__(
            name="task_list",
            description="List all tasks",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "status": {
                    "type": "string",
                    "enum": ["pending", "in_progress", "completed", "failed"],
                    "description": "Filter by status",
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high", "urgent"],
                    "description": "Filter by priority",
                },
            },
            required=[],
        )

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        status = input_data.get("status")
        priority = input_data.get("priority")

        tasks = _task_manager.list_tasks(status=status, priority=priority)

        if not tasks:
            return ToolResult(
                status=ToolResultStatus.SUCCESS,
                output="No tasks found",
                metadata={"count": 0},
            )

        output = ["Tasks:", ""]
        for task in tasks:
            output.extend([
                f"ID: {task.id}",
                f"Title: {task.title}",
                f"Status: {task.status}",
                f"Priority: {task.priority}",
                f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
                "",
            ])

        return ToolResult(
            status=ToolResultStatus.SUCCESS,
            output="\n".join(output),
            metadata={"count": len(tasks), "tasks": [t.model_dump() for t in tasks]},
        )


class TaskGetTool(Tool):
    """Tool for getting a specific task"""

    def __init__(self):
        super().__init__(
            name="task_get",
            description="Get details of a specific task",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "task_id": {
                    "type": "string",
                    "description": "Task ID",
                },
            },
            required=["task_id"],
        )

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        task_id = input_data["task_id"]
        task = _task_manager.get_task(task_id)

        if not task:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Task not found: {task_id}",
            )

        output = [
            f"Task ID: {task.id}",
            f"Title: {task.title}",
            f"Description: {task.description or 'N/A'}",
            f"Status: {task.status}",
            f"Priority: {task.priority}",
            f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Updated: {task.updated_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Tags: {', '.join(task.tags) if task.tags else 'None'}",
        ]

        return ToolResult(
            status=ToolResultStatus.SUCCESS,
            output="\n".join(output),
            metadata={"task": task.model_dump()},
        )


class TaskUpdateTool(Tool):
    """Tool for updating a task"""

    def __init__(self):
        super().__init__(
            name="task_update",
            description="Update a task",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "task_id": {
                    "type": "string",
                    "description": "Task ID",
                },
                "title": {
                    "type": "string",
                    "description": "New title",
                },
                "description": {
                    "type": "string",
                    "description": "New description",
                },
                "status": {
                    "type": "string",
                    "enum": ["pending", "in_progress", "completed", "failed"],
                    "description": "New status",
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high", "urgent"],
                    "description": "New priority",
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "New tags",
                },
            },
            required=["task_id"],
        )

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        task_id = input_data["task_id"]
        updates = {k: v for k, v in input_data.items() if k != "task_id"}

        task = _task_manager.update_task(task_id, **updates)

        if not task:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Task not found: {task_id}",
            )

        return ToolResult(
            status=ToolResultStatus.SUCCESS,
            output=f"Updated task: {task.id}\nTitle: {task.title}\nStatus: {task.status}",
            metadata={"task": task.model_dump()},
        )


class TaskDeleteTool(Tool):
    """Tool for deleting a task"""

    def __init__(self):
        super().__init__(
            name="task_delete",
            description="Delete a task",
        )

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "task_id": {
                    "type": "string",
                    "description": "Task ID",
                },
            },
            required=["task_id"],
        )

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        task_id = input_data["task_id"]
        deleted = _task_manager.delete_task(task_id)

        if not deleted:
            return ToolResult(
                status=ToolResultStatus.ERROR,
                error=f"Task not found: {task_id}",
            )

        return ToolResult(
            status=ToolResultStatus.SUCCESS,
            output=f"Deleted task: {task_id}",
        )


class TodoWriteTool(Tool):
    """Tool for writing todo lists (simpler task management)"""

    def __init__(self):
        super().__init__(
            name="todo_write",
            description="Write or update a todo list",
        )
        self._todos: List[Dict[str, Any]] = []

    @property
    def input_schema(self) -> ToolInputSchema:
        return ToolInputSchema(
            properties={
                "todos": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string"},
                            "status": {
                                "type": "string",
                                "enum": ["pending", "in_progress", "completed"],
                            },
                            "activeForm": {"type": "string"},
                        },
                    },
                    "description": "List of todo items",
                },
            },
            required=["todos"],
        )

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: ToolContext,
    ) -> ToolResult:
        todos = input_data["todos"]
        self._todos = todos

        output = ["Todo List:", ""]
        for i, todo in enumerate(todos, 1):
            status_icon = {
                "pending": "○",
                "in_progress": "◐",
                "completed": "●",
            }.get(todo.get("status", "pending"), "○")

            content = todo.get("content", "")
            active_form = todo.get("activeForm", "")

            output.append(f"{i}. {status_icon} {content}")
            if active_form and todo.get("status") == "in_progress":
                output.append(f"   → {active_form}")

        return ToolResult(
            status=ToolResultStatus.SUCCESS,
            output="\n".join(output),
            metadata={"todos": todos},
        )
