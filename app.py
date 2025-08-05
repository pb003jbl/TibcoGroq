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
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🧪 Test Case Generator", 
        "📊 Code Complexity Analyzer",
        "🔧 Process Optimizer",
        "📋 Documentation Generator", 
        "🚀 Migration Assistant"
    ])
    
    groq_client = get_groq_client(api_key)
    
    with tab1:
        test_case_generator_tab(groq_client, selected_model)
    
    with tab2:
        complexity_analyzer_tab(groq_client, selected_model)
    
    with tab3:
        process_optimizer_tab(groq_client, selected_model)
    
    with tab4:
        documentation_generator_tab(groq_client, selected_model)
    
    with tab5:
        migration_assistant_tab(groq_client, selected_model)

def test_case_generator_tab(groq_client, model):
    st.header("🧪 Test Case Generator")
    st.markdown("Generate comprehensive test cases for your TIBCO BusinessWorks processes")
    
    # Input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Input method selection
        input_method = st.radio(
            "Choose input method:",
            options=["Paste Code", "Upload File"],
            horizontal=True
        )
        
        code_input = ""
        
        if input_method == "Paste Code":
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
        else:
            uploaded_file = st.file_uploader(
                "Upload TIBCO file",
                type=['xml', 'txt', 'bwp', 'process'],
                help="Upload your TIBCO BusinessWorks process file (XML, BWP, or text format)"
            )
            
            if uploaded_file is not None:
                try:
                    # Read file content
                    file_content = uploaded_file.read()
                    
                    # Try to decode as text
                    try:
                        code_input = file_content.decode('utf-8')
                    except UnicodeDecodeError:
                        code_input = file_content.decode('latin-1')
                    
                    # Display file info
                    file_size = len(code_input)
                    st.info(f"📁 File loaded: {uploaded_file.name} ({file_size:,} characters)")
                    
                    # Show preview for large files
                    if file_size > 5000:
                        st.warning(f"⚠️ Large file detected ({file_size:,} characters). Preview shown below:")
                        with st.expander("📄 File Preview (first 2000 characters)"):
                            st.code(code_input[:2000] + "..." if len(code_input) > 2000 else code_input, language="xml")
                    else:
                        with st.expander("📄 File Content"):
                            st.code(code_input, language="xml")
                            
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
                    code_input = ""
    
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
        # Input method selection
        input_method = st.radio(
            "Choose input method:",
            options=["Paste Code", "Upload File"],
            horizontal=True,
            key="complexity_input_method"
        )
        
        code_input = ""
        
        if input_method == "Paste Code":
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
        else:
            uploaded_file = st.file_uploader(
                "Upload TIBCO file for analysis",
                type=['xml', 'txt', 'bwp', 'process'],
                help="Upload your TIBCO BusinessWorks process file (XML, BWP, or text format)",
                key="complexity_file_upload"
            )
            
            if uploaded_file is not None:
                try:
                    # Read file content
                    file_content = uploaded_file.read()
                    
                    # Try to decode as text
                    try:
                        code_input = file_content.decode('utf-8')
                    except UnicodeDecodeError:
                        code_input = file_content.decode('latin-1')
                    
                    # Display file info
                    file_size = len(code_input)
                    st.info(f"📁 File loaded: {uploaded_file.name} ({file_size:,} characters)")
                    
                    # Show preview for large files
                    if file_size > 5000:
                        st.warning(f"⚠️ Large file detected ({file_size:,} characters). Preview shown below:")
                        with st.expander("📄 File Preview (first 2000 characters)"):
                            st.code(code_input[:2000] + "..." if len(code_input) > 2000 else code_input, language="xml")
                    else:
                        with st.expander("📄 File Content"):
                            st.code(code_input, language="xml")
                            
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
                    code_input = ""
    
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

