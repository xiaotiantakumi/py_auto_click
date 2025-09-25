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
    print("マウスクリック自動化を開始します...")
    print("終了するにはCtrl+Cを押してください")
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

