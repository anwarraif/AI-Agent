#!/usr/bin/env python3
"""
Simple test script untuk testing supervisor service
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.supervisor import SupervisorService

def test_supervisor():
    print("=== Testing Supervisor Service ===")
    
    supervisor = SupervisorService()
    
    # Test questions
    test_cases = [
        {
            "question": "infoin dong nomor telpon dinas kesehatan jkt",
            "expected_agent": "RAG"
        },
        {
            "question": "Total kematian baru akibat Covid di Jakarta pada bulan Juli 2021",
            "expected_agent": "SQL"
        },
        {
            "question": "infoin ttg Rata-rata kasus baru per hari pada April 2020",
            "expected_agent": "SQL"
        },
        {
            "question": "Total kematian baru akibat Covid di Jakarta pada bulan august 2021",
            "expected_agent": "SQL"
        },
        {
            "question": "apa protokol kesehatan untuk covid?",
            "expected_agent": "RAG"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Question: {test_case['question']}")
        
        # Test decision making
        decision = supervisor.decide_agent(test_case['question'])
        print(f"Supervisor Decision: {decision}")
        print(f"Expected: {test_case['expected_agent']}")
        
        # Test full query processing
        print("\nProcessing full query...")
        try:
            result = supervisor.process_query(test_case['question'])
            print(f"Source: {result['source']}")
            print(f"Answer: {result['answer'][:100]}...")  # First 100 chars
            print(f"Reasoning: {result['reasoning']}")
        except Exception as e:
            print(f"Error: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_supervisor()
