#!/usr/bin/env python3
"""
Simple test script untuk testing individual components
"""

import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_config():
    print("=== Testing Config ===")
    try:
        from config.settings import settings
        print(f"✅ Config loaded successfully")
        print(f"   - Ollama URL: {settings.OLLAMA_BASE_URL}")
        print(f"   - Vector DB Path: {settings.VECTOR_DB_PATH}")
        print(f"   - Database URL: {settings.database_url}")
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_rag_service():
    print("\n=== Testing RAG Service ===")
    try:
        from services.rag_service import RAGService
        rag = RAGService()
        print("✅ RAG Service initialized successfully")
        
        # Test simple query
        response = rag.query("test")
        print(f"✅ RAG query test completed")
        return True
    except Exception as e:
        print(f"❌ RAG Service error: {e}")
        return False

def test_sql_service():
    print("\n=== Testing SQL Service ===")
    try:
        from services.sql_service import SQLService
        sql = SQLService()
        print("✅ SQL Service initialized successfully")
        return True
    except Exception as e:
        print(f"❌ SQL Service error: {e}")
        return False

def test_supervisor():
    print("\n=== Testing Supervisor ===")
    try:
        from services.supervisor import SupervisorService
        supervisor = SupervisorService()
        print("✅ Supervisor initialized successfully")
        
        # Test decision making
        decision = supervisor.decide_agent("nomor telepon dinas kesehatan")
        print(f"✅ Decision test: {decision}")
        return True
    except Exception as e:
        print(f"❌ Supervisor error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Component Tests...\n")
    
    results = []
    results.append(test_config())
    results.append(test_rag_service())
    results.append(test_sql_service())
    results.append(test_supervisor())
    
    print(f"\n📊 Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("🎉 All tests passed! FastAPI should work fine.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
