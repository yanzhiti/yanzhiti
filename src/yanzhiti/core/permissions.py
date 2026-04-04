"""
Permission System - Rule-based permission engine
"""

import re
from collections.abc import Callable
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class PermissionAction(str, Enum):
    """Permission actions"""

    ALLOW = "allow"
    DENY = "deny"
    ASK = "ask"  # Ask user for permission


class PermissionScope(str, Enum):
    """Permission scopes"""

    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    DELETE = "delete"
    ALL = "all"


class PermissionRule(BaseModel):
    """A single permission rule"""

    id: str
    name: str
    description: str = ""
    action: PermissionAction
    scope: PermissionScope = PermissionScope.ALL
    pattern: str  # Regex pattern to match
    priority: int = 0  # Higher priority rules are checked first
    enabled: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)


class PermissionContext(BaseModel):
    """Context for permission check"""

    tool_name: str
    operation: str
    path: str | None = None
    command: str | None = None
    user: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class PermissionResult(BaseModel):
    """Result of permission check"""

    granted: bool
    action: PermissionAction
    rule: PermissionRule | None = None
    reason: str = ""
    ask_user: bool = False
    message: str = ""


class PermissionEngine:
    """
    Permission engine with rule-based access control
    """

    def __init__(self):
        self.rules: list[PermissionRule] = []
        self._default_action = PermissionAction.ASK
        self._user_callbacks: dict[str, Callable] = {}

    def add_rule(self, rule: PermissionRule):
        """Add a permission rule"""
        self.rules.append(rule)
        # Sort by priority (descending)
        self.rules.sort(key=lambda r: r.priority, reverse=True)

    def remove_rule(self, rule_id: str):
        """Remove a rule by ID"""
        self.rules = [r for r in self.rules if r.id != rule_id]

    def set_default_action(self, action: PermissionAction):
        """Set default action when no rules match"""
        self._default_action = action

    def register_user_callback(self, callback_id: str, callback: Callable):
        """Register a callback for user interaction"""
        self._user_callbacks[callback_id] = callback

    async def check_permission(
        self,
        context: PermissionContext,
    ) -> PermissionResult:
        """
        Check permission for a given context
        """
        # Check each rule in priority order
        for rule in self.rules:
            if not rule.enabled:
                continue

            # Check if rule matches
            if self._rule_matches(rule, context):
                # Rule matches, return result
                if rule.action == PermissionAction.ALLOW:
                    return PermissionResult(
                        granted=True,
                        action=rule.action,
                        rule=rule,
                        reason=f"Allowed by rule: {rule.name}",
                    )
                elif rule.action == PermissionAction.DENY:
                    return PermissionResult(
                        granted=False,
                        action=rule.action,
                        rule=rule,
                        reason=f"Denied by rule: {rule.name}",
                    )
                elif rule.action == PermissionAction.ASK:
                    # Need to ask user
                    return PermissionResult(
                        granted=False,
                        action=rule.action,
                        rule=rule,
                        reason=f"Requires user approval: {rule.name}",
                        ask_user=True,
                        message=self._build_ask_message(rule, context),
                    )

        # No rules matched, use default action
        if self._default_action == PermissionAction.ALLOW:
            return PermissionResult(
                granted=True,
                action=self._default_action,
                reason="Allowed by default",
            )
        elif self._default_action == PermissionAction.DENY:
            return PermissionResult(
                granted=False,
                action=self._default_action,
                reason="Denied by default",
            )
        else:
            return PermissionResult(
                granted=False,
                action=self._default_action,
                reason="Requires user approval (default)",
                ask_user=True,
                message=f"Allow {context.tool_name} to {context.operation}?",
            )

    def _rule_matches(self, rule: PermissionRule, context: PermissionContext) -> bool:
        """Check if a rule matches the context"""
        # Check scope
        if rule.scope != PermissionScope.ALL:
            # Map operation to scope
            op_scope = self._operation_to_scope(context.operation)
            if op_scope != rule.scope:
                return False

        # Check pattern
        pattern = rule.pattern

        # Try to match against different context fields
        if context.path and re.search(pattern, context.path):
            return True

        if context.command and re.search(pattern, context.command):
            return True

        return context.tool_name and re.search(pattern, context.tool_name)

    def _operation_to_scope(self, operation: str) -> PermissionScope:
        """Map operation string to scope"""
        operation = operation.lower()

        if operation in ["read", "get", "list", "show", "cat"]:
            return PermissionScope.READ
        elif operation in ["write", "create", "update", "edit", "delete"]:
            return PermissionScope.WRITE
        elif operation in ["execute", "run", "bash", "shell"]:
            return PermissionScope.EXECUTE
        else:
            return PermissionScope.ALL

    def _build_ask_message(self, rule: PermissionRule, context: PermissionContext) -> str:
        """Build message to show user when asking for permission"""
        parts = [f"Permission Request: {rule.name}"]

        if context.tool_name:
            parts.append(f"Tool: {context.tool_name}")
        if context.operation:
            parts.append(f"Operation: {context.operation}")
        if context.path:
            parts.append(f"Path: {context.path}")
        if context.command:
            parts.append(f"Command: {context.command}")

        if rule.description:
            parts.append(f"Description: {rule.description}")

        return "\n".join(parts)

    def create_default_rules(self) -> list[PermissionRule]:
        """Create default permission rules"""
        rules = [
            # Allow reading files in current directory
            PermissionRule(
                id="allow-read-cwd",
                name="Allow reading files in current directory",
                action=PermissionAction.ALLOW,
                scope=PermissionScope.READ,
                pattern=r"^\.\/.*",
                priority=10,
            ),
            # Deny reading sensitive files
            PermissionRule(
                id="deny-sensitive-files",
                name="Deny access to sensitive files",
                action=PermissionAction.DENY,
                pattern=r"(\.env|\.ssh|\.gitconfig|id_rsa|\.pem)$",
                priority=100,
            ),
            # Ask for write operations
            PermissionRule(
                id="ask-write",
                name="Ask for write operations",
                action=PermissionAction.ASK,
                scope=PermissionScope.WRITE,
                pattern=r".*",
                priority=5,
            ),
            # Ask for execute operations
            PermissionRule(
                id="ask-execute",
                name="Ask for execute operations",
                action=PermissionAction.ASK,
                scope=PermissionScope.EXECUTE,
                pattern=r".*",
                priority=5,
            ),
            # Allow safe commands
            PermissionRule(
                id="allow-safe-commands",
                name="Allow safe commands",
                action=PermissionAction.ALLOW,
                scope=PermissionScope.EXECUTE,
                pattern=r"^(ls|cat|pwd|echo|which|git status|git log|git diff)",
                priority=20,
            ),
        ]

        return rules


