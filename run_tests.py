#!/usr/bin/env python3
"""
Test runner script for COSMO Digitals Backend
Runs both admin API and dashboard test suites
"""
import sys
import os
import subprocess
import time
from datetime import datetime

def print_header(title: str):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"🧪 {title}")
    print("=" * 80)

def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n📋 {title}")
    print("-" * 60)

def check_server_running() -> bool:
    """Check if the FastAPI server is running"""
    try:
        import requests
        response = requests.get("http://localhost:8000/docs", timeout=5)
        return response.status_code == 200
    except:
        return False

def run_test_script(script_name: str, description: str) -> bool:
    """Run a test script and return success status"""
    print_section(f"Running {description}")
    
    try:
        # Run the test script
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, timeout=120)
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        # Return success based on exit code
        success = result.returncode == 0
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"\n{status} {description}")
        
        return success
    except subprocess.TimeoutExpired:
        print(f"❌ TIMEOUT {description} (took longer than 2 minutes)")
        return False
    except Exception as e:
        print(f"❌ ERROR running {description}: {str(e)}")
        return False

def main():
    """Main test runner function"""
    print_header("COSMO Digitals Backend Test Suite")
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if we're in the right directory
    if not os.path.exists("app"):
        print("❌ Error: Please run this script from the COSMO_Digitals-BE directory")
        sys.exit(1)
    
    # Check if server is running
    print_section("Checking Server Status")
    if check_server_running():
        print("✅ FastAPI server is running on http://localhost:8000")
    else:
        print("❌ FastAPI server is not running!")
        print("💡 Please start the server first with: python run.py")
        print("   Or: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        sys.exit(1)
    
    # Test results
    test_results = []
    
    # Run Admin API tests
    if os.path.exists("test_admin_api.py"):
        success = run_test_script("test_admin_api.py", "Admin API Tests")
        test_results.append(("Admin API", success))
    else:
        print("❌ test_admin_api.py not found")
        test_results.append(("Admin API", False))
    
    # Run Admin Dashboard tests
    if os.path.exists("test_admin_dashboard.py"):
        success = run_test_script("test_admin_dashboard.py", "Admin Dashboard Tests")
        test_results.append(("Admin Dashboard", success))
    else:
        print("❌ test_admin_dashboard.py not found")
        test_results.append(("Admin Dashboard", False))
    
    # Run Contact API tests (existing)
    if os.path.exists("test_contact_api.py"):
        success = run_test_script("test_contact_api.py", "Contact API Tests")
        test_results.append(("Contact API", success))
    else:
        print("❌ test_contact_api.py not found")
        test_results.append(("Contact API", False))
    
    # Summary
    print_header("Test Results Summary")
    
    passed = sum(1 for _, success in test_results if success)
    total = len(test_results)
    
    print(f"📊 Overall Results: {passed}/{total} test suites passed")
    print()
    
    for test_name, success in test_results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} {test_name}")
    
    print(f"\n🕐 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if passed == total:
        print("\n🎉 All test suites passed! Your backend is working correctly.")
        sys.exit(0)
    else:
        print(f"\n⚠️  {total - passed} test suite(s) failed. Please check the implementation.")
        sys.exit(1)

if __name__ == "__main__":
    main() 