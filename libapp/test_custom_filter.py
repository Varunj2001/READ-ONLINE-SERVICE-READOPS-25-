#!/usr/bin/env python
"""
Test script for custom mul filter
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
django.setup()

from libapp.templatetags.custom_filters import mul

def test_mul_filter():
    """Test the mul filter function"""
    print("Testing custom mul filter...")
    
    # Test cases
    test_cases = [
        (5, 20, 100),
        (10, 3, 30),
        (0, 5, 0),
        (2.5, 4, 10.0),
        ("5", "20", 100.0),
        ("invalid", "20", 0),
    ]
    
    for value, arg, expected in test_cases:
        result = mul(value, arg)
        status = "✅" if result == expected else "❌"
        print(f"{status} mul({value}, {arg}) = {result} (expected: {expected})")
    
    print("\nCustom mul filter test completed!")

if __name__ == "__main__":
    test_mul_filter()
