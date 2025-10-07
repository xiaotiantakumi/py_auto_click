#!/usr/bin/env python3
"""
macOS用マウスクリック自動化スクリプト
PowerShellスクリプトのmacOS版
"""

import pyautogui
import random
import time
import sys
import os
import datetime
import re

def check_accessibility_permission():
    """アクセシビリティ権限をチェック"""
    try:
        # 現在のマウス位置を取得
        current_pos = pyautogui.position()
        print(f"現在のマウス位置: {current_pos}")
        
        # テスト用のマウス移動を試行
        test_x, test_y = current_pos.x + 10, current_pos.y + 10
        pyautogui.moveTo(test_x, test_y)
        
        # 移動後の位置を確認
        new_pos = pyautogui.position()
        print(f"テスト移動後の位置: {new_pos}")
        
        # 元の位置に戻す
        pyautogui.moveTo(current_pos.x, current_pos.y)
        
        # 位置が実際に変更されたかチェック
        if new_pos.x != current_pos.x or new_pos.y != current_pos.y:
            print("✅ アクセシビリティ権限が正常に設定されています")
            return True
        else:
            print("❌ マウス移動が実行されませんでした")
            return False
            
    except Exception as e:
        print(f"❌ アクセシビリティ権限エラー: {e}")
        return False

def parse_time_argument(time_str):
    """時間文字列を解析してdatetimeオブジェクトを返す"""
    try:
        # 現在の日付を取得
        today = datetime.date.today()
        
        # 時間形式をチェック（HH:MM または HH）
        if ':' in time_str:
            # HH:MM形式
            hour, minute = map(int, time_str.split(':'))
        else:
            # HH形式
            hour = int(time_str)
            minute = 0
        
        # 時間の妥当性をチェック
        if not (0 <= hour <= 23):
            raise ValueError(f"時間は0-23の範囲で指定してください: {hour}")
        if not (0 <= minute <= 59):
            raise ValueError(f"分は0-59の範囲で指定してください: {minute}")
        
        # datetimeオブジェクトを作成（その日の指定時間）
        target_time = datetime.datetime.combine(today, datetime.time(hour, minute))
        
        return target_time
        
    except ValueError as e:
        print(f"時間の解析エラー: {e}")
        return None

def wait_until_time(target_time):
    """指定された時間まで待機"""
    now = datetime.datetime.now()
    if target_time <= now:
        print("指定された時間は既に過ぎています")
        return False
    
    print(f"指定された時間 ({target_time.strftime('%H:%M')}) まで待機中...")
    
    # 1秒ごとに残り時間を表示
    while datetime.datetime.now() < target_time:
        remaining = target_time - datetime.datetime.now()
        remaining_minutes = int(remaining.total_seconds() // 60)
        remaining_seconds = int(remaining.total_seconds() % 60)
        
        if remaining_minutes > 0:
            print(f"残り時間: {remaining_minutes}分{remaining_seconds}秒", end='\r')
        else:
            print(f"残り時間: {remaining_seconds}秒", end='\r')
        
        time.sleep(1)
    
    print("\n指定された時間に達しました。オフ期間を開始します。")
    return True

def single_click_at(x, y):
    """指定された座標にマウスを移動してクリックを実行"""
    try:
        # マウスカーソルを指定座標に移動
        pyautogui.moveTo(x, y)
        
        # クリックを実行
        pyautogui.click()
        print(f"座標 ({x}, {y}) に移動してクリックしました")
        
    except Exception as e:
        print(f"クリックエラー: {e}")

def main():
    """メイン処理"""
    # 引数を解析
    off_start_time = None
    off_duration_minutes = None
    
    if len(sys.argv) >= 2:
        off_start_time_str = sys.argv[1]
        off_start_time = parse_time_argument(off_start_time_str)
        if off_start_time is None:
            print("エラー: 時間の形式が正しくありません")
            print("使用例: python auto_click.py 12:00 60")
            print("使用例: python auto_click.py 22:15 30")
            sys.exit(1)
    
    if len(sys.argv) >= 3:
        try:
            off_duration_minutes = int(sys.argv[2])
            if off_duration_minutes <= 0:
                raise ValueError("オフ期間は正の数で指定してください")
        except ValueError as e:
            print(f"エラー: {e}")
            sys.exit(1)
    
    print("マウスクリック自動化を開始します...")
    print("終了するにはCtrl+Cを押してください")
    
    # オフ時間が指定されている場合の情報表示
    if off_start_time and off_duration_minutes:
        off_end_time = off_start_time + datetime.timedelta(minutes=off_duration_minutes)
        print(f"オフ期間: {off_start_time.strftime('%H:%M')} - {off_end_time.strftime('%H:%M')} ({off_duration_minutes}分間)")
    elif off_start_time:
        print(f"オフ開始時間: {off_start_time.strftime('%H:%M')} (終了時間は指定されていません)")
    
    print("-" * 50)
    
    # PyAutoGUIの設定
    pyautogui.FAILSAFE = True  # フェイルセーフを有効化
    pyautogui.PAUSE = 0.1      # 各操作間の待機時間を短縮
    
    # 現在の画面サイズを表示
    screen_size = pyautogui.size()
    print(f"画面サイズ: {screen_size}")
    
    # アクセシビリティ権限をチェック
    if not check_accessibility_permission():
        print("エラー: アクセシビリティ権限が必要です")
        print("以下の手順で権限を有効にしてください:")
        print("1. システム環境設定 → セキュリティとプライバシー")
        print("2. プライバシー → アクセシビリティ")
        print("3. ターミナル（またはPython）にチェックを入れる")
        sys.exit(1)
    
    try:
        while True:
            current_time = datetime.datetime.now()
            
            # オフ期間のチェック
            if off_start_time and off_duration_minutes:
                off_end_time = off_start_time + datetime.timedelta(minutes=off_duration_minutes)
                
                # オフ期間前の待機
                if current_time < off_start_time:
                    if not wait_until_time(off_start_time):
                        continue
                
                # オフ期間中の待機
                if off_start_time <= current_time < off_end_time:
                    remaining_off_time = off_end_time - current_time
                    remaining_minutes = int(remaining_off_time.total_seconds() // 60)
                    remaining_seconds = int(remaining_off_time.total_seconds() % 60)
                    
                    if remaining_minutes > 0:
                        print(f"オフ期間中... 残り: {remaining_minutes}分{remaining_seconds}秒", end='\r')
                    else:
                        print(f"オフ期間中... 残り: {remaining_seconds}秒", end='\r')
                    
                    time.sleep(1)
                    continue
                
                # オフ期間終了後の処理
                if current_time >= off_end_time:
                    print(f"\nオフ期間が終了しました ({off_end_time.strftime('%H:%M')})")
                    # オフ期間が終了したら、次の日の同じ時間に設定
                    off_start_time += datetime.timedelta(days=1)
            
            # 通常のクリック処理
            # ランダムな座標を生成（画面サイズ内に調整）
            screen_width, screen_height = pyautogui.size()
            x = random.randint(screen_width - 100, screen_width - 50)  # 画面右端付近
            y = random.randint(400, 500)  # 画面中央付近
            
            # マウスクリックを実行
            single_click_at(x, y)
            
            # 60秒待機
            print("60秒待機中...")
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\nプログラムを終了します...")
    except pyautogui.FailSafeException:
        print("\nフェイルセーフが発動しました。プログラムを終了します...")
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")

if __name__ == "__main__":
    main()

