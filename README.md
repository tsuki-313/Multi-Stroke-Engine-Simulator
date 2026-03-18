概要Python (Tkinter) で制作した、エンジンの動的サイクルを可視化するシミュレーターです。ボア・ストローク・圧縮比などの基本スペックから、点火順序までリアルタイムにシミュレート可能です。
主な機能
・マルチストローク対応：2サイクル / 4サイクル / 6サイクルを切り替え可能。
・多気筒シミュレーション: 1気筒から最大24気筒までのレイアウトを表示。
・リアルタイム調整: 全数値をスライダーおよび直接入力（Entry）で調整可能。圧縮比 ($\epsilon$) / ボア径 (mm) / ストローク (mm) / コンロッド長 (mm)
パフォーマンス予測: 設定値に基づいたトルク・馬力カーブの動的生成。
バイリンガル対応: 日本語 / 英語のワンタッチ切り替え。

# Sanctuary Engine Simulator v7.3

A high-performance dynamic engine cycle simulator developed in Python (Tkinter). 
Designed for visualizing internal combustion engine mechanisms with extreme flexibility.

## ✨ Key Features
- **Multi-Stroke Support**: Toggle between 2-stroke, 4-stroke, and 6-stroke cycles.
- **Up to 24 Cylinders**: Supports multi-cylinder configurations from 1 to 24.
- **Dual Adjustment System**: Seamlessly adjust parameters via **UI Sliders** or **Manual Text Input**.
- **Sanctuary Concept**: Optimized layout with a clear "Safe Zone" for piston/crank visibility and bank labels.
- **Dynamic Performance Curves**: Real-time generation of Torque and Horsepower (PS) graphs based on your specs.
- **Bilingual Interface**: Quick switch between Japanese and English.

## ⚙️ Adjustable Parameters
- **Compression Ratio (ε)**: Range 1.0 - 25.0
- **Bore & Stroke**: Min 10mm (Supports micro-engine simulations)
- **Connecting Rod Length**: Adjustable for R/L ratio optimization.
- **Firing Order**: Fully customizable sequence (e.g., `1,6,5,10...`).
- **Engine Speed**: Variable RPM simulation.

## 🚀 How to Run
1. Ensure you have Python 3.x installed.
2. Run the script:
   ```bash
   python engine.py

