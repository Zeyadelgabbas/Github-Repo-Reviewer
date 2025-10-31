import sys
from Src.agents import CodeReviewOrchestrator
from Src.utils import get_logger, config

# Create logger for main module
logging = get_logger(__name__)

def print_header():
    """Print application header to console (not logged)."""
    print("\n" + "=" * 70)
    print("🤖 CODE REVIEW & DOCUMENTATION AGENT")
    print("Powered by LangChain, LangGraph & OpenAI")
    print("=" * 70 + "\n")

def print_usage():
    """Print usage instructions."""
    print("Usage:")
    print("  python -m src.main <github_repo_url>")
    print("\nExample:")
    print("  python -m src.main https://github.com/username/repo")
    print()

def validate_repo_url(url: str) -> bool:
    """Validate GitHub repository URL."""
    if not url.startswith("https://github.com/"):
        logging.error(f"Invalid GitHub URL provided: {url}")
        print("❌ Error: Invalid GitHub URL. Must start with https://github.com/")
        return False
    return True

def print_results(final_state: dict):
    """Print final results to console."""
    print("\n" + "=" * 70)
    print("✓ WORKFLOW COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    
    print("\n📋 Workflow Messages:")
    for i, msg in enumerate(final_state["messages"], 1):
        print(f"  {i}. {msg}")
    
    print(f"\n📊 Final Status: {final_state['current_step']}")
    print(f"📁 Files Analyzed: {final_state['total_files_analyzed']}")
    print(f"⚠️  Issues Found: {final_state['total_issues_found']}")
    print(f"❌ Errors: {len(final_state['errors'])}")
    
    if final_state['errors']:
        print("\n🔴 Errors encountered:")
        for i, error in enumerate(final_state['errors'], 1):
            print(f"  {i}. {error}")
    
    print(f"\n💾 Logs saved to: logs/")
    print("=" * 70 + "\n")

def main():
    """Main function."""
    # Print header (UI only, not logged)
    print_header()
    
    # Log application start
    logging.info("=" * 70)
    logging.info("Application started")
    logging.info("=" * 70)
    
    # Check if repo URL is provided
    if len(sys.argv) < 2:
        logging.error("No repository URL provided in arguments")
        print("❌ Error: Please provide a GitHub repository URL\n")
        print_usage()
        sys.exit(1)
    
    repo_url = sys.argv[1]
    logging.info(f"Repository URL argument: {repo_url}")
    
    # Validate URL
    if not validate_repo_url(repo_url):
        sys.exit(1)
    
    # Print configuration
    print(f"📦 Repository: {repo_url}")
    print(f"🤖 Model: {config.model_name}")
    print(f"🌡️  Temperature: {config.temperature}")
    print(f"🔢 Max Tokens: {config.max_tokens}")
    print()
    
    # Log configuration
    logging.info(f"Configuration - Model: {config.model_name}")
    logging.info(f"Configuration - Temperature: {config.temperature}")
    logging.info(f"Configuration - Max Tokens: {config.max_tokens}")
    
    try:
        print("🚀 Starting workflow...\n")
        logging.info("Creating orchestrator instance")
        
        # Create orchestrator
        orchestrator = CodeReviewOrchestrator()
        
        # Run workflow
        logging.info("Running workflow")
        final_state = orchestrator.run(repo_url)
        
        # Display results
        print_results(final_state)
        
        logging.info("Application completed successfully")
        logging.info("=" * 70)
        
    except KeyboardInterrupt:
        logging.warning("Workflow interrupted by user (Ctrl+C)")
        print("\n⚠️  Workflow interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        logging.error(f"Application failed with error: {str(e)}")
        logging.exception("Detailed error traceback:")
        print(f"\n❌ Error: An error occurred - {str(e)}")
        print(f"💾 Check logs for details: logs/")
        sys.exit(1)

if __name__ == "__main__":
    main()
