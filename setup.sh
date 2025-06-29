#!/bin/bash

echo "🎰 宝くじ予想AI セットアップスクリプト"
echo "=================================="

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 が見つかりません。Python3をインストールしてください。"
    exit 1
fi

echo "✅ Python3 が見つかりました: $(python3 --version)"

# Check if pip3 is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 が見つかりません。pipをインストールしてください。"
    exit 1
fi

echo "✅ pip3 が見つかりました"

# Install required packages
echo "📦 必要なライブラリをインストール中..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ ライブラリのインストールが完了しました"
else
    echo "❌ ライブラリのインストールに失敗しました"
    exit 1
fi

# Test basic functionality
echo "🧪 基本機能をテスト中..."
python3 test_basic.py

if [ $? -eq 0 ]; then
    echo "✅ 基本機能テスト完了"
else
    echo "❌ 基本機能テストに失敗しました"
    exit 1
fi

echo ""
echo "🎉 セットアップ完了！"
echo ""
echo "アプリを起動するには:"
echo "  streamlit run app.py"
echo ""
echo "その後、ブラウザで http://localhost:8501 にアクセスしてください"