from typing import Dict , List , Any 

from ..utils import get_logger 
from ..tools import FileScanner , GitHubTools
from .state import AgentState 

logging = get_logger(__name__)

class RepositoryAnalyzer:
    """
    Agent handles github repository analyses

    1- clone repository
    2- scan for code files
    3- update workflow state with the results
    
    """


    def __init__(self):

        self.filescanner = FileScanner()
        self.githubtool = GitHubTools()


    def analyze(self, state : AgentState) -> AgentState: 


        repo_url = state['repo_url']
        try:

            clone_result = self._clone_repository(repo_url=repo_url)

            if clone_result['error']:
                return self._handle_clone_failure(state = state , error = clone_result['error'])
            
            local_path = clone_result['local_path']
            state['local_path'] = local_path
            state['repo_name'] = clone_result['repo_name']

            logging.info(f"repo cloned to {local_path}")
            
            scan_results = self.filescanner.scan_repository(repo_path=local_path)

            state['files_to_review'] = scan_results['files_to_review']
            state['file_structure'] = scan_results['file_structure']
            state['total_files_analyzed'] = scan_results['total_files']

            message = f"found {scan_results['total_files']} files "
            state['messages'].append(message)

            return state

            
        except Exception as e: 
            error_msg = f"Error analyzing repository {e}"
            logging.error(error_msg)
            state['errors'].append(error_msg)
            state['messages'].append("Repository analysis failed")

            return state
        
    
    def _handle_clone_failure(self, state: AgentState, error: str) -> AgentState:
        """
        Handle clone failure by updating state with error information.
        
        Args:
            state: Current workflow state
            error: Error message from clone operation
            
        Returns:
            Updated state with error information
        """
        logging.error(f"Handling clone failure: {error}")
        
        # Add error to state
        state["errors"].append(f"Clone failed: {error}")
        state["messages"].append("❌ Failed to clone repository")
        
        # Set empty values for fields that depend on clone
        state["local_path"] = None
        state["files_to_review"] = []
        state["file_structure"] = {}
        state["total_files_analyzed"] = 0
        
        return state        
    

    def _clone_repository(self, repo_url: str) -> Dict[str, Any]:
        """
        Clone repository using GitHubTools.
        
        Args:
            repo_url: GitHub repository URL
            
        Returns:
            Dictionary with clone results from GitHubTools
        """
        logging.info(f"Cloning repository: {repo_url}")
        
        # Call GitHubTools to clone
        result = self.githubtool.clone_repository(repo_url)
        
        if result["success"]:
            logging.info("Clone successful")
        else:
            logging.error(f"Clone failed: {result['error']}")
        
        return result
    def cleanup(self, local_path: str) -> bool:
        """
        Clean up cloned repository (optional - for manual cleanup).
        
        Args:
            local_path: Path to cloned repository
            
        Returns:
            True if cleanup successful
        """
        if local_path:
            logging.info(f"Cleaning up repository at: {local_path}")
            return self.githubtool.cleanup_repository(local_path)
        return False