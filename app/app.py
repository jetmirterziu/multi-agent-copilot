"""
Streamlit UI for Insurance Multi-Agent Copilot
"""

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from retrieval.retriever import initialize_retriever
from agents.copilot import create_copilot_system


# Page config
st.set_page_config(
    page_title="Insurance Multi-Agent Copilot",
    page_icon="🏢",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    .citation {
        background-color: #f0f0f0;
        padding: 0.2rem 0.5rem;
        border-radius: 3px;
        font-family: monospace;
        font-size: 0.85rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_system():
    """Load and cache the copilot system"""
    with st.spinner("Initializing retrieval system and loading documents..."):
        retriever = initialize_retriever()
    with st.spinner("Building multi-agent system..."):
        copilot = create_copilot_system(retriever)
    return copilot


def display_trace_log(trace_log):
    """Display the agent trace log"""
    st.markdown('<div class="section-header">🔍 Agent Trace Log</div>', unsafe_allow_html=True)
    
    with st.expander("View detailed agent execution trace", expanded=False):
        for entry in trace_log:
            if "===" in entry:
                st.markdown(f"**{entry}**")
            else:
                st.text(entry)


def display_sources(sources):
    """Display the sources and citations used"""
    st.markdown('<div class="section-header">📚 Sources Used</div>', unsafe_allow_html=True)
    
    # Group sources by document
    docs = {}
    for source in sources:
        doc_name = source['document']
        if doc_name not in docs:
            docs[doc_name] = []
        docs[doc_name].append(source)
    
    # Display grouped by document
    for doc_name, chunks in docs.items():
        with st.expander(f"📄 {doc_name} ({len(chunks)} chunks used)"):
            for chunk in chunks:
                st.markdown(f"**{chunk['citation']}** (Relevance: {chunk['relevance']:.2%})")
                st.text(chunk['text'][:300] + "..." if len(chunk['text']) > 300 else chunk['text'])
                st.markdown("---")


def display_verification(verification_result):
    """Display verification results"""
    if verification_result['passed']:
        st.markdown('<div class="success-box">✅ <strong>Verification PASSED</strong> - All claims are supported by sources</div>', 
                   unsafe_allow_html=True)
    else:
        st.markdown('<div class="warning-box">⚠️ <strong>Verification FAILED</strong> - Some issues were found</div>', 
                   unsafe_allow_html=True)
    
    with st.expander("View verification report"):
        st.text(verification_result['report'])


def main():
    # Header
    st.markdown('<div class="main-header">🏢 Insurance Multi-Agent Copilot</div>', unsafe_allow_html=True)
    st.markdown("*Turn business requests into structured, decision-ready deliverables with AI agents*")
    
    # Initialize system
    copilot = load_system()
    
    st.success("✅ System initialized with 9 insurance documents")
    
    # Sidebar with example queries
    with st.sidebar:
        st.header("📋 Example Queries")
        st.markdown("""
        Try these sample queries:
        
        **Claims & Processing:**
        - What are the steps for filing an auto insurance claim?
        - What red flags indicate potential insurance fraud?
        
        **Policy Information:**
        - What factors affect homeowners insurance premiums?
        - What is covered under comprehensive auto insurance?
        
        **Underwriting:**
        - What are the underwriting guidelines for high-risk drivers?
        - What property conditions make a home uninsurable?
        
        **Compliance:**
        - What are the prompt payment requirements for claims?
        - What information must be included in claim denials?
        """)
        
        st.markdown("---")
        st.header("⚙️ System Info")
        st.info("""
        **Agents:**
        - 🎯 Planner
        - 🔍 Researcher  
        - ✍️ Writer
        - ✅ Verifier
        
        **Documents:** 9 insurance docs
        **Citations:** Automatic tracking
        """)
    
    # Main input form
    st.markdown('<div class="section-header">📝 Submit Your Request</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_query = st.text_area(
            "What would you like to know?",
            height=100,
            placeholder="e.g., What are the key factors that affect auto insurance premiums?"
        )
    
    with col2:
        user_goal = st.text_area(
            "What's your goal?",
            height=100,
            placeholder="e.g., Create a summary for client presentation"
        )
    
    # Process button
    if st.button("🚀 Generate Deliverable", type="primary", use_container_width=True):
        if not user_query or not user_goal:
            st.error("Please provide both a query and a goal.")
            return
        
        # Run the multi-agent system
        with st.spinner("🤖 Multi-agent system working..."):
            try:
                result = copilot.run(user_query, user_goal)
                
                # Store in session state
                st.session_state['result'] = result
                st.session_state['query'] = user_query
                st.session_state['goal'] = user_goal
                
                st.success("✅ Deliverable generated successfully!")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.exception(e)
                return
    
    # Display results if available
    if 'result' in st.session_state:
        result = st.session_state['result']
        final_output = result['final_output']
        
        st.markdown("---")
        st.markdown('<div class="section-header">📊 Final Deliverable</div>', unsafe_allow_html=True)
        
        # Display verification status
        display_verification(result['verification_result'])
        
        # Tabs for different sections
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Executive Summary", 
            "📧 Client Email", 
            "✅ Action List",
            "📄 Full Deliverable",
            "📚 Sources"
        ])
        
        with tab1:
            if final_output.get('executive_summary'):
                st.markdown(final_output['executive_summary'])
            else:
                st.info("Executive summary not found in output")
        
        with tab2:
            if final_output.get('email'):
                st.markdown(final_output['email'])
            else:
                st.info("Email not found in output")
        
        with tab3:
            if final_output.get('action_list'):
                st.markdown(final_output['action_list'])
            else:
                st.info("Action list not found in output")
        
        with tab4:
            st.markdown(final_output['full_deliverable'])
            
            # Download button
            st.download_button(
                label="📥 Download Full Deliverable",
                data=final_output['full_deliverable'],
                file_name=f"insurance_deliverable_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
        
        with tab5:
            display_sources(final_output['sources'])
        
        # Trace log at the bottom
        st.markdown("---")
        display_trace_log(result['trace_log'])


if __name__ == "__main__":
    main()