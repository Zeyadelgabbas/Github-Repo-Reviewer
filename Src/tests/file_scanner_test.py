from Src.tools.file_tools import FileScanner
from Src.tools.github_tools import GitHubTools

# Clone a repo
github = GitHubTools()
result = github.clone_repository("https://github.com/Zeyadelgabbas/dialogue-summarization")

if result['success']:
    # Scan the repo
    scanner = FileScanner()
    scan_result = scanner.scan_repository(result['local_path'])
    
    print(f"Total files: {scan_result['total_files']}")
    print(f"Files to review: {len(scan_result['files_to_review'])}")
    print(f"Languages: {scan_result['language_stats']}")
    
    # Read a file
    if scan_result['files_to_review']:
        first_file = scan_result['files_to_review'][0]
        content = scanner.read_file_content(result['local_path'], first_file)
        print(f"\nFirst file content ({first_file}):")
        print(content)  # First 200 chars
    
    # Cleanup
    github.cleanup_repository(result['local_path'])