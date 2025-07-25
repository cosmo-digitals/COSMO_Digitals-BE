<!-- # COSMO Digitals Backend Testing Guide

This document provides comprehensive information about testing the COSMO Digitals backend API and admin dashboard functionality.

## 📋 Test Files Overview

The backend includes three main test suites:

1. **`test_admin_api.py`** - Comprehensive API endpoint testing
2. **`test_admin_dashboard.py`** - Dashboard-specific functionality testing
3. **`test_contact_api.py`** - Contact API CRUD operations testing
4. **`run_tests.py`** - Test runner that executes all test suites

## 🚀 Quick Start

### Prerequisites

1. **Start the FastAPI server:**
   ```bash
   # From the COSMO_Digitals-BE directory
   python run.py
   # OR
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Install test dependencies:**
   ```bash
   pip install requests
   ```

### Running Tests

#### Run All Tests
```bash
python run_tests.py
```

#### Run Individual Test Suites
```bash
# Admin API tests
python test_admin_api.py

# Admin Dashboard tests
python test_admin_dashboard.py

# Contact API tests
python test_contact_api.py
```

## 🧪 Test Suite Details

### 1. Admin API Tests (`test_admin_api.py`)

**Purpose:** Comprehensive testing of all API endpoints and functionality.

**Tests Include:**
- ✅ Health check and server connectivity
- ✅ CORS headers validation
- ✅ Contact creation (POST /api/v1/contact)
- ✅ Contact retrieval (GET /api/v1/contact)
- ✅ Contact updates (PUT /api/v1/contact/{id})
- ✅ Contact deletion (DELETE /api/v1/contact/{id})
- ✅ Data validation and error handling
- ✅ Invalid data rejection

**Key Features:**
- Object-oriented test structure
- Detailed logging and reporting
- Error handling and timeout management
- Schema validation
- Performance testing

### 2. Admin Dashboard Tests (`test_admin_dashboard.py`)

**Purpose:** Testing dashboard-specific functionality and frontend-backend integration.

**Tests Include:**
- ✅ Dashboard data retrieval and display
- ✅ Contact sorting (newest first)
- ✅ Search functionality simulation
- ✅ Contact management operations
- ✅ Performance testing (multiple requests)
- ✅ Error handling for invalid requests
- ✅ Test data setup and cleanup

**Key Features:**
- Realistic test data creation
- Dashboard-specific validation
- Search functionality testing
- Performance benchmarking
- Automatic cleanup

### 3. Contact API Tests (`test_contact_api.py`)

**Purpose:** Basic CRUD operations testing for the contact API.

**Tests Include:**
- ✅ Contact creation
- ✅ Contact retrieval
- ✅ Contact updates
- ✅ Contact deletion
- ✅ Data integrity verification

## 📊 Test Results Interpretation

### Success Indicators
- ✅ **PASS** - Test completed successfully
- 🎉 **All tests passed** - Complete test suite success

### Failure Indicators
- ❌ **FAIL** - Test failed
- ⚠️ **Some tests failed** - Partial test suite failure
- 🕐 **TIMEOUT** - Test exceeded time limit

### Common Issues and Solutions

#### Server Not Running
```
❌ Server is not running. Please start the FastAPI server first.
```
**Solution:** Start the server with `python run.py`

#### Connection Errors
```
❌ Error connecting to API: Connection refused
```
**Solution:** Check if the server is running on the correct port (8000)

#### Database Connection Issues
```
❌ Error: Database connection failed
```
**Solution:** Ensure MongoDB is running and properly configured

#### CORS Issues
```
❌ CORS Headers: CORS configuration check
```
**Solution:** Check CORS configuration in `app/main.py`

## 🔧 Test Configuration

### Environment Variables
The tests use the following default configuration:
- **Base URL:** `http://localhost:8000`
- **API Endpoint:** `http://localhost:8000/api/v1`
- **Timeout:** 10 seconds per request
- **Test Data:** 3 sample contacts

### Customizing Tests

#### Change Base URL
```python
# In test files
tester = AdminAPITester(base_url="http://your-server:8000")
```

#### Modify Test Data
```python
# In test_admin_dashboard.py
test_contacts_data = [
    {
        "first_name": "Your",
        "last_name": "Name",
        "email": "your.email@example.com",
        # ... other fields
    }
]
```

#### Adjust Timeouts
```python
# In test files
response = requests.get(url, timeout=30)  # 30 seconds
```

## 📈 Performance Testing

The test suites include performance benchmarks:

- **Response Time:** Individual request timing
- **Throughput:** Multiple concurrent requests
- **Load Testing:** 5 sequential requests within 10 seconds

### Performance Thresholds
- Single request: < 5 seconds
- Multiple requests: < 10 seconds for 5 requests
- Database operations: < 2 seconds

## 🛠️ Debugging Tests

### Enable Verbose Output
```python
# Add to test files for detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Manual API Testing
```bash
# Test specific endpoints manually
curl -X GET http://localhost:8000/api/v1/contact
curl -X POST http://localhost:8000/api/v1/contact \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Test","last_name":"User","email":"test@example.com","phone_number":"1234567890","message":"Test message","services":["Web Development"]}'
```

### Database Inspection
```python
# Add to test files for database debugging
from app.database.mongodb import get_db
db = await get_db()
contacts = await db["contacts"].find().to_list(1000)
print(f"Database contains {len(contacts)} contacts")
```

## 🔄 Continuous Integration

### GitHub Actions Example
```yaml
name: Backend Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Start MongoDB
        run: sudo systemctl start mongod
      - name: Run tests
        run: python run_tests.py
```

## 📝 Adding New Tests

### Creating a New Test File
```python
#!/usr/bin/env python3
"""
Test script for [Feature Name]
"""
import requests
import sys
from datetime import datetime

class FeatureTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1"
    
    def test_feature(self):
        """Test the new feature"""
        # Your test implementation here
        pass
    
    def run_all_tests(self):
        """Run all tests"""
        self.test_feature()
        # Add more tests as needed

if __name__ == "__main__":
    tester = FeatureTester()
    tester.run_all_tests()
```

### Integration with Test Runner
Add your new test to `run_tests.py`:
```python
# Run new feature tests
if os.path.exists("test_new_feature.py"):
    success = run_test_script("test_new_feature.py", "New Feature Tests")
    test_results.append(("New Feature", success))
```

## 🤝 Contributing

When adding new tests:

1. Follow the existing naming conventions
2. Include comprehensive error handling
3. Add proper documentation
4. Update this testing guide
5. Ensure tests are idempotent (can run multiple times)

## 📞 Support

For issues with the test suites:

1. Check the server logs for errors
2. Verify database connectivity
3. Ensure all dependencies are installed
4. Review the test output for specific failure details

---

**Last Updated:** December 2024  
**Version:** 1.0.0  -->