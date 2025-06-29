#!/usr/bin/env python3
"""
大量のサンプルデータを生成するスクリプト（pandas不要版）
実際のデータパターンに近い統計的な分布を持つサンプルを作成
"""

import csv
from datetime import datetime, timedelta
import random

def generate_loto6_data(num_draws=500):
    """ロト6のサンプルデータを生成（500回分）"""
    data = []
    start_date = datetime(2000, 10, 5)  # ロト6開始日
    current_date = start_date
    
    # 月・木曜日の抽選
    for i in range(num_draws):
        # 次の月曜日または木曜日を探す
        while current_date.weekday() not in [0, 3]:  # 0=月曜, 3=木曜
            current_date += timedelta(days=1)
        
        # より現実的な数字分布を生成
        numbers = []
        while len(numbers) < 6:
            # 1-43の範囲で偏りを持たせて選択
            if len(numbers) < 2:
                # 小さい数字を優先
                num = random.choices(range(1, 16), weights=[1.5, 1.4, 1.3, 1.2, 1.1] + [1.0]*10)[0]
            elif len(numbers) < 4:
                # 中間の数字
                num = random.choice(range(16, 31))
            else:
                # 大きい数字
                num = random.choice(range(31, 44))
            
            if num not in numbers:
                numbers.append(num)
        
        numbers.sort()
        
        # ボーナス数字（本数字以外から選択）
        bonus_candidates = [x for x in range(1, 44) if x not in numbers]
        bonus = random.choice(bonus_candidates)
        
        day_name = current_date.strftime('%A')
        
        data.append([
            current_date.strftime('%Y-%m-%d'),
            day_name,
            numbers[0], numbers[1], numbers[2], 
            numbers[3], numbers[4], numbers[5],
            bonus
        ])
        
        # 次の抽選日へ（3-4日後）
        current_date += timedelta(days=3 if current_date.weekday() == 0 else 4)
    
    return data

def generate_loto7_data(num_draws=400):
    """ロト7のサンプルデータを生成（400回分）"""
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
                num = random.choice(range(1, 13))
            elif len(numbers) < 5:
                num = random.choice(range(13, 26))
            else:
                num = random.choice(range(26, 38))
            
            if num not in numbers:
                numbers.append(num)
        
        numbers.sort()
        
        # ボーナス数字2個
        bonus_candidates = [x for x in range(1, 38) if x not in numbers]
        bonus1, bonus2 = random.sample(bonus_candidates, 2)
        
        data.append([
            current_date.strftime('%Y-%m-%d'),
            current_date.strftime('%A'),
            numbers[0], numbers[1], numbers[2], numbers[3],
            numbers[4], numbers[5], numbers[6],
            bonus1, bonus2
        ])
        
        current_date += timedelta(days=7)  # 次の金曜日
    
    return data

def generate_numbers_data(digits, num_draws=600):
    """ナンバーズ3/4のサンプルデータを生成（600回分）"""
    data = []
    start_date = datetime(1994, 10, 7)  # ナンバーズ開始日
    current_date = start_date
    
    # 月〜金の抽選
    for i in range(num_draws):
        while current_date.weekday() > 4:  # 土日をスキップ
            current_date += timedelta(days=1)
        
        # より現実的な数字分布
        number_str = ""
        for digit_pos in range(digits):
            # 各桁で微妙に異なる確率（0-9で微妙な偏り）
            digit = random.choices(
                range(10), 
                weights=[8, 12, 11, 9, 10, 11, 9, 12, 9, 9]
            )[0]
            number_str += str(digit)
        
        data.append([
            current_date.strftime('%Y-%m-%d'),
            current_date.strftime('%A'),
            int(number_str)
        ])
        
        current_date += timedelta(days=1)
    
    return data

def save_csv(filename, headers, data):
    """CSVファイルを保存"""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

def main():
    print("📊 大量サンプルデータ生成中...")
    
    # ロト6データ生成（500回分）
    print("🎯 ロト6データ生成中...")
    loto6_data = generate_loto6_data(500)
    loto6_headers = ['date', 'day', 'loto6_1', 'loto6_2', 'loto6_3', 'loto6_4', 'loto6_5', 'loto6_6', 'bonus']
    save_csv('data/loto6_large_sample.csv', loto6_headers, loto6_data)
    print(f"✅ ロト6: {len(loto6_data)}回分のデータを生成")
    
    # ロト7データ生成（400回分）
    print("🎯 ロト7データ生成中...")
    loto7_data = generate_loto7_data(400)
    loto7_headers = ['date', 'day', 'loto7_1', 'loto7_2', 'loto7_3', 'loto7_4', 'loto7_5', 'loto7_6', 'loto7_7', 'bonus1', 'bonus2']
    save_csv('data/loto7_large_sample.csv', loto7_headers, loto7_data)
    print(f"✅ ロト7: {len(loto7_data)}回分のデータを生成")
    
    # ナンバーズ3データ生成（600回分）
    print("🎯 ナンバーズ3データ生成中...")
    numbers3_data = generate_numbers_data(3, 600)
    numbers_headers = ['date', 'day', 'number']
    save_csv('data/numbers3_large_sample.csv', numbers_headers, numbers3_data)
    print(f"✅ ナンバーズ3: {len(numbers3_data)}回分のデータを生成")
    
    # ナンバーズ4データ生成（600回分）
    print("🎯 ナンバーズ4データ生成中...")
    numbers4_data = generate_numbers_data(4, 600)
    save_csv('data/numbers4_large_sample.csv', numbers_headers, numbers4_data)
    print(f"✅ ナンバーズ4: {len(numbers4_data)}回分のデータを生成")
    
    print("🎉 全てのサンプルデータ生成完了！")
    print("\n📝 使用方法:")
    print("1. 各 *_large_sample.csv ファイルをStreamlitアプリにアップロード")
    print("2. 分析対象回数を50-100回に設定")
    print("3. 予想実行で統計的により意味のある予測を確認")
    print("\n📊 生成されたファイル:")
    print("- data/loto6_large_sample.csv (500回分)")
    print("- data/loto7_large_sample.csv (400回分)")
    print("- data/numbers3_large_sample.csv (600回分)")
    print("- data/numbers4_large_sample.csv (600回分)")

if __name__ == "__main__":
    main()