def process_optimizer_tab(groq_client, model):
    st.header("🔧 Process Optimizer")
    st.markdown("Optimize TIBCO processes for better performance, efficiency, and maintainability")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Input method selection
        input_method = st.radio(
            "Choose input method:",
            options=["Paste Code", "Upload File"],
            horizontal=True,
            key="optimizer_input_method"
        )
        
        code_input = ""
        
        if input_method == "Paste Code":
            code_input = st.text_area(
                "TIBCO Process Definition",
                height=300,
                placeholder="""Paste your TIBCO BusinessWorks process definition here...

The optimizer will analyze and suggest improvements for:
- Performance bottlenecks
- Resource utilization
- Error handling patterns
- Best practice implementations
- Memory optimization
- Connection pooling""",
                key="optimizer_input"
            )
        else:
            uploaded_file = st.file_uploader(
                "Upload TIBCO file for optimization",
                type=['xml', 'txt', 'bwp', 'process'],
                key="optimizer_file_upload"
            )
            
            if uploaded_file is not None:
                try:
                    file_content = uploaded_file.read()
                    try:
                        code_input = file_content.decode('utf-8')
                    except UnicodeDecodeError:
                        code_input = file_content.decode('latin-1')
                    
                    file_size = len(code_input)
                    st.info(f"📁 File loaded: {uploaded_file.name} ({file_size:,} characters)")
                    
                    if file_size > 5000:
                        st.warning(f"⚠️ Large file detected ({file_size:,} characters)")
                        with st.expander("📄 File Preview"):
                            st.code(code_input[:2000] + "..." if len(code_input) > 2000 else code_input, language="xml")
                    else:
                        with st.expander("📄 File Content"):
                            st.code(code_input, language="xml")
                            
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
                    code_input = ""
    
    with col2:
        st.markdown("### ⚡ Optimization Areas")
        optimization_areas = st.multiselect(
            "Select optimization focus:",
            options=[
                "Performance Tuning",
                "Memory Optimization",
                "Error Handling",
                "Connection Pooling",
                "Resource Management",
                "Async Processing",
                "Caching Strategies",
                "Load Balancing"
            ],
            default=["Performance Tuning", "Memory Optimization", "Error Handling"]
        )
        
        optimization_level = st.selectbox(
            "Optimization Level",
            options=["Conservative", "Moderate", "Aggressive"],
            index=1,
            help="Conservative: Safe optimizations only\nModerate: Balanced approach\nAggressive: Maximum performance gains"
        )
        
        include_code_examples = st.checkbox(
            "Include code examples",
            value=True,
            help="Generate optimized code snippets"
        )
    
    if st.button("⚡ Optimize Process", type="primary", use_container_width=True):
        if not code_input.strip():
            st.error("⚠️ Please provide TIBCO code to optimize")
            return
        
        if not optimization_areas:
            st.error("⚠️ Please select at least one optimization area")
            return
        
        with st.spinner(f"🤖 Analyzing and optimizing using {model}..."):
            try:
                optimization_result = groq_client.optimize_process(
                    code_input,
                    optimization_areas,
                    optimization_level,
                    include_code_examples,
                    model
                )
                
                if optimization_result:
                    st.success("✅ Process optimization completed!")
                    st.markdown("## ⚡ Optimization Recommendations")
                    st.markdown(optimization_result)
                else:
                    st.error("❌ Failed to optimize process. Please try again.")
                    
            except Exception as e:
                st.error(f"❌ Error optimizing process: {str(e)}")

def documentation_generator_tab(groq_client, model):
    st.header("📋 Documentation Generator")
    st.markdown("Generate comprehensive documentation for TIBCO processes and components")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        input_method = st.radio(
            "Choose input method:",
            options=["Paste Code", "Upload File"],
            horizontal=True,
            key="docs_input_method"
        )
        
        code_input = ""
        
        if input_method == "Paste Code":
            code_input = st.text_area(
                "TIBCO Code/Process Definition",
                height=300,
                placeholder="""Paste your TIBCO BusinessWorks code here...

Generate documentation including:
- Process overview and purpose
- Input/output specifications
- Component descriptions
- Data flow diagrams
- Error handling procedures
- Deployment guidelines""",
                key="docs_input"
            )
        else:
            uploaded_file = st.file_uploader(
                "Upload TIBCO file for documentation",
                type=['xml', 'txt', 'bwp', 'process'],
                key="docs_file_upload"
            )
            
            if uploaded_file is not None:
                try:
                    file_content = uploaded_file.read()
                    try:
                        code_input = file_content.decode('utf-8')
                    except UnicodeDecodeError:
                        code_input = file_content.decode('latin-1')
                    
                    file_size = len(code_input)
                    st.info(f"📁 File loaded: {uploaded_file.name} ({file_size:,} characters)")
                    
                    if file_size > 5000:
                        with st.expander("📄 File Preview"):
                            st.code(code_input[:2000] + "..." if len(code_input) > 2000 else code_input, language="xml")
                    else:
                        with st.expander("📄 File Content"):
                            st.code(code_input, language="xml")
                            
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
                    code_input = ""
    
    with col2:
        st.markdown("### 📖 Documentation Types")
        doc_types = st.multiselect(
            "Select documentation to generate:",
            options=[
                "Technical Overview",
                "API Documentation",
                "Deployment Guide",
                "User Manual",
                "Troubleshooting Guide",
                "Configuration Reference",
                "Performance Tuning",
                "Security Guidelines"
            ],
            default=["Technical Overview", "API Documentation", "Deployment Guide"]
        )
        
        doc_format = st.selectbox(
            "Documentation Format",
            options=["Markdown", "HTML", "Plain Text", "Confluence"],
            index=0
        )
        
        include_diagrams = st.checkbox(
            "Include ASCII diagrams",
            value=True,
            help="Generate ASCII flow diagrams where applicable"
        )
    
    if st.button("📝 Generate Documentation", type="primary", use_container_width=True):
        if not code_input.strip():
            st.error("⚠️ Please provide TIBCO code to document")
            return
        
        if not doc_types:
            st.error("⚠️ Please select at least one documentation type")
            return
        
        with st.spinner(f"🤖 Generating documentation using {model}..."):
            try:
                documentation = groq_client.generate_documentation(
                    code_input,
                    doc_types,
                    doc_format,
                    include_diagrams,
                    model
                )
                
                if documentation:
                    st.success("✅ Documentation generated successfully!")
                    st.markdown("## 📋 Generated Documentation")
                    st.markdown(documentation)
                    
                    # Download button
                    st.download_button(
                        label="💾 Download Documentation",
                        data=documentation,
                        file_name=f"tibco_documentation.{doc_format.lower()}",
                        mime="text/plain"
                    )
                else:
                    st.error("❌ Failed to generate documentation. Please try again.")
                    
            except Exception as e:
                st.error(f"❌ Error generating documentation: {str(e)}")

