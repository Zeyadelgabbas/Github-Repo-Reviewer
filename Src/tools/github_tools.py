import os 
import shutil 
import tempfile 
import requests 
import time


from git import Repo , GitCommandError 
from typing import Dict , Any

from Src.utils import get_logger , config


logging = get_logger(__name__)

class GitHubTools:

    """ Tool to interact with github tools """

    def __init__(self):

        self.temp_dir = tempfile.gettempdir()

    def clone_repository(self, repo_url: str) -> Dict[str,Any]:

        """
        Clone a github repository to a temp directory 

        returns: 
            dictionary with : repo_name , local_path , sucess , error 
        """

        try:

            repo_name = self._get_repo_name(repo_url=repo_url)
            local_path = os.path.join(
                self.temp_dir,
                f"code_review_{repo_name.replace('/','_')}_{os.urandom(4).hex()}"
            )

            repo = Repo.clone_from(url = repo_url , to_path = local_path ,depth = 1)
            logging.info(f"Successfully cloned the repo to {local_path}")
            repo.close()

            return {
                'repo_name' : repo_name,
                'local_path' : local_path , 
                'success' : True,
                'error' : None
            }

        except GitCommandError as e : 
            error = f"Git command error : {e}"
            logging.error(error)
            return {
                'repo_name' : None,
                'local_path' : None , 
                'success' : False,
                'error' : error
            }
        
        except Exception as e: 
            error = f"error cloning the repository : {e}"
            logging.error(error)
            return {
                'repo_name' : None,
                'local_path' : None , 
                'success' : False,
                'error' : error
            }
    def _get_repo_name(self,repo_url : str) -> str:

        """ Extract repo name from repo url """

        url = repo_url.rstrip('/').replace('.git','')

        url_parts = url.split('/')

        return f"{url_parts[-2]}/{url_parts[-1]}"
    

    def cleanup_repository(self, local_path: str) -> bool:
        """
        Delete the cloned repository from disk.
        Handles Windows permission issues with .git folders.
        
        Args:
            local_path: Path to the cloned repository
            
        Returns:
            True if cleanup successful, False otherwise
        """
        try:
            if os.path.exists(local_path):
                logging.info(f"Cleaning up repository at: {local_path}")
                
                # Windows fix: Remove read-only attributes
                self._remove_readonly(local_path)
                
                # Now delete
                shutil.rmtree(local_path)
                logging.info("Cleanup successful")
                return True
            return False
            
        except Exception as e:
            logging.error(f"Error cleaning up cloned repo from disk: {str(e)}")
            return False

    def _remove_readonly(self, path: str):
        """
        Remove read-only attribute from files (Windows fix).
        
        Args:
            path: Directory path to process
        """
        import stat
        
        def handle_remove_readonly(func, path, exc_info):
            """Error handler for Windows permission issues."""
            # If permission error, make file writable and retry
            if not os.access(path, os.W_OK):
                # Change file permissions to writable
                os.chmod(path, stat.S_IWUSR | stat.S_IREAD)
                # Retry the operation
                func(path)
            else:
                raise
        
        try:
            # Walk through all files and remove read-only
            for root, dirs, files in os.walk(path):
                for d in dirs:
                    dir_path = os.path.join(root, d)
                    os.chmod(dir_path, stat.S_IWUSR | stat.S_IREAD)
                for f in files:
                    file_path = os.path.join(root, f)
                    os.chmod(file_path, stat.S_IWUSR | stat.S_IREAD)
        except Exception as e:
            logging.warning(f"Could not remove read-only attributes: {str(e)}")


    def check_repo_exists(self,repo_url : str) -> bool:

        """ Check if github repository exists"""

        try: 

            repo_name = self._get_repo_name(repo_url=repo_url)
            api_url = "https://api.github.com/repos/{repo_name}"
            headers = {"Authorization": f"token {config.github_token}"}

            response = requests.get(url = api_url,headers=headers )

            if response.status_code ==200:
                logging.info(f"repo named : {repo_name} exists and acessible")
                return True
            
            elif response.status_code == 401:
                logging.info(f"repo ({repo_name}) exists but is private")
                return False
            else:
                logging.error(f"repo check failed with status : {response.status_code} ")
                return False

        except Exception as e: 
            logging.error(f"repository check failed with status")
            return False
        


