# Insurance Document Corpus

This directory contains synthetic insurance documents used for the multi-agent copilot system's retrieval layer.

## Document Overview

The corpus consists of 9 comprehensive insurance documents covering various aspects of insurance operations:

### 1. **auto_insurance_policy.txt**
Complete auto insurance policy document including:
- Liability, collision, and comprehensive coverage details
- Claims process and timelines
- Premium calculation factors
- Available discounts
- Policy exclusions

### 2. **claims_procedures.txt**
Detailed claims handling procedures covering:
- First Notice of Loss (FNOL) process
- Investigation requirements and fraud indicators
- Coverage determination procedures
- Settlement and payment processes
- Subrogation and dispute resolution
- Regulatory compliance requirements

### 3. **homeowners_policy.txt**
Comprehensive homeowners insurance policy including:
- Dwelling and property coverage (Coverages A-F)
- Covered perils and exclusions
- Claims process
- Optional endorsements
- Premium factors and discounts

### 4. **underwriting_guidelines.txt**
Underwriting standards for personal lines insurance:
- Driver and vehicle eligibility (auto)
- Property eligibility and inspection requirements (home)
- Credit-based insurance scoring
- Claims history evaluation
- Special considerations and binding authority

### 5. **fraud_detection.txt**
Fraud detection and prevention guidelines:
- Types of insurance fraud (hard and soft)
- Red flags and indicators for different claim types
- Investigation protocols and techniques
- Evidence collection procedures
- Reporting requirements and legal actions

### 6. **risk_assessment.txt**
Risk assessment framework covering:
- Auto and homeowners risk factors
- Geographic and catastrophe risk
- Credit and financial risk indicators
- Predictive analytics and telematics
- Portfolio management strategies

### 7. **regulatory_compliance.txt**
Comprehensive regulatory compliance guide:
- State insurance regulations
- Unfair Claims Settlement Practices Act
- Privacy and data security requirements (GLBA, FCRA)
- Anti-Money Laundering (AML) requirements
- Market conduct examination procedures
- Advertising and marketing compliance

### 8. **life_insurance_policy.txt**
Term life insurance policy document:
- Coverage provisions and death benefit
- Premium information and payment options
- Policy riders and conversion privileges
- Claims process and exclusions
- Underwriting classification

### 9. **customer_service_standards.txt**
Customer service excellence standards:
- Response time standards across channels
- Call handling procedures
- Inquiry type handling (policy, billing, claims)
- Handling difficult situations and complaints
- Quality assurance and compliance

## Document Statistics

- **Total Documents**: 9
- **Total Word Count**: ~25,000 words
- **Coverage Areas**: Policy details, claims handling, underwriting, fraud detection, risk assessment, compliance, customer service
- **Format**: Plain text (.txt) for easy processing

## Usage in the System

These documents are:
1. Chunked and embedded using sentence transformers
2. Stored in a vector database (FAISS)
3. Retrieved based on semantic similarity to user queries
4. Used by the Research Agent to ground responses
5. Cited with document name and chunk ID in final outputs

## Data Source

All documents are synthetic and created for educational purposes. They represent realistic insurance industry content but do not contain any confidential or proprietary information.

## Citation Format

When documents are cited in system outputs, the format is:
```
[DocumentName, Chunk ID]
```

Example: `[auto_insurance_policy.txt, chunk_3]`