def migration_assistant_tab(groq_client, model):
    st.header("🚀 Migration Assistant")
    st.markdown("Assist with TIBCO version migrations, platform transitions, and modernization")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        migration_type = st.selectbox(
            "Migration Type",
            options=[
                "TIBCO BW 5.x to 6.x",
                "TIBCO BW 6.x to Container Edition",
                "Legacy to Cloud Native",
                "On-premise to Cloud",
                "Custom Migration"
            ],
            index=0
        )
        
        input_method = st.radio(
            "Choose input method:",
            options=["Paste Code", "Upload File"],
            horizontal=True,
            key="migration_input_method"
        )
        
        code_input = ""
        
        if input_method == "Paste Code":
            code_input = st.text_area(
                "Legacy TIBCO Code",
                height=300,
                placeholder="""Paste your legacy TIBCO code here...

Migration assistance includes:
- Compatibility analysis
- Deprecated feature identification
- Modern equivalent suggestions
- Migration roadmap
- Risk assessment
- Modernization opportunities""",
                key="migration_input"
            )
        else:
            uploaded_file = st.file_uploader(
                "Upload legacy TIBCO file",
                type=['xml', 'txt', 'bwp', 'process'],
                key="migration_file_upload"
            )
            
            if uploaded_file is not None:
                try:
                    file_content = uploaded_file.read()
                    try:
                        code_input = file_content.decode('utf-8')
                    except UnicodeDecodeError:
                        code_input = file_content.decode('latin-1')
                    
                    file_size = len(code_input)
                    st.info(f"📁 File loaded: {uploaded_file.name} ({file_size:,} characters)")
                    
                    if file_size > 5000:
                        with st.expander("📄 File Preview"):
                            st.code(code_input[:2000] + "..." if len(code_input) > 2000 else code_input, language="xml")
                    else:
                        with st.expander("📄 File Content"):
                            st.code(code_input, language="xml")
                            
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
                    code_input = ""
    
    with col2:
        st.markdown("### 🔄 Migration Focus")
        migration_areas = st.multiselect(
            "Select migration areas:",
            options=[
                "API Compatibility",
                "Configuration Changes",
                "Deprecated Components",
                "Performance Impact",
                "Security Updates",
                "Cloud Readiness",
                "Container Support",
                "DevOps Integration"
            ],
            default=["API Compatibility", "Configuration Changes", "Deprecated Components"]
        )
        
        migration_priority = st.selectbox(
            "Migration Priority",
            options=["Critical Issues Only", "High Priority", "Comprehensive"],
            index=1
        )
        
        include_migration_code = st.checkbox(
            "Generate migration code",
            value=True,
            help="Provide updated code examples"
        )
    
    if st.button("🚀 Analyze Migration", type="primary", use_container_width=True):
        if not code_input.strip():
            st.error("⚠️ Please provide legacy TIBCO code to analyze")
            return
        
        if not migration_areas:
            st.error("⚠️ Please select at least one migration area")
            return
        
        with st.spinner(f"🤖 Analyzing migration requirements using {model}..."):
            try:
                migration_analysis = groq_client.analyze_migration(
                    code_input,
                    migration_type,
                    migration_areas,
                    migration_priority,
                    include_migration_code,
                    model
                )
                
                if migration_analysis:
                    st.success("✅ Migration analysis completed!")
                    st.markdown("## 🚀 Migration Analysis & Recommendations")
                    st.markdown(migration_analysis)
                else:
                    st.error("❌ Failed to analyze migration. Please try again.")
                    
            except Exception as e:
                st.error(f"❌ Error analyzing migration: {str(e)}")

        if __name__ == "__main__":
    main()
