# Evaluation Test Prompts
# 10 test queries for the Insurance Multi-Agent Copilot

## Test 1: Claims Processing
**Query:** What are the required steps for handling an auto insurance claim from initial report to settlement?
**Goal:** Create a process checklist for new claims adjusters
**Expected:** Should find information from claims_procedures.txt about FNOL, investigation, and settlement

## Test 2: Fraud Detection
**Query:** What red flags should I look for when evaluating a potentially fraudulent homeowners theft claim?
**Goal:** Train claims team on fraud indicators
**Expected:** Should retrieve fraud indicators from fraud_detection.txt specific to theft claims

## Test 3: Premium Factors
**Query:** What factors influence auto insurance premium calculations and which have the highest impact?
**Goal:** Explain to a client why their premium increased
**Expected:** Should cite premium calculation factors from auto_insurance_policy.txt and underwriting_guidelines.txt

## Test 4: Coverage Limitations
**Query:** What are the coverage limits and exclusions for jewelry under a standard homeowners policy?
**Goal:** Advise a client on whether they need additional coverage
**Expected:** Should find special limits from homeowners_policy.txt

## Test 5: Regulatory Compliance
**Query:** What are the prompt payment requirements for insurance claims and what happens if we violate them?
**Goal:** Ensure claims department follows compliance standards
**Expected:** Should cite prompt payment laws from regulatory_compliance.txt

## Test 6: Underwriting Guidelines
**Query:** Under what conditions would we decline auto insurance coverage for a driver?
**Goal:** Create guidelines document for underwriters
**Expected:** Should find unacceptable risks from underwriting_guidelines.txt

## Test 7: Risk Assessment
**Query:** How do we assess wildfire risk for homeowners properties and what mitigation measures reduce premiums?
**Goal:** Advise homeowner in high-risk area
**Expected:** Should retrieve wildfire risk information from risk_assessment.txt

## Test 8: Policy Conversion
**Query:** What options does a customer have when their 20-year term life insurance policy is about to expire?
**Goal:** Prepare renewal conversation script for agents
**Expected:** Should find renewal and conversion information from life_insurance_policy.txt

## Test 9: Customer Service Standards
**Query:** What are our response time commitments for different customer service channels?
**Goal:** Set performance targets for customer service team
**Expected:** Should cite response standards from customer_service_standards.txt

## Test 10: Missing Information Test
**Query:** What is the process for filing a claim for earthquake damage to a home?
**Goal:** Create an earthquake claim guide
**Expected:** Should state "Not found in sources" since earthquake details are limited, but may reference general claims process

## Evaluation Criteria

For each test, evaluate:
1. **Retrieval Quality:** Are the most relevant documents retrieved?
2. **Citation Accuracy:** Are citations properly formatted and present?
3. **Groundedness:** Is the answer based only on source documents?
4. **Completeness:** Does the answer address the query and goal?
5. **Verification:** Does the verifier catch any unsupported claims?
6. **Structure:** Are all required sections present (summary, email, actions)?
7. **Trace Visibility:** Can we see which agent did what?

## Success Metrics

- Retrieval Precision: >80% relevant chunks
- Citation Coverage: 100% of factual claims cited
- Verification Pass Rate: >80%
- First Call Resolution: All queries answered in one run
- Processing Time: <60 seconds per query

---

## 1️⃣6️⃣ `.env.example`

# OpenAI API Key
# Get your API key from: https://platform.openai.com/api-keys
```OPENAI_API_KEY=your-api-key-here```