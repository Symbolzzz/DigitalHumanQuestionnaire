import streamlit as st
import pandas as pd
import os
from datetime import datetime
import random

# 设置页面宽度和配置
st.set_page_config(layout="wide")
# 定义保存数据的文件路径
csv_file = "survey_results.csv"

# 定义一个函数来加载或初始化数据
def load_data():
    if os.path.exists(csv_file):
        return pd.read_csv(csv_file)
    else:
        return pd.DataFrame(columns=[
            "timestamp", "username", "group_id", "ai_video_id", "model_name",
            "similarity_score", "motion_accuracy_score",
            "mouth_movement_score", "overall_coordination_score"
        ])

# 定义一个函数来保存数据
def save_data(data):
    data.to_csv(csv_file, index=False)

# 加载现有数据
data = load_data()

# 获取视频组
source_path = '/mnt/disk1/xey/DiffuseStyleGesture/DigitalHumanQuestionnaire/survey_source'

def get_video_groups(source_path):
    videos = os.listdir(source_path)
    video_dict = {}

    for video in videos:
        parts = video.split('_')
        group_key = f"{parts[1]}_{parts[2]}_{parts[3]}_{parts[4]}_{parts[5]}_{parts[6]}"
        
        if group_key not in video_dict:
            video_dict[group_key] = []
        video_dict[group_key].append(video)
    
    video_groups = []
    for group in video_dict.values():
        if len(group) == 3:
            gt_video = next((v for v in group if v.startswith("GT")), None)
            other_videos = [v for v in group if not v.startswith("GT")]
            random.shuffle(other_videos)
            video_groups.append([gt_video] + other_videos)
    
    return video_groups

# 随机获取视频分组
video_groups = get_video_groups(source_path)

st.write("# 欢迎！")
st.markdown("Hello, welcome to my voice-driven digital human full-body motion model test. Thank you very much for participating! In this test, you will see 10 sets of video files, each of which consists of three videos, one is the ground truth video, and the other is two AI-generated videos. You need to watch and compare the two AI-generated videos with the ground truth video. Each video is about 30 seconds long, and it may take 20 minutes to complete the entire test. We will collect your feedback on watching the video. I hope you can be fair and objective when making judgments. Thank you again for your participation!")
st.markdown("你好，欢迎来到我的语音驱动数字人全身动作模型测试。非常感谢您的参与！在本次测试中，你将会看到10组视频文件，每组视频文件由三个视频组成，分别是**地面真值视频，还有两个ai生成的视频**。**您需要观看并对比两个ai生成的视频与地面真值视频**，每个视频大概30s左右，完成整个测试可能需要20分钟。我们将会收集您观看视频的反馈。希望您在做判断时可以公平客观，再次感谢您的参与！")
# 获取用户名
username = st.text_input("请输入您的名字：", key="username")
if not username:
    st.warning("请输入您的名字以继续。该名称仅仅用于做区分，你可以填写你喜欢的任何符号。")
    st.stop()

# 使用 CSS 调整页面宽度
st.markdown("""
    <style>
        .main .block-container {
            max-width: 90%;
        }
    </style>
    """, unsafe_allow_html=True)
# 初始化 ratings 列表
ratings = []

# 问卷界面占位符
placeholder = st.empty()

st.markdown("> **下面将会展示10组视频，每组都有三个30秒左右的视频，其中最左边的是GT视频，中间和右边分别是两个模型生成的视频，请你先观看GT视频，再观看两个生成的视频，并完成视频底下的四个问题。**")

random.shuffle(video_groups)
# 创建评分表单
with st.form("survey_form"):
    for i, group in enumerate(video_groups):
        st.write(f"### 组别: {i + 1}")
        
        # 获取模型名称（去掉文件扩展名）
        gt_video = group[0]
        ai_video_1, ai_video_2 = group[1], group[2]
        model_name_1 = ai_video_1.split('_')[0]
        model_name_2 = ai_video_2.split('_')[0]
        
        file_name_1 = ai_video_1.split('.')[0]
        file_name_2 = ai_video_2.split('.')[0]
        
        # 创建三列布局
        col1, col2, col3 = st.columns(3)

        # 在每个列中添加视频和评分控件
        with col1:
            st.subheader("GT")
            st.video(os.path.join(source_path, gt_video))

        with col2:
            st.subheader(f"AI 视频 1")
            st.video(os.path.join(source_path, ai_video_1))
            similarity_score_1 = st.slider(
                f"与 GT 的相似度评分 (1-5)", 1, 5, 3,
                key=f"similarity_{i}_1"
            )
            motion_accuracy_score_1 = st.slider(
                f"动作是否符合音频语义评分 (1-5)", 1, 5, 3,
                key=f"motion_accuracy_{i}_1"
            )
            mouth_movement_score_1 = st.slider(
                f"嘴部运动与 GT 的接近程度 (1-5)", 1, 5, 3,
                key=f"mouth_movement_{i}_1"
            )
            overall_coordination_score_1 = st.slider(
                f"请你结合身体运动和面部表情，给出综合协调度评分 (1-5)", 1, 5, 3,
                key=f"overall_coordination_{i}_1"
            )

        with col3:
            st.subheader(f"AI 视频 2")
            st.video(os.path.join(source_path, ai_video_2))
            similarity_score_2 = st.slider(
                f"与 GT 的相似度评分 (1-5)", 1, 5, 3,
                key=f"similarity_{i}_2"
            )
            motion_accuracy_score_2 = st.slider(
                f"动作是否符合音频语义评分 (1-5)", 1, 5, 3,
                key=f"motion_accuracy_{i}_2"
            )
            mouth_movement_score_2 = st.slider(
                f"嘴部运动与 GT 的接近程度 (1-5)", 1, 5, 3,
                key=f"mouth_movement_{i}_2"
            )
            overall_coordination_score_2 = st.slider(
                f"请你结合身体运动和面部表情，综合协调度评分 (1-5)", 1, 5, 3,
                key=f"overall_coordination_{i}_2"
            )

        # 将该组评分结果添加到字典中
        ratings.append({
            "group_id": i + 1,
            "model_name": model_name_1,
            "file_name": file_name_1,
            "similarity_score": similarity_score_1,
            "motion_accuracy_score": motion_accuracy_score_1,
            "mouth_movement_score": mouth_movement_score_1,
            "overall_coordination_score": overall_coordination_score_1
        })
        
        ratings.append({
            "group_id": i + 1,
            "model_name": model_name_2,
            "file_name": file_name_2,
            "similarity_score": similarity_score_2,
            "motion_accuracy_score": motion_accuracy_score_2,
            "mouth_movement_score": mouth_movement_score_2,
            "overall_coordination_score": overall_coordination_score_2
        })

    # 提交评分按钮
    if st.form_submit_button("提交所有评分"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 为所有评分数据添加时间戳和用户名
        for rating in ratings:
            rating["timestamp"] = timestamp
            rating["username"] = username
        
        # 将评分数据转换为 DataFrame 并保存
        new_data = pd.DataFrame(ratings)
        updated_data = pd.concat([data, new_data], ignore_index=True)
        save_data(updated_data)
        # data = updated_data  # 更新数据
        
        # 清空问卷界面并显示感谢界面
        st.success("所有评分已提交！")
        st.balloons()  # 显示气球特效

        # 清空问卷界面并显示感谢页面
        placeholder = st.empty()  # 创建一个占位符
        with placeholder.container():
            st.write("### 感谢您的参与！")
            st.write("您的反馈对我们非常宝贵，我们会认真分析并改进。")

# 显示当前保存的数据
# st.write("当前数据：")
# st.dataframe(data)