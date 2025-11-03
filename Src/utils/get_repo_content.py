from ..agents import RepositoryAnalyzer , CodeReviewer , AgentState , create_initial_state
from ..tools import GitHubTools , FileScanner , LLMTools
from ..utils import get_logger

logging = get_logger(__name__)




def get_all_repo_content(repo_url: str):
        githubtools = GitHubTools()
        filescanner =FileScanner()
        codereview = CodeReviewer()
        llm = LLMTools()
        

        state = create_initial_state(repo_url)

        repo_results = githubtools.clone_repository(repo_url=repo_url)

        state['local_path'] = repo_results['local_path']
        state['repo_name']  = repo_results['repo_name']

    

        scan_results = filescanner.scan_repository(repo_path=state['local_path'])
        all_files = scan_results['files_to_review']
        file_structure = scan_results['file_structure']

        state['files_to_review'] = all_files
        state['file_structure'] = file_structure

        content = codereview._concatenate_files(state=state)

        return content 
if __name__ == '__main__':

    content = get_all_repo_content(repo_url='https://github.com/Zeyadelgabbas/Github-Repo-Reviewer')
    with open('all_files_content.txt','w',encoding='utf-8') as f :
          f.write(content)
          


