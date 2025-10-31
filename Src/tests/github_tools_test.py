from Src.tools.github_tools import GitHubTools

# Create tools instance
tools = GitHubTools()

# Test cloning
result = tools.clone_repository("https://github.com/Zeyadelgabbas/dialogue-summarization")

print(f"Success: {result['success']}")
print(f"Local path: {result['local_path']}")
print(f"Repo name: {result['repo_name']}")

# Cleanup
if result['success']:
    tools.cleanup_repository(result['local_path'])
    