class PermissionManager:
    """
    High-level permission manager
    """

    def __init__(self):
        self.engine = PermissionEngine()
        self._setup_default_rules()

    def _setup_default_rules(self):
        """Setup default permission rules"""
        default_rules = self.engine.create_default_rules()
        for rule in default_rules:
            self.engine.add_rule(rule)

    async def check_file_read(self, path: str) -> PermissionResult:
        """Check permission for reading a file"""
        context = PermissionContext(
            tool_name="file_read",
            operation="read",
            path=path,
        )
        return await self.engine.check_permission(context)

    async def check_file_write(self, path: str) -> PermissionResult:
        """Check permission for writing a file"""
        context = PermissionContext(
            tool_name="file_write",
            operation="write",
            path=path,
        )
        return await self.engine.check_permission(context)

    async def check_command_execute(self, command: str) -> PermissionResult:
        """Check permission for executing a command"""
        context = PermissionContext(
            tool_name="bash",
            operation="execute",
            command=command,
        )
        return await self.engine.check_permission(context)

    def add_custom_rule(self, rule: PermissionRule):
        """Add a custom permission rule"""
        self.engine.add_rule(rule)

    def set_mode(self, mode: str):
        """
        Set permission mode
        - "permissive": Allow all by default
        - "strict": Deny all by default
        - "interactive": Ask for all by default
        """
        if mode == "permissive":
            self.engine.set_default_action(PermissionAction.ALLOW)
        elif mode == "strict":
            self.engine.set_default_action(PermissionAction.DENY)
        else:
            self.engine.set_default_action(PermissionAction.ASK)
