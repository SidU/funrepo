#!/usr/bin/env python3
"""
Tests for the Cooling System - Ensuring it solves the "too hot" problem!
"""

import sys
import os
import unittest
from unittest.mock import patch

# Add the current directory to the path so we can import cooling_system
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cooling_system import CoolingSystem


class TestCoolingSystem(unittest.TestCase):
    """Test cases for the CoolingSystem class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.cooler = CoolingSystem(target_temp=22.0)
    
    def test_initialization(self):
        """Test that the cooling system initializes correctly."""
        self.assertEqual(self.cooler.target_temp, 22.0)
        self.assertEqual(self.cooler.current_temp, 30.0)
        self.assertEqual(self.cooler.fan_speed, 0)
        self.assertFalse(self.cooler.ac_on)
        self.assertEqual(len(self.cooler.cooling_history), 0)
    
    def test_is_too_hot(self):
        """Test the 'too hot' detection functionality."""
        # Mock temperature to be definitely too hot
        with patch.object(self.cooler, 'get_current_temperature', return_value=28.0):
            self.assertTrue(self.cooler.is_too_hot())
        
        # Mock temperature to be comfortable
        with patch.object(self.cooler, 'get_current_temperature', return_value=22.0):
            self.assertFalse(self.cooler.is_too_hot())
    
    def test_fan_speed_adjustment(self):
        """Test that fan speed adjusts correctly based on temperature difference."""
        # Test high temperature difference
        self.cooler.adjust_fan_speed(6.0)
        self.assertEqual(self.cooler.fan_speed, 100)
        
        # Test medium temperature difference
        self.cooler.adjust_fan_speed(4.0)
        self.assertEqual(self.cooler.fan_speed, 75)
        
        # Test low temperature difference
        self.cooler.adjust_fan_speed(2.0)
        self.assertEqual(self.cooler.fan_speed, 50)
        
        # Test minimal temperature difference
        self.cooler.adjust_fan_speed(0.5)
        self.assertEqual(self.cooler.fan_speed, 25)
    
    def test_activate_cooling_when_hot(self):
        """Test that cooling activates when temperature is too hot."""
        # Set a high temperature
        with patch.object(self.cooler, 'get_current_temperature', return_value=30.0):
            result = self.cooler.activate_cooling()
            
            # Should activate cooling measures
            self.assertIn("HOT", result)
            self.assertTrue(self.cooler.fan_speed > 0)
            self.assertEqual(len(self.cooler.cooling_history), 1)
    
    def test_activate_cooling_when_comfortable(self):
        """Test that cooling doesn't activate when temperature is comfortable."""
        # Set a comfortable temperature
        with patch.object(self.cooler, 'get_current_temperature', return_value=21.0):
            result = self.cooler.activate_cooling()
            
            # Should indicate no cooling needed
            self.assertIn("perfect", result.lower())
            self.assertIn("no cooling needed", result.lower())
    
    def test_cooling_reduces_temperature(self):
        """Test that the cooling system actually reduces temperature."""
        initial_temp = self.cooler.current_temp
        
        # Activate cooling
        with patch.object(self.cooler, 'get_current_temperature', return_value=30.0):
            self.cooler.activate_cooling()
        
        # Temperature should be reduced
        self.assertLess(self.cooler.current_temp, initial_temp)
    
    def test_ac_activation_on_very_hot(self):
        """Test that AC activates when it's very hot."""
        # Set very hot temperature
        with patch.object(self.cooler, 'get_current_temperature', return_value=32.0):
            self.cooler.activate_cooling()
            
            # AC should be activated for very hot conditions
            self.assertTrue(self.cooler.ac_on)
    
    def test_cool_down_process(self):
        """Test the complete cool down process."""
        # Run the cooling process
        results = self.cooler.cool_down(max_iterations=5)
        
        # Should return a list of status messages
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        
        # Should have some indication of the process
        results_text = " ".join(results)
        self.assertIn("temperature", results_text.lower())


def run_tests():
    """Run all tests and return the result."""
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCoolingSystem)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("🧪 Testing the Cooling System - Making sure it solves 'too hot' problems!")
    print("=" * 70)
    
    success = run_tests()
    
    print("=" * 70)
    if success:
        print("✅ All tests passed! The cooling system is working perfectly!")
        print("🎉 'It's too hot' problem is officially solved!")
    else:
        print("❌ Some tests failed. The cooling system needs more work.")
        sys.exit(1)