from typing import TypedDict, List, Dict, Any, Optional
from enum import Enum

class WorkflowStep(Enum):
    """Enum for workflow steps."""
    INIT = "init"
    REPO_ANALYSIS = "repo_analysis"
    CODE_REVIEW = "code_review"
    DOC_GENERATION = "doc_generation"
    PR_CREATION = "pr_creation"
    COMPLETE = "complete"
    ERROR = "error"

class AgentState(TypedDict):
    """State schema for the code review agent workflow."""
    
    # Input
    repo_url: str
    
    # Repository Info
    local_path: Optional[str]
    repo_name: Optional[str]
    file_structure: Optional[Dict[str, Any]]
    files_to_review: List[str]
    
    # Code Review Results (NEW!)
    understanding: Optional[Dict[str, Any]]
    code_review: Optional[Dict[str, Any]]
    enhancements: Optional[List[Dict[str, Any]]]
    documentation: Optional[Dict[str, Any]]
    summary: Optional[Dict[str, Any]]
    
    # Review Summary
    review_results: List[Dict[str, Any]]
    review_summary: Optional[str]
    
    # Documentation
    readme_content: Optional[str]
    
    # PR Info
    pr_created: bool
    pr_url: Optional[str]
    
    # Workflow Control
    current_step: str
    errors: List[str]
    messages: List[str]
    
    # Metadata
    total_files_analyzed: int
    total_issues_found: int
    start_time: Optional[str]
    end_time: Optional[str]

def create_initial_state(repo_url: str) -> AgentState:
    """Create initial state for the workflow."""
    from datetime import datetime
    
    return AgentState(
        repo_url=repo_url,
        local_path=None,
        repo_name=None,
        file_structure=None,
        files_to_review=[],

        understanding=None,
        code_review=None,
        enhancements=None,
        documentation=None,
        summary=None,
        total_issues_found=0,


        review_results=[],
        review_summary=None,
        readme_content=None,
        pr_created=False,
        pr_url=None,
        current_step=WorkflowStep.INIT.value,
        errors=[],
        messages=[],
        total_files_analyzed=0,
        start_time=datetime.now().isoformat(),
        end_time=None
    )