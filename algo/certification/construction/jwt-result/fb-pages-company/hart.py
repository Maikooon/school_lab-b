import matplotlib.pyplot as plt

# データの準備 (例)
x = [300000, 400000, 450000, 475000, 500000,550000]
y = [20,11,7.4,1.5,0,0]

# 散布図の作成
plt.scatter(x, y)

# グラフのタイトルと軸ラベルの設定
plt.title('実行時間と回数の関係')
plt.xlabel('実行時間')
plt.ylabel('回数')

# グリッド線の表示
plt.grid(True)

# グラフの表示
plt.show()