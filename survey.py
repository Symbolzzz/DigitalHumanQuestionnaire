import streamlit as st
import pandas as pd
import os
from datetime import datetime
from io import StringIO

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
            "timestamp", "username", "group_id", "file_name", "diversity_score",
            "expression_score", "holistic_score",
        ])

# 定义一个函数来保存数据
def save_data(data):
    data.to_csv(csv_file, index=False)

# 加载现有数据
data = load_data()

# 获取视频组
source_path = './survey_source'
expr_source_path = './survey_expr_source'

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
        if len(group) == 4:
            gt_video = next((v for v in group if v.startswith("GT")), None)
            camn_video = next((v for v in group if v.startswith("camn")), None)
            diffshge_video = next((v for v in group if v.startswith("diffshge")), None)
            ours_video = next((v for v in group if v.startswith("ours")), None)
            # random.shuffle(other_videos)
            video_groups.append([gt_video] + [camn_video] + [diffshge_video] + [ours_video])
    
    return video_groups

# 随机获取视频分组
video_groups = get_video_groups(source_path)

st.write("# 欢迎！")
st.markdown("你好，欢迎来到我的语音驱动数字人全身动作模型测试。非常感谢您的参与！在本次测试中，你将会看到9组视频文件，每组视频文件由5个视频组成，分别是**三个ai生成的视频**。**您需要观看并对比三个ai生成的视频**，每个视频大概30s左右，完成整个测试可能需要30分钟。我们将会收集您观看视频的反馈。希望您在做判断时可以公平客观，再次感谢您的参与！")
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

st.markdown("> **下面将会展示9组视频，每组都有5个30秒左右的视频，分别是三个模型生成的视频，其中有两个模型是可以生成表情与动作，为了更好地观察表情的准确度，每个视频下方展示的是单独渲染表情的效果。请你观看三个生成的视频，并完成视频底下的三个问题。**")
st.markdown("*Tips1：你可以点击三个视频为静音，同时播放三个视频来更直观地对比。*")
st.markdown("*Tips2：在测试开始之前请先往下滑确保每个视频都正确加载了，若有视频没有加载，刷新一下即可。*")
st.markdown("三个问题分别是：")
st.markdown("- 1. 你认为哪个的动作更丰富多样？（可以从动作幅度、动作重复度来评判）")
st.markdown("- 2. 你认为这两个模型的面部表情哪一个更好？（嘴唇运动是否符合音频发音）")
st.markdown("- 3. 综合考虑身体动作和面部表情，你认为哪一个的整体效果更好？（如果你觉得两者的动作没有明显的优劣，那请选择表情生成表现更好的模型）")

