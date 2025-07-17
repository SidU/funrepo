#!/usr/bin/env python3
"""
Cooling System - A simple solution for when it's too hot!

This module provides a basic temperature monitoring and cooling control system
to address the "too hot" problem.
"""

import time
import random
from typing import Dict, List


class CoolingSystem:
    """A simple cooling system that can help when it's too hot."""
    
    def __init__(self, target_temp: float = 22.0):
        """
        Initialize the cooling system.
        
        Args:
            target_temp: The desired temperature in Celsius (default: 22°C)
        """
        self.target_temp = target_temp
        self.current_temp = 30.0  # Start hot!
        self.fan_speed = 0  # 0-100%
        self.ac_on = False
        self.cooling_history: List[Dict] = []
        
    def get_current_temperature(self) -> float:
        """Get the current temperature reading."""
        # Simulate some temperature fluctuation
        fluctuation = random.uniform(-0.5, 0.5)
        return round(self.current_temp + fluctuation, 1)
    
    def is_too_hot(self) -> bool:
        """Check if the current temperature is too hot."""
        return self.get_current_temperature() > self.target_temp + 2.0
    
    def adjust_fan_speed(self, temp_diff: float) -> None:
        """Adjust fan speed based on temperature difference."""
        if temp_diff > 5:
            self.fan_speed = 100
        elif temp_diff > 3:
            self.fan_speed = 75
        elif temp_diff > 1:
            self.fan_speed = 50
        else:
            self.fan_speed = 25
            
        # Cap fan speed
        self.fan_speed = min(100, max(0, self.fan_speed))
    
    def activate_cooling(self) -> str:
        """Activate cooling measures when it's too hot."""
        current = self.get_current_temperature()
        temp_diff = current - self.target_temp
        
        if temp_diff <= 0:
            return f"Temperature is perfect at {current}°C! No cooling needed."
        
        # Adjust cooling based on how hot it is
        self.adjust_fan_speed(temp_diff)
        
        if temp_diff > 6:
            self.ac_on = True
            status = f"🔥 VERY HOT ({current}°C)! AC ON + Fan at {self.fan_speed}%"
        elif temp_diff > 3:
            self.ac_on = False
            status = f"🌡️ Too hot ({current}°C)! Fan at {self.fan_speed}%"
        else:
            self.ac_on = False
            status = f"😰 Warm ({current}°C). Fan at {self.fan_speed}%"
        
        # Simulate cooling effect
        cooling_effect = (self.fan_speed / 100) * 2 + (3 if self.ac_on else 0)
        self.current_temp = max(self.target_temp, self.current_temp - cooling_effect)
        
        # Record this cooling action
        self.cooling_history.append({
            'timestamp': time.time(),
            'temp_before': current,
            'temp_after': self.current_temp,
            'fan_speed': self.fan_speed,
            'ac_on': self.ac_on
        })
        
        return status
    
    def get_status(self) -> str:
        """Get current system status."""
        current = self.get_current_temperature()
        if current <= self.target_temp:
            return f"😎 Cool and comfortable at {current}°C!"
        else:
            return f"🔥 Still hot at {current}°C - cooling in progress..."
    
    def cool_down(self, max_iterations: int = 10) -> List[str]:
        """Run the cooling system until temperature is acceptable."""
        results = []
        results.append(f"🌡️ Starting temperature: {self.get_current_temperature()}°C")
        results.append(f"🎯 Target temperature: {self.target_temp}°C")
        results.append("=" * 50)
        
        for i in range(max_iterations):
            if not self.is_too_hot():
                results.append(f"✅ SUCCESS! Temperature is now comfortable!")
                break
                
            status = self.activate_cooling()
            results.append(f"Step {i+1}: {status}")
            
            # Small delay to simulate time passing
            time.sleep(0.1)
        
        results.append("=" * 50)
        results.append(self.get_status())
        return results


def main():
    """Main function to demonstrate the cooling system."""
    print("🔥 COOLING SYSTEM - Solution for 'It's too hot!' 🔥")
    print()
    
    # Create cooling system
    cooler = CoolingSystem(target_temp=22.0)
    
    # Run the cooling process
    results = cooler.cool_down()
    
    # Display results
    for result in results:
        print(result)
    
    print()
    print("🎉 Problem solved! No more 'too hot' issues!")


if __name__ == "__main__":
    main()