from typing import Dict, Any, List
from datetime import datetime
from ..utils import get_logger

logging = get_logger(__name__)

class ReportFormatter:
    """
    Formats code review analysis results into readable markdown reports.
    
    Takes structured JSON data and converts it to human-friendly format.
    """
    
    def __init__(self):
        """Initialize report formatter."""
        logging.info("ReportFormatter initialized")
    
    def generate_report(self, state: Dict[str, Any]) -> str:
        """
        Generate comprehensive markdown report from state.
        
        This is the main method that creates the complete report.
        
        Args:
            state: Workflow state containing all analysis results
            
        Returns:
            Markdown-formatted report as string
        """
        logging.info("Generating comprehensive report...")
        
        # Build report sections
        sections = []
        
        # Header
        sections.append(self._generate_header(state))
        
        # Table of Contents
        sections.append(self._generate_toc())
        
        # Executive Summary
        if state.get("summary"):
            sections.append(self._generate_executive_summary(state["summary"]))
        
        # Project Understanding
        if state.get("understanding"):
            sections.append(self._generate_understanding_section(state["understanding"]))
        
        # Code Review Findings
        if state.get("code_review"):
            sections.append(self._generate_code_review_section(state["code_review"]))
        
        # Enhancement Suggestions
        if state.get("enhancements"):
            sections.append(self._generate_enhancements_section(state["enhancements"]))
        
        # Documentation Assessment
        if state.get("documentation"):
            sections.append(self._generate_documentation_section(state["documentation"]))
        
        # Footer
        sections.append(self._generate_footer(state))
        
        # Join all sections
        report = "\n\n---\n\n".join(sections)
        
        logging.info("Report generated successfully")
        return report
    
    def _generate_header(self, state: Dict[str, Any]) -> str:
        """
        Generate report header with metadata.
        
        Args:
            state: Workflow state
            
        Returns:
            Markdown header
        """
        repo_name = state.get("repo_name", "Unknown Repository")
        repo_url = state.get("repo_url", "")
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        header = f"""# 🤖 AI Code Review Report

## Repository: {repo_name}

**URL:** {repo_url}  
**Analysis Date:** {timestamp}  
**Files Analyzed:** {state.get('total_files_analyzed', 0)}  
**Issues Found:** {state.get('total_issues_found', 0)}
"""
        return header
    
    def _generate_toc(self) -> str:
        """
        Generate table of contents.
        
        Returns:
            Markdown table of contents
        """
        toc = """## 📋 Table of Contents

1. [Executive Summary](#-executive-summary)
2. [Project Understanding](#-project-understanding)
3. [Code Review Findings](#-code-review-findings)
   - [Security Issues](#security-issues)
   - [Bugs & Errors](#bugs--errors)
   - [Performance Issues](#performance-issues)
   - [Code Quality](#code-quality)
   - [Architecture](#architecture)
4. [Enhancement Suggestions](#-enhancement-suggestions)
5. [Documentation Assessment](#-documentation-assessment)
"""
        return toc
    
    def _generate_executive_summary(self, summary: Dict[str, Any]) -> str:
        """
        Generate executive summary section.
        
        Args:
            summary: Summary data from analysis
            
        Returns:
            Markdown executive summary
        """
        overall_quality = summary.get("overall_quality", "N/A")
        production_ready = "✅ Yes" if summary.get("production_ready", False) else "❌ No"
        
        # Severity counts
        critical = summary.get("critical_count", 0)
        high = summary.get("high_count", 0)
        medium = summary.get("medium_count", 0)
        low = summary.get("low_count", 0)
        
        section = f"""## 📊 Executive Summary

### Overall Assessment

**Quality Score:** {overall_quality}/10  
**Production Ready:** {production_ready}

### Issue Breakdown

| Severity | Count |
|----------|-------|
| 🔴 Critical | {critical} |
| 🟠 High | {high} |
| 🟡 Medium | {medium} |
| 🟢 Low | {low} |
| **Total** | **{critical + high + medium + low}** |

### Key Strengths
"""
        
        # Add strengths
        strengths = summary.get("strengths", [])
        if strengths:
            for strength in strengths:
                section += f"\n- ✅ {strength}"
        else:
            section += "\n- No specific strengths identified"
        
        section += "\n\n### Key Weaknesses"
        
        # Add weaknesses
        weaknesses = summary.get("weaknesses", [])
        if weaknesses:
            for weakness in weaknesses:
                section += f"\n- ⚠️ {weakness}"
        else:
            section += "\n- No major weaknesses identified"
        
        section += "\n\n### Top Recommendations"
        
        # Add main recommendations
        recommendations = summary.get("main_recommendations", [])
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                section += f"\n{i}. {rec}"
        else:
            section += "\n- Continue with current approach"
        
        return section
    
    def _generate_understanding_section(self, understanding: Dict[str, Any]) -> str:
        """
        Generate project understanding section.
        
        Args:
            understanding: Understanding data from analysis
            
        Returns:
            Markdown understanding section
        """
        section = f"""## 🎯 Project Understanding

### What This Project Does

{understanding.get('description', 'No description provided')}

### Project Type

**{understanding.get('project_type', 'Unknown')}**

### Tech Stack
"""
        
        # Add tech stack
        tech_stack = understanding.get("tech_stack", [])
        if tech_stack:
            for tech in tech_stack:
                section += f"\n- {tech}"
        else:
            section += "\n- Not specified"
        
        section += "\n\n### Key Features"
        
        # Add key features
        features = understanding.get("key_features", [])
        if features:
            for feature in features:
                section += f"\n- ✨ {feature}"
        else:
            section += "\n- No key features identified"
        
        section += "\n\n### Use Cases"
        
        # Add use cases
        use_cases = understanding.get("use_cases", [])
        if use_cases:
            for use_case in use_cases:
                section += f"\n- 🎯 {use_case}"
        else:
            section += "\n- No specific use cases identified"
        
        section += f"\n\n### Complexity Level\n\n**{understanding.get('complexity', 'Unknown').capitalize()}**"
        
        return section
    
    def _generate_code_review_section(self, code_review: Dict[str, Any]) -> str:
        """
        Generate code review findings section.
        
        Args:
            code_review: Code review data with all issues
            
        Returns:
            Markdown code review section
        """
        section = "## 🔍 Code Review Findings\n"
        
        # Security Issues
        section += "\n### 🔒 Security Issues\n"
        security_issues = code_review.get("security", [])
        if security_issues:
            section += f"\n**Found {len(security_issues)} security issue(s)**\n"
            section += self._format_issues(security_issues)
        else:
            section += "\n✅ No security issues found!\n"
        
        # Bugs & Errors
        section += "\n### 🐛 Bugs & Errors\n"
        bugs = code_review.get("bugs", [])
        if bugs:
            section += f"\n**Found {len(bugs)} bug(s)**\n"
            section += self._format_issues(bugs)
        else:
            section += "\n✅ No bugs found!\n"
        
        # Performance Issues
        section += "\n### ⚡ Performance Issues\n"
        performance = code_review.get("performance", [])
        if performance:
            section += f"\n**Found {len(performance)} performance issue(s)**\n"
            section += self._format_issues(performance)
        else:
            section += "\n✅ No performance issues found!\n"
        
        # Code Quality
        section += "\n### 📝 Code Quality\n"
        quality = code_review.get("code_quality", [])
        if quality:
            section += f"\n**Found {len(quality)} code quality issue(s)**\n"
            section += self._format_issues(quality)
        else:
            section += "\n✅ Code quality looks good!\n"
        
        # Architecture
        section += "\n### 🏛️ Architecture\n"
        architecture = code_review.get("architecture", [])
        if architecture:
            section += f"\n**{len(architecture)} architectural concern(s)**\n"
            for i, issue in enumerate(architecture, 1):
                section += f"\n#### {i}. {issue.get('issue', 'Unknown issue')}\n"
                section += f"\n**Recommendation:** {issue.get('recommendation', 'No recommendation')}\n"
                section += f"\n**Impact:** {issue.get('impact', 'Unknown impact')}\n"
        else:
            section += "\n✅ Architecture looks solid!\n"
        
        return section
    
    def _format_issues(self, issues: List[Dict[str, Any]]) -> str:
        """
        Format a list of issues as markdown.
        
        Args:
            issues: List of issue dictionaries
            
        Returns:
            Formatted markdown string
        """
        if not issues:
            return "\n✅ None found\n"
        
        formatted = ""
        
        for i, issue in enumerate(issues, 1):
            severity = issue.get("severity", "unknown")
            severity_icon = self._get_severity_icon(severity)
            
            formatted += f"\n#### {i}. {severity_icon} {issue.get('issue', 'Unknown issue')}\n"
            formatted += f"\n- **Severity:** {severity.capitalize()}\n"
            formatted += f"- **File:** `{issue.get('file', 'Unknown')}`\n"
            
            if issue.get("line"):
                formatted += f"- **Line:** {issue.get('line')}\n"
            
            if issue.get("category"):
                formatted += f"- **Category:** {issue.get('category')}\n"
            
            formatted += f"\n**Fix:** {issue.get('fix', 'No fix provided')}\n"
            
            if issue.get("impact"):
                formatted += f"\n**Impact:** {issue.get('impact')}\n"
        
        return formatted
    
    def _get_severity_icon(self, severity: str) -> str:
        """
        Get emoji icon for severity level.
        
        Args:
            severity: Severity level string
            
        Returns:
            Emoji icon
        """
        severity_lower = severity.lower()
        
        icons = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢"
        }
        
        return icons.get(severity_lower, "⚪")
    
    def _generate_enhancements_section(self, enhancements: List[Dict[str, Any]]) -> str:
        """
        Generate enhancement suggestions section.
        
        Args:
            enhancements: List of enhancement suggestions
            
        Returns:
            Markdown enhancements section
        """
        section = "## 💡 Enhancement Suggestions\n"
        
        if not enhancements:
            section += "\n✅ No enhancement suggestions at this time.\n"
            return section
        
        # Group by priority
        high = [e for e in enhancements if e.get("priority") == "high"]
        medium = [e for e in enhancements if e.get("priority") == "medium"]
        low = [e for e in enhancements if e.get("priority") == "low"]
        
        if high:
            section += "\n### 🔴 High Priority\n"
            section += self._format_enhancements(high)
        
        if medium:
            section += "\n### 🟡 Medium Priority\n"
            section += self._format_enhancements(medium)
        
        if low:
            section += "\n### 🟢 Low Priority\n"
            section += self._format_enhancements(low)
        
        return section
    
    def _format_enhancements(self, enhancements: List[Dict[str, Any]]) -> str:
        """
        Format enhancement suggestions.
        
        Args:
            enhancements: List of enhancements
            
        Returns:
            Formatted markdown
        """
        formatted = ""
        
        for i, enhancement in enumerate(enhancements, 1):
            formatted += f"\n#### {i}. {enhancement.get('title', 'Untitled Enhancement')}\n"
            formatted += f"\n{enhancement.get('description', 'No description')}\n"
            formatted += f"\n- **Impact:** {enhancement.get('impact', 'Unknown')}\n"
            formatted += f"- **Effort:** {enhancement.get('effort', 'Unknown')}\n"
        
        return formatted
    
    def _generate_documentation_section(self, documentation: Dict[str, Any]) -> str:
        """
        Generate documentation assessment section.
        
        Args:
            documentation: Documentation assessment data
            
        Returns:
            Markdown documentation section
        """
        section = "## 📚 Documentation Assessment\n"
        
        readme_quality = documentation.get("readme_quality", 0)
        section += f"\n### README Quality: {readme_quality}/10\n"
        
        # Status checks
        section += "\n### Documentation Status\n"
        section += f"\n- Installation Guide: {'✅' if documentation.get('has_installation_guide') else '❌'}\n"
        section += f"- Usage Examples: {'✅' if documentation.get('has_usage_examples') else '❌'}\n"
        section += f"- API Documentation: {'✅' if documentation.get('has_api_docs') else '❌'}\n"
        
        # Missing items
        missing = documentation.get("missing", [])
        if missing:
            section += "\n### Missing Documentation\n"
            for item in missing:
                section += f"\n- ❌ {item}"
        
        # Recommendations
        recommendations = documentation.get("recommendations", [])
        if recommendations:
            section += "\n\n### Recommendations\n"
            for i, rec in enumerate(recommendations, 1):
                section += f"\n{i}. {rec}"
        
        return section
    
    def _generate_footer(self, state: Dict[str, Any]) -> str:
        """
        Generate report footer.
        
        Args:
            state: Workflow state
            
        Returns:
            Markdown footer
        """
        footer = """## 🤖 About This Report

This report was generated by an AI-powered code review system using:
- **LangChain** for agent orchestration
- **LangGraph** for workflow management  
- **OpenAI GPT-4** for code analysis

**Note:** This is an automated analysis. While comprehensive, it should be reviewed by human developers for final decisions.
"""
        
        # Add timing info if available
        if state.get("start_time") and state.get("end_time"):
            footer += f"\n**Analysis Duration:** {self._calculate_duration(state)}"
        
        return footer
    
    def _calculate_duration(self, state: Dict[str, Any]) -> str:
        """
        Calculate analysis duration.
        
        Args:
            state: Workflow state
            
        Returns:
            Duration string
        """
        try:
            start = datetime.fromisoformat(state["start_time"])
            end = datetime.fromisoformat(state["end_time"])
            duration = end - start
            
            minutes = int(duration.total_seconds() / 60)
            seconds = int(duration.total_seconds() % 60)
            
            return f"{minutes}m {seconds}s"
        except:
            return "Unknown"
    
    def save_report(self, report: str, output_path: str) -> bool:
        """
        Save report to file.
        
        Args:
            report: Report content
            output_path: File path to save to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            
            logging.info(f"Report saved to: {output_path}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to save report: {str(e)}")
            return False