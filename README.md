# Insurance Multi-Agent Copilot 🏢

A production-ready multi-agent system that transforms insurance business requests into structured, decision-ready deliverables using LangGraph and OpenAI GPT-4o-mini.

## 🎯 Project Overview

This system implements a **Plan → Research → Draft → Verify → Deliver** workflow using four coordinated AI agents to process insurance queries with grounded, cited responses.

### Key Features

- ✅ **Multi-agent orchestration** with LangGraph
- 🔍 **RAG-based retrieval** with semantic search (FAISS + sentence-transformers)
- 📚 **Automatic citation tracking** in `[DocumentName, chunk_id]` format
- ✅ **Hallucination detection** via dedicated verifier agent
- 📊 **Structured outputs** (Executive Summary, Email, Action List, Sources)
- 🎯 **Complete trace logging** showing which agent did what
- 🚀 **Streamlit UI** for interactive use

## 🏗️ Architecture

### Agents

1. **Planner Agent** - Decomposes task and creates execution plan
2. **Research Agent** - Retrieves grounded information with citations from document corpus
3. **Writer Agent** - Produces structured deliverable using research notes
4. **Verifier Agent** - Checks for hallucinations, missing evidence, and contradictions

### Data Flow
```
User Query → Planner → Research → Writer → Verifier → Final Output
                ↓          ↓         ↓         ↓
            Plan    Citations   Draft   Verification
```

### Technology Stack

- **LangGraph**: Multi-agent orchestration
- **OpenAI GPT-4o-mini**: LLM for all agents
- **FAISS**: Vector database for semantic search
- **Sentence Transformers**: Document embeddings
- **Streamlit**: Web UI
- **Python 3.11+**

## 📁 Repository Structure
```
multi-agent-copilot/
├── agents/                     # Multi-agent system implementation
│   ├── __init__.py
│   ├── base_agent.py           # Base agent class definition
│   ├── copilot.py              # Main multi-agent orchestrator (LangGraph)
│   ├── planner.py              # Planner agent - decomposes tasks
│   ├── researcher.py           # Research agent - retrieves grounded info
│   ├── writer.py               # Writer agent - creates deliverables
│   ├── verifier.py             # Verifier agent - checks hallucinations
│   └── prompts.py              # Shared prompts for all agents
├── app/
│   └── app.py                  # Streamlit UI application
├── retrieval/
│   └── retriever.py            # Document loader & FAISS vector search
├── data/
│   ├── README.md               # Document corpus overview
│   └── documents/              # 9 insurance documents (~25K words)
│       ├── auto_insurance_policy.txt
│       ├── claims_procedures.txt
│       ├── customer_service_standards.txt
│       ├── fraud_detection.txt
│       ├── homeowners_policy.txt
│       ├── life_insurance_policy.txt
│       ├── regulatory_compliance.txt
│       ├── risk_assessment.txt
│       └── underwriting_guidelines.txt
├── eval/                       # Evaluation suite
│   ├── run_evaluation.py       # Script to run evaluation tests
│   ├── evaluation_results.md   # Test results and metrics
│   └── test_prompts.md         # 10 evaluation test cases
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Quick Start (< 5 minutes)

### Prerequisites

- Python 3.11 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd insurance-copilot
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up API key**
```bash
# Create .env file
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

Or export as environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

5. **Run the application**
```bash
streamlit run app/app.py
```

The app will open in your browser at `http://localhost:8501`

## 💡 Usage

### Using the Streamlit UI

1. Enter your **query** (what you want to know)
2. Enter your **goal** (what you want to accomplish)
3. Click **"Generate Deliverable"**
4. View the structured output with:
   - Executive Summary
   - Client-Ready Email
   - Action List
   - Complete Sources with Citations
   - Agent Trace Log

### Example Queries

**Query:** "What factors affect auto insurance premiums?"
**Goal:** "Create a brief summary for a client presentation"

**Query:** "What red flags indicate potential insurance fraud?"
**Goal:** "Train claims team on fraud detection"

**Query:** "What are the steps for filing an auto insurance claim?"
**Goal:** "Create a process guide for new adjusters"

### Using Programmatically
```python
from retrieval.retriever import initialize_retriever
from agents.copilot import create_copilot_system

# Initialize system
retriever = initialize_retriever()
copilot = create_copilot_system(retriever)

# Run query
result = copilot.run(
    user_query="What factors affect auto insurance premiums?",
    user_goal="Create a brief for client presentation"
)

# Access outputs
print(result['final_output']['executive_summary'])
print(result['final_output']['email'])
print(result['trace_log'])
```

## 📊 Output Format

### Executive Summary
Concise overview (max 150 words) of key findings with citations.

### Client-Ready Email
Professional email format ready to send to clients.

### Action List
Specific action items with:
- **Owner**: Who is responsible
- **Due Date**: When it's due
- **Confidence**: How confident we are (High/Medium/Low)

### Sources and Citations
All sources used with:
- Document name
- Chunk ID
- Relevance score
- Full text excerpt

### Verification Report
Details from the Verifier agent on:
- Whether all claims are supported
- Any unsupported claims found
- Citation accuracy
- Contradictions or issues

## ✅ Acceptance Criteria Status

- ✅ **End-to-end multi-agent routing works** - LangGraph workflow fully implemented
- ✅ **Output includes citations** - All claims cited in `[DocumentName, chunk_id]` format
- ✅ **Verifier blocks unsupported claims** - Verification agent checks all claims against sources
- ✅ **Trace log visible** - Complete execution trace in UI and programmatic output
- ✅ **Runs locally within 5 minutes** - Quick start guide above

## 🎨 Features Implemented

### Required ✅
- [x] Planner, Research, Writer, Verifier agents
- [x] 9 insurance documents with retrieval
- [x] Citation format: `[DocumentName, chunk_id]`
- [x] "Not found in sources" detection
- [x] Executive Summary (max 150 words)
- [x] Client-ready Email
- [x] Action List (owner, due date, confidence)
- [x] Sources and citations
- [x] Streamlit UI
- [x] Complete trace logging

### Nice-to-Have (Implemented 2/4)
- [x] **Evaluation set** - 10 test questions in eval/test_prompts.md
- [x] **Observability** - Detailed trace log with timing per agent
- [ ] Prompt injection defense
- [ ] Multi-output mode (executive vs analyst)

## 📈 Performance

Typical processing time:
- **Document indexing**: ~10 seconds (one-time, cached)
- **Query processing**: ~15-30 seconds
  - Planner: ~3 seconds
  - Research: ~2 seconds
  - Writer: ~8-15 seconds
  - Verifier: ~5-8 seconds

## 🐛 Troubleshooting

### "Module not found" errors
```bash
# Make sure you're in the virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

### "API key not found"
```bash
# Check your .env file or environment variable
echo $OPENAI_API_KEY
```

### "FAISS index not found"
The index builds automatically on first run. Delete `data/faiss_index.pkl` to rebuild.

### Slow performance
First run takes ~10 seconds to build the index (one-time). Subsequent runs are faster due to caching.

## 📚 Document Corpus

The system includes 9 comprehensive insurance documents:
- Auto Insurance Policy
- Claims Handling Procedures
- Homeowners Policy
- Underwriting Guidelines
- Fraud Detection Guide
- Risk Assessment Framework
- Regulatory Compliance
- Life Insurance Policy
- Customer Service Standards

**Total**: ~25,000 words covering all aspects of insurance operations

See `data/README.md` for detailed document descriptions.

## 🔐 Security & Privacy

- No confidential data used (all synthetic documents)
- API keys stored in environment variables
- No data persistence beyond session
- All processing happens locally

## 📝 License

This project is created for educational purposes as part of Giga Academy Cohort IV.

## 👥 Author

*Jetmir Terziu* <br>
Giga Academy Cohort IV - Project #6

---