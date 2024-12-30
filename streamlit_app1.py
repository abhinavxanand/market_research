import streamlit as st
import os
from main3 import MarketResearchAgents
from dotenv import load_dotenv
import time
import json

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Market Research Assistant",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stAlert {
        margin-top: 1rem;
    }
    .report-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .section-header {
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'current_analysis' not in st.session_state:
        st.session_state.current_analysis = None

def validate_environment():
    """Validate required environment variables"""
    required_vars = [
        "AZURE_API_KEY",
        "AZURE_API_VERSION",
        "AZURE_API_BASE",
        "AZURE_DEPLOYMENT_NAME",
        "TAVILY_API_KEY"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        st.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        st.stop()

def run_analysis(company_name: str, industry: str) -> dict:
    """Run the market research analysis"""
    try:
        agent_system = MarketResearchAgents()
        with st.spinner(f"Analyzing {company_name}... This may take a few minutes."):
            analysis = agent_system.analyze_company(company_name, industry)
        return analysis
    except Exception as e:
        st.error(f"Error during analysis: {str(e)}")
        return None

def display_analysis(analysis: dict):
    """Display the analysis results in a structured format"""
    if not analysis:
        return

    st.markdown("## 📊 Analysis Results")
    
    # Company Info
    st.markdown(f"### 🏢 Company Analysis: {analysis['company']}")
    
    # Market Research
    with st.expander("📈 Market Research", expanded=True):
        st.markdown("""
            <div class="report-container">
                <h4 class="section-header">Industry Analysis & Market Position</h4>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(analysis['research'])
    
    # AI Use Cases
    with st.expander("🤖 AI/ML Use Cases", expanded=True):
        st.markdown("""
            <div class="report-container">
                <h4 class="section-header">Proposed Solutions & Applications</h4>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(analysis['use_cases'])
    
    # Implementation Resources
    with st.expander("🛠️ Implementation Resources", expanded=True):
        st.markdown("""
            <div class="report-container">
                <h4 class="section-header">Datasets & Technical Resources</h4>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(analysis['resources'])

    # Download options
    st.markdown("### 📥 Download Results")
    
    # Convert analysis to markdown
    markdown_content = f"""# Market Research Analysis: {analysis['company']}

## Market Research
{analysis['research']}

## AI/ML Use Cases
{analysis['use_cases']}

## Implementation Resources
{analysis['resources']}
"""
    
    # Create download buttons
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="Download as Markdown",
            data=markdown_content,
            file_name=f"{analysis['company'].lower()}_analysis.md",
            mime="text/markdown"
        )
    
    with col2:
        st.download_button(
            label="Download as JSON",
            data=json.dumps(analysis, indent=2),
            file_name=f"{analysis['company'].lower()}_analysis.json",
            mime="application/json"
        )

def main():
    st.title("🔍 AI Market Research Assistant")
    st.markdown("""
        Get comprehensive market research and AI use case analysis for any company.
        This tool uses advanced AI agents to gather and analyze information from reliable sources.
    """)
    
    # Initialize session state
    initialize_session_state()
    
    # Validate environment
    validate_environment()
    
    # Input form
    with st.form("analysis_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input(
                "Company Name",
                help="Enter the name of the company you want to analyze"
            )
        
        with col2:
            industry = st.text_input(
                "Industry (Optional)",
                help="Specify the industry sector for more focused analysis"
            )
        
        submitted = st.form_submit_button("Start Analysis")
        
        if submitted and company_name:
            # Run analysis
            analysis = run_analysis(company_name, industry)
            
            if analysis:
                st.session_state.current_analysis = analysis
                st.session_state.analysis_complete = True
    
    # Display results if analysis is complete
    if st.session_state.analysis_complete and st.session_state.current_analysis:
        display_analysis(st.session_state.current_analysis)

if __name__ == "__main__":
    main()