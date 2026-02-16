"""
Automated evaluation script for testing the copilot system
"""

from dotenv import load_dotenv
load_dotenv()


import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from retrieval.retriever import initialize_retriever
from agents import create_copilot_system


# Test cases from test_prompts.md
TEST_CASES = [
    {
        "name": "Test 1: Claims Processing",
        "query": "What are the required steps for handling an auto insurance claim from initial report to settlement?",
        "goal": "Create a process checklist for new claims adjusters",
        "expected_docs": ["claims_procedures.txt"]
    },
    {
        "name": "Test 2: Fraud Detection",
        "query": "What red flags should I look for when evaluating a potentially fraudulent homeowners theft claim?",
        "goal": "Train claims team on fraud indicators",
        "expected_docs": ["fraud_detection.txt"]
    },
    {
        "name": "Test 3: Premium Factors",
        "query": "What factors influence auto insurance premium calculations and which have the highest impact?",
        "goal": "Explain to a client why their premium increased",
        "expected_docs": ["auto_insurance_policy.txt", "underwriting_guidelines.txt"]
    },
    {
        "name": "Test 4: Coverage Limitations",
        "query": "What are the coverage limits and exclusions for jewelry under a standard homeowners policy?",
        "goal": "Advise a client on whether they need additional coverage",
        "expected_docs": ["homeowners_policy.txt"]
    },
    {
        "name": "Test 5: Regulatory Compliance",
        "query": "What are the prompt payment requirements for insurance claims and what happens if we violate them?",
        "goal": "Ensure claims department follows compliance standards",
        "expected_docs": ["regulatory_compliance.txt"]
    },
    {
        "name": "Test 6: Underwriting Guidelines",
        "query": "Under what conditions would we decline auto insurance coverage for a driver?",
        "goal": "Create guidelines document for underwriters",
        "expected_docs": ["underwriting_guidelines.txt"]
    },
    {
        "name": "Test 7: Risk Assessment",
        "query": "How do we assess wildfire risk for homeowners properties and what mitigation measures reduce premiums?",
        "goal": "Advise homeowner in high-risk area",
        "expected_docs": ["risk_assessment.txt"]
    },
    {
        "name": "Test 8: Policy Conversion",
        "query": "What options does a customer have when their 20-year term life insurance policy is about to expire?",
        "goal": "Prepare renewal conversation script for agents",
        "expected_docs": ["life_insurance_policy.txt"]
    },
    {
        "name": "Test 9: Customer Service Standards",
        "query": "What are our response time commitments for different customer service channels?",
        "goal": "Set performance targets for customer service team",
        "expected_docs": ["customer_service_standards.txt"]
    },
    {
        "name": "Test 10: Missing Information Test",
        "query": "What is the process for filing a claim for earthquake damage to a home?",
        "goal": "Create an earthquake claim guide",
        "expected_docs": None  # Should find limited info
    }
]


def run_evaluation():
    """Run all test cases and generate report"""
    
    print("="*80)
    print("INSURANCE MULTI-AGENT COPILOT - EVALUATION SUITE")
    print("="*80)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Tests: {len(TEST_CASES)}\n")
    
    # Initialize system
    print("Initializing system...")
    retriever = initialize_retriever()
    copilot = create_copilot_system(retriever)
    print("✅ System initialized\n")
    
    results = []
    passed = 0
    failed = 0
    
    # Run each test
    for i, test in enumerate(TEST_CASES, 1):
        print(f"\n{'='*80}")
        print(f"Running {test['name']} ({i}/{len(TEST_CASES)})")
        print(f"{'='*80}")
        print(f"Query: {test['query'][:80]}...")
        print(f"Goal: {test['goal'][:80]}...")
        
        start_time = datetime.now()
        
        try:
            # Run the copilot
            result = copilot.run(
                user_query=test['query'],
                user_goal=test['goal']
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Extract metrics
            verification_passed = result['verification_result']['passed']
            num_sources = len(result['final_output']['sources'])
            docs_used = set(s['document'] for s in result['final_output']['sources'])
            
            # Determine pass/fail
            test_passed = verification_passed and num_sources > 0
            
            if test_passed:
                passed += 1
                status = "✅ PASSED"
            else:
                failed += 1
                status = "❌ FAILED"
            
            # Store results
            results.append({
                'test': test['name'],
                'status': status,
                'verification': "PASSED" if verification_passed else "FAILED",
                'sources': num_sources,
                'documents': docs_used,
                'duration': duration
            })
            
            # Print summary
            print(f"\n{status}")
            print(f"Verification: {'PASSED' if verification_passed else 'FAILED'}")
            print(f"Sources Retrieved: {num_sources}")
            print(f"Documents Used: {', '.join(docs_used)}")
            print(f"Duration: {duration:.2f}s")
            
        except Exception as e:
            failed += 1
            print(f"\n❌ ERROR: {str(e)}")
            results.append({
                'test': test['name'],
                'status': "❌ ERROR",
                'error': str(e)
            })
    
    # Generate summary report
    print(f"\n\n{'='*80}")
    print("EVALUATION SUMMARY")
    print(f"{'='*80}")
    print(f"Total Tests: {len(TEST_CASES)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(TEST_CASES)*100):.1f}%")
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Save detailed results
    save_results(results, passed, failed)
    
    print(f"\n✅ Results saved to eval/evaluation_results.md")


def save_results(results, passed, failed):
    """Save results to markdown file"""
    
    with open("eval/evaluation_results.md", "w", encoding="utf-8") as f:
        f.write("# Evaluation Results\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total Tests:** {len(results)}\n")
        f.write(f"**Passed:** {passed}\n")
        f.write(f"**Failed:** {failed}\n")
        f.write(f"**Success Rate:** {(passed/len(results)*100):.1f}%\n\n")
        
        f.write("---\n\n")
        f.write("## Test Results\n\n")
        
        for result in results:
            f.write(f"### {result['test']}\n")
            f.write(f"- **Status:** {result['status']}\n")
            
            if 'verification' in result:
                f.write(f"- **Verification:** {result['verification']}\n")
                f.write(f"- **Sources Retrieved:** {result['sources']}\n")
                f.write(f"- **Documents Used:** {', '.join(result['documents'])}\n")
                f.write(f"- **Duration:** {result['duration']:.2f}s\n")
            elif 'error' in result:
                f.write(f"- **Error:** {result['error']}\n")
            
            f.write("\n")


if __name__ == "__main__":
    try:
        run_evaluation()
    except KeyboardInterrupt:
        print("\n\n⚠️ Evaluation interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()