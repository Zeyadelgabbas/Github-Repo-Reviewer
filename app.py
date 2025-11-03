import streamlit as st
import os
from datetime import datetime
from Src.agents import CodeReviewOrchestrator, create_initial_state
from Src.agents.code_reviewer import CodeReviewer
from Src.agents.repo_analyzer import RepositoryAnalyzer
from Src.utils import ReportFormatter, get_logger
from Src.tools import GitHubTools

# Configure page
st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🤖",
    layout="wide"
)

# Initialize logger
logging = get_logger(__name__)

# Custom CSS (same as before)
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border-radius: 5px;
        height: 3em;
        font-weight: bold;
    }
    .cost-box {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #FFF3CD;
        border: 2px solid #FFC107;
        color: #856404;
        font-size: 1.1em;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "report" not in st.session_state:
        st.session_state.report = None
    if "local_path" not in st.session_state:
        st.session_state.local_path = None
    if "analyzing" not in st.session_state:
        st.session_state.analyzing = False
    if "cost_estimated" not in st.session_state:
        st.session_state.cost_estimated = False
    if "cost_info" not in st.session_state:
        st.session_state.cost_info = None
    if "pending_state" not in st.session_state:
        st.session_state.pending_state = None

def add_message(role: str, content: str):
    """Add message to chat history."""
    st.session_state.messages.append({"role": role, "content": content})

def estimate_analysis_cost(repo_url: str):
    """
    Estimate cost of analysis without running it.
    
    Args:
        repo_url: GitHub repository URL
    """
    try:
        add_message("user", f"Analyze: {repo_url}")
        add_message("assistant", "🔄 Preparing cost estimate...")
        
        # Step 1: Analyze repository
        with st.spinner("📂 Cloning and analyzing repository structure..."):
            analyzer = RepositoryAnalyzer()
            initial_state = create_initial_state(repo_url)
            state = analyzer.analyze(initial_state)
        
        if state["errors"]:
            error_msg = "\n".join(state["errors"])
            add_message("assistant", f"❌ Failed to analyze repository:\n{error_msg}")
            return
        
        st.session_state.local_path = state.get("local_path")
        
        # Step 2: Estimate cost
        with st.spinner("💰 Calculating cost estimate..."):
            reviewer = CodeReviewer()
            cost_info = reviewer.estimate_cost(state)
        
        if not cost_info:
            add_message("assistant", f"❌ Failed to estimate cost: {cost_info['error']}")
            return
        
        # Store for later use
        st.session_state.cost_info = cost_info
        st.session_state.pending_state = state
        st.session_state.cost_estimated = True
        
        # Show cost estimate
        cost_msg = f"""💰 **Cost Estimate**

**Repository:** {state.get('repo_name', 'Unknown')}
**Files to Analyze:** {len(state['files_to_review'])}
**Estimated Cost:** ${cost_info:.4f} USD

Click **Confirm & Analyze** below to proceed with the analysis.
"""
        add_message("assistant", cost_msg)
        
    except Exception as e:
        logging.error(f"Cost estimation failed: {str(e)}")
        add_message("assistant", f"❌ Error: {str(e)}")

def run_analysis_with_confirmation():
    """Run analysis after user confirms cost."""
    try:
        state = st.session_state.pending_state
        cost_info = st.session_state.cost_info
        
        add_message("assistant", f"✅ Proceeding with analysis (estimated cost: ${cost_info:.4f})")
        
        # Run code review (skip cost check since we already confirmed)
        with st.spinner("🔍 Analyzing code... This may take 1-2 minutes."):
            reviewer = CodeReviewer()
            final_state = reviewer.review(state)
        
        # Check for errors
        if final_state["errors"]:
            error_msg = "\n".join(final_state["errors"])
            add_message("assistant", f"❌ Analysis completed with errors:\n{error_msg}")
            return
        
        # Generate report
        with st.spinner("📝 Generating report..."):
            formatter = ReportFormatter()
            report = formatter.generate_report(final_state)
            st.session_state.report = report
        
        # Success message
        summary = final_state.get("summary", {})
        issues_found = final_state.get("total_issues_found", 0)
        
        success_msg = f"""✅ **Analysis Complete!**

**Repository:** {final_state.get('repo_name', 'Unknown')}
**Files Analyzed:** {final_state.get('total_files_analyzed', 0)}
**Issues Found:** {issues_found}
**Overall Quality:** {summary.get('overall_quality', 'N/A')}/10
**Production Ready:** {'✅ Yes' if summary.get('production_ready') else '❌ No'}
"""
        add_message("assistant", success_msg)
        add_message("assistant", "📄 **Full Report:**\n\n" + report)
        
        # Reset cost estimation state
        st.session_state.cost_estimated = False
        st.session_state.cost_info = None
        st.session_state.pending_state = None
        
    except Exception as e:
        logging.error(f"Analysis failed: {str(e)}")
        add_message("assistant", f"❌ Error: {str(e)}")

def cleanup_repository():
    """Clean up cloned repository."""
    if st.session_state.local_path:
        try:
            github_tools = GitHubTools()
            success = github_tools.cleanup_repository(st.session_state.local_path)
            
            if success:
                st.success("✅ Cloned repository cleaned up successfully!")
                st.session_state.local_path = None
            else:
                st.warning("⚠️ Repository might not exist or already cleaned up.")
                
        except Exception as e:
            st.error(f"❌ Cleanup failed: {str(e)}")
    else:
        st.info("ℹ️ No repository to clean up.")

def main():
    """Main application."""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("🤖 AI Code Review Agent")
    st.markdown("Powered by LangChain, LangGraph & OpenAI GPT-5")
    
    # Sidebar (same as before)
    with st.sidebar:
        st.header("⚙️ Settings")
        
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            st.success("✅ OpenAI API Key loaded")
        else:
            st.error("❌ OpenAI API Key not found!")
            st.info("Add OPENAI_API_KEY to your .env file")
        
        st.markdown("---")
        
        st.header("📖 How to Use")
        st.markdown("""
1. Enter a GitHub repository URL
2. Click **Estimate Cost**
3. Review the cost estimate
4. Click **Confirm & Analyze**
5. Wait for analysis (1-2 minutes)
6. View the comprehensive report
7. Download the report
8. Clean up when done
        """)
        
        st.markdown("---")
        
        st.header("🧹 Cleanup")
        if st.button("🗑️ Delete Cloned Repository", key="cleanup"):
            cleanup_repository()
        
        if st.session_state.local_path:
            st.info(f"📁 Current clone:\n`{st.session_state.local_path}`")
        else:
            st.info("ℹ️ No active repository clone")
        
        st.markdown("---")
        
        st.header("ℹ️ About")
        st.markdown("""
This tool uses AI to analyze code repositories and provide:
- Project understanding
- Security analysis
- Bug detection
- Performance insights
- Enhancement suggestions
        """)
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        repo_url = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/username/repository",
            help="Enter a public GitHub repository URL",
            disabled=st.session_state.cost_estimated  # Disable if waiting for confirmation
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Show appropriate button based on state
        if not st.session_state.cost_estimated:
            estimate_button = st.button(
                "💰 Estimate Cost",
                disabled=st.session_state.analyzing
            )
        else:
            estimate_button = False
    
    # Handle estimate button
    if estimate_button and repo_url:
        if not repo_url.startswith("https://github.com/"):
            st.error("❌ Invalid URL. Must be a GitHub repository URL.")
        else:
            st.session_state.analyzing = True
            st.session_state.messages = []
            st.session_state.report = None
            
            estimate_analysis_cost(repo_url)
            
            st.session_state.analyzing = False
            st.rerun()
    
    # Display chat messages
    st.markdown("---")
    st.header("💬 Analysis Chat")
    
    if st.session_state.messages:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    else:
        st.info("👆 Enter a GitHub repository URL above to start")
    
    # Show confirmation button if cost is estimated
    if st.session_state.cost_estimated:
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("✅ Confirm & Analyze", use_container_width=True, type="primary"):
                st.session_state.analyzing = True
                run_analysis_with_confirmation()
                st.session_state.analyzing = False
                st.rerun()
            
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.cost_estimated = False
                st.session_state.cost_info = None
                st.session_state.pending_state = None
                add_message("assistant", "❌ Analysis cancelled by user")
                st.rerun()
    
    # Download button
    if st.session_state.report:
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"code_review_report_{timestamp}.md"
            
            st.download_button(
                label="📥 Download Report as Markdown",
                data=st.session_state.report,
                file_name=filename,
                mime="text/markdown",
                use_container_width=True
            )

if __name__ == "__main__":
    main()