# random.shuffle(video_groups)
# 创建评分表单
with st.form("survey_form"):
    for i, group in enumerate(video_groups):
        st.write(f"### 组别: {i + 1}")
        
        # 获取模型名称（去掉文件扩展名）
        gt_video = group[0]
        ai_video_1, ai_video_2, ai_video_3 = group[1], group[2], group[3]
        model_name_1 = ai_video_1.split('_')[0]
        model_name_2 = ai_video_2.split('_')[0]
        model_name_3 = ai_video_3.split('_')[0]
        
        parts = ai_video_1.split('_')
        file_name = f"{parts[1]}_{parts[2]}_{parts[3]}_{parts[4]}_{parts[5]}_{parts[6]}"
        
        # 创建三列布局
        col2, col3, col4 = st.columns([1, 1, 1])  # 1:1:1 表示每个列的宽度相等

        # 在每个列中添加视频和评分控件            
        with col2:
            st.subheader(f"AI 视频 1")
            parts = ai_video_1.split('_')
            if parts[0] != 'camn':
                expr_file_name = f"{parts[0]}_{parts[1]}_{parts[2]}_{parts[3]}_{parts[4]}_{parts[5]}_expr_{parts[6]}"
                st.video(os.path.join(expr_source_path, expr_file_name))
                
            st.video(os.path.join(source_path, ai_video_1))
            # 添加选择题
            # st.write("1. 你认为哪个的动作更丰富多样？（可以从动作幅度、动作重复度来评判）")
            question1 = st.radio(
                "1. 你认为哪个的动作更丰富多样？（可以从动作幅度、动作重复度来评判）",
                ("AI 视频 1", "AI 视频 2", "AI 视频 3"),
                key=f"q1_{i}",
                # label_visibility='hidden'
            )

            # st.write("2. 你认为这两个模型的面部表情哪一个更好？（嘴唇运动是否符合音频发音）")
            question2 = st.radio(
                "2. 你认为这两个模型的面部表情哪一个更好？（嘴唇运动是否符合音频发音）",
                ("AI 视频 1", "AI 视频 2", "AI 视频 3"),
                key=f"q2_{i}",
                # label_visibility='hidden'
            )

            # st.write("3. 综合考虑身体动作和面部表情，你认为哪一个的整体效果更好？（如果你觉得两者的动作没有明显的优劣，那请选择表情生成表现更好的模型）")
            question3 = st.radio(
                "3. 综合考虑身体动作和面部表情，你认为哪一个的整体效果更好？（如果你觉得两者的动作没有明显的优劣，那请选择表情生成表现更好的模型）",
                ("AI 视频 1", "AI 视频 2", "AI 视频 3"),
                key=f"q3_{i}",
                # label_visibility='hidden'
            )

        with col3:
            st.subheader(f"AI 视频 2")
            st.video(os.path.join(source_path, ai_video_2))
            parts = ai_video_2.split('_')
            if parts[0] != 'camn':
                expr_file_name = f"{parts[0]}_{parts[1]}_{parts[2]}_{parts[3]}_{parts[4]}_{parts[5]}_expr_{parts[6]}"
                st.video(os.path.join(expr_source_path, expr_file_name))
            # st.video(os.path.join(source_path, ai_video_2))
            
        with col4:
            st.subheader(f"AI 视频 3")
            st.video(os.path.join(source_path, ai_video_3))
            parts = ai_video_3.split('_')
            if parts[0] != 'camn':
                expr_file_name = f"{parts[0]}_{parts[1]}_{parts[2]}_{parts[3]}_{parts[4]}_{parts[5]}_expr_{parts[6]}"
                st.video(os.path.join(expr_source_path, expr_file_name))
            # st.video(os.path.join(source_path, ai_video_3))

        # 将该组评分结果添加到字典中
        if question1 == 'AI 视频 1':
            ans1 = model_name_1
        elif question1 == 'AI 视频 2':
            ans1 = model_name_2
        else:
            ans1 = model_name_3
            
        if question2 == 'AI 视频 1':
            ans2 = model_name_1
        elif question2 == 'AI 视频 2':
            ans2 = model_name_2
        else:
            ans2 = model_name_3
            
        if question3 == 'AI 视频 1':
            ans3 = model_name_1
        elif question3 == 'AI 视频 2':
            ans3 = model_name_2
        else:
            ans3 = model_name_3
            
        ratings.append({
            "group_id": i + 1,
            "file_name": file_name,
            "diversity_score": ans1,  # 记录用户对第1题的选择
            "expression_score": ans2,  # 记录用户对第2题的选择
            "holistic_score": ans3   # 记录用户对第3题的选择
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
            # st.stop()

    # 示例的问卷结果数据

# 当问卷填完后生成结果文件
csv_buffer = StringIO()
new_data = pd.DataFrame(ratings)
new_data.to_csv(csv_buffer, index=False, encoding="utf-8")
csv_data = csv_buffer.getvalue()

# 下载按钮
st.download_button(
    label="下载问卷结果",
    data=csv_data,
    file_name="survey_results.csv",
    mime="text/csv"
)

# 显示当前保存的数据
# st.write("当前数据：")
# st.dataframe(data)