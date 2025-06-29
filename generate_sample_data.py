#!/usr/bin/env python3
"""
大量のサンプルデータを生成するスクリプト
実際のデータパターンに近い統計的な分布を持つサンプルを作成
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_loto6_data(num_draws=500):
    """ロト6のサンプルデータを生成（より現実的な分布）"""
    data = []
    start_date = datetime(2000, 10, 5)  # ロト6開始日
    current_date = start_date
    
    # 月・木曜日の抽選
    for i in range(num_draws):
        # 次の月曜日または木曜日を探す
        while current_date.weekday() not in [0, 3]:  # 0=月曜, 3=木曜
            current_date += timedelta(days=1)
        
        # より現実的な数字分布（1-43の範囲で偏りを持たせる）
        # 実際のロト6では小さい数字と大きい数字が偏る傾向がある
        numbers = []
        while len(numbers) < 6:
            if len(numbers) < 2:
                # 小さい数字（1-15）を2個程度
                num = np.random.choice(range(1, 16), p=create_weighted_prob(1, 16, 'low'))
            elif len(numbers) < 4:
                # 中間（16-30）を2個程度
                num = np.random.choice(range(16, 31), p=create_weighted_prob(16, 31, 'mid'))
            else:
                # 大きい数字（31-43）を2個程度
                num = np.random.choice(range(31, 44), p=create_weighted_prob(31, 44, 'high'))
            
            if num not in numbers:
                numbers.append(num)
        
        numbers.sort()
        
        # ボーナス数字（本数字以外から選択）
        bonus_candidates = [x for x in range(1, 44) if x not in numbers]
        bonus = random.choice(bonus_candidates)
        
        day_name = current_date.strftime('%A')
        
        data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'day': day_name,
            'loto6_1': numbers[0],
            'loto6_2': numbers[1],
            'loto6_3': numbers[2],
            'loto6_4': numbers[3],
            'loto6_5': numbers[4],
            'loto6_6': numbers[5],
            'bonus': bonus
        })
        
        # 次の抽選日へ（3-4日後）
        current_date += timedelta(days=3 if current_date.weekday() == 0 else 4)
    
    return pd.DataFrame(data)

def generate_loto7_data(num_draws=400):
    """ロト7のサンプルデータを生成"""
    data = []
    start_date = datetime(2013, 4, 5)  # ロト7開始日
    current_date = start_date
    
    # 金曜日の抽選
    for i in range(num_draws):
        while current_date.weekday() != 4:  # 4=金曜
            current_date += timedelta(days=1)
        
        # ロト7の数字生成（1-37）
        numbers = []
        while len(numbers) < 7:
            if len(numbers) < 3:
                num = np.random.choice(range(1, 13), p=create_weighted_prob(1, 13, 'low'))
            elif len(numbers) < 5:
                num = np.random.choice(range(13, 26), p=create_weighted_prob(13, 26, 'mid'))
            else:
                num = np.random.choice(range(26, 38), p=create_weighted_prob(26, 38, 'high'))
            
            if num not in numbers:
                numbers.append(num)
        
        numbers.sort()
        
        # ボーナス数字2個
        bonus_candidates = [x for x in range(1, 38) if x not in numbers]
        bonus1, bonus2 = random.sample(bonus_candidates, 2)
        
        data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'day': current_date.strftime('%A'),
            'loto7_1': numbers[0],
            'loto7_2': numbers[1],
            'loto7_3': numbers[2],
            'loto7_4': numbers[3],
            'loto7_5': numbers[4],
            'loto7_6': numbers[5],
            'loto7_7': numbers[6],
            'bonus1': bonus1,
            'bonus2': bonus2
        })
        
        current_date += timedelta(days=7)  # 次の金曜日
    
    return pd.DataFrame(data)

def generate_numbers_data(digits, num_draws=600):
    """ナンバーズ3/4のサンプルデータを生成"""
    data = []
    start_date = datetime(1994, 10, 7)  # ナンバーズ開始日
    current_date = start_date
    
    # 月〜金の抽選
    for i in range(num_draws):
        while current_date.weekday() > 4:  # 土日をスキップ
            current_date += timedelta(days=1)
        
        # より現実的な数字分布（各桁で偏りを持たせる）
        number_str = ""
        for digit_pos in range(digits):
            # 各桁で微妙に異なる確率分布
            prob_weights = [0.08, 0.12, 0.11, 0.09, 0.10, 0.11, 0.09, 0.12, 0.09, 0.09]
            digit = np.random.choice(range(10), p=prob_weights)
            number_str += str(digit)
        
        data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'day': current_date.strftime('%A'),
            'number': int(number_str)
        })
        
        current_date += timedelta(days=1)
    
    return pd.DataFrame(data)

def create_weighted_prob(start, end, range_type):
    """範囲に応じた重み付き確率分布を作成"""
    size = end - start
    if range_type == 'low':
        # 小さい数字ほど高確率
        weights = np.exp(-np.linspace(0, 2, size))
    elif range_type == 'high':
        # 大きい数字ほど高確率
        weights = np.exp(-np.linspace(2, 0, size))
    else:  # mid
        # 中央が高確率（正規分布風）
        weights = np.exp(-0.5 * (np.linspace(-1, 1, size) ** 2))
    
    return weights / weights.sum()

def main():
    print("📊 大量サンプルデータ生成中...")
    
    # ロト6データ生成（500回分）
    print("🎯 ロト6データ生成中...")
    loto6_df = generate_loto6_data(500)
    loto6_df.to_csv('data/loto6_large_sample.csv', index=False, encoding='utf-8')
    print(f"✅ ロト6: {len(loto6_df)}回分のデータを生成")
    
    # ロト7データ生成（400回分）
    print("🎯 ロト7データ生成中...")
    loto7_df = generate_loto7_data(400)
    loto7_df.to_csv('data/loto7_large_sample.csv', index=False, encoding='utf-8')
    print(f"✅ ロト7: {len(loto7_df)}回分のデータを生成")
    
    # ナンバーズ3データ生成（600回分）
    print("🎯 ナンバーズ3データ生成中...")
    numbers3_df = generate_numbers_data(3, 600)
    numbers3_df.to_csv('data/numbers3_large_sample.csv', index=False, encoding='utf-8')
    print(f"✅ ナンバーズ3: {len(numbers3_df)}回分のデータを生成")
    
    # ナンバーズ4データ生成（600回分）
    print("🎯 ナンバーズ4データ生成中...")
    numbers4_df = generate_numbers_data(4, 600)
    numbers4_df.to_csv('data/numbers4_large_sample.csv', index=False, encoding='utf-8')
    print(f"✅ ナンバーズ4: {len(numbers4_df)}回分のデータを生成")
    
    print("🎉 全てのサンプルデータ生成完了！")
    print("\n📝 使用方法:")
    print("1. 各CSVファイルをStreamlitアプリにアップロード")
    print("2. 分析対象回数を50-100回に設定")
    print("3. 予想実行で統計的により意味のある予測を確認")

if __name__ == "__main__":
    main()