from langgraph.graph import StateGraph, END
from typing import Dict, Any
from .state import AgentState, WorkflowStep, create_initial_state
from ..utils import get_logger

logging = get_logger(__name__)

class CodeReviewOrchestrator:
    """
    Main orchestrator for the code review workflow using LangGraph.
    Coordinates all agents and manages the workflow state.
    """
    
    def __init__(self):
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        
        # Create workflow graph
        workflow = StateGraph(AgentState)
        
        # Add nodes (we'll implement these in later phases)
        workflow.add_node("analyze_repo", self._analyze_repo_node)
        workflow.add_node("review_code", self._review_code_node)
        workflow.add_node("generate_docs", self._generate_docs_node)
        workflow.add_node("create_pr", self._create_pr_node)
        workflow.add_node("complete", self._complete_node)
        
        # Set entry point
        workflow.set_entry_point("analyze_repo")
        
        # Add edges (workflow transitions)
        workflow.add_edge("analyze_repo", "review_code")
        workflow.add_edge("review_code", "generate_docs")
        workflow.add_edge("generate_docs", "create_pr")
        workflow.add_edge("create_pr", "complete")
        workflow.add_edge("complete", END)
        
        # Compile graph
        return workflow.compile()
    
    # Placeholder node functions (we'll implement these in later phases)
    def _analyze_repo_node(self, state: AgentState) -> AgentState:
        """Node for repository analysis."""
        logging.info("Repository Analysis , Analyzing repository structure...")
        state["current_step"] = WorkflowStep.REPO_ANALYSIS.value
        state["messages"].append("Repository analysis completed (placeholder)")
        return state
    
    def _review_code_node(self, state: AgentState) -> AgentState:
        """Node for code review."""
        logging.info("Code Review,  Reviewing code...")
        state["current_step"] = WorkflowStep.CODE_REVIEW.value
        state["messages"].append("Code review completed (placeholder)")
        return state
    
    def _generate_docs_node(self, state: AgentState) -> AgentState:
        """Node for documentation generation."""
        logging.info("Documentation , Generating documentation...")
        state["current_step"] = WorkflowStep.DOC_GENERATION.value
        state["messages"].append("Documentation generated (placeholder)")
        return state
    
    def _create_pr_node(self, state: AgentState) -> AgentState:
        """Node for PR creation."""
        logging.info("PR Creation , Creating pull request...")
        state["current_step"] = WorkflowStep.PR_CREATION.value
        state["messages"].append("PR creation skipped (placeholder)")
        return state
    
    def _complete_node(self, state: AgentState) -> AgentState:
        """Final node - mark workflow as complete."""
        from datetime import datetime
        
        logging.info("Complete, Workflow completed successfully!")
        state["current_step"] = WorkflowStep.COMPLETE.value
        state["end_time"] = datetime.now().isoformat()
        
        # Print summary
        logging.info(f"Total files analyzed: {state['total_files_analyzed']}")
        logging.info(f"Total issues found: {state['total_issues_found']}")
        
        return state
    
    def run(self, repo_url: str) -> AgentState:
        """
        Run the complete code review workflow.
        
        Args:
            repo_url: GitHub repository URL
            
        Returns:
            Final state after workflow completion
        """
        logging.info(f"Starting code review workflow for: {repo_url}")
        
        try:
            # Create initial state
            initial_state = create_initial_state(repo_url)
            
            # Execute workflow
            final_state = self.graph.invoke(initial_state)
            
            logging.info("Workflow completed successfully!")
            return final_state
            
        except Exception as e:
            logging.error(f"Workflow failed: {str(e)}")
            raise e