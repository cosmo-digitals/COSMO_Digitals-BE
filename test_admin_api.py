#!/usr/bin/env python3
"""
Comprehensive test script for the COSMO Digitals Admin API
Tests all endpoints and validates responses
"""
import requests
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional

class AdminAPITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1"
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, message: str, data: Any = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if data and not success:
            print(f"   Details: {data}")
    
    def test_health_check(self) -> bool:
        """Test if the API server is running"""
        try:
            response = requests.get(f"{self.base_url}/docs", timeout=5)
            success = response.status_code == 200
            self.log_test("Health Check", success, f"Server status: {response.status_code}")
            return success
        except Exception as e:
            self.log_test("Health Check", False, f"Server not reachable: {str(e)}")
            return False
    
    def test_cors_headers(self) -> bool:
        """Test CORS headers for frontend integration"""
        try:
            response = requests.options(f"{self.api_url}/contact")
            cors_headers = {
                "access-control-allow-origin": response.headers.get("access-control-allow-origin"),
                "access-control-allow-methods": response.headers.get("access-control-allow-methods"),
                "access-control-allow-headers": response.headers.get("access-control-allow-headers")
            }
            
            success = all(cors_headers.values())
            self.log_test("CORS Headers", success, "CORS configuration check", cors_headers)
            return success
        except Exception as e:
            self.log_test("CORS Headers", False, f"CORS test failed: {str(e)}")
            return False
    
    def test_create_contact(self) -> Optional[str]:
        """Test creating a new contact"""
        test_contact = {
            "first_name": "Admin",
            "last_name": "TestUser",
            "email": "admin.test@cosmodigitals.com",
            "phone_number": "+1234567890",
            "message": "This is a test contact submission from the admin API test script.",
            "services": ["Web Development", "SEO", "Mobile App Development"]
        }
        
        try:
            response = requests.post(f"{self.api_url}/contact", json=test_contact, timeout=10)
            
            if response.status_code == 201:
                result = response.json()
                contact_id = result.get("id")
                self.log_test("Create Contact", True, f"Contact created with ID: {contact_id}")
                return contact_id
            else:
                self.log_test("Create Contact", False, f"Status {response.status_code}: {response.text}")
                return None
        except Exception as e:
            self.log_test("Create Contact", False, f"Request failed: {str(e)}")
            return None
    
    def test_get_contacts(self) -> list:
        """Test retrieving all contacts"""
        try:
            response = requests.get(f"{self.api_url}/contact", timeout=10)
            
            if response.status_code == 200:
                contacts = response.json()
                self.log_test("Get Contacts", True, f"Retrieved {len(contacts)} contacts")
                
                # Validate contact structure
                if contacts:
                    contact = contacts[0]
                    required_fields = ["id", "first_name", "last_name", "email", "phone_number", "message", "services"]
                    missing_fields = [field for field in required_fields if field not in contact]
                    
                    if missing_fields:
                        self.log_test("Contact Schema", False, f"Missing fields: {missing_fields}")
                    else:
                        self.log_test("Contact Schema", True, "Contact structure is valid")
                
                return contacts
            else:
                self.log_test("Get Contacts", False, f"Status {response.status_code}: {response.text}")
                return []
        except Exception as e:
            self.log_test("Get Contacts", False, f"Request failed: {str(e)}")
            return []
    
    def test_update_contact(self, contact_id: str) -> bool:
        """Test updating a contact"""
        if not contact_id:
            self.log_test("Update Contact", False, "No contact ID provided")
            return False
        
        update_data = {
            "first_name": "Admin Updated",
            "last_name": "TestUser Updated",
            "email": "admin.updated@cosmodigitals.com",
            "phone_number": "+1234567890",
            "message": "This contact has been updated via admin API test.",
            "services": ["Web Development", "SEO", "Digital Marketing"]
        }
        
        try:
            response = requests.put(f"{self.api_url}/contact/{contact_id}", json=update_data, timeout=10)
            
            if response.status_code == 200:
                self.log_test("Update Contact", True, "Contact updated successfully")
                return True
            else:
                self.log_test("Update Contact", False, f"Status {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Update Contact", False, f"Request failed: {str(e)}")
            return False
    
    def test_delete_contact(self, contact_id: str) -> bool:
        """Test deleting a contact"""
        if not contact_id:
            self.log_test("Delete Contact", False, "No contact ID provided")
            return False
        
        try:
            response = requests.delete(f"{self.api_url}/contact/{contact_id}", timeout=10)
            
            if response.status_code == 200:
                self.log_test("Delete Contact", True, "Contact deleted successfully")
                return True
            else:
                self.log_test("Delete Contact", False, f"Status {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Delete Contact", False, f"Request failed: {str(e)}")
            return False
    
    def test_invalid_contact_creation(self) -> bool:
        """Test contact creation with invalid data"""
        invalid_contacts = [
            {
                "name": "Missing required fields",
                "data": {"first_name": "Test"},
                "expected_error": True
            },
            {
                "name": "Invalid email",
                "data": {
                    "first_name": "Test",
                    "last_name": "User",
                    "email": "invalid-email",
                    "phone_number": "1234567890",
                    "message": "Test message"
                },
                "expected_error": True
            },
            {
                "name": "Empty required fields",
                "data": {
                    "first_name": "",
                    "last_name": "",
                    "email": "",
                    "phone_number": "",
                    "message": ""
                },
                "expected_error": True
            }
        ]
        
        all_passed = True
        for test_case in invalid_contacts:
            try:
                response = requests.post(f"{self.api_url}/contact", json=test_case["data"], timeout=10)
                success = (response.status_code >= 400) == test_case["expected_error"]
                self.log_test(f"Invalid Contact - {test_case['name']}", success, 
                            f"Status {response.status_code}")
                if not success:
                    all_passed = False
            except Exception as e:
                self.log_test(f"Invalid Contact - {test_case['name']}", False, f"Request failed: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🧪 COSMO Digitals Admin API Test Suite")
        print("=" * 60)
        print(f"📍 Testing API at: {self.api_url}")
        print()
        
        # Check if server is running
        if not self.test_health_check():
            print("❌ Server is not running. Please start the FastAPI server first.")
            return False
        
        # Test CORS
        self.test_cors_headers()
        
        # Test contact operations
        contact_id = self.test_create_contact()
        self.test_get_contacts()
        
        if contact_id:
            self.test_update_contact(contact_id)
            self.test_get_contacts()  # Verify update
            self.test_delete_contact(contact_id)
            self.test_get_contacts()  # Verify deletion
        
        # Test invalid data handling
        self.test_invalid_contact_creation()
        
        # Summary
        print("\n" + "=" * 60)
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        print(f"📊 Test Summary: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Admin API is working correctly.")
        else:
            print("⚠️  Some tests failed. Please check the API implementation.")
        
        return passed == total

def main():
    """Main function to run the test suite"""
    tester = AdminAPITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 