#!/usr/bin/env python3
"""
Test version of lottery analyzer without pandas dependency
"""

import csv
from datetime import datetime
from collections import Counter
import random

class TestLotteryAnalyzer:
    def __init__(self):
        self.data = {}
    
    def load_data(self, lottery_type, csv_path):
        """Load CSV data without pandas"""
        data = []
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row['date'] = datetime.strptime(row['date'], '%Y-%m-%d')
                    data.append(row)
            
            self.data[lottery_type] = data
            return len(data)
        except Exception as e:
            print(f"Error loading {csv_path}: {e}")
            return 0
    
    def get_recent_data(self, lottery_type, recent_count=50):
        if lottery_type not in self.data:
            return None
        return self.data[lottery_type][-recent_count:]
    
    def analyze_frequency(self, lottery_type, numbers_column_prefix, number_range, recent_count=30):
        recent_data = self.get_recent_data(lottery_type, recent_count)
        if recent_data is None:
            return {}
        
        frequency = {i: 0 for i in range(1, number_range + 1)}
        
        for row in recent_data:
            for col, value in row.items():
                if col.startswith(numbers_column_prefix):
                    try:
                        number = int(value)
                        if number in frequency:
                            frequency[number] += 1
                    except ValueError:
                        continue
        
        return frequency
    
    def test_loto6_prediction(self):
        """Test Loto6 prediction with sample data"""
        if 'loto6' not in self.data:
            return None, "No Loto6 data loaded"
        
        frequency = self.analyze_frequency('loto6', 'loto6_', 43, 30)
        
        # Create weights based on frequency and random factors
        weights = {}
        for i in range(1, 44):
            base_weight = frequency.get(i, 0)
            weights[i] = base_weight + random.uniform(0.1, 0.5)
        
        sorted_numbers = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        prediction = [num for num, _ in sorted_numbers[:6]]
        
        bonus_weights = {k: v for k, v in weights.items() if k not in prediction}
        bonus = max(bonus_weights.items(), key=lambda x: x[1])[0]
        
        explanation = f"Prediction based on frequency analysis of recent draws"
        
        return (sorted(prediction), bonus), explanation

def test_with_sample_data():
    print("🧪 Testing with sample data...")
    
    analyzer = TestLotteryAnalyzer()
    
    # Test loading Loto6 sample data
    count = analyzer.load_data('loto6', 'data/loto6_sample.csv')
    print(f"Loaded {count} Loto6 records")
    
    if count > 0:
        # Test frequency analysis
        frequency = analyzer.analyze_frequency('loto6', 'loto6_', 43, 10)
        print(f"Frequency analysis sample: {dict(list(frequency.items())[:5])}")
        
        # Test prediction
        result, explanation = analyzer.test_loto6_prediction()
        if result:
            prediction, bonus = result
            print(f"Loto6 prediction: {prediction}")
            print(f"Bonus: {bonus}")
            print(f"Explanation: {explanation}")
    
    print("✅ Sample data test completed!")

if __name__ == "__main__":
    test_with_sample_data()