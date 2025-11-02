from typing import Dict, List

def get_system_prompt() -> str:
    """
    System prompt defining the AI's role and expertise.

    Returns:
        System prompt string
    """
    return """You are an expert software engineer and code reviewer with deep expertise in:

- Software architecture and design patterns
- Security best practices (OWASP Top 10, secure coding)
- Performance optimization and algorithmic efficiency
- Code quality and maintainability
- Multiple programming languages and frameworks
- Documentation and API design
- DevOps and deployment practices

Your goal is to provide comprehensive, actionable, and constructive feedback.
Be thorough but concise. Focus on real issues, not nitpicking."""


def get_comprehensive_review_prompt(
    repo_name: str,
    repo_content: str,
    file_structure: Dict,
    language_stats: Dict[str, int]
) -> str:
    """
    Create comprehensive prompt for full repository analysis.
    
    This single prompt asks GPT for EVERYTHING we need:
    - Project understanding
    - Code review
    - Enhancement suggestions
    - Documentation assessment
    
    Args:
        repo_name: Name of repository (e.g., "user/repo")
        repo_content: All code files concatenated
        file_structure: Dictionary of file tree
        language_stats: Count of files by extension
        
    Returns:
        Formatted prompt string
    """
    
    # Format file structure as text
    structure_text = _format_file_structure(file_structure)
    
    # Format language stats
    languages = ", ".join([f"{ext}: {count}" for ext, count in language_stats.items()])
    
    prompt = f"""# REPOSITORY ANALYSIS TASK

You are analyzing the repository: **{repo_name}**

## REPOSITORY STRUCTURE
```
{structure_text}
```

## LANGUAGE BREAKDOWN
{languages}

## COMPLETE REPOSITORY CODE
{repo_content}

---

# YOUR TASK

Provide a **comprehensive analysis** covering ALL of the following sections.
Return your response as a **valid JSON object** with this exact structure:
```json
{{
  "understanding": {{
    "description": "Clear 2-3 sentence description of what this project does",
    "project_type": "Type of project (e.g., 'Web Application', 'CLI Tool', 'Library', 'API')",
    "tech_stack": ["Primary language/framework", "Database", "Other key technologies"],
    "key_features": ["Feature 1", "Feature 2", "Feature 3"],
    "use_cases": ["When to use this", "Who should use this", "What problems it solves"],
    "complexity": "simple/moderate/complex"
  }},
  
  "code_review": {{
    "security": [
      {{
        "severity": "critical/high/medium/low",
        "file": "path/to/file.py",
        "line": 42,
        "issue": "Brief description of security issue",
        "fix": "How to fix it",
        "category": "SQL Injection/XSS/Auth/etc"
      }}
    ],
    "bugs": [
      {{
        "severity": "critical/high/medium/low",
        "file": "path/to/file.py",
        "line": 15,
        "issue": "Description of bug",
        "fix": "How to fix it"
      }}
    ],
    "performance": [
      {{
        "severity": "high/medium/low",
        "file": "path/to/file.py",
        "line": 78,
        "issue": "Performance problem",
        "fix": "Optimization suggestion",
        "impact": "Expected improvement (e.g., '3x faster')"
      }}
    ],
    "code_quality": [
      {{
        "severity": "medium/low",
        "file": "path/to/file.py",
        "line": 23,
        "issue": "Code quality issue",
        "fix": "How to improve",
        "category": "Complexity/Duplication/Naming/etc"
      }}
    ],
    "architecture": [
      {{
        "issue": "Architectural concern",
        "recommendation": "How to improve architecture",
        "impact": "Benefits of change"
      }}
    ]
  }},
  
  "enhancements": [
    {{
      "priority": "high/medium/low",
      "title": "Brief enhancement title",
      "description": "What to add/improve",
      "impact": "Why this matters",
      "effort": "low/medium/high"
    }}
  ],
  
  "documentation": {{
    "readme_quality": 7,
    "has_installation_guide": true,
    "has_usage_examples": false,
    "has_api_docs": false,
    "missing": ["What's missing in docs"],
    "recommendations": ["How to improve documentation"]
  }},
  
  "summary": {{
    "overall_quality": 7,
    "strengths": ["Key strength 1", "Key strength 2"],
    "weaknesses": ["Key weakness 1", "Key weakness 2"],
    "critical_count": 2,
    "high_count": 5,
    "medium_count": 12,
    "low_count": 8,
    "production_ready": false,
    "main_recommendations": ["Top recommendation 1", "Top recommendation 2", "Top recommendation 3"]
  }}
}}
```

---

# GUIDELINES

1. **Be Specific**: Include exact file names and line numbers
2. **Be Actionable**: Provide clear fixes, not just problems
3. **Prioritize**: Focus on critical/high severity issues first
4. **Be Realistic**: Consider the project's scope and purpose
5. **Be Constructive**: Suggest improvements, not just criticisms

## SEVERITY LEVELS
- **Critical**: Security vulnerabilities, data loss risks, crashes
- **High**: Major bugs, significant performance issues, serious security concerns
- **Medium**: Code quality issues, minor bugs, optimization opportunities
- **Low**: Style improvements, minor refactoring suggestions

## IMPORTANT
- Return ONLY the JSON object, no additional text before or after
- Ensure the JSON is properly formatted and valid
- If no issues found in a category, use empty array: []
- Be thorough but focus on the most important findings
"""
    
    return prompt


def _format_file_structure(structure: Dict, indent: int = 0) -> str:
    """
    Format file structure dictionary as readable tree.
    
    Args:
        structure: Nested dictionary of files/folders
        indent: Current indentation level
        
    Returns:
        Formatted tree string
    """
    lines = []
    
    for key, value in structure.items():
        if isinstance(value, dict):
            # It's a directory
            lines.append("  " * indent + f"📁 {key}/")
            # Recursively format subdirectories
            lines.append(_format_file_structure(value, indent + 1))
        else:
            # It's a file
            lines.append("  " * indent + f"📄 {key}")
    
    return "\n".join(lines)


def get_quick_review_prompt(repo_content: str) -> str:
    """
    Simplified prompt for quick reviews (optional - for faster analysis).
    
    Use this when you want fast results and don't need full analysis.
    
    Args:
        repo_content: Repository code
        
    Returns:
        Quick review prompt
    """
    return f"""Review this code and identify ONLY critical and high severity issues:

{repo_content}

Return JSON:
{{
  "critical_issues": [{{"file": "...", "line": 10, "issue": "...", "fix": "..."}}],
  "high_issues": [{{"file": "...", "line": 20, "issue": "...", "fix": "..."}}]
}}

Focus on: Security vulnerabilities, major bugs, data integrity issues.
Return ONLY valid JSON."""