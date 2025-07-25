#!/usr/bin/env python3
"""
Comprehensive test script for the COSMO Digitals Admin Dashboard
Tests dashboard-specific functionality and frontend-backend integration
"""
import requests
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

class AdminDashboardTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1"
        self.test_results = []
        self.test_contacts = []
        
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
    
    def setup_test_data(self) -> bool:
        """Create test contacts for dashboard testing"""
        test_contacts_data = [
            {
                "first_name": "John",
                "last_name": "Smith",
                "email": "john.smith@example.com",
                "phone_number": "+1234567890",
                "message": "Interested in web development services for my startup.",
                "services": ["Web Development", "SEO"]
            },
            {
                "first_name": "Sarah",
                "last_name": "Johnson",
                "email": "sarah.johnson@company.com",
                "phone_number": "+1987654321",
                "message": "Looking for mobile app development and digital marketing.",
                "services": ["Mobile App Development", "Digital Marketing"]
            },
            {
                "first_name": "Mike",
                "last_name": "Davis",
                "email": "mike.davis@enterprise.com",
                "phone_number": "+1555123456",
                "message": "Need comprehensive digital transformation services.",
                "services": ["Web Development", "Mobile App Development", "SEO", "Digital Marketing"]
            }
        ]
        
        created_contacts = []
        for contact_data in test_contacts_data:
            try:
                response = requests.post(f"{self.api_url}/contact", json=contact_data, timeout=10)
                if response.status_code == 201:
                    result = response.json()
                    created_contacts.append(result.get("id"))
                else:
                    self.log_test("Setup Test Data", False, f"Failed to create test contact: {response.text}")
                    return False
            except Exception as e:
                self.log_test("Setup Test Data", False, f"Error creating test contact: {str(e)}")
                return False
        
        self.test_contacts = created_contacts
        self.log_test("Setup Test Data", True, f"Created {len(created_contacts)} test contacts")
        return True
    
    def test_dashboard_data_retrieval(self) -> bool:
        """Test that dashboard can retrieve and display contact data"""
        try:
            response = requests.get(f"{self.api_url}/contact", timeout=10)
            
            if response.status_code == 200:
                contacts = response.json()
                
                # Check if we have the expected test contacts
                if len(contacts) >= len(self.test_contacts):
                    self.log_test("Dashboard Data Retrieval", True, f"Retrieved {len(contacts)} contacts")
                    
                    # Validate data structure for dashboard display
                    for contact in contacts[:3]:  # Check first 3 contacts
                        required_fields = ["id", "first_name", "last_name", "email", "phone_number", "message", "services", "created_at"]
                        missing_fields = [field for field in required_fields if field not in contact]
                        
                        if missing_fields:
                            self.log_test("Dashboard Data Structure", False, f"Missing fields: {missing_fields}")
                            return False
                    
                    self.log_test("Dashboard Data Structure", True, "All required fields present")
                    return True
                else:
                    self.log_test("Dashboard Data Retrieval", False, f"Expected {len(self.test_contacts)} contacts, got {len(contacts)}")
                    return False
            else:
                self.log_test("Dashboard Data Retrieval", False, f"Status {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Dashboard Data Retrieval", False, f"Request failed: {str(e)}")
            return False
    
    def test_dashboard_sorting(self) -> bool:
        """Test that contacts are sorted by creation date (newest first)"""
        try:
            response = requests.get(f"{self.api_url}/contact", timeout=10)
            
            if response.status_code == 200:
                contacts = response.json()
                
                if len(contacts) >= 2:
                    # Check if contacts are sorted by created_at (newest first)
                    for i in range(len(contacts) - 1):
                        current_created = contacts[i].get("created_at")
                        next_created = contacts[i + 1].get("created_at")
                        
                        if current_created and next_created:
                            # Parse datetime strings for comparison
                            try:
                                current_dt = datetime.fromisoformat(current_created.replace('Z', '+00:00'))
                                next_dt = datetime.fromisoformat(next_created.replace('Z', '+00:00'))
                                
                                if current_dt < next_dt:
                                    self.log_test("Dashboard Sorting", False, "Contacts not sorted by newest first")
                                    return False
                            except ValueError:
                                # If datetime parsing fails, skip this check
                                continue
                    
                    self.log_test("Dashboard Sorting", True, "Contacts sorted by newest first")
                    return True
                else:
                    self.log_test("Dashboard Sorting", True, "Not enough contacts to test sorting")
                    return True
            else:
                self.log_test("Dashboard Sorting", False, f"Status {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Dashboard Sorting", False, f"Request failed: {str(e)}")
            return False
    
    def test_dashboard_search_functionality(self) -> bool:
        """Test dashboard search by retrieving contacts and checking data integrity"""
        try:
            response = requests.get(f"{self.api_url}/contact", timeout=10)
            
            if response.status_code == 200:
                contacts = response.json()
                
                # Simulate dashboard search functionality
                search_terms = ["john", "sarah", "mike", "web development", "mobile"]
                found_contacts = []
                
                for term in search_terms:
                    matching_contacts = []
                    for contact in contacts:
                        # Search in name, email, message, and services
                        searchable_text = f"{contact.get('first_name', '')} {contact.get('last_name', '')} {contact.get('email', '')} {contact.get('message', '')} {' '.join(contact.get('services', []))}".lower()
                        if term.lower() in searchable_text:
                            matching_contacts.append(contact)
                    
                    if matching_contacts:
                        found_contacts.extend(matching_contacts)
                
                self.log_test("Dashboard Search", True, f"Found {len(set(found_contacts))} contacts matching search terms")
                return True
            else:
                self.log_test("Dashboard Search", False, f"Status {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Dashboard Search", False, f"Request failed: {str(e)}")
            return False
    
    def test_dashboard_contact_management(self) -> bool:
        """Test dashboard contact management operations"""
        if not self.test_contacts:
            self.log_test("Dashboard Contact Management", False, "No test contacts available")
            return False
        
        contact_id = self.test_contacts[0]
        
        # Test contact update
        update_data = {
            "first_name": "John Updated",
            "last_name": "Smith Updated",
            "email": "john.updated@example.com",
            "phone_number": "+1234567890",
            "message": "Updated message for dashboard testing.",
            "services": ["Web Development", "SEO", "Digital Marketing"]
        }
        
        try:
            response = requests.put(f"{self.api_url}/contact/{contact_id}", json=update_data, timeout=10)
            
            if response.status_code == 200:
                self.log_test("Dashboard Contact Update", True, "Contact updated successfully")
                
                # Verify the update
                get_response = requests.get(f"{self.api_url}/contact", timeout=10)
                if get_response.status_code == 200:
                    contacts = get_response.json()
                    updated_contact = next((c for c in contacts if c.get("id") == contact_id), None)
                    
                    if updated_contact and updated_contact.get("first_name") == "John Updated":
                        self.log_test("Dashboard Contact Verification", True, "Update verified successfully")
                        return True
                    else:
                        self.log_test("Dashboard Contact Verification", False, "Update not reflected in data")
                        return False
                else:
                    self.log_test("Dashboard Contact Verification", False, "Failed to retrieve updated contact")
                    return False
            else:
                self.log_test("Dashboard Contact Update", False, f"Status {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Dashboard Contact Management", False, f"Request failed: {str(e)}")
            return False
    
    def test_dashboard_performance(self) -> bool:
        """Test dashboard performance with multiple requests"""
        try:
            start_time = datetime.now()
            
            # Make multiple requests to simulate dashboard usage
            for i in range(5):
                response = requests.get(f"{self.api_url}/contact", timeout=10)
                if response.status_code != 200:
                    self.log_test("Dashboard Performance", False, f"Request {i+1} failed: {response.status_code}")
                    return False
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Performance threshold: 5 requests should complete within 10 seconds
            if duration <= 10:
                self.log_test("Dashboard Performance", True, f"5 requests completed in {duration:.2f}s")
                return True
            else:
                self.log_test("Dashboard Performance", False, f"5 requests took {duration:.2f}s (too slow)")
                return False
        except Exception as e:
            self.log_test("Dashboard Performance", False, f"Performance test failed: {str(e)}")
            return False
    
    def test_dashboard_error_handling(self) -> bool:
        """Test dashboard error handling with invalid requests"""
        invalid_tests = [
            {
                "name": "Invalid Contact ID",
                "url": f"{self.api_url}/contact/invalid-id",
                "method": "GET",
                "expected_status": 404
            },
            {
                "name": "Non-existent Contact",
                "url": f"{self.api_url}/contact/507f1f77bcf86cd799439011",
                "method": "GET",
                "expected_status": 404
            }
        ]
        
        all_passed = True
        for test in invalid_tests:
            try:
                if test["method"] == "GET":
                    response = requests.get(test["url"], timeout=10)
                elif test["method"] == "PUT":
                    response = requests.put(test["url"], json={}, timeout=10)
                elif test["method"] == "DELETE":
                    response = requests.delete(test["url"], timeout=10)
                
                success = response.status_code == test["expected_status"]
                self.log_test(f"Error Handling - {test['name']}", success, f"Status {response.status_code}")
                if not success:
                    all_passed = False
            except Exception as e:
                self.log_test(f"Error Handling - {test['name']}", False, f"Request failed: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def cleanup_test_data(self) -> bool:
        """Clean up test contacts"""
        if not self.test_contacts:
            return True
        
        deleted_count = 0
        for contact_id in self.test_contacts:
            try:
                response = requests.delete(f"{self.api_url}/contact/{contact_id}", timeout=10)
                if response.status_code == 200:
                    deleted_count += 1
            except Exception:
                pass
        
        self.log_test("Cleanup Test Data", True, f"Deleted {deleted_count}/{len(self.test_contacts)} test contacts")
        return True
    
    def run_all_tests(self):
        """Run all dashboard tests in sequence"""
        print("🧪 COSMO Digitals Admin Dashboard Test Suite")
        print("=" * 60)
        print(f"📍 Testing Dashboard at: {self.api_url}")
        print()
        
        # Setup test data
        if not self.setup_test_data():
            print("❌ Failed to setup test data. Aborting tests.")
            return False
        
        # Run dashboard tests
        self.test_dashboard_data_retrieval()
        self.test_dashboard_sorting()
        self.test_dashboard_search_functionality()
        self.test_dashboard_contact_management()
        self.test_dashboard_performance()
        self.test_dashboard_error_handling()
        
        # Cleanup
        self.cleanup_test_data()
        
        # Summary
        print("\n" + "=" * 60)
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        print(f"📊 Test Summary: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All dashboard tests passed! Admin dashboard is working correctly.")
        else:
            print("⚠️  Some dashboard tests failed. Please check the implementation.")
        
        return passed == total

def main():
    """Main function to run the dashboard test suite"""
    tester = AdminDashboardTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 