#!/bin/bash

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# 仮想環境が存在しない場合は作成
if [ ! -d "auto_click_env" ]; then
    echo "仮想環境が見つかりません。セットアップを実行します..."
    ./setup.sh
    if [ $? -ne 0 ]; then
        echo "セットアップに失敗しました。"
        exit 1
    fi
fi

# 仮想環境をアクティベート
source auto_click_env/bin/activate

# 必要なパッケージがインストールされているかチェック
if ! python -c "import pyautogui" 2>/dev/null; then
    echo "必要なパッケージがインストールされていません。インストール中..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "パッケージのインストールに失敗しました。"
        exit 1
    fi
fi

# Pythonスクリプトを実行（引数を渡す）
python auto_click.py "$@"

