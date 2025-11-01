import os
from typing import List, Dict, Set , Any
from pathlib import Path
from ..utils import get_logger, config

logging = get_logger(__name__)

class FileScanner:
    """Scans repository for code files to review."""
    
    def __init__(self):
        # Get configuration from config.yaml
        self.supported_extensions = config.get('review.supported_extensions')
        self.ignore_patterns = config.get('review.ignore_patterns')
        self.max_files = config.get('review.max_files')
        
        logging.info(f"FileScanner initialized with {len(self.supported_extensions)} supported extensions")
    
    def scan_repository(self, repo_path: str) -> Dict[str, any]:
        """
        Scan the repo and return info about the files 

        Args: 
            repo_path : path to the cloned repo locally

        returns:
            Dictionary contatining : (total_files , files_to_review : list , file_structure : tree structure , language_stats)
        """

        try:
            # Getting all supported code files in repo
            all_files = self._find_code_files(repo_path=repo_path)
            logging.info(f"Found {len(all_files)} code files in {repo_path}")
            if len(all_files) > self.max_files:
                all_files = all_files[:self.max_files]

            # Getting file structure
            file_structure = self._build_file_structure( files_to_review = all_files)

            # Getting language statistics
            language_stats = self._get_language_stats(all_files)

            result = {
                'total_files': len(all_files),
                "files_to_review" : all_files , 
                "file_structure" : file_structure,
                "language_stats" : language_stats
            }
            logging.info(f"Scan completed {len(all_files)} files ready for review")

            return result


        except Exception as e: 
            logging.error(f"Error scanning the repo {repo_path} : {e}")
            raise e
    
    def _find_code_files(self, repo_path: str) -> List[str]:
        """" returns all supported code files found in a local repository """
        try: 
            code_files = []
            for root , dirs , files  in os.walk(repo_path): 

                dirs[:] = [d for d in dirs if not self._should_ignore(d)]
                
                for file in files:
                    file_path = os.path.join(root,file)
                    if self._is_supported_file(filename=file):
                        
                        file_path = os.path.relpath(file_path,repo_path)
                        code_files.append(file_path)

            return code_files

        except Exception as e: 
            logging.error(f"Error finding code files : {e} ")
            raise e
            
    def _should_ignore(self, directory: str) -> bool:

        """"
        Checks if the directory should be ignored

        returns : True if the directory in the ignored pattern
        """
       
        for pattern in self.ignore_patterns:
            clean_pattern = pattern.strip("*").strip("/")

            if clean_pattern == directory or pattern in directory:
                return True
           
        return False
    
       
    def _is_supported_file(self, filename: str) -> bool:
       
        """ Check if the file is a valid supported code file """

        try: 

            ext = os.path.splitext(filename)[1]
            if ext in self.supported_extensions:
                return True
            else:
                return False
        except Exception as e: 
            raise e  
    
    def _build_file_structure(self,files_to_review: list) -> Dict[str,Any]:

        """" Build the structure of the repository """
        structure = {}

        for file in files_to_review:

            current = structure
            parts = file.split(os.sep)

            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}

                current = current[part]

            file_name = parts[-1]
            current[file_name] = "file"

        return structure
        
        
    def _get_language_stats(self, files: List[str]) -> Dict[str, int]:
        
        """ Counts the files by programming language and extension"""

        stats = {}

        for file in files:
            ext = os.path.splitext(file)[1]
            stats[ext] = stats.get(ext,0) + 1

        return stats
    
    def read_file_content(self, repo_path: str, file_path: str) -> str:

        """" 
        Reads the content of files safely 

        Returns : 
            file content as string
        """

        try:
            full_path = os.path.join(repo_path,file_path)

            with open(full_path,'r',encoding='utf-8') as f:
                content = f.read()

            logging.info(f"sucess reading file : {file_path} with {len(content)} characters")

            return content

        except UnicodeDecodeError as e:
            logging.error(f"Couldnt decode file {file_path} error : {e}")
            raise e 
        
        except Exception as e:
            logging.error(f"Error reading file content from {file_path} : {e}")
            raise e
