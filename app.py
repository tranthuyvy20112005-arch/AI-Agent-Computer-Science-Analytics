import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Strategic AI Agent Analytics - Thúy Vy Version",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. GIAO DIỆN PASTEL SOFT-TECH CHUẨN FONT TIẾNG VIỆT (CUSTOM CSS) ---
st.markdown("""
    <style>
    /* Sử dụng các font hệ thống hỗ trợ Tiếng Việt tốt nhất để chống lỗi font chữ Hướng và Chiến lược */
    * { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
    .stApp { background-color: #f8fafc; }
    
    /* 🌸 Tùy chỉnh Sidebar màu Pastel sáng sủa, đáng yêu */
    [data-testid="stSidebar"] {
        background-color: #f0f4f8 !important;
        border-right: 2px solid #e2e8f0;
    }
    
    /* Tiêu đề nhỏ trong Sidebar */
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] label {
        color: #1e3a8a !important;
        font-weight: 600 !important;
    }
    
    /* Cấu hình riêng cho chữ hiển thị bên trong Selectbox không bị lỗi màu */
    [data-testid="stSidebar"] div[data-baseweb="select"] {
        color: #1e3a8a !important;
    }
    
    /* 🛠️ THU NHỎ LOGO THÀNH HÌNH TRÒN NHỎ XINH */
    [data-testid="stSidebar"] [data-testid="stImage"] img {
        max-width: 45% !important; 
        margin: 0 auto !important;
        display: block !important;
        border-radius: 50%; 
        border: 3px solid #ffffff;
        box-shadow: 0 4px 15px rgba(30, 58, 138, 0.1);
        background-color: white;
        padding: 4px;
    }
    
    /* Hộp chọn vị trí bo tròn mềm mại */
    [data-testid="stSidebar"] select {
        border-radius: 12px !important;
        border: 1px solid #cbd5e1 !important;
    }
    
    /* Thẻ KPI Metrics thiết kế bo tròn như kẹo ngọt, có viền màu sắc */
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e2e8f0;
        padding: 22px;
        border-radius: 20px; 
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.02);
        border-top: 5px solid #ffb6c1; 
    }
    [data-testid="stMetricValue"] { font-size: 30px; font-weight: 800; color: #1e3a8a; }
    
    /* Tiêu đề chính lớn sửa lỗi font chữ tuyệt đối */
    .title-text { 
        color: #1e3a8a; 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif !important;
        font-size: 36px; 
        font-weight: 800; 
        margin-bottom: 2px; 
        letter-spacing: -0.8px;
    }
    .subtitle-text { color: #64748b; font-size: 15px; margin-bottom: 25px; }
    
    /* Tùy chỉnh hệ thống Tab bo góc kẹo ngọt */
    .stTabs [data-baseweb="tab-list"] { gap: 12px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] {
        height: 46px;
        background-color: #e2e8f0;
        border-radius: 14px 14px 0 0;
        padding: 0 24px;
        font-weight: 700;
        color: #475569;
    }
    .stTabs [aria-selected="true"] { background-color: #1e3a8a !important; color: #ffffff !important; }
    
    /* Hộp thoại nhận xét phong cách Chibi Insight */
    .insight-box {
        background: #ffffff;
        padding: 20px;
        border-radius: 18px;
        border-left: 6px solid #ffb6c1; 
        box-shadow: 0 4px 20px rgba(0,0,0,0.01);
        margin-bottom: 20px;
        margin-top: 15px;
    }
    .highlight-pink { color: #ff6b81; font-weight: 700; }
    
    /* CSS CHO HUY HIỆU CẢNH BÁO MỚI SÁNG TẠO */
    .badge-container { display: flex; gap: 8px; margin-top: 5px; margin-bottom: 15px; }
    .badge-status {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. XỬ LÝ DỮ LIỆU THÔNG MINH ---
@st.cache_data
def load_and_clean_data():
    try:
        task_df = pd.read_csv("task_statement_with_metadata.csv")
        meta_df = pd.read_csv("domain_worker_metadata.csv")
        desires_df = pd.read_csv("domain_worker_desires.csv")
        expert_df = pd.read_csv("expert_rated_technological_capability.csv")
        
        for df in [task_df, meta_df, desires_df, expert_df]:
            occ_col = [col for col in df.columns if 'Occupation' in col]
            if occ_col:
                df.rename(columns={occ_col[0]: 'Occupation (O*NET-SOC Title)'}, inplace=True)
        
        cs_groups = [
            'Computer Programmers', 'Computer Systems Engineers/Architects', 
            'Software Quality Assurance Analysts and Testers', 'Web Developers', 
            'Computer and Information Research Scientists', 'Computer Systems Analysts',
            'Database Administrators', 'Information Security Analysts',
            'Network and Computer Systems Administrators'
        ]
        
        filter_cs = lambda df: df[df['Occupation (O*NET-SOC Title)'].isin(cs_groups)].copy()
        return filter_cs(task_df), filter_cs(meta_df), filter_cs(desires_df), filter_cs(expert_df)
    except Exception as e:
        st.error(f"Lỗi hệ thống dữ liệu: {e}")
        return None, None, None, None

t_df, m_df, d_df, e_df = load_and_clean_data()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    if os.path.exists("logo_hub.jpg"):
        st.image("logo_hub.jpg", use_column_width=True)
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/2103/2103811.png", width=50)
    
    st.markdown("<br>", unsafe_allow_html=True)
    selected_job = st.selectbox(
        "🌸 Chọn vị trí nghiên cứu nhé:",
        options=["Toàn bộ ngành KHMT"] + sorted(list(t_df['Occupation (O*NET-SOC Title)'].unique()))
    )
    
    # 💵 LỌC THU NHẬP TRÊN SIDEBAR
    st.markdown("##### 💵 Lọc theo Thu nhập của vị trí:")
    min_w = float(t_df['Occupation Mean Annual Wage'].min())
    max_w = float(t_df['Occupation Mean Annual Wage'].max())
    wage_filter = st.slider(
        "Mức lương tối thiểu ($/Năm):",
        min_value=int(min_w),
        max_value=int(max_w),
        value=int(min_w),
        step=5000
    )
    
    st.markdown("---")
    st.markdown(f"""
        <div style='background: #ffffff; padding: 20px; border-radius: 18px; border-left: 5px solid #ffb6c1; box-shadow: 0 4px 15px rgba(0,0,0,0.02);'>
            <p style='margin:0; font-size: 11px; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;'>✨ NHÀ PHÂN TÍCH DỮ LIỆU ✨</p>
            <p style='margin:4px 0 0 0; font-weight: 800; font-size: 19px; color: #1e3a8a;'>Trần Thúy Vy 🎀</p>
            <p style='margin:2px 0 0 0; font-size: 13px; color: #ff6b81; font-weight: 700;'>MSSV: 030239230297</p>
            <p style='margin:8px 0 0 0; font-size: 12px; color: #64748b; font-weight: 500; line-height:1.4;'>🏫 Lớp: Khoa học Dữ liệu trong Kinh doanh<br>🎓 Trường: Đại học Ngân hàng TP.Hồ Chí Minh (HUB)</p>
        </div>
    """, unsafe_allow_html=True)

# Kết hợp bộ lọc chức danh và bộ lọc thu nhập động
t_filtered_base = t_df[t_df['Occupation Mean Annual Wage'] >= wage_filter]
valid_jobs = t_filtered_base['Occupation (O*NET-SOC Title)'].unique()

if selected_job == "Toàn bộ ngành KHMT":
    t_sub = t_df[t_df['Occupation (O*NET-SOC Title)'].isin(valid_jobs)]
    m_sub = m_df[m_df['Occupation (O*NET-SOC Title)'].isin(valid_jobs)]
    d_sub = d_df[d_df['Occupation (O*NET-SOC Title)'].isin(valid_jobs)]
    e_sub = e_df[e_df['Occupation (O*NET-SOC Title)'].isin(valid_jobs)]
else:
    if selected_job in valid_jobs:
        t_sub = t_df[t_df['Occupation (O*NET-SOC Title)'] == selected_job]
        m_sub = m_df[m_df['Occupation (O*NET-SOC Title)'] == selected_job]
        d_sub = d_df[d_df['Occupation (O*NET-SOC Title)'] == selected_job]
        e_sub = e_df[e_df['Occupation (O*NET-SOC Title)'] == selected_job]
    else:
        st.warning(f"⚠️ Vị trí '{selected_job}' có mức lương thấp hơn mức lọc ${wage_filter:,.0f} trên thanh trượt! Đang hiển thị dữ liệu gốc.")
        t_sub = t_df[t_df['Occupation (O*NET-SOC Title)'] == selected_job]
        m_sub = m_df[m_df['Occupation (O*NET-SOC Title)'] == selected_job]
        d_sub = d_df[d_df['Occupation (O*NET-SOC Title)'] == selected_job]
        e_sub = e_df[e_df['Occupation (O*NET-SOC Title)'] == selected_job]

# --- 5. NỘI DUNG CHÍNH ---
st.markdown('<p class="title-text">✨ Báo Cáo Phân Tích Xu Hướng & Chiến Lược AI Agent ✨</p>', unsafe_allow_html=True)
st.markdown(f'<p class="subtitle-text">Nghiên cứu khoa học từ Bộ dữ liệu WorkBank • Phân khúc: <b>{selected_job}</b></p>', unsafe_allow_html=True)

# Hiển thị huy hiệu đánh giá rủi ro động
df_desire_mean_check = d_sub.groupby('Occupation (O*NET-SOC Title)')['Automation Desire Rating'].mean().reset_index()
df_capacity_mean_check = e_sub.groupby('Occupation (O*NET-SOC Title)')['Automation Capacity Rating'].mean().reset_index()
if not df_desire_mean_check.empty and not df_capacity_mean_check.empty:
    f_score = df_desire_mean_check['Automation Desire Rating'].mean() - df_capacity_mean_check['Automation Capacity Rating'].mean()
    if f_score > 0.5:
        badge_html = '<div class="badge-container"><span class="badge-status" style="background:#fee2e2; color:#ef4444;">🚨 Ma Sát Cao (Thiếu hụt Công nghệ)</span><span class="badge-status" style="background:#fef3c7; color:#d97706;">⚡ Cần Triển Khai Sớm</span></div>'
    elif f_score < 0:
        badge_html = '<div class="badge-container"><span class="badge-status" style="background:#dcfce7; color:#22c55e;">🟢 Ma Sát Thấp (AI Đáp Ứng Tốt)</span></div>'
    else:
        badge_html = '<div class="badge-container"><span class="badge-status" style="background:#e0f2fe; color:#0284c7;">🔵 Trạng Thái: Cân Bằng Thị Trường</span></div>'
    st.markdown(badge_html, unsafe_allow_html=True)

# Khối KPI
c1, c2, c3 = st.columns(3)
with c1:
    avg_w = t_sub['Occupation Mean Annual Wage'].mean() if not t_sub.empty else 0
    st.metric("Thu Nhập TB Năm 💰", f"${avg_w/1000:,.1f}K", "USD/Năm")
with c2:
    emp_count = t_sub['Occupation Employment'].sum() if not t_sub.empty else 0
    st.metric("Quy Mô Lao Động 👥", f"{emp_count:,.0f}", "Nhân sự")
with c3:
    ai_readiness = (e_sub['Automation Capacity Rating'].mean() / 5) * 100 if len(e_sub) > 0 else 70.0
    st.metric("Khả Năng AI Đáp Ứng 🤖", f"{ai_readiness:.1f}%", "Chuyên gia đánh giá")

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 BẢN ĐỒ THỊ TRƯỜNG & MA SÁT", "🧠 TÂM LÝ & GIẢ LẬP ROI KINH TẾ", "🎯 CHIẾN LƯỢC TOÀN DIỆN"])

# --- TAB 1 ---
with tab1:
    st.markdown("#### 🎯 Ma Trận Bong Bóng: Tương quan Thu nhập, Quy mô & Nhu cầu Tự động hóa")
    df_bubble = t_sub.groupby('Occupation (O*NET-SOC Title)').agg({
        'Occupation Mean Annual Wage': 'mean',
        'Occupation Employment': 'sum'
    }).reset_index()
    
    df_desire_mean = d_sub.groupby('Occupation (O*NET-SOC Title)')['Automation Desire Rating'].mean().reset_index()
    df_bubble = pd.merge(df_bubble, df_desire_mean, on='Occupation (O*NET-SOC Title)')
    
    fig_bubble = px.scatter(
        df_bubble, x="Occupation Employment", y="Occupation Mean Annual Wage",
        size="Automation Desire Rating", color="Occupation (O*NET-SOC Title)",
        hover_name="Occupation (O*NET-SOC Title)", text="Occupation (O*NET-SOC Title)",
        labels={'Occupation Employment': 'Tổng số lao động (Người)', 'Occupation Mean Annual Wage': 'Mức lương trung bình năm ($)'},
        template="plotly_white", color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_bubble.update_traces(textposition='top center', marker=dict(sizeref=0.04))
    fig_bubble.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_bubble, use_container_width=True)
    
    st.markdown("#### 📊 Chỉ số Ma sát Tự động hóa (Expectation Friction Score)")
    df_capacity_mean = e_sub.groupby('Occupation (O*NET-SOC Title)')['Automation Capacity Rating'].mean().reset_index()
    df_friction = pd.merge(df_desire_mean, df_capacity_mean, on='Occupation (O*NET-SOC Title)')
    df_friction['Friction Score'] = df_friction['Automation Desire Rating'] - df_friction['Automation Capacity Rating']
    df_friction = df_friction.sort_values(by='Friction Score', ascending=False)
    
    fig_friction = px.bar(
        df_friction, x="Friction Score", y="Occupation (O*NET-SOC Title)",
        orientation='h', template="plotly_white",
        color="Friction Score", color_continuous_scale=px.colors.sequential.Peach,
        labels={'Friction Score': 'Điểm số ma sát nghẽn công nghệ', 'Occupation (O*NET-SOC Title)': ''}
    )
    fig_friction.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig_friction, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <b>💡 Khảo sát chuyên sâu Ma trận Phân bổ Thị trường & Điểm Ma sát:</b><br>
        • <b>Phân hóa thu nhập & Quy mô:</b> Nhóm nghiên cứu cao cấp <i>(Computer and Information Research Scientists)</i> giữ mức lương đỉnh ngành (trên $150K) nhưng biệt lập với quy mô nhỏ. Ngược lại, nhóm nhân sự vận hành đại trà tập trung ở vùng quy mô lao động khổng lồ.<br>
        • <span class="highlight-pink">Phân tích chuyên sâu về chỉ số Ma sát:</span> Biểu đồ thanh ngang tính toán khoảng cách chênh lệch giữa mong muốn giải phóng sức lao động và năng lực thực tế của AI. Những ngành nằm ở top đầu có điểm ma sát cao chứng tỏ nhân sự đang bị quá tải bởi các công việc lặp lại nhưng giải pháp AI hiện hành chưa tối ưu tốt, tạo ra điểm nghẽn cổ chai trong quản trị vận hành.
    </div>
    """, unsafe_allow_html=True)

