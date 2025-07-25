#!/usr/bin/env python3
"""
Test script for the Contact API endpoints
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

def test_create_contact():
    """Test creating a new contact"""
    contact_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone_number": "+1234567890",
        "message": "This is a test message from the API test script.",
        "services": ["Web Development", "Mobile App"]
    }
    
    response = requests.post(f"{BASE_URL}/contact", json=contact_data)
    print(f"Create Contact Response: {response.status_code}")
    if response.status_code == 201:
        print(f"Contact created: {response.json()}")
        return response.json().get("id")
    else:
        print(f"Error: {response.text}")
        return None

def test_get_contacts():
    """Test getting all contacts"""
    response = requests.get(f"{BASE_URL}/contact")
    print(f"Get Contacts Response: {response.status_code}")
    if response.status_code == 200:
        contacts = response.json()
        print(f"Found {len(contacts)} contacts")
        for contact in contacts[:3]:  # Show first 3
            print(f"- {contact['first_name']} {contact['last_name']}: {contact['email']}")
        return contacts
    else:
        print(f"Error: {response.text}")
        return []

def test_update_contact(contact_id):
    """Test updating a contact"""
    if not contact_id:
        print("No contact ID provided for update test")
        return
    
    update_data = {
        "first_name": "John Updated",
        "last_name": "Doe Updated",
        "email": "john.updated@example.com",
        "phone_number": "+1234567890",
        "message": "This message has been updated via API test.",
        "services": ["Web Development", "SEO"]
    }
    
    response = requests.put(f"{BASE_URL}/contact/{contact_id}", json=update_data)
    print(f"Update Contact Response: {response.status_code}")
    if response.status_code == 200:
        print(f"Contact updated: {response.json()}")
    else:
        print(f"Error: {response.text}")

def test_delete_contact(contact_id):
    """Test deleting a contact"""
    if not contact_id:
        print("No contact ID provided for delete test")
        return
    
    response = requests.delete(f"{BASE_URL}/contact/{contact_id}")
    print(f"Delete Contact Response: {response.status_code}")
    if response.status_code == 200:
        print(f"Contact deleted: {response.json()}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    print("=== Contact API Test Script ===")
    print(f"Testing API at: {BASE_URL}")
    print()
    
    # Test creating a contact
    print("1. Testing contact creation...")
    contact_id = test_create_contact()
    print()
    
    # Test getting all contacts
    print("2. Testing contact retrieval...")
    contacts = test_get_contacts()
    print()
    
    # Test updating a contact
    print("3. Testing contact update...")
    test_update_contact(contact_id)
    print()
    
    # Test getting contacts again to see the update
    print("4. Testing contact retrieval after update...")
    test_get_contacts()
    print()
    
    # Test deleting a contact
    print("5. Testing contact deletion...")
    test_delete_contact(contact_id)
    print()
    
    # Test getting contacts again to see the deletion
    print("6. Testing contact retrieval after deletion...")
    test_get_contacts()
    print()
    
    print("=== Test Complete ===") 