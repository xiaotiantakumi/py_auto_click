#!/bin/bash

echo "マウスクリック自動化プロセスを停止します..."

# auto_click.pyプロセスを検索
PIDS=$(ps aux | grep "python auto_click.py" | grep -v grep | awk '{print $2}')

if [ -z "$PIDS" ]; then
    echo "実行中のauto_click.pyプロセスは見つかりませんでした。"
    exit 0
fi

echo "見つかったプロセス:"
ps aux | grep "python auto_click.py" | grep -v grep

echo ""
echo "以下のプロセスを停止します: $PIDS"

# 各プロセスをkill
for PID in $PIDS; do
    echo "プロセス $PID を停止中..."
    kill $PID
    if [ $? -eq 0 ]; then
        echo "✅ プロセス $PID を正常に停止しました"
    else
        echo "❌ プロセス $PID の停止に失敗しました"
    fi
done

# 確認
sleep 1
REMAINING=$(ps aux | grep "python auto_click.py" | grep -v grep | awk '{print $2}')

if [ -z "$REMAINING" ]; then
    echo "✅ すべてのauto_click.pyプロセスが停止されました"
else
    echo "⚠️  以下のプロセスがまだ実行中です: $REMAINING"
    echo "強制終了しますか？ (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        for PID in $REMAINING; do
            echo "プロセス $PID を強制終了中..."
            kill -9 $PID
        done
        echo "✅ 強制終了完了"
    fi
fi