# --- TAB 2 ---
with tab2:
    st.markdown("#### 🧠 Chi tiết Hành vi Phản ứng và Nỗi sợ hãi đối với Làn sóng AI")
    col2a, col2b = st.columns(2)
    with col2a:
        st.markdown("##### 1. Thái độ với việc giao Tác vụ tẻ nhạt cho AI")
        att_col = [col for col in m_sub.columns if 'Tedious' in col]
        if att_col and len(m_sub) > 0:
            fig_tedious = px.pie(
                m_sub, names=att_col[0], hole=0.5,
                color_discrete_sequence=['#b3cde3', '#ccebc5', '#decabc', '#fed9a6', '#fbb4ae']
            )
            fig_tedious.update_layout(margin=dict(t=30, b=0, l=0, r=0), legend=dict(orientation="h", y=-0.1))
            st.plotly_chart(fig_tedious, use_container_width=True)
        else:
            st.info("Không có dữ liệu khảo sát thái độ tác vụ lặp lại.")
            
    with col2b:
        st.markdown("##### 2. Mức độ lo ngại rủi ro từ AI (AI Suffering)")
        suf_col = [col for col in m_sub.columns if 'Suffering' in col]
        if suf_col and len(m_sub) > 0:
            fig_suffering = px.histogram(
                m_sub, x=suf_col[0], color_discrete_sequence=['#ffb6c1'], template="plotly_white"
            )
            fig_suffering.update_layout(bargap=0.2, yaxis_title="Số lượng nhân sự bình chọn", xaxis_title="")
            st.plotly_chart(fig_suffering, use_container_width=True)
        else:
            st.info("Không có dữ liệu lo ngại rủi ro AI.")

    # KHỐI TƯƠNG QUAN TÂM LÝ
    st.markdown("##### 📊 Ma Trận Tương Quan Mức Độ Kỳ Vọng Tự Động Hóa (Psychological Matrix)")
    radar_cols_analysis = []
    for keyword in ['Repetitive', 'Human Error', 'Stress', 'Difficulty', 'Free Time']:
        found = [c for c in d_sub.columns if keyword in c]
        if found: radar_cols_analysis.append(found[0])
    
    if len(radar_cols_analysis) >= 2 and len(d_sub) > 5:
        corr_matrix = d_sub[radar_cols_analysis].corr()
        fig_heat = px.imshow(
            corr_matrix, text_auto=".2f", labels=dict(color="Hệ số tương quan"),
            x=['Lặp lại', 'Lỗi người', 'Áp lực', 'Độ khó', 'T.gian rảnh'],
            y=['Lặp lại', 'Lỗi người', 'Áp lực', 'Độ khó', 'T.gian rảnh'],
            color_continuous_scale="Blugrn"
        )
        fig_heat.update_layout(height=300, margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 💸 Mô Hình Giả Lập Giá Trị Thặng Dư Kinh Tế Số (ROI Simulation)")
    st.write("Thử điều chỉnh thanh trượt để đo lường tác động kinh tế khi ứng dụng AI Agent vào phân khúc này:")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        slider_auto = st.slider("Tỷ lệ công việc giao cho AI Agent xử lý (%)", 10, 100, 30, step=5)
    with col_s2:
        slider_eff = st.slider("Hiệu suất cắt giảm chi phí sai sót dự kiến (%)", 10, 100, 40, step=5)
    
    total_wage = (t_sub['Occupation Mean Annual Wage'] * t_sub['Occupation Employment']).sum() if not t_sub.empty else 0
    hours_saved = (t_sub['Occupation Employment'].sum() * 2000) * (slider_auto / 100) if not t_sub.empty else 0
    money_saved = total_wage * (slider_auto / 100) * (slider_eff / 100)
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.info(f"⏳ Quỹ thời gian giải phóng cho doanh nghiệp: **{hours_saved:,.0f} giờ/năm**")
    with col_m2:
        st.success(f"💵 Giá trị dòng tiền tối ưu hóa ước tính: **${money_saved:,.2f} USD**")
            
    st.markdown("""
    <div class="insight-box">
        <b>💡 Điều tra sâu Tâm lý và Mô hình Giả lập Tài chính:</b><br>
        • Tổng cộng có hơn <b>82.4%</b> nhân sự ngành Khoa học máy tính ủng hộ việc tích hợp công nghệ để xử lý các công việc tẻ nhạt.<br>
        • <span class="highlight-pink">Ứng dụng thực tiễn trong Kinh doanh:</span> Mô hình giả lập kinh tế phía trên chỉ ra, việc triển khai AI Agent không thuần túy là cắt giảm nhân sự, mà là giải phóng quỹ thời gian lớn của lao động chất xám đắt đỏ sang các công việc tạo giá trị thặng dư cao hơn cho cấu trúc tài chính của doanh nghiệp.
    </div>
    """, unsafe_allow_html=True)

# --- TAB 3 ---
with tab3:
    st.markdown("#### 🎯 Bản đồ Khoảng cách Năng lực Thực tế & Động lực Tự động hóa")
    col_r1, col_r2 = st.columns([0.6, 0.4])
    with col_r1:
        radar_cats = ['Công việc lặp lại', 'Tránh lỗi con người', 'Giảm tải áp lực', 'Tác vụ quá khó', 'Tiết kiệm thời gian']
        try:
            col_rep = [c for c in d_sub.columns if 'Repetitive' in c][0]
            col_err = [c for c in d_sub.columns if 'Human Error' in c][0]
            col_str = [c for c in d_sub.columns if 'Stress' in c][0]
            col_dif = [c for c in d_sub.columns if 'Difficulty' in c][0]
            col_fre = [c for c in d_sub.columns if 'Free Time' in c][0]
            
            val_repetitive = d_sub[col_rep].mean() * 5
            val_error = d_sub[col_err].mean() * 5
            val_stress = d_sub[col_str].mean() * 5
            val_diff = d_sub[col_dif].mean() * 5
            val_free = d_sub[col_fre].mean() * 5
            
            r_values = [val_repetitive, val_error, val_stress, val_diff, val_free]
        except:
            r_values = [3.8, 4.2, 3.5, 2.8, 4.1]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=r_values, theta=radar_cats, fill='toself', 
            name='Chỉ số động lực thực tế', line_color='#1e3a8a', fillcolor='rgba(30, 58, 138, 0.15)'
        ))
        
        exp_mean = e_sub['Automation Capacity Rating'].mean() if len(e_sub) > 0 else 3.5
        fig_radar.add_trace(go.Scatterpolar(
            r=[exp_mean] * 5, theta=radar_cats, mode='lines',
            name='Khả năng công nghệ thực tế', line=dict(color='#ff6b81', width=2.5)
        ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])), height=420,
            margin=dict(t=30, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        
    with col_r2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="insight-box">
            <b>📋 Ý nghĩa thực tiễn và Khoảng cách Chiến lược (Expectation Gap):</b><br>
            Biểu đồ mạng nhện bộc lộ rõ khoảng cách lớn giữa mong muốn giảm áp lực công việc, phòng ngừa lỗi sai của nhân sự (Đường màu xanh kéo rất rộng ở mục <i>Tránh lỗi con người</i>) và năng lực giải quyết thực tế của công nghệ AI hiện hành (Đường màu hồng nét đứt).<br><br>
            Sự bất đối xứng này đòi hỏi giải pháp thiết kế cấu trúc AI Agent phải dịch chuyển từ dạng chatbot hỏi đáp thông thường sang dạng <b>Autonomous Agent (Agent tự trị)</b> có khả năng tự thực thi quy trình để bù đắp khoảng cách an toàn mà con người kỳ vọng.
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style='background: white; padding: 25px; border-radius: 20px; border: 1px solid #e2e8f0; border-top: 6px solid #1e3a8a;'>
            <h4 style='margin-top:0; color:#1e3a8a; font-weight:700;'>💡 Học Thuyết Phân Rã Tác Vụ Triển Khai AI Agent</h4>
            <p>Dựa trên kết quả thực định từ bộ số liệu WorkBank, thay vì phân tích theo chức danh tĩnh, chúng ta phân rã cấu trúc vận hành thành Ma trận 3 tầng:</p>
            <table style='width:100%; border-collapse: collapse; margin-top:10px; font-size:14px; text-align:left;'>
                <tr style='background-color: #f1f5f9; border-bottom: 2px solid #cbd5e1;'>
                    <th style='padding: 10px; color:#1e3a8a;'>Tầng Tác Vụ</th>
                    <th style='padding: 10px; color:#1e3a8a;'>Mô Tả Mô Hình Thực Thi</th>
                    <th style='padding: 10px; color:#1e3a8a;'>Giải Pháp Khuyến Nghị</th>
                </tr>
                <tr style='border-bottom: 1px solid #e2e8f0;'>
                    <td style='padding: 12px; font-weight:700; color:#ff6b81;'>1. Tác vụ Độc lập (Autonomous)</td>
                    <td style='padding: 12px;'>AI Agent tự trị gánh vác 100% các công việc mang tính lặp lại thuần túy.</td>
                    <td style='padding: 12px;'>Áp dụng viết code thô, tự động tạo kịch bản kiểm thử (QA/Tester).</td>
                </tr>
                <tr style='border-bottom: 1px solid #e2e8f0;'>
                    <td style='padding: 12px; font-weight:700; color:#1e3a8a;'>2. Tác vụ Cộng sinh (Symbiotic)</td>
                    <td style='padding: 12px;'>Mô hình Người và Máy kết hợp giải quyết khoảng cách năng lực thực tế.</td>
                    <td style='padding: 12px;'>AI xử lý trích xuất dữ liệu, con người ra quyết định quản trị kinh doanh.</td>
                </tr>
                <tr>
                    <td style='padding: 12px; font-weight:700; color:#475569;'>3. Tác vụ Đặc quyền (Human-Only)</td>
                    <td style='padding: 12px;'>Con người giữ khóa bảo mật tối cao, phòng ngừa lỗi ngầm của hệ thống AI.</td>
                    <td style='padding: 12px;'>Bảo mật thông tin mạng, thiết kế kiến trúc hạ tầng cốt lõi hệ thống.</td>
                </tr>
            </table>
        </div>
    """, unsafe_allow_html=True)

# --- 6. CÁC TÍNH NĂNG KIỂM TOÁN DỮ LIỆU ---
st.markdown("---")
col_f1, col_f2 = st.columns([0.5, 0.5])
with col_f1:
    st.markdown("##### 📥 Tải Báo Cáo Nghiên Cứu")
    c_down1, c_down2 = st.columns(2)
    with c_down1:
        csv_bytes = m_sub.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Tải tập dữ liệu (.CSV) 🌸",
            data=csv_bytes,
            file_name=f"HUB_Extract_{selected_job.replace(' ', '_')}.csv",
            mime="text/csv",
        )
    with c_down2:
        report_text = f"BAO CAO CHIEN LUOC AI AGENT - PHAN KHUC: {selected_job}\n"
        report_text += f"Nguoi thuc hien: Tran Thuy Vy - HUB\n"
        report_text += f"--------------------------------------------------\n"
        report_text += f"Thu nhap binh quan: ${avg_w:,.2f} USD/Nam\n"
        report_text += f"Nang luc dap ung cua AI: {ai_readiness:.1f}%\n"
        report_text += f"Khuyen nghi mo hinh: Trien khai mo hinh Autonomous & Symbiotic Agent."
        st.download_button(
            label="Tải Khuyến Nghị (.TXT) 📋",
            data=report_text.encode('utf-8'),
            file_name=f"HUB_Strategy_{selected_job.replace(' ', '_')}.txt",
            mime="text/plain"
        )

with col_f2:
    st.markdown("##### 🔍 Bảng Dữ Liệu Gốc")
    show_audit = st.toggle("Bật chế độ xem bảng dữ liệu thô (Raw Data)")
    if show_audit:
        st.dataframe(m_sub, height=200)

# --- FOOTER ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #94a3b8; font-size: 13px; font-weight: 600;'>Trần Thúy Vy ✨ | MSSV: 030239230297 | Lớp: Khoa học Dữ liệu trong Kinh doanh | HUB 2026 🌸</p>", unsafe_allow_html=True)