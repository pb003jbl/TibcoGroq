import streamlit as st
import os
from utils.groq_client import GroqClient
from utils.formatters import format_test_cases, format_complexity_analysis

# Page configuration
st.set_page_config(
    page_title="TIBCO Developer Assistant",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Groq client
@st.cache_resource
def get_groq_client(api_key):
    return GroqClient(api_key)

def main():
    # Header
    st.title("🔧 TIBCO Developer Assistant")
    st.markdown("*Powered by Groq Llama 3.3 70b for intelligent TIBCO BusinessWorks analysis*")
    
    # Sidebar for model selection
    st.sidebar.header("⚙️ Configuration")
    
    # API Key input
    default_api_key = os.getenv("GROQ_API_KEY", "")
    api_key = st.sidebar.text_input(
        "Groq API Key",
        value=default_api_key,
        type="password",
        help="Enter your Groq API key. Get one from https://console.groq.com/keys"
    )
    
    if not api_key:
        st.sidebar.error("⚠️ Please enter your Groq API key to use the application")
        st.error("⚠️ Groq API key is required. Please enter it in the sidebar.")
        st.stop()
    
    model_options = [
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile", 
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768"
    ]
    
    selected_model = st.sidebar.selectbox(
        "Select AI Model",
        options=model_options,
        index=0,
        help="Choose the Groq model for analysis"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 Instructions")
    st.sidebar.markdown("""
    **Getting Started:**
    - Enter your Groq API key above (get one from console.groq.com)
    - Select your preferred AI model
    
    **Test Case Generator:**
    - Paste your TIBCO BW process XML or code
    - Generate comprehensive test scenarios
    - Get input values, expected results, and edge cases
    
    **Code Complexity Analyzer:**
    - Analyze TIBCO code structure
    - Identify nested logic and dependencies
    - Detect anti-patterns and issues
    """)
    
    # Main tabs
    tab1, tab2 = st.tabs(["🧪 Test Case Generator", "📊 Code Complexity Analyzer"])
    
    groq_client = get_groq_client(api_key)
    
    with tab1:
        test_case_generator_tab(groq_client, selected_model)
    
    with tab2:
        complexity_analyzer_tab(groq_client, selected_model)

def test_case_generator_tab(groq_client, model):
    st.header("🧪 Test Case Generator")
    st.markdown("Generate comprehensive test cases for your TIBCO BusinessWorks processes")
    
    # Input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        code_input = st.text_area(
            "TIBCO BW Process Code/XML",
            height=300,
            placeholder="""Paste your TIBCO BusinessWorks process XML or code here...

Example:
<pd:ProcessDefinition xmlns:pd="http://xmlns.tibco.com/bw/process/2003">
    <pd:name>SampleProcess</pd:name>
    <pd:startName>Start</pd:startName>
    <!-- Your TIBCO process definition -->
</pd:ProcessDefinition>""",
            key="test_case_input"
        )
    
    with col2:
        st.markdown("### 🎯 Test Case Types")
        test_types = st.multiselect(
            "Select test scenarios to generate:",
            options=[
                "Happy Path Tests",
                "Edge Cases",
                "Error Scenarios", 
                "Boundary Value Tests",
                "Integration Tests",
                "Performance Tests"
            ],
            default=["Happy Path Tests", "Edge Cases", "Error Scenarios"]
        )
        
        complexity_level = st.selectbox(
            "Test Complexity Level",
            options=["Basic", "Intermediate", "Advanced"],
            index=1
        )
    
    # Generate button
    if st.button("🚀 Generate Test Cases", type="primary", use_container_width=True):
        if not code_input.strip():
            st.error("⚠️ Please provide TIBCO code/XML to analyze")
            return
        
        if not test_types:
            st.error("⚠️ Please select at least one test scenario type")
            return
        
        with st.spinner(f"🤖 Generating test cases using {model}..."):
            try:
                test_cases = groq_client.generate_test_cases(
                    code_input, 
                    test_types, 
                    complexity_level,
                    model
                )
                
                if test_cases:
                    st.success("✅ Test cases generated successfully!")
                    
                    # Display results
                    st.markdown("## 📋 Generated Test Cases")
                    formatted_output = format_test_cases(test_cases)
                    st.markdown(formatted_output)
                    
                    # Copy button
                    if st.button("📋 Copy Test Cases to Clipboard"):
                        st.code(test_cases, language="text")
                        st.info("💡 Test cases displayed above - copy manually from the code block")
                else:
                    st.error("❌ Failed to generate test cases. Please try again.")
                    
            except Exception as e:
                st.error(f"❌ Error generating test cases: {str(e)}")

def complexity_analyzer_tab(groq_client, model):
    st.header("📊 Code Complexity Analyzer")
    st.markdown("Analyze TIBCO code complexity, dependencies, and identify potential issues")
    
    # Input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        code_input = st.text_area(
            "TIBCO Code/Process Definition",
            height=300,
            placeholder="""Paste your TIBCO BusinessWorks code, process definition, or XML here...

The analyzer will examine:
- Nested logic complexity
- Dependency patterns
- Anti-patterns
- Performance implications
- Maintainability issues""",
            key="complexity_input"
        )
    
    with col2:
        st.markdown("### 🔍 Analysis Focus")
        analysis_types = st.multiselect(
            "Select analysis areas:",
            options=[
                "Cyclomatic Complexity",
                "Dependency Analysis",
                "Anti-pattern Detection",
                "Performance Issues",
                "Maintainability Score",
                "Security Concerns"
            ],
            default=["Cyclomatic Complexity", "Dependency Analysis", "Anti-pattern Detection"]
        )
        
        detail_level = st.selectbox(
            "Analysis Detail Level",
            options=["Summary", "Detailed", "Comprehensive"],
            index=1
        )
    
    # Analyze button
    if st.button("🔬 Analyze Code Complexity", type="primary", use_container_width=True):
        if not code_input.strip():
            st.error("⚠️ Please provide TIBCO code to analyze")
            return
        
        if not analysis_types:
            st.error("⚠️ Please select at least one analysis area")
            return
        
        with st.spinner(f"🤖 Analyzing code complexity using {model}..."):
            try:
                analysis_result = groq_client.analyze_complexity(
                    code_input,
                    analysis_types,
                    detail_level,
                    model
                )
                
                if analysis_result:
                    st.success("✅ Code analysis completed!")
                    
                    # Display results
                    st.markdown("## 📈 Complexity Analysis Results")
                    formatted_output = format_complexity_analysis(analysis_result)
                    st.markdown(formatted_output)
                    
                    # Copy button
                    if st.button("📋 Copy Analysis Results"):
                        st.code(analysis_result, language="text")
                        st.info("💡 Analysis results displayed above - copy manually from the code block")
                else:
                    st.error("❌ Failed to analyze code complexity. Please try again.")
                    
            except Exception as e:
                st.error(f"❌ Error analyzing code: {str(e)}")

if __name__ == "__main__":
    main()
