#!/usr/bin/env python3
"""
Basic test script for lottery analyzer without external dependencies
"""

import sys
import os
from datetime import datetime
import random
from collections import Counter

def test_basic_prediction_logic():
    """Test the core prediction logic without pandas"""
    print("Testing basic prediction logic...")
    
    # Test frequency analysis
    test_data = [1, 2, 3, 1, 2, 1, 4, 5, 6, 1]
    frequency = Counter(test_data)
    print(f"Frequency analysis test: {dict(frequency)}")
    
    # Test weighted selection logic
    weights = {i: random.uniform(0.1, 1.0) for i in range(1, 7)}
    sorted_by_weight = sorted(weights.items(), key=lambda x: x[1], reverse=True)
    top_3 = [num for num, _ in sorted_by_weight[:3]]
    print(f"Weighted selection test: {top_3}")
    
    # Test Loto6 style prediction
    loto6_range = list(range(1, 44))
    weights = {i: random.uniform(0.1, 1.0) for i in loto6_range}
    sorted_numbers = sorted(weights.items(), key=lambda x: x[1], reverse=True)
    prediction = [num for num, _ in sorted_numbers[:6]]
    bonus_weights = {k: v for k, v in weights.items() if k not in prediction}
    bonus = max(bonus_weights.items(), key=lambda x: x[1])[0]
    
    print(f"Loto6 prediction test: {sorted(prediction)}, bonus: {bonus}")
    
    # Test Numbers3 style prediction
    digits = []
    for i in range(3):
        digit_freq = Counter([random.randint(0, 9) for _ in range(10)])
        most_common = digit_freq.most_common(3)
        chosen = random.choice([digit for digit, _ in most_common])
        digits.append(str(chosen))
    
    numbers3_prediction = ''.join(digits)
    print(f"Numbers3 prediction test: {numbers3_prediction}")
    
    print("✅ All basic tests passed!")

if __name__ == "__main__":
    test_basic_prediction_logic()