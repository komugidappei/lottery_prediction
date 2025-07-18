# 🎰 宝くじ予想AI

過去の当選履歴データを統計的に分析し、次回の当選番号を予想するWebアプリケーションです。

## 対応する宝くじ

- **ロト6**: 1〜43から6個 + ボーナス1個
- **ロト7**: 1〜37から7個 + ボーナス2個  
- **ナンバーズ3**: 000〜999の3桁数字
- **ナンバーズ4**: 0000〜9999の4桁数字

## 特徴

- 📊 過去データの出現頻度分析
- 📅 曜日別傾向の統計分析
- 🎯 直近データを重視した予測アルゴリズム
- 📝 予想根拠の詳細説明
- 📈 インタラクティブなグラフ表示

## インストール方法

1. リポジトリをクローンまたはダウンロード
2. 必要なライブラリをインストール

```bash
pip install -r requirements.txt
```

## 使用方法

1. アプリケーションを起動

```bash
streamlit run app.py
```

2. ブラウザで `http://localhost:8501` にアクセス
3. 各タブで対応するCSVファイルをアップロード
4. 分析対象回数を調整
5. 「予想実行」ボタンをクリック

## CSVファイル形式

### ロト6
```csv
date,day,loto6_1,loto6_2,loto6_3,loto6_4,loto6_5,loto6_6,bonus
2024-06-20,Thursday,3,12,18,21,30,43,16
```

### ロト7
```csv
date,day,loto7_1,loto7_2,loto7_3,loto7_4,loto7_5,loto7_6,loto7_7,bonus1,bonus2
2024-06-21,Friday,2,8,15,22,29,34,37,11,25
```

### ナンバーズ3
```csv
date,day,number
2024-06-20,Thursday,582
```

### ナンバーズ4
```csv
date,day,number
2024-06-20,Thursday,5829
```

## サンプルデータ

### 📊 大量サンプルデータ（推奨）
統計的により意味のある予測のため、以下の大量サンプルデータを使用してください：
- `loto6_large_sample.csv` - **500回分**（2000年から）
- `loto7_large_sample.csv` - **400回分**（2013年から）
- `numbers3_large_sample.csv` - **600回分**（1994年から）
- `numbers4_large_sample.csv` - **600回分**（1994年から）

### 📋 小量サンプルデータ（テスト用）
- `loto6_sample.csv` - 10回分
- `loto7_sample.csv` - 10回分
- `numbers3_sample.csv` - 10回分
- `numbers4_sample.csv` - 10回分

## 🎯 実際のデータ取得方法

### 公式データソース
1. **みずほ銀行 宝くじコーナー**
   - ロト6: https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto6/
   - ロト7: https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto7/
   - 過去データのCSVダウンロード可能

2. **宝くじ公式サイト**
   - ナンバーズ3・4の履歴データ
   - https://www.takarakuji-official.jp/

### データ生成スクリプト
より多くのサンプルデータが必要な場合：
```bash
python3 generate_sample_data_simple.py
```

## 予測アルゴリズム

1. **出現頻度分析**: 指定期間内での各数字の出現回数を計算
2. **曜日別傾向**: 曜日ごとの数字出現パターンを分析
3. **重み付け計算**: 出現頻度と曜日傾向を組み合わせて各数字の重みを算出
4. **予測実行**: 重みの高い数字を選択し、ランダム要素も加えて予測

## 注意事項

⚠️ **重要**: この予想は過去データの統計分析に基づく参考情報です。実際の当選を保証するものではありません。宝くじは計画的に楽しみましょう。

## 技術スタック

- **Python**: 3.8+
- **Streamlit**: Webアプリフレームワーク
- **Pandas**: データ処理
- **NumPy**: 数値計算
- **Plotly**: グラフ表示
- **Scikit-learn**: 機械学習ライブラリ

## ライセンス

MIT License