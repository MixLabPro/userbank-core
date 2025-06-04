"""
Personal Profile Data Management System - FastMCP SSE Mode
Using FastMCP's @mcp.tool() decorator, parameters defined directly in function signature
"""

from fastmcp import FastMCP
from typing import List, Dict, Any, Optional, Union
import json
import os
from pathlib import Path
from datetime import datetime
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import uvicorn

# Import configuration manager and initialize immediately
from config_manager import get_config_manager

# Initialize configuration manager immediately to ensure configuration is ready before importing tools
config_manager = get_config_manager()
print(f"Database path: {config_manager.get_database_path()}")
print(f"Server port: {config_manager.get_server_port()}")
print(f"Configuration file path: {config_manager.config_path}")

# Import tool modules
from tools import (
    PersonaTools, MemoryTools, ViewpointTools, InsightTools,
    GoalTools, PreferenceTools, MethodologyTools, FocusTools,
    PredictionTools, DatabaseTools
)

# Define CORS middleware
cors_middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins, recommend specifying specific domains in production
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all request headers
    ),
]

# Create FastMCP server instance
mcp = FastMCP("Personal Profile Data Management System")

# Initialize tool instances
persona_tools = PersonaTools()
memory_tools = MemoryTools()
viewpoint_tools = ViewpointTools()
insight_tools = InsightTools()
goal_tools = GoalTools()
preference_tools = PreferenceTools()
methodology_tools = MethodologyTools()
focus_tools = FocusTools()
prediction_tools = PredictionTools()
database_tools = DatabaseTools()

# ============ Persona Related Operations ============

@mcp.tool()
def get_persona() -> Dict[str, Any]:
    """Get current user's core profile information. This information is used for AI personalized interaction. There is only one user profile in the system with fixed ID 1."""
    return persona_tools.get_persona()

@mcp.tool()
def save_persona(name: str = None, gender: str = None, personality: str = None, 
                avatar_url: str = None, bio: str = None, privacy_level: str = None) -> Dict[str, Any]:
    """Save (update) current user's core profile information. Since ID is fixed as 1, this operation is mainly used to update existing profile. Only provide fields that need to be modified."""
    return persona_tools.save_persona(name, gender, personality, avatar_url, bio, privacy_level)

# ============ Memory Tools ============

@mcp.tool()
def manage_memories(action: str, id: int = None, content: str = None, memory_type: str = None,
                   importance: int = None, related_people: str = None, location: str = None,
                   memory_date: str = None, keywords: List[str] = None, source_app: str = 'unknown',
                   reference_urls: List[str] = None, privacy_level: str = 'public',
                   filter: Dict[str, Any] = None, sort_by: str = 'created_time', 
                   sort_order: str = 'desc', limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """Memory data management tool. Supports query and save operations.
    
    Parameter description:
    - action: Operation type, 'query' (query) or 'save' (save)
    
    Query operation (action='query') uses parameters:
    - filter: Query condition dictionary
    - sort_by, sort_order, limit, offset: Sorting and pagination parameters
    
    Save operation (action='save') uses parameters:
    - id: Record ID, None means create new record, value means update existing record
    - content, memory_type, importance etc: Memory data fields
    """
    if action == "query":
        return memory_tools.query_memories(filter, sort_by, sort_order, limit, offset)
    elif action == "save":
        return memory_tools.save_memory(id, content, memory_type, importance, related_people, 
                                       location, memory_date, keywords, source_app, 
                                       reference_urls, privacy_level)
    else:
        return {
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": f"Invalid operation type: {action}, supported operations: 'query', 'save'"
        }

# ============ Viewpoint Tools ============

@mcp.tool()
def manage_viewpoints(action: str, id: int = None, content: str = None, source_people: str = None,
                     keywords: List[str] = None, source_app: str = 'unknown',
                     related_event: str = None, reference_urls: List[str] = None,
                     privacy_level: str = 'public', filter: Dict[str, Any] = None, 
                     sort_by: str = 'created_time', sort_order: str = 'desc', 
                     limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """Viewpoint data management tool. Supports query and save operations."""
    if action == "query":
        return viewpoint_tools.query_viewpoints(filter, sort_by, sort_order, limit, offset)
    elif action == "save":
        return viewpoint_tools.save_viewpoint(id, content, source_people, keywords, 
                                             source_app, related_event, reference_urls, privacy_level)
    else:
        return {
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": f"Invalid operation type: {action}, supported operations: 'query', 'save'"
        }

# ============ Insight Tools ============

@mcp.tool()
def manage_insights(action: str, id: int = None, content: str = None, source_people: str = None,
                   keywords: List[str] = None, source_app: str = 'unknown',
                   reference_urls: List[str] = None, privacy_level: str = 'public',
                   filter: Dict[str, Any] = None, sort_by: str = 'created_time', 
                   sort_order: str = 'desc', limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """Insight data management tool. Supports query and save operations."""
    if action == "query":
        return insight_tools.query_insights(filter, sort_by, sort_order, limit, offset)
    elif action == "save":
        return insight_tools.save_insight(id, content, source_people, keywords, 
                                         source_app, reference_urls, privacy_level)
    else:
        return {
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": f"Invalid operation type: {action}, supported operations: 'query', 'save'"
        }

# ============ Goal Tools ============

@mcp.tool()
def manage_goals(action: str, id: int = None, content: str = None, type: str = None, 
                deadline: str = None, status: str = 'planning', keywords: List[str] = None, 
                source_app: str = 'unknown', privacy_level: str = 'public',
                filter: Dict[str, Any] = None, sort_by: str = 'deadline', 
                sort_order: str = 'asc', limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """Goal data management tool. Supports query and save operations."""
    if action == "query":
        return goal_tools.query_goals(filter, sort_by, sort_order, limit, offset)
    elif action == "save":
        return goal_tools.save_goal(id, content, type, deadline, status, keywords, 
                                   source_app, privacy_level)
    else:
        return {
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": f"Invalid operation type: {action}, supported operations: 'query', 'save'"
        }

# ============ Preference Tools ============

@mcp.tool()
def manage_preferences(action: str, id: int = None, content: str = None, context: str = None,
                      keywords: List[str] = None, source_app: str = 'unknown',
                      privacy_level: str = 'public', filter: Dict[str, Any] = None, 
                      sort_by: str = 'created_time', sort_order: str = 'desc', 
                      limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """Preference data management tool. Supports query and save operations."""
    if action == "query":
        return preference_tools.query_preferences(filter, sort_by, sort_order, limit, offset)
    elif action == "save":
        return preference_tools.save_preference(id, content, context, keywords, 
                                               source_app, privacy_level)
    else:
        return {
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": f"Invalid operation type: {action}, supported operations: 'query', 'save'"
        }

# ============ Methodology Tools ============

@mcp.tool()
def manage_methodologies(action: str, id: int = None, content: str = None, type: str = None,
                        effectiveness: str = 'experimental', use_cases: str = None,
                        keywords: List[str] = None, source_app: str = 'unknown',
                        reference_urls: List[str] = None, privacy_level: str = 'public',
                        filter: Dict[str, Any] = None, sort_by: str = 'created_time', 
                        sort_order: str = 'desc', limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """Methodology data management tool. Supports query and save operations."""
    if action == "query":
        return methodology_tools.query_methodologies(filter, sort_by, sort_order, limit, offset)
    elif action == "save":
        return methodology_tools.save_methodology(id, content, type, effectiveness, use_cases, 
                                                 keywords, source_app, reference_urls, privacy_level)
    else:
        return {
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": f"Invalid operation type: {action}, supported operations: 'query', 'save'"
        }

# ============ Focus Tools ============

@mcp.tool()
def manage_focuses(action: str, id: int = None, content: str = None, priority: int = None, 
                  status: str = 'active', context: str = None, keywords: List[str] = None, 
                  source_app: str = 'unknown', deadline: str = None, privacy_level: str = 'public',
                  filter: Dict[str, Any] = None, sort_by: str = 'priority', 
                  sort_order: str = 'desc', limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """Focus data management tool. Supports query and save operations."""
    if action == "query":
        return focus_tools.query_focuses(filter, sort_by, sort_order, limit, offset)
    elif action == "save":
        return focus_tools.save_focus(id, content, priority, status, context, keywords, 
                                     source_app, deadline, privacy_level)
    else:
        return {
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": f"Invalid operation type: {action}, supported operations: 'query', 'save'"
        }

# ============ Prediction Tools ============

@mcp.tool()
def manage_predictions(action: str, id: int = None, content: str = None, timeframe: str = None, 
                      basis: str = None, verification_status: str = 'pending', 
                      keywords: List[str] = None, source_app: str = 'unknown', 
                      reference_urls: List[str] = None, privacy_level: str = 'public',
                      filter: Dict[str, Any] = None, sort_by: str = 'created_time', 
                      sort_order: str = 'desc', limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """Prediction data management tool. Supports query and save operations."""
    if action == "query":
        return prediction_tools.query_predictions(filter, sort_by, sort_order, limit, offset)
    elif action == "save":
        return prediction_tools.save_prediction(id, content, timeframe, basis, verification_status, 
                                               keywords, source_app, reference_urls, privacy_level)
    else:
        return {
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": f"Invalid operation type: {action}, supported operations: 'query', 'save'"
        }

# ============ Database Tools ============

@mcp.tool()
def execute_custom_sql(sql: str, params: List[str] = None, fetch_results: bool = True) -> Dict[str, Any]:
    """Execute custom SQL statement"""
    return database_tools.execute_custom_sql(sql, params, fetch_results)

@mcp.tool()
def get_table_schema(table_name: str = None) -> Dict[str, Any]:
    """Get table structure information"""
    return database_tools.get_table_schema(table_name)

# ============ Start Server ============

if __name__ == "__main__":
    print("Starting Personal Profile Data Management System - FastMCP SSE Mode")

    # Create HTTP application with CORS middleware
    http_app = mcp.http_app(transport="sse", middleware=cors_middleware)
    
    # Get server configuration from config file
    host = config_manager.get_server_host()
    port = config_manager.get_server_port()
    
    print(f"Server will start at {host}:{port}")
    
    # Start server using uvicorn
    uvicorn.run(http_app, host=host, port=port) 