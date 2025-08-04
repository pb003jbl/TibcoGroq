import re
import streamlit as st

def format_test_cases(raw_output):
    """Format test case output for better display"""
    if not raw_output:
        return "No test cases generated."
    
    # Add some basic formatting for better readability
    formatted = raw_output
    
    # Make headers bold
    formatted = re.sub(r'^(#{1,3})\s*(.+)$', r'**\2**', formatted, flags=re.MULTILINE)
    
    # Format numbered sections
    formatted = re.sub(r'^(\d+\.)\s*\*\*(.+?)\*\*', r'### \1 \2', formatted, flags=re.MULTILINE)
    
    # Ensure proper spacing around sections
    formatted = re.sub(r'\n\n\n+', '\n\n', formatted)
    
    return formatted

def format_complexity_analysis(raw_output):
    """Format complexity analysis output for better display"""
    if not raw_output:
        return "No analysis results generated."
    
    formatted = raw_output
    
    # Make headers bold and properly sized
    formatted = re.sub(r'^(#{1,3})\s*(.+)$', r'**\2**', formatted, flags=re.MULTILINE)
    
    # Format numbered sections
    formatted = re.sub(r'^(\d+\.)\s*\*\*(.+?)\*\*', r'### \1 \2', formatted, flags=re.MULTILINE)
    
    # Highlight metrics and scores
    formatted = re.sub(r'(\w+\s+score:?\s*\d+(?:\.\d+)?(?:/\d+)?)', r'`\1`', formatted, flags=re.IGNORECASE)
    formatted = re.sub(r'(complexity:?\s*(?:low|medium|high))', r'`\1`', formatted, flags=re.IGNORECASE)
    
    # Format risk levels
    formatted = re.sub(r'\b(LOW|MEDIUM|HIGH|CRITICAL)\b', r'**\1**', formatted)
    
    # Ensure proper spacing
    formatted = re.sub(r'\n\n\n+', '\n\n', formatted)
    
    return formatted

def create_metrics_display(metrics_dict):
    """Create a formatted metrics display for complexity analysis"""
    if not metrics_dict:
        return ""
    
    cols = st.columns(len(metrics_dict))
    
    for i, (metric, value) in enumerate(metrics_dict.items()):
        with cols[i]:
            st.metric(label=metric, value=value)

def highlight_code_sections(code, language="xml"):
    """Highlight code sections for better readability"""
    return f"```{language}\n{code}\n```"
