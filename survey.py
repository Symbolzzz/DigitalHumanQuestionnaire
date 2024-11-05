import streamlit as st
import pandas as pd
from datetime import datetime

# 定义视频数据，包含每组的视频文件路径
video_groups = [
    {
        "group_id": "group_1",
        "gt": "survey_source/GT_2_scott_0_2_2_part1.mp4",
        "ai_1": "survey_source/diffshge_2_scott_0_2_2_part1.mp4",
        "ai_2": "survey_source/ours_2_scott_0_2_2_part1.mp4",
    },
    {
        "group_id": "group_2",
        "gt": "render/GT_4_lawrence_0_2_2.mp4",
        "ai_1": "render/diffshge_4_lawrence_0_2_2.mp4",
        "ai_2": "render/ours_4_lawrence_0_2_2.mp4",
    },
    # 可以继续添加更多组
]

# 初始化或加载现有数据文件
def load_data():
    try:
        return pd.read_csv("survey_results.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["timestamp", "group_id", "ai_video_id", 
                                     "similarity_score", "motion_accuracy_score"])

# 保存数据到 CSV 文件
def save_data(data):
    data.to_csv("survey_results.csv", index=False)

# 加载当前数据
data = load_data()

# 显示问卷界面
st.title("AI Generated Video Survey")

# 遍历视频组
for group in video_groups:
    st.write(f"### 组别: {group['group_id']}")

    # 创建三列布局
    col1, col2, col3 = st.columns(3)

    # 在每个列中添加视频和评分控件
    with col1:
        st.subheader("GT")
        st.video(group["gt"])

    with col2:
        st.subheader("AI 视频 1")
        st.video(group["ai_1"])
        similarity_score_1 = st.slider(
            f"{group['group_id']} - AI 视频 1 与 GT 的相似度评分 (1-5)", 1, 5, 3, key=f"{group['group_id']}_ai_1_similarity"
        )
        motion_accuracy_score_1 = st.slider(
            f"{group['group_id']} - AI 视频 1 动作是否符合音频语义评分 (1-5)", 1, 5, 3, key=f"{group['group_id']}_ai_1_motion_accuracy"
        )

    with col3:
        st.subheader("AI 视频 2")
        st.video(group["ai_2"])
        similarity_score_2 = st.slider(
            f"{group['group_id']} - AI 视频 2 与 GT 的相似度评分 (1-5)", 1, 5, 3, key=f"{group['group_id']}_ai_2_similarity"
        )
        motion_accuracy_score_2 = st.slider(
            f"{group['group_id']} - AI 视频 2 动作是否符合音频语义评分 (1-5)", 1, 5, 3, key=f"{group['group_id']}_ai_2_motion_accuracy"
        )

    # 提交评分按钮
    if st.button(f"提交评分 - {group['group_id']}"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entries = pd.DataFrame({
            "timestamp": [timestamp, timestamp],
            "group_id": [group["group_id"], group["group_id"]],
            "ai_video_id": ["ai_1", "ai_2"],
            "similarity_score": [similarity_score_1, similarity_score_2],
            "motion_accuracy_score": [motion_accuracy_score_1, motion_accuracy_score_2]
        })
        updated_data = pd.concat([data, new_entries], ignore_index=True)
        save_data(updated_data)
        st.success(f"{group['group_id']} 的评分已提交！")
        data = updated_data  # 更新数据

# 显示当前保存的数据
st.write("当前数据：")
st.dataframe(data)