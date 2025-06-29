import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import Counter
import random

class LotteryAnalyzer:
    def __init__(self):
        self.data = {}
        self.day_mapping = {
            'Monday': '月', 'Tuesday': '火', 'Wednesday': '水',
            'Thursday': '木', 'Friday': '金', 'Saturday': '土', 'Sunday': '日'
        }
    
    def load_data(self, lottery_type, csv_path):
        self.data[lottery_type] = pd.read_csv(csv_path, encoding='utf-8')
        self.data[lottery_type]['date'] = pd.to_datetime(self.data[lottery_type]['date'])
        return len(self.data[lottery_type])
    
    def get_recent_data(self, lottery_type, recent_count=50):
        if lottery_type not in self.data:
            return None
        return self.data[lottery_type].tail(recent_count)
    
    def analyze_frequency(self, lottery_type, numbers_column_prefix, number_range, recent_count=30):
        recent_data = self.get_recent_data(lottery_type, recent_count)
        if recent_data is None:
            return {}
        
        frequency = {}
        for i in range(1, number_range + 1):
            frequency[i] = 0
        
        for _, row in recent_data.iterrows():
            for col in recent_data.columns:
                if col.startswith(numbers_column_prefix):
                    number = int(row[col])
                    if number in frequency:
                        frequency[number] += 1
        
        return frequency
    
    def analyze_day_tendency(self, lottery_type, numbers_column_prefix, number_range):
        if lottery_type not in self.data:
            return {}
        
        data = self.data[lottery_type]
        day_stats = {}
        
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            day_data = data[data['day'] == day]
            day_stats[day] = {'total': len(day_data), 'numbers': []}
            
            for _, row in day_data.iterrows():
                for col in data.columns:
                    if col.startswith(numbers_column_prefix):
                        day_stats[day]['numbers'].append(int(row[col]))
        
        return day_stats
    
    def predict_loto6(self, recent_count=30):
        if 'loto6' not in self.data:
            return None, "データが読み込まれていません"
        
        frequency = self.analyze_frequency('loto6', 'loto6_', 43, recent_count)
        day_stats = self.analyze_day_tendency('loto6', 'loto6_', 43)
        
        recent_data = self.get_recent_data('loto6', recent_count)
        last_draw_day = recent_data.iloc[-1]['day']
        
        weights = {}
        for i in range(1, 44):
            base_weight = frequency.get(i, 0)
            day_weight = 0
            
            if last_draw_day in day_stats and day_stats[last_draw_day]['total'] > 0:
                day_numbers = day_stats[last_draw_day]['numbers']
                day_weight = day_numbers.count(i) / len(day_numbers) if day_numbers else 0
            
            weights[i] = base_weight * 0.7 + day_weight * 100 * 0.3 + random.uniform(0.1, 0.5)
        
        sorted_numbers = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        
        prediction = [num for num, _ in sorted_numbers[:6]]
        
        bonus_weights = {k: v for k, v in weights.items() if k not in prediction}
        bonus = max(bonus_weights.items(), key=lambda x: x[1])[0]
        
        explanation = self._generate_loto6_explanation(prediction, bonus, frequency, recent_count)
        
        return (prediction, bonus), explanation
    
    def predict_loto7(self, recent_count=30):
        if 'loto7' not in self.data:
            return None, "データが読み込まれていません"
        
        frequency = self.analyze_frequency('loto7', 'loto7_', 37, recent_count)
        day_stats = self.analyze_day_tendency('loto7', 'loto7_', 37)
        
        recent_data = self.get_recent_data('loto7', recent_count)
        last_draw_day = recent_data.iloc[-1]['day']
        
        weights = {}
        for i in range(1, 38):
            base_weight = frequency.get(i, 0)
            day_weight = 0
            
            if last_draw_day in day_stats and day_stats[last_draw_day]['total'] > 0:
                day_numbers = day_stats[last_draw_day]['numbers']
                day_weight = day_numbers.count(i) / len(day_numbers) if day_numbers else 0
            
            weights[i] = base_weight * 0.7 + day_weight * 100 * 0.3 + random.uniform(0.1, 0.5)
        
        sorted_numbers = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        
        prediction = [num for num, _ in sorted_numbers[:7]]
        
        remaining_numbers = [k for k, v in weights.items() if k not in prediction]
        bonus1 = random.choice(remaining_numbers)
        remaining_numbers.remove(bonus1)
        bonus2 = random.choice(remaining_numbers)
        
        explanation = self._generate_loto7_explanation(prediction, [bonus1, bonus2], frequency, recent_count)
        
        return (prediction, [bonus1, bonus2]), explanation
    
    def predict_numbers3(self, recent_count=30):
        if 'numbers3' not in self.data:
            return None, "データが読み込まれていません"
        
        recent_data = self.get_recent_data('numbers3', recent_count)
        
        digit_frequency = {0: Counter(), 1: Counter(), 2: Counter()}
        
        for _, row in recent_data.iterrows():
            number = str(row['number']).zfill(3)
            for i, digit in enumerate(number):
                digit_frequency[i][int(digit)] += 1
        
        prediction = ""
        explanations = []
        
        for i in range(3):
            most_common = digit_frequency[i].most_common(3)
            weights = [freq for _, freq in most_common]
            if weights:
                total_weight = sum(weights)
                probabilities = [w / total_weight for w in weights]
                chosen_digit = np.random.choice([digit for digit, _ in most_common], p=probabilities)
                prediction += str(chosen_digit)
                explanations.append(f"{i+1}桁目: {chosen_digit} (過去{recent_count}回中{digit_frequency[i][chosen_digit]}回出現)")
            else:
                digit = random.randint(0, 9)
                prediction += str(digit)
                explanations.append(f"{i+1}桁目: {digit} (ランダム選択)")
        
        explanation = "\n".join(explanations)
        
        return prediction, explanation
    
    def predict_numbers4(self, recent_count=30):
        if 'numbers4' not in self.data:
            return None, "データが読み込まれていません"
        
        recent_data = self.get_recent_data('numbers4', recent_count)
        
        digit_frequency = {0: Counter(), 1: Counter(), 2: Counter(), 3: Counter()}
        
        for _, row in recent_data.iterrows():
            number = str(row['number']).zfill(4)
            for i, digit in enumerate(number):
                digit_frequency[i][int(digit)] += 1
        
        prediction = ""
        explanations = []
        
        for i in range(4):
            most_common = digit_frequency[i].most_common(3)
            weights = [freq for _, freq in most_common]
            if weights:
                total_weight = sum(weights)
                probabilities = [w / total_weight for w in weights]
                chosen_digit = np.random.choice([digit for digit, _ in most_common], p=probabilities)
                prediction += str(chosen_digit)
                explanations.append(f"{i+1}桁目: {chosen_digit} (過去{recent_count}回中{digit_frequency[i][chosen_digit]}回出現)")
            else:
                digit = random.randint(0, 9)
                prediction += str(digit)
                explanations.append(f"{i+1}桁目: {digit} (ランダム選択)")
        
        explanation = "\n".join(explanations)
        
        return prediction, explanation
    
    def _generate_loto6_explanation(self, prediction, bonus, frequency, recent_count):
        explanations = []
        for num in prediction:
            freq = frequency.get(num, 0)
            explanations.append(f"数字 {num}: 過去{recent_count}回中{freq}回出現")
        
        bonus_freq = frequency.get(bonus, 0)
        explanations.append(f"ボーナス {bonus}: 過去{recent_count}回中{bonus_freq}回出現")
        
        return "\n".join(explanations)
    
    def _generate_loto7_explanation(self, prediction, bonus_list, frequency, recent_count):
        explanations = []
        for num in prediction:
            freq = frequency.get(num, 0)
            explanations.append(f"数字 {num}: 過去{recent_count}回中{freq}回出現")
        
        for i, bonus in enumerate(bonus_list):
            bonus_freq = frequency.get(bonus, 0)
            explanations.append(f"ボーナス{i+1} {bonus}: 過去{recent_count}回中{bonus_freq}回出現")
        
        return "\n".join(explanations)