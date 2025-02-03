import matplotlib.pyplot as plt
import numpy as np

files = {
    "proposal-α": "./first-time/100-log.txt",
    "proposal-β": "./parent-token/100-log.txt",
}

total_move_time_results = []


def extract_move_time(files):
    for label, path in files.items():
        move_time_total = []
        with open(path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if "total execution time:" in line:
                    move_time = float(line.split(":")[1].split(" ")[1])
                if "サーバのまたぎ回数:" in line:
                    if 200 <= int(line.split(":")[1].strip()) <= 300:
                        move_time_total.append(move_time)
            total_move_time_results.append((label, move_time_total))
    return total_move_time_results


def plt_picture(move_array):
    plt.figure(figsize=(8, 6))
    colors = plt.cm.tab10(range(len(move_array)))

    x = [0.0, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]  # X軸のラベルと位置を定義

    # Y軸データを準備
    y = [
        57.876,
        54.729,
        54.528,
        55.25,
        54.272,
        55.097,
        54.944,
        52.684,
        48.711642485,
        54.100127481,
        53.440346330,
        48.711642485,
        34.869,
        38.634,
        32.864,
        35.655,
        40.32,
        33.248,
        34.782,
        20.626,
        27.022,
        23.827,
        25.895,
        23.563,
        17.164,
        19.365,
        17.365,
        17.298,
        20.077,
        16.86,
        19.123,
        14.243,
        17.333,
        17.513,
        16.165,
        15.162,
        15.833,
        13.098,
        15.588,
        14.408,
        18.319,
        16.394,
        13.592,
        13.567,
        12.998,
        15.548,
        14.291,
        14.322,
    ]

    # 箱ひげ図用のデータ処理
    unique_x = sorted(set(x))
    grouped_y = {ux: [] for ux in unique_x}
    for xi, yi in zip(x, y):
        grouped_y[xi].append(yi)
    data = [grouped_y[ux] for ux in unique_x]

    # 箱ひげ図のプロット
    plt.boxplot(
        data,
        vert=True,
        patch_artist=True,
        boxprops=dict(facecolor="purple", color="black"),
        medianprops=dict(color="yellow"),
        positions=np.arange(len(unique_x)),  # X軸位置の設定
    )

    # 平均値の計算とプロット
    for i, (label, move_time_results) in enumerate(move_array):
        x_values = [i] * len(move_time_results)
        y_values = [y / 100 for y in move_time_results]
        avg_y = np.mean(y_values)

        # 平均値の線を追加
        plt.hlines(
            avg_y,
            min(np.arange(len(unique_x))),
            max(np.arange(len(unique_x))),
            colors=colors[i],
            linestyles="dashed",
            label=f"{label} (avg)",
        )

        # データ点のプロット
        plt.scatter(
            x_values,
            y_values,
            label=f"{label}",
            color=colors[i],
            s=15,
            alpha=0.7,
        )

    # 軸のラベル設定
    plt.xticks(np.arange(len(unique_x)), [f"{ux:.2f}" for ux in unique_x], rotation=45)
    plt.ylim(0, 1.5)
    plt.xlabel("Parent token valid time")
    plt.ylabel("1RW Move Time (seconds)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("0129-valid.pdf")
    plt.show()


if __name__ == "__main__":
    total_move_time_results = extract_move_time(files)
    plt_picture(total_move_time_results)
