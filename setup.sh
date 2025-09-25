#!/bin/bash

echo "マウスクリック自動化環境をセットアップします..."

# 仮想環境を作成
echo "仮想環境を作成中..."
python3 -m venv auto_click_env

# 仮想環境をアクティベート
echo "仮想環境をアクティベート中..."
source auto_click_env/bin/activate

# パッケージをインストール
echo "必要なパッケージをインストール中..."
pip install --upgrade pip
pip install pyautogui

# 依存関係を保存
echo "依存関係を保存中..."
pip freeze > requirements.txt

# 実行権限を付与
chmod +x run_auto_click.sh
chmod +x auto_click.py

echo "セットアップ完了！"
echo ""
echo "使用方法:"
echo "1. アクセシビリティ権限を有効にしてください"
echo "2. ./run_auto_click.sh を実行してください"

