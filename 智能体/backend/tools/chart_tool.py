import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime
from langchain_core.tools import tool
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
CHANNEL_DATA = [
    {"channel": "抖音/短视频信息流", "investment": 86, "roi": 6.9},
    {"channel": "小红书种草", "investment": 42, "roi": 8.2},
    {"channel": "天猫/京东站内推广", "investment": 65, "roi": 9.1},
    {"channel": "线下商超/体验店", "investment": 48, "roi": 5.4},
    {"channel": "行业展会与B端渠道", "investment": 35, "roi": 6.1},
    {"channel": "搜索引擎/信息流广告", "investment": 10, "roi": 7.0},
]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs", "charts")
@tool
def generate_sales_chart() -> str:
    """
    生成2025年9月各营销渠道投入金额的柱状图，并保存为PNG图片文件。

    这个工具不需要任何参数，调用它会自动使用9月营销报告里的渠道投放数据画图。

    返回：生成的图片文件在电脑上的完整路径。
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    channels = [item["channel"] for item in CHANNEL_DATA]
    investments = [item["investment"] for item in CHANNEL_DATA]

    plt.figure(figsize=(9, 5.5))
    bars = plt.bar(channels, investments, color="#2F6FED")

    plt.title("2025年9月各渠道营销投入（万元）", fontsize=14)
    plt.ylabel("投入金额（万元）")
    plt.xticks(rotation=25, ha="right")

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1,
            str(height),
            ha="center",
            fontsize=9,
        )

    plt.tight_layout()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(OUTPUT_DIR, f"channel_investment_{timestamp}.png")
    plt.savefig(file_path, dpi=150)
    plt.close()

    return file_path