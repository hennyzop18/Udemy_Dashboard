import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter
import re
from streamlit_option_menu import option_menu

# 1. Cấu hình trang & CSS
st.set_page_config(page_title="Hệ thống quản lý Udemy", layout="wide")

# st.markdown("""
#     <style>
#     .main { background-color: #f5f5f5; }
#     .stMetric {
#         background-color: white;
#         padding: 15px;
#         border-radius: 10px;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.05);
#     }
#     [data-testid="stSidebar"] {
#         background-color: #f0f2f6;
#     }
#     .sales-card {
#         background-color: #6A1B9A;
#         padding: 20px;
#         border-radius: 10px;
#         color: white;
#         margin-bottom: 20px;
#     }
#     </style>
#     """, unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Premium Modern UI CSS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #ffffff;
        color: #1e293b;
    }
    
    /* Make top header transparent */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* ===== SIDEBAR - Clean Light Card Style ===== */
    [data-testid="stSidebar"] {
        background: #f3f4f6 !important;
        border-right: 1px solid #e5e7eb;
        box-shadow: 2px 0 12px rgba(0,0,0,0.04);
    }
    /* Sidebar section label */
    [data-testid="stSidebar"] .stMarkdown h3 {
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        color: #9ca3af !important;
        margin-bottom: 0.4rem !important;
        margin-top: 0.2rem !important;
    }
    /* Sidebar separator */
    [data-testid="stSidebar"] hr {
        border-top: 1px solid #e5e7eb !important;
        margin: 0.6rem 0 !important;
    }
    /* Sidebar selectbox */
    [data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
        background: #ffffff !important;
        border: 1.5px solid #e5e7eb !important;
        border-radius: 10px !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        transition: border-color 0.2s ease;
    }
    [data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div:hover {
        border-color: #a78bfa !important;
    }
    /* Sidebar radio button labels */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label {
        background: #ffffff;
        border: 1.5px solid #e5e7eb;
        border-radius: 10px;
        padding: 7px 12px !important;
        margin-bottom: 5px !important;
        transition: all 0.18s ease;
        cursor: pointer;
        display: flex;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        color: #374151 !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:hover {
        background: #ede9fe !important;
        border-color: #a78bfa !important;
        color: #6d28d9 !important;
    }
    /* Reset button */
    [data-testid="stSidebar"] .stButton > button {
        background: #ffffff !important;
        border: 1.5px solid #fca5a5 !important;
        color: #ef4444 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
        font-size: 0.9rem;
        border-radius: 10px !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: #fef2f2 !important;
        border-color: #ef4444 !important;
        color: #dc2626 !important;
        transform: translateY(-1px);
        box-shadow: 0 3px 8px rgba(239, 68, 68, 0.2) !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #7184fc 0%, #505fc8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(113, 132, 252, 0.25);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(113, 132, 252, 0.4);
        color: white;
    }

    /* Metric Cards (KPI) - Glassmorphism */
    .metric-container {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.6);
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(31, 38, 135, 0.12);
        background: var(--hover-bg) !important;
        border-color: var(--hover-bg) !important;
    }
    .metric-container:hover .metric-label,
    .metric-container:hover .metric-value {
        color: white !important;
    }
    .metric-label {
        font-size: 13px;
        color: #475569;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
        transition: color 0.3s ease;
    }
    .metric-value {
        font-size: 32px;
        color: #0f172a;
        font-weight: 800;
        line-height: 1.2;
        transition: color 0.3s ease;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5 {
        color: #0f172a;
        font-weight: 800;
        letter-spacing: -0.5px;
        text-shadow: 0 2px 10px rgba(255,255,255,0.5);
    }
    
    /* Radio and Selectbox */
    .stRadio label, .stSelectbox label {
        font-weight: 600 !important;
        color: #1e293b;
    }
    
    /* Custom divider */
    hr {
        border-top: 1px solid rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Hàm vẽ Thẻ KPI tùy chỉnh
def style_metric(label, value, color="#A16AE8"):
    st.markdown(f"""
        <div class="metric-container" style="--hover-bg: {color}; border-top: 4px solid {color};">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)

# 2. Hàm xử lý dữ liệu
def parse_duration(duration_str):
    try:
        s = str(duration_str).lower().strip()
        # Tìm con số trong chuỗi
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", s)
        if not numbers: return 0
        number = float(numbers[0])
        
        # Nếu có chữ 'min' thì chia 60, còn lại mặc định là 'giờ'
        if 'min' in s:
            return number / 60
        return number # Trả về con số (mặc định là giờ)
    except:
        return 0


@st.cache_data
def load_data():
    import os
    clean_file = 'udemy_cleaned.csv'
    original_file = 'udemy.csv'
    
    if os.path.exists(clean_file):
        # Nếu đã có file sạch từ Notebook, load trực tiếp cho nhanh
        df = pd.read_csv(clean_file)
        if 'published_timestamp' in df.columns:
            df['published_timestamp'] = pd.to_datetime(df['published_timestamp'])
            df['month']   = df['published_timestamp'].dt.month
            df['weekday'] = df['published_timestamp'].dt.day_name()
        # Đảm bảo các cột cần thiết có tên đúng cho Dashboard
        if 'content_duration' in df.columns and 'duration_hours' not in df.columns:
            df['duration_hours'] = df['content_duration']
        if 'estimated_revenue' in df.columns:
            df['sales'] = df['estimated_revenue']
        return df
    
    # Fallback nếu chưa có file sạch
    df = pd.read_csv(original_file)
    df['price'] = df['price'].replace('Free', 0).astype(float)
    df['sales'] = df['price'] * df['num_subscribers']
    df['published_timestamp'] = pd.to_datetime(df['published_timestamp'])
    df['year'] = df['published_timestamp'].dt.year
    df['month'] = df['published_timestamp'].dt.month
    df['weekday'] = df['published_timestamp'].dt.day_name()
    df['duration_hours'] = df['content_duration'].apply(parse_duration)
    
    # Lọc bỏ năm 2024-2026, chỉ lấy từ 2011 đến 2023
    df = df[df['year'] <= 2023]
    
    return df

df = load_data()

# --- SIDEBAR (Điều hướng & Bộ lọc) ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/e3/Udemy_logo.svg", width=150)

# Menu điều hướng trang
with st.sidebar:
    page = option_menu(
        menu_title=None,
        options=["Tổng quan", "Doanh thu", "Học viên", "Nội dung", "Khóa học", "Dự đoán"],
        icons=["activity", "cash-coin", "people", "collection", "play-btn", "magic"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {
                "padding": "4px 0",
                "background-color": "transparent",
                "border": "none",
            },
            "icon": {
                "color": "#6b7280",
                "font-size": "1rem",
                "margin-right": "8px",
            },
            "nav-link": {
                "font-size": "0.97rem",
                "text-align": "left",
                "margin": "3px 0",
                "color": "#374151",
                "font-weight": "500",
                "padding": "11px 16px",
                "border-radius": "12px",
                "background-color": "#ffffff",
                "border": "1.5px solid #e5e7eb",
                "box-shadow": "0 1px 3px rgba(0,0,0,0.04)",
                "--hover-color": "#ede9fe",
                "transition": "all 0.2s ease",
            },
            "nav-link-selected": {
                "background-color": "#ede9fe",
                "color": "#6d28d9",
                "font-weight": "700",
                "border": "1.5px solid #ede9fe",
                "box-shadow": "0 2px 8px rgba(109, 40, 217, 0.08)",
            },
        }
    )

# Khởi tạo reset counter
if "_reset_count" not in st.session_state:
    st.session_state["_reset_count"] = 0
rc = st.session_state["_reset_count"]

# 1. Bộ lọc Publish Year
st.sidebar.markdown("### Năm xuất bản")
years = sorted(df['year'].unique())
selected_year = st.sidebar.selectbox("Chọn năm", ["Tất cả"] + list(years), index=0, key=f"sel_year_{rc}")

st.sidebar.markdown("---")
st.sidebar.markdown("### Chủ đề")
subjects = ["Tất cả"] + list(df['subject'].unique())
selected_subject = st.sidebar.radio("", subjects, index=0, key=f"sel_subject_{rc}")

st.sidebar.markdown("### Trình độ")
levels = ["Tất cả", "Beginner Level", "Intermediate Level", "Expert Level"]
selected_level = st.sidebar.radio("", levels, index=0, key=f"sel_level_{rc}")

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Xóa tất cả bộ lọc", use_container_width=True):
    st.session_state["_reset_count"] += 1
    st.rerun()

# --- LỌC DỮ LIỆU DÙNG CHUNG ---
df_f = df.copy()
if selected_year != "Tất cả":
    df_f = df_f[df_f['year'] == int(selected_year)]
if selected_subject != "Tất cả":
    df_f = df_f[df_f['subject'] == selected_subject]
if selected_level != "Tất cả":
    df_f = df_f[df_f['level'] == selected_level]

# --- PHÂN CHIA NỘI DUNG TỪNG TRANG ---

# ================= PAGE: OVERVIEW =================
if page == "Tổng quan":
    st.title("Tổng quan")

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        style_metric("Tổng khóa học", f"{len(df_f):,}", "#7184fc")

    with k2:
        style_metric("Doanh thu ước tính", f"${df_f['sales'].sum()/1e6:,.2f}M", "#fc970f")

    with k3:
        style_metric("Thời lượng nội dung", f"{df_f['duration_hours'].sum():,.0f} Giờ", "#66ce7e")

    with k4:
        style_metric("Học viên", f"{df_f['num_subscribers'].sum()/1e6:,.2f}M", "#68c9fe")

    # BIỂU ĐỒ HÀNG 2
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("#### Trả phí vs Miễn phí")
            st.markdown("<p style='color: #64748b; font-size: 0.9rem; margin-top: -10px;'>Khóa miễn phí ít hơn nhưng hút học viên gấp 3×</p>", unsafe_allow_html=True)
            
            paid_df = df_f[df_f['is_paid'] == True]
            free_df = df_f[df_f['is_paid'] == False]
            total_courses = len(df_f) if len(df_f) > 0 else 1
            paid_pct = len(paid_df) / total_courses * 100
            free_pct = 100 - paid_pct
            paid_subs = paid_df['num_subscribers'].sum()
            free_subs = free_df['num_subscribers'].sum()
            avg_paid = paid_df['num_subscribers'].mean() if len(paid_df) > 0 else 0
            avg_free = free_df['num_subscribers'].mean() if len(free_df) > 0 else 0
            max_avg = max(avg_paid, avg_free) if max(avg_paid, avg_free) > 0 else 1
            paid_bar_pct = avg_paid / max_avg * 100
            free_bar_pct = avg_free / max_avg * 100

            st.markdown(f"""
<div style="display: flex; gap: 12px; margin-bottom: 20px;">
<div style="flex: 1; background: #f8fafc; border-radius: 10px; padding: 16px;">
<div style="font-size: 0.75rem; font-weight: 700; letter-spacing: 0.05em; color: #94a3b8; text-transform: uppercase; margin-bottom: 6px;">TRẢ PHÍ</div>
<div style="font-size: 2rem; font-weight: 700; color: #5a67d8; margin-bottom: 4px;">{paid_pct:.1f}%</div>
<div style="font-size: 0.85rem; color: #64748b;">{len(paid_df):,} khóa · {paid_subs/1e6:.1f}M subs</div>
</div>
<div style="flex: 1; background: #f8fafc; border-radius: 10px; padding: 16px;">
<div style="font-size: 0.75rem; font-weight: 700; letter-spacing: 0.05em; color: #94a3b8; text-transform: uppercase; margin-bottom: 6px;">MIỄN PHÍ</div>
<div style="font-size: 2rem; font-weight: 700; color: #10b981; margin-bottom: 4px;">{free_pct:.1f}%</div>
<div style="font-size: 0.85rem; color: #64748b;">{len(free_df):,} khóa · {free_subs/1e6:.1f}M subs</div>
</div>
</div>
<div style="margin-bottom: 12px;">
<div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #475569; margin-bottom: 4px;">
<span>Trung bình Học viên / khóa trả phí</span><span style="font-weight: 600;">{avg_paid:,.0f}</span>
</div>
<div style="height: 8px; background: #f1f5f9; border-radius: 4px; overflow: hidden;">
<div style="width: {paid_bar_pct:.0f}%; height: 100%; background: #5a67d8; border-radius: 4px;"></div>
</div>
</div>
<div style="margin-bottom: 16px;">
<div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #475569; margin-bottom: 4px;">
<span>Trung bình Học viên / khóa miễn phí</span><span style="font-weight: 600;">{avg_free:,.0f}</span>
</div>
<div style="height: 8px; background: #f1f5f9; border-radius: 4px; overflow: hidden;">
<div style="width: {free_bar_pct:.0f}%; height: 100%; background: #10b981; border-radius: 4px;"></div>
</div>
</div>
<div style="font-size: 0.85rem; color: #64748b; font-style: italic;">
Khóa free thu hút trung bình {avg_free:,.0f} đăng kí — gấp {avg_free/avg_paid:.1f}× khóa trả phí
</div>
""", unsafe_allow_html=True)

    with c2:
        with st.container(border=True):
            st.markdown("#### Học viên theo chủ đề")
            st.markdown("<p style='color: #64748b; font-size: 0.9rem; margin-top: -10px;'>Web Dev chiếm 60% tổng học viên toàn nền tảng</p>", unsafe_allow_html=True)
            
            subj_subs = df_f.groupby('subject')['num_subscribers'].sum().sort_values(ascending=True).reset_index()
            subj_color_map = {
                'Web Development': '#6366f1',
                'Business Finance': '#10b981',
                'Graphic Design': '#f97316',
                'Musical Instruments': '#ec4899'
            }
            colors_subj = [subj_color_map.get(s, '#94a3b8') for s in subj_subs['subject']]
            
            fig_subj_bar = go.Figure()
            fig_subj_bar.add_trace(go.Bar(
                x=subj_subs['num_subscribers'],
                y=subj_subs['subject'],
                orientation='h',
                marker_color=colors_subj,
                marker_line_width=0,
                text=[f"{v/1e6:.0f}M" for v in subj_subs['num_subscribers']],
                textposition='outside',
                textfont=dict(color='#475569', size=11),
                hovertemplate='<b>%{y}</b><br>%{x:,.0f} học viên<extra></extra>'
            ))
            fig_subj_bar.update_layout(
                height=300, margin=dict(t=10, b=10, l=0, r=50),
                xaxis=dict(showgrid=False, visible=False),
                yaxis=dict(showgrid=False, tickfont=dict(size=11, color='#475569')),
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            fig_subj_bar.update_xaxes(range=[0, subj_subs['num_subscribers'].max() * 1.2])
            st.plotly_chart(fig_subj_bar, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # BIỂU ĐỒ HÀNG 3
    c3, c4 = st.columns(2)
    with c3:
        with st.container(border=True):
            st.markdown("#### Từ khóa xuất hiện nhiều nhất trong khóa học")
            st.markdown("<p style='color: #64748b; font-size: 0.9rem; margin-top: -10px;'>Kích thước tương ứng tần suất xuất hiện</p>", unsafe_allow_html=True)
            
            text = " ".join(df_f['course_title'].str.lower())
            words = re.findall(r'\w+', text)
            stop_words = {'to', 'the', 'and', 'for', 'in', 'of', 'a', 'with', 'your', 'from', 'learn', 'how', 'on', 'by', 'you', 'an', 'this', 'that', 'are', 'is', 'it', 'be', 'as', 'at', 'so', 'we', 'he', 'she', 'they', 'do', 'its', 'was', 'but', 'not'}
            keywords = [w for w in words if w not in stop_words and len(w) > 3]
            word_counts = Counter(keywords).most_common(15)
            
            palette = ['#5a67d8', '#10b981', '#f59e0b', '#e879a0', '#6366f1', '#d97706', '#22c55e', '#818cf8']
            max_count = word_counts[0][1] if word_counts else 1
            
            cloud_html = '<div style="display: flex; flex-wrap: wrap; gap: 12px 18px; align-items: baseline; padding: 20px 0; min-height: 260px;">'
            for idx, (word, count) in enumerate(word_counts):
                size = 13 + (count / max_count) * 32
                color = palette[idx % len(palette)]
                weight = 700 if size > 28 else (600 if size > 20 else 500)
                cloud_html += f'<span style="font-size: {size:.0f}px; color: {color}; font-weight: {weight}; line-height: 1.4;">{word}</span>'
            cloud_html += '</div>'
            st.markdown(cloud_html, unsafe_allow_html=True)

    with c4:
        with st.container(border=True):
            st.markdown("#### Trung bình học viên theo thời lượng khóa học")
            st.markdown("<p style='color: #64748b; font-size: 0.9rem; margin-top: -10px;'>Khóa dài 20-50h có trung bình học viên cao nhất</p>", unsafe_allow_html=True)
            
            bins = [0, 1, 2, 5, 10, 20, 30, 50, 500]
            labels_dur = ['<1h', '1-2h', '2-5h', '5-10h', '10-20h', '20-30h', '30-50h', '50h+']
            df_f['dur_bin_c4'] = pd.cut(df_f['duration_hours'], bins=bins, labels=labels_dur)
            dur_stats_c4 = df_f.groupby('dur_bin_c4', observed=False)['num_subscribers'].mean().reset_index()
            dur_stats_c4.columns = ['dur_bin', 'avg_subs']
            
            peak_dur = dur_stats_c4['avg_subs'].idxmax()
            colors_dur = ['#c7d2fe'] * len(dur_stats_c4)
            if not pd.isna(peak_dur):
                colors_dur[peak_dur] = '#5a67d8'
            
            fig_avg_dur = go.Figure()
            fig_avg_dur.add_trace(go.Bar(
                x=dur_stats_c4['dur_bin'], y=dur_stats_c4['avg_subs'],
                marker_color=colors_dur, marker_line_width=0,
                hovertemplate='<b>%{x}</b><br>Avg: %{y:,.0f} học viên<extra></extra>'
            ))
            fig_avg_dur.update_layout(
                height=300, margin=dict(t=20, b=10, l=0, r=0),
                xaxis=dict(showgrid=False, tickfont=dict(color='#64748b', size=10)),
                yaxis=dict(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(color='#94a3b8', size=10), tickformat=',.0f'),
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_avg_dur, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # ---- HÀNG 4: Tăng trưởng học viên theo năm ----
    with st.container(border=True):
        st.markdown("<p style='font-size: 0.8rem; font-weight: 700; letter-spacing: 0.08em; color: #111111; text-transform: uppercase; margin-bottom: 0;'>Tăng trưởng học viên theo chủ đề (Triệu)</p>", unsafe_allow_html=True)
        
        subj_year = df.groupby(['year', 'subject'])['num_subscribers'].sum().reset_index()
        subj_year['num_subscribers_m'] = subj_year['num_subscribers'] / 1e6
        subj_colors = {
            'Web Development': '#5a67d8',
            'Business Finance': '#d97706',
            'Graphic Design': '#e879a0',
            'Musical Instruments': '#22c55e'
        }
        
        fig_growth = go.Figure()
        for subj in subj_year['subject'].unique():
            d = subj_year[subj_year['subject'] == subj].sort_values('year')
            color = subj_colors.get(subj, '#94a3b8')
            is_web = subj == 'Web Development'
            fig_growth.add_trace(go.Scatter(
                x=d['year'], y=d['num_subscribers_m'],
                name=subj,
                mode='lines+markers',
                line=dict(color=color, width=2.5, shape='spline'),
                fill='tozeroy' if is_web else 'none',
                fillcolor='rgba(90, 103, 216, 0.1)' if is_web else None,
                marker=dict(size=5, color=color)
            ))
        
        fig_growth.update_layout(
            height=340, margin=dict(t=10, b=10, l=0, r=0),
            legend=dict(orientation="h", yanchor="top", y=1.08, xanchor="left", x=0, font=dict(size=11)),
            xaxis=dict(showgrid=False, tickmode='array', tickvals=list(range(2011, 2024)), tickformat='d', tickfont=dict(color='#64748b', size=10)),
            yaxis=dict(showgrid=True, gridcolor='#f1f5f9', ticksuffix='M', tickfont=dict(color='#94a3b8', size=10)),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            hovermode='x unified'
        )
        st.plotly_chart(fig_growth, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ---- HÀNG 5: 2 biểu đồ theo năm ----
    row5_l, row5_r = st.columns(2)
    
    with row5_l:
        with st.container(border=True):
            st.markdown("<p style='font-size: 0.8rem; font-weight: 700; letter-spacing: 0.08em; color: #111111; text-transform: uppercase; margin-bottom: 0;'>Khóa học mới theo chủ đề mỗi năm</p>", unsafe_allow_html=True)
            
            new_courses = df.groupby(['year', 'subject']).size().reset_index(name='count')
            bar_colors = {
                'Web Development': '#5a67d8',
                'Business Finance': '#d97706',
                'Graphic Design': '#e879a0',
                'Musical Instruments': '#22c55e'
            }
            
            fig_new = go.Figure()
            for subj in new_courses['subject'].unique():
                d = new_courses[new_courses['subject'] == subj].sort_values('year')
                fig_new.add_trace(go.Bar(
                    x=d['year'], y=d['count'],
                    name=subj, marker_color=bar_colors.get(subj, '#94a3b8'),
                    marker_line_width=0
                ))
            
            fig_new.update_layout(
                barmode='stack', height=320, margin=dict(t=20, b=10, l=0, r=0),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
                xaxis=dict(showgrid=False, tickmode='array', tickvals=list(range(2011, 2024)), tickformat='d', tickfont=dict(color='#64748b', size=9)),
                yaxis=dict(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(color='#94a3b8', size=10)),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_new, use_container_width=True)
    
    with row5_r:
        with st.container(border=True):
            st.markdown("<p style='font-size: 0.8rem; font-weight: 700; letter-spacing: 0.08em; color: #111111; text-transform: uppercase; margin-bottom: 0;'>Trung bình Reviews / Khóa học theo năm</p>", unsafe_allow_html=True)
            
            avg_reviews_year = df.groupby('year').apply(lambda x: x['num_reviews'].sum() / len(x) if len(x) > 0 else 0).reset_index(name='avg_reviews')
            avg_reviews_year = avg_reviews_year[avg_reviews_year['year'] <= 2020]
            
            fig_rev = go.Figure()
            fig_rev.add_trace(go.Scatter(
                x=avg_reviews_year['year'], y=avg_reviews_year['avg_reviews'],
                mode='lines',
                line=dict(color='#e879a0', width=2.5, shape='spline'),
                fill='tozeroy',
                fillcolor='rgba(232, 121, 160, 0.15)'
            ))
            
            fig_rev.update_layout(
                height=320, margin=dict(t=20, b=10, l=0, r=0),
                xaxis=dict(showgrid=False, tickmode='array', tickvals=list(range(2011, 2021)), tickformat='d', tickfont=dict(color='#64748b', size=9)),
                yaxis=dict(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(color='#94a3b8', size=10)),
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_rev, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ---- HÀNG 6: Giá trung bình theo năm ----
    with st.container(border=True):
        st.markdown("<p style='font-size: 0.8rem; font-weight: 700; letter-spacing: 0.08em; color: #111111; text-transform: uppercase; margin-bottom: 0;'>Giá trung bình (Khóa trả phí) theo năm ($)</p>", unsafe_allow_html=True)
        
        avg_price_year = df[df['is_paid']==True].groupby('year')['price'].mean().reset_index(name='avg_price')
        
        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(
            x=avg_price_year['year'], y=avg_price_year['avg_price'],
            mode='lines+markers',
            line=dict(color='#d97706', width=2.5, shape='spline'),
            fill='tozeroy',
            fillcolor='rgba(217, 119, 6, 0.1)',
            marker=dict(size=5, color='#d97706')
        ))
        
        fig_price.update_layout(
            height=280, margin=dict(t=10, b=10, l=0, r=0),
            xaxis=dict(showgrid=False, tickmode='array', tickvals=list(range(2011, 2024)), tickformat='d', tickfont=dict(color='#64748b', size=10)),
            yaxis=dict(showgrid=True, gridcolor='#f1f5f9', tickprefix='$', tickfont=dict(color='#94a3b8', size=10)),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            hovermode='x unified'
        )
        st.plotly_chart(fig_price, use_container_width=True)

# ================= PAGE: SALES =================
elif page == "Doanh thu":
    st.title("💰 Phân tích hiệu suất doanh thu")

    total_sales = df_f['sales'].sum()
    top_subj = df_f.groupby('subject')['sales'].sum().idxmax()
    top_subj_pct = df_f.groupby('subject')['sales'].sum().max() / total_sales * 100 if total_sales > 0 else 0
    paid_course_pct = (len(df_f[df_f['is_paid']==True]) / len(df_f) * 100) if len(df_f) > 0 else 0
    
    st.markdown(f"""
        <div style="background: linear-gradient(90deg, #6366f1 0%, #4f46e5 100%); padding: 25px 35px; border-radius: 12px; color: white; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <div>
                <div style="font-size: 1rem; opacity: 0.9; margin-bottom: 4px;">Tổng doanh thu ước tính</div>
                <div style="font-size: 3.2rem; font-weight: 700; line-height: 1.1; margin-bottom: 8px;">${total_sales:,.0f}</div>
                <div style="font-size: 1.05rem; opacity: 0.9;">{top_subj} chiếm {top_subj_pct:.0f}% tổng doanh thu</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 1rem; opacity: 0.9; margin-bottom: 4px;">Khóa trả phí</div>
                <div style="font-size: 1.9rem; font-weight: 700; line-height: 1.2; margin-bottom: 4px;">{paid_course_pct:.2f}%</div>
                <div style="font-size: 1.05rem; opacity: 0.9;">nội dung</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("#### Doanh thu theo chủ đề ")
            st.markdown("<p style='color: #64748b; font-size: 0.9rem; margin-top: -10px;'>Diện tích = tỷ lệ đóng góp doanh thu</p>", unsafe_allow_html=True)
            
            subj_sales = df_f.groupby('subject')['sales'].sum().reset_index()
            total_s = subj_sales['sales'].sum() if subj_sales['sales'].sum() > 0 else 1
            subj_sales['pct'] = subj_sales['sales'] / total_s * 100
            
            short_names = {'Web Development': 'Web Dev', 'Business Finance': 'Biz Finance', 'Graphic Design': 'Graphic', 'Musical Instruments': 'Musical Instruments'}
            subj_sales['label'] = subj_sales['subject'].map(lambda x: short_names.get(x, x))
            
            subj_sales = subj_sales.sort_values('sales', ascending=False).reset_index(drop=True)
            colors_tree = ['#5a67d8', '#818cf8', '#a5b4fc', '#c7d2fe']
            text_colors = ['white', 'white', '#1e293b', '#1e293b']
            
            texts = []
            for i, row in subj_sales.iterrows():
                tcolor = text_colors[i] if i < len(text_colors) else 'white'
                tcolor_sub = 'rgba(255,255,255,0.8)' if tcolor == 'white' else 'rgba(30,41,59,0.7)'
                texts.append(f"<span style='font-size:12px; color:{tcolor};'>{row['label']}</span><br><b style='font-size:18px; color:{tcolor};'>${row['sales']/1e6:.0f}M</b><br><span style='font-size:11px; color:{tcolor_sub};'>{row['pct']:.0f}%</span>")
                
            fig_tree2 = go.Figure(go.Treemap(
                labels=subj_sales['label'],
                parents=[""] * len(subj_sales),
                values=subj_sales['sales'],
                textinfo="text",
                text=texts,
                marker=dict(colors=colors_tree[:len(subj_sales)]),
                hovertemplate="<b>%{label}</b><br>Doanh thu: $%{value:,.0f}<extra></extra>"
            ))
            fig_tree2.update_layout(margin=dict(t=5, l=5, r=5, b=5), height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_tree2, use_container_width=True)

    with c2:
        with st.container(border=True):
            st.markdown("#### Mức giá tối ưu cho doanh thu")
            
            bins_p = [-1, 0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200]
            labels_p = ['Free', '$1-20', '$21-40', '$41-60', '$61-80', '$81-100', '$101-120', '$121-140', '$141-160', '$161-180', '$181-200']
            df_f['price_range'] = pd.cut(df_f['price'], bins=bins_p, labels=labels_p)
            price_sales = df_f.groupby('price_range', observed=False)['sales'].sum().reset_index()
            
            peak_idx = price_sales['sales'].idxmax()
            peak_row = price_sales.iloc[peak_idx]
            peak_range = peak_row['price_range']
            
            st.markdown(f"<p style='color: #64748b; font-size: 0.9rem; margin-top: -10px;'>Đường line thể hiện Doanh thu · Đỉnh doanh thu ở nhóm <b>{peak_range}</b></p>", unsafe_allow_html=True)
            
            fig_price = go.Figure()
            fig_price.add_trace(go.Scatter(
                x=price_sales['price_range'], y=price_sales['sales'],
                name="Doanh thu",
                mode='lines',
                line=dict(color='#5a67d8', width=3, shape='spline'),
                fill='tozeroy',
                fillcolor='rgba(90,103,216,0.1)',
                hovertemplate='<b>Khoảng giá: %{x}</b><br>Doanh thu: $%{y:,.0f}<extra></extra>'
            ))
            
            fig_price.add_trace(go.Scatter(
                x=[peak_row['price_range']], y=[peak_row['sales']],
                mode='markers+text',
                marker=dict(color='#5a67d8', size=8),
                text=[f"<b>Peak Doanh thu</b><br>{peak_row['price_range']}"],
                textposition='top center',
                textfont=dict(color='#5a67d8', size=11),
                hovertemplate='<b>Đỉnh doanh thu</b><br>Khoảng giá: %{x}<br>Tổng: $%{y:,.0f}<extra></extra>'
            ))
            
            fig_price.add_vline(x=peak_row['price_range'], line_width=1, line_dash="dash", line_color="#a5b4fc")
            
            fig_price.update_layout(
                height=280, margin=dict(t=30, b=10, l=10, r=10),
                xaxis=dict(showgrid=False, tickmode='array', tickvals=['Free', '$21-40', '$101-120', '$161-180'], tickfont=dict(color='#64748b', size=10)),
                yaxis=dict(showgrid=False, visible=False),
                showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            fig_price.update_yaxes(range=[0, price_sales['sales'].max() * 1.3])
            
            st.plotly_chart(fig_price, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    c3, c4 = st.columns(2)
    with c3:
        with st.container(border=True):
            st.markdown("#### Phân khúc nào chi tiêu mạnh tay nhất?")
            st.markdown("<p style='color: #64748b; font-size: 0.9rem; margin-top: -10px;'>All Levels chiếm phần lớn — ai cũng muốn học tổng quan</p>", unsafe_allow_html=True)
            
            lvl_sales = df_f.groupby('level')['sales'].sum().sort_values(ascending=False).reset_index()
            total_sales_lvl = lvl_sales['sales'].sum() if lvl_sales['sales'].sum() > 0 else 1
            
            html_lvl = '<div style="margin-top: 15px;">'
            color_map = {0: '#5a67d8', 1: '#818cf8', 2: '#a5b4fc', 3: '#e2e8f0'}
            for i, row in lvl_sales.iterrows():
                pct = row['sales'] / total_sales_lvl * 100
                color = color_map.get(i, '#e2e8f0')
                html_lvl += f"""<div style="margin-bottom: 15px;">
<div style="display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 0.95rem; color: #334155; font-weight: 500;">
<span>{row['level']}</span>
<span style="font-weight: 700;">~{pct:.0f}%</span>
</div>
<div style="width: 100%; background-color: #f1f5f9; border-radius: 10px; height: 10px; overflow: hidden;">
<div style="width: {pct}%; background-color: {color}; height: 100%; border-radius: 10px;"></div>
</div>
</div>"""
            html_lvl += """<div style="background-color: #f8fafc; padding: 12px 16px; border-radius: 8px; margin-top: 20px; font-size: 0.9rem; color: #475569;">
Insight: Expert Level ít nhưng mức giá cao — tiềm năng tăng trưởng còn lớn
</div>
</div>"""
            st.markdown(html_lvl, unsafe_allow_html=True)

    with c4:
        with st.container(border=True):
            st.markdown("#### Khóa học độ dài nào mang lại nhiều tiền nhất?")
            st.markdown("<p style='color: #64748b; font-size: 0.9rem; margin-top: -10px;'>Phân bổ doanh thu theo số lượng bài giảng</p>", unsafe_allow_html=True)
            
            bins_lec = [0, 10, 20, 30, 40, 50, 60, 1000]
            labels_lec = ['1-10', '11-20', '21-30', '31-40', '41-50', '51-60', '60+']
            df_f['lec_bin'] = pd.cut(df_f['num_lectures'], bins=bins_lec, labels=labels_lec)
            lec_stats = df_f.groupby('lec_bin', observed=False)['sales'].sum().reset_index()
            
            peak_idx = lec_stats['sales'].idxmax()
            
            colors_lec = ['#e0e7ff'] * len(lec_stats)
            if not pd.isna(peak_idx):
                colors_lec[peak_idx] = '#5a67d8'
            
            fig_lec = go.Figure()
            fig_lec.add_trace(go.Bar(
                x=lec_stats['lec_bin'], y=lec_stats['sales'],
                marker_color=colors_lec,
                marker_line_width=0,
                text=['<b>Peak</b>' if i == peak_idx else '' for i in range(len(lec_stats))],
                textposition='outside',
                textfont=dict(color='#5a67d8', size=11),
                hovertemplate="<b>%{x} bài giảng</b><br>Doanh thu: $%{y:,.0f}<extra></extra>"
            ))
            
            fig_lec.update_layout(
                height=280, margin=dict(t=30, b=10, l=10, r=10),
                xaxis=dict(showgrid=False, tickfont=dict(color='#64748b', size=10)),
                yaxis=dict(showgrid=False, visible=False),
                showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            fig_lec.update_yaxes(range=[0, lec_stats['sales'].max() * 1.2])
            
            st.plotly_chart(fig_lec, use_container_width=True)

# ================= PAGE: SUBSCRIBER =================
elif page == "Học viên":
    st.title("Phân tích học viên")

    df_f['review_ratio'] = (df_f['num_reviews'] / df_f['num_subscribers']).fillna(0)
    total_subs = df_f['num_subscribers'].sum()
    paid_subs_pct = (df_f[df_f['is_paid']==True]['num_subscribers'].sum() / total_subs * 100) if total_subs > 0 else 0
    
    top_subj = df_f.groupby('subject')['num_subscribers'].sum().idxmax()
    top_subj_subs = df_f.groupby('subject')['num_subscribers'].sum().max()
    short_names = {'Web Development': 'Web Dev', 'Business Finance': 'Biz Finance', 'Graphic Design': 'Graphic', 'Musical Instruments': 'Musical Instruments'}
    top_subj_short = short_names.get(top_subj, top_subj)
    
    st.markdown(f"""
        <div style="background: linear-gradient(90deg, #c47c21 0%, #b26815 100%); padding: 25px 35px; border-radius: 12px; color: white; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <div>
                <div style="font-size: 3.2rem; font-weight: 700; line-height: 1.1; margin-bottom: 8px;">{int(total_subs):,}</div>
                <div style="font-size: 1.05rem; opacity: 0.9;">{paid_subs_pct:.2f}% là học viên trả phí</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 1rem; opacity: 0.9; margin-bottom: 4px;">Chủ đề hot nhất</div>
                <div style="font-size: 1.9rem; font-weight: 700; line-height: 1.2; margin-bottom: 4px;">{top_subj_short}</div>
                <div style="font-size: 1.05rem; opacity: 0.9;">{top_subj_subs/1e6:.2f}M học viên</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("#### Học viên theo chủ đề")
            sorted_subj = df_f.groupby('subject')['num_subscribers'].sum().sort_values(ascending=False)
            if len(sorted_subj) > 1:
                ratio = sorted_subj.iloc[0] / sorted_subj.iloc[1]
                subtitle_c1 = f"{short_names.get(sorted_subj.index[0], sorted_subj.index[0])} áp đảo — gấp {ratio:.0f} lần chủ đề kế tiếp"
            else:
                subtitle_c1 = "Phân bổ học viên theo chủ đề"
            st.markdown(f"<p style='color: #64748b; font-size: 0.9rem; margin-top: -10px;'>{subtitle_c1}</p>", unsafe_allow_html=True)
            
            html_sub = '<div style="margin-top: 20px;">'
            max_subs = sorted_subj.max()
            total_subs_val = sorted_subj.sum()
            for i, (subj, subs) in enumerate(sorted_subj.items()):
                pct = subs / max_subs * 100
                color = '#f59e0b' if i == 0 else '#fde68a'
                subs_text = f"{subs/1e6:.2f}M".replace('.00', '') if subs >= 1e6 else f"{subs/1000:.0f}K"
                html_sub += f"""<div style="margin-bottom: 15px;">
<div style="display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 0.95rem; color: #334155; font-weight: 500;">
<span>{subj}</span>
<span style="font-weight: 700;">{subs_text}</span>
</div>
<div style="width: 100%; background-color: #f1f5f9; border-radius: 10px; height: 10px; overflow: hidden;">
<div style="width: {pct}%; background-color: {color}; height: 100%; border-radius: 10px;"></div>
</div>
</div>"""
            top_pct = sorted_subj.iloc[0] / total_subs_val * 100 if total_subs_val > 0 else 0
            html_sub += f"""<div style="background-color: #f8fafc; padding: 12px 16px; border-radius: 8px; margin-top: 20px; font-size: 0.9rem; color: #475569;">
{short_names.get(sorted_subj.index[0], sorted_subj.index[0])} chiếm {top_pct:.0f}% tổng học viên — rủi ro phụ thuộc vào 1 chủ đề
</div>
</div>"""
            st.markdown(html_sub, unsafe_allow_html=True)

    with c2:
        with st.container(border=True):
            st.markdown("#### Học viên theo trình độ")
            st.markdown("<p style='color: #64748b; font-size: 0.9rem; margin-top: -10px;'>Đa số không phân định trình độ cụ thể</p>", unsafe_allow_html=True)
            
            lvl_subs = df_f.groupby('level')['num_subscribers'].sum().sort_values(ascending=False).reset_index()
            def format_subs(x):
                return f"{x/1e6:.1f}M" if x >= 1e6 else f"{x/1000:.0f}K"
            lvl_subs['label_full'] = lvl_subs.apply(lambda row: f"{row['level']} · {format_subs(row['num_subscribers'])}", axis=1)
            
            colors_donut = ['#f59e0b', '#fcd34d', '#fef3c7', '#78350f']
            fig_donut = go.Figure(go.Pie(
                labels=lvl_subs['label_full'],
                values=lvl_subs['num_subscribers'],
                hole=0.6,
                domain=dict(x=[0, 0.55]),
                marker=dict(colors=colors_donut, line=dict(color='white', width=2)),
                textinfo='none',
                hovertemplate="<b>%{label}</b><br>Học viên: %{value:,.0f}<extra></extra>"
            ))
            fig_donut.add_annotation(
                text=f"<b>{format_subs(total_subs)}</b><br><span style='font-size:12px;color:#64748b'>học viên</span>",
                x=0.275, y=0.5, font_size=16, showarrow=False, align="center"
            )
            fig_donut.update_layout(
                height=280, margin=dict(t=10, b=10, l=10, r=10),
                legend=dict(yanchor="middle", y=0.5, xanchor="left", x=0.6, font=dict(size=14)),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("#### Mức giá nào học viên tương tác nhiều nhất?")
        st.markdown("<p style='color: #64748b; font-size: 0.9rem; margin-top: -10px;'>Cột = tổng học viên · Đường = tỷ lệ đánh giá/học viên · Vùng $81-120 có rating cao nhất tương đối</p>", unsafe_allow_html=True)
        
        bins_p = [-1, 0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200]
        labels_p = ['Miễn phí', '0-20', '21-40', '41-60', '61-80', '81-100', '101-120', '121-140', '141-160', '161-180', '181-200']
        df_f['price_range'] = pd.cut(df_f['price'], bins=bins_p, labels=labels_p)
        price_stats_s = df_f.groupby('price_range', observed=False).agg({'num_subscribers':'sum', 'review_ratio':'mean'}).reset_index()
        
        fig_p_s = make_subplots(specs=[[{"secondary_y": True}]])
        
        colors_bar = ['#f59e0b'] + ['#fdd8a4'] * (len(price_stats_s)-1)
        
        fig_p_s.add_trace(go.Bar(
            x=price_stats_s['price_range'], y=price_stats_s['num_subscribers'], 
            name="Học viên", marker_color=colors_bar, opacity=0.9
        ), secondary_y=False)
        
        fig_p_s.add_trace(go.Scatter(
            x=price_stats_s['price_range'], y=price_stats_s['review_ratio'], 
            name="Rating", line=dict(color='#5a67d8', width=3, shape='spline'),
            mode='lines'
        ), secondary_y=True)
        
        peak_idx = price_stats_s['review_ratio'].idxmax()
        if not pd.isna(peak_idx):
            peak_row = price_stats_s.iloc[peak_idx]
            fig_p_s.add_trace(go.Scatter(
                x=[peak_row['price_range']], y=[peak_row['review_ratio']],
                mode='markers+text',
                marker=dict(color='#5a67d8', size=10),
                text=['Cao nhất'],
                textposition='top center',
                textfont=dict(color='#5a67d8', size=11, weight='bold'),
                showlegend=False
            ), secondary_y=True)
            
            tickvals = price_stats_s['price_range'].tolist()
            ticktext = [f"<span style='color: #5a67d8; font-weight: bold;'>{val}</span>" if val == peak_row['price_range'] else str(val) for val in tickvals]
        else:
            tickvals = price_stats_s['price_range'].tolist()
            ticktext = tickvals
            
        fig_p_s.update_layout(
            height=320, margin=dict(t=30, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1, font=dict(size=12)),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, tickmode='array', tickvals=tickvals, ticktext=ticktext, tickfont=dict(color='#64748b', size=10))
        )
        
        fig_p_s.update_yaxes(showgrid=False, visible=False, secondary_y=False)
        fig_p_s.update_yaxes(showgrid=False, visible=False, secondary_y=True)
        fig_p_s.update_yaxes(range=[0, price_stats_s['review_ratio'].max() * 1.3], secondary_y=True)
        
        st.plotly_chart(fig_p_s, use_container_width=True)

# ================= PAGE: CONTENT =================
elif page == "Nội dung":
    st.title("Phân tích nội dung")

    total_duration = df_f['duration_hours'].sum()
    paid_duration_pct = (df_f[df_f['is_paid']==True]['duration_hours'].sum() / total_duration * 100) if total_duration > 0 else 0
    
    top_subj_dur = df_f.groupby('subject')['duration_hours'].sum().idxmax()
    top_subj_dur_val = df_f.groupby('subject')['duration_hours'].sum().max()
    short_names = {'Web Development': 'Web Dev', 'Business Finance': 'Biz Finance', 'Graphic Design': 'Graphic', 'Musical Instruments': 'Music'}
    top_subj_short = short_names.get(top_subj_dur, top_subj_dur)
    
    st.markdown(f"""
        <div style="background: linear-gradient(90deg, #1f7762 0%, #14532d 100%); padding: 25px 35px; border-radius: 12px; color: white; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <div>
                <div style="font-size: 1rem; opacity: 0.9; margin-bottom: 4px;">Thời lượng nội dung (giờ)</div>
                <div style="font-size: 3.2rem; font-weight: 700; line-height: 1.1; margin-bottom: 8px;">{total_duration:,.2f}</div>
                <div style="font-size: 1.05rem; opacity: 0.9;">{paid_duration_pct:.2f}% là nội dung trả phí</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 1rem; opacity: 0.9; margin-bottom: 4px;">Chủ đề nhiều giờ nhất</div>
                <div style="font-size: 1.9rem; font-weight: 700; line-height: 1.2; margin-bottom: 4px;">{top_subj_short}</div>
                <div style="font-size: 1.05rem; opacity: 0.9;">{top_subj_dur_val:,.0f} giờ</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("#### Số giờ nội dung: Chủ đề × Trình độ")
            st.markdown("<p style='color: #64748b; font-size: 0.9rem; margin-top: -10px;'>Màu đậm = nhiều giờ hơn</p>", unsafe_allow_html=True)
            
            heatmap_data = df_f.groupby(['subject', 'level'])['duration_hours'].sum().unstack(fill_value=0)
            level_short = {'All Levels': 'All', 'Beginner Level': 'Beg', 'Intermediate Level': 'Int', 'Expert Level': 'Exp'}
            heatmap_data = heatmap_data.rename(columns=level_short)
            cols_ordered = ['All', 'Beg', 'Int', 'Exp']
            for c in cols_ordered:
                if c not in heatmap_data.columns:
                    heatmap_data[c] = 0
            heatmap_data = heatmap_data[cols_ordered]
            
            heatmap_data.index = heatmap_data.index.map(lambda x: short_names.get(x, x))
            heatmap_data['total'] = heatmap_data.sum(axis=1)
            heatmap_data = heatmap_data.sort_values('total', ascending=False).drop(columns='total')
            
            max_val = heatmap_data.values.max()
            if max_val == 0: max_val = 1
            
            html_heat = f"""<div style="width: 100%; margin-top: 20px;">
<div style="display: flex; text-align: center; font-size: 0.9rem; color: #64748b; margin-bottom: 8px;">
<div style="width: 100px;"></div>
<div style="flex: 1;">All</div>
<div style="flex: 1;">Beg</div>
<div style="flex: 1;">Int</div>
<div style="flex: 1;">Exp</div>
</div>"""
            for subj in heatmap_data.index:
                html_heat += f"""<div style="display: flex; align-items: center; margin-bottom: 4px;">
<div style="width: 100px; font-size: 0.9rem; color: #334155;">{subj}</div>"""
                for col in cols_ordered:
                    val = heatmap_data.loc[subj, col]
                    pct = val / max_val
                    if val == 0:
                        bg_color = "#f8fafc"
                        text_color = "#94a3b8"
                    else:
                        opacity = max(0.2, min(1.0, pct + 0.1))
                        bg_color = f"rgba(16, 185, 129, {opacity})"
                        text_color = "#ffffff" if opacity > 0.5 else "#047857"
                        
                    val_str = f"{val/1000:.1f}k" if val >= 1000 else f"{val:.0f}"
                    html_heat += f"""<div style="flex: 1; background-color: {bg_color}; color: {text_color}; text-align: center; padding: 10px 0; margin: 0 2px; border-radius: 4px; font-size: 0.85rem; font-weight: 500;">
{val_str}
</div>"""
                html_heat += "</div>"
                
            html_heat += """<div style="display: flex; align-items: center; margin-top: 15px; font-size: 0.85rem; color: #64748b;">
<span style="margin-right: 8px;">Ít</span>
<div style="flex: 1; display: flex; height: 8px; border-radius: 4px; overflow: hidden;">
<div style="flex: 1; background-color: rgba(16, 185, 129, 0.2); margin: 0 1px;"></div>
<div style="flex: 1; background-color: rgba(16, 185, 129, 0.4); margin: 0 1px;"></div>
<div style="flex: 1; background-color: rgba(16, 185, 129, 0.6); margin: 0 1px;"></div>
<div style="flex: 1; background-color: rgba(16, 185, 129, 0.8); margin: 0 1px;"></div>
<div style="flex: 1; background-color: rgba(16, 185, 129, 1.0); margin: 0 1px;"></div>
</div>
<span style="margin-left: 8px;">Nhiều</span>
</div>
</div>"""
            st.markdown(html_heat, unsafe_allow_html=True)
            
    with c2:
        with st.container(border=True):
            st.markdown("#### Độ dài khóa học phổ biến nhất")
            st.markdown("<p style='color: #64748b; font-size: 0.9rem; margin-top: -10px;'>Phần lớn khóa học nằm trong vùng 5-20 giờ</p>", unsafe_allow_html=True)
            
            bins_d = [0, 2, 5, 10, 20, 30, 50, 100]
            labels_d = ['0-2h', '2-5h', '5-10h', '10-20h', '20-30h', '30-50h', '50h+']
            df_f['dur_bin'] = pd.cut(df_f['duration_hours'], bins=bins_d, labels=labels_d)
            dur_pop = df_f.groupby('dur_bin', observed=False)['course_id'].count().reset_index()
            dur_pop = dur_pop[dur_pop['dur_bin'] != '50h+']
            
            fig_dur = go.Figure()
            fig_dur.add_trace(go.Scatter(
                x=dur_pop['dur_bin'], y=dur_pop['course_id'],
                mode='lines',
                line=dict(color='#10b981', width=3, shape='spline'),
                fill='tozeroy',
                fillcolor='rgba(16, 185, 129, 0.2)'
            ))
            
            peak_idx = dur_pop['course_id'].idxmax()
            if not pd.isna(peak_idx):
                peak_row = dur_pop.iloc[peak_idx]
                
                fig_dur.add_trace(go.Scatter(
                    x=[peak_row['dur_bin']], y=[peak_row['course_id']],
                    mode='markers+text',
                    marker=dict(color='#10b981', size=10),
                    text=[f"{peak_row['dur_bin']} (Peak)"],
                    textposition='top center',
                    textfont=dict(color='#10b981', size=11, weight='bold'),
                    showlegend=False
                ))
                
                fig_dur.add_vline(x=peak_row['dur_bin'], line_width=1, line_dash="dash", line_color="#a7f3d0")
                
                tickvals = dur_pop['dur_bin'].tolist()
                ticktext = [f"<span style='color: #10b981; font-weight: bold;'>{val}</span>" if val == peak_row['dur_bin'] else str(val) for val in tickvals]
            else:
                tickvals = dur_pop['dur_bin'].tolist()
                ticktext = tickvals
            
            fig_dur.update_layout(
                height=280, margin=dict(t=30, b=10, l=10, r=10),
                xaxis=dict(showgrid=False, tickmode='array', tickvals=tickvals, ticktext=ticktext, tickfont=dict(color='#64748b', size=10)),
                yaxis=dict(showgrid=False, visible=False),
                showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            fig_dur.update_yaxes(range=[0, dur_pop['course_id'].max() * 1.3])
            
            st.plotly_chart(fig_dur, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("#### Số bài giảng tối ưu để thu hút học viên")
        
        bins_lec = [0, 10, 20, 30, 40, 50, 60, 80, 1000]
        labels_lec = ['1-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-80', '80+']
        df_f['lec_range'] = pd.cut(df_f['num_lectures'], bins=bins_lec, labels=labels_lec)
        lec_stats = df_f.groupby('lec_range', observed=False).agg({'course_id': 'count', 'num_subscribers': 'mean'}).reset_index()
        lec_stats.columns = ['lec_range', 'course_count', 'avg_subscribers']
        
        peak_idx = lec_stats['avg_subscribers'].idxmax()
        peak_val = lec_stats.loc[peak_idx, 'lec_range'] if not pd.isna(peak_idx) else "21-30"
        
        st.markdown(f"<p style='color: #64748b; font-size: 0.9rem; margin-top: -10px;'>Cột thể hiện Trung bình Học viên / khóa học · Nhóm <b>{peak_val} bài giảng</b> thu hút học viên tốt nhất</p>", unsafe_allow_html=True)
        
        col_c, col_info = st.columns([3, 1])
        
        with col_c:
            fig_lec = go.Figure()
            
            colors_lec = []
            for i, row in lec_stats.iterrows():
                if i == peak_idx:
                    colors_lec.append('#10b981')
                else:
                    colors_lec.append('#a7f3d0')
                    
            fig_lec.add_trace(go.Bar(
                x=lec_stats['lec_range'], y=lec_stats['avg_subscribers'],
                marker_color=colors_lec,
                marker_line_width=0,
                hovertemplate="<b>%{x} bài giảng</b><br>TB Học viên: %{y:,.0f}<extra></extra>"
            ))
            
            tickvals = lec_stats['lec_range'].tolist()
            ticktext = [f"<span style='color: #10b981; font-weight: bold;'>{val}</span>" if val == peak_val else str(val) for val in tickvals]
            
            fig_lec.update_layout(
                height=320, margin=dict(t=20, b=10, l=10, r=10),
                xaxis=dict(showgrid=False, tickmode='array', tickvals=tickvals, ticktext=ticktext, tickfont=dict(color='#64748b', size=10)),
                yaxis=dict(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(color='#94a3b8', size=10), tickformat=',.0f'),
                showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_lec, use_container_width=True)
            
        with col_info:
            st.markdown(f"""<div style="background-color: #f5f5f4; padding: 20px; border-radius: 12px; height: 100%; display: flex; flex-direction: column; justify-content: center;">
<div style="font-weight: 700; color: #334155; margin-bottom: 15px; font-size: 0.95rem;">Kết luận cho giảng viên</div>
<div style="font-size: 0.9rem; color: #475569; margin-bottom: 15px;">
Khóa học khoảng <span style="color: #059669; font-weight: 700;">{peak_val} bài</span> đang thu hút lượng học viên đăng ký trung bình cao nhất.
</div>
<div style="font-size: 0.9rem; color: #475569; margin-bottom: 15px;">
Dưới 10 bài — học viên cảm thấy nội dung chưa đủ sâu.
</div>
<div style="font-size: 0.9rem; color: #475569;">
Trên 60 bài — lượng đăng ký trung bình bắt đầu giảm nhiệt.
</div>
</div>""", unsafe_allow_html=True)
# ================= PAGE: COURSES =================
elif page == "Khóa học":
    st.title("Danh sách khóa học & Phân tích tăng trưởng")

    # --- HÀNG 1: KPI CARDS ---
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        # Tổng số khóa học hiện tại (đã lọc)
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #7184fc 0%, #505fc8 100%); padding: 24px; border-radius: 16px; color: white; box-shadow: 0 8px 20px rgba(113, 132, 252, 0.25); transition: transform 0.3s ease;" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
                <p style="margin:0; font-size: 1rem; font-weight: 500; opacity: 0.9;">🎓 Tổng khóa học</p>
                <h2 style="margin:10px 0 0 0; font-size: 2.5rem; font-weight: 800; color: white;">{len(df_f):,}</h2>
            </div>
        """, unsafe_allow_html=True)
    with col_k2:
        # Hiển thị Chủ đề có nhiều khóa học nhất trong danh sách đã lọc
        if not df_f.empty:
            top_sub_name = df_f['subject'].value_counts().idxmax()
            top_sub_val = df_f['subject'].value_counts().max()
        else:
            top_sub_name, top_sub_val = "N/A", 0
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #68c9fe 0%, #32a0dc 100%); padding: 24px; border-radius: 16px; color: white; box-shadow: 0 8px 20px rgba(104, 201, 254, 0.25); transition: transform 0.3s ease;" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
                <p style="margin:0; font-size: 1rem; font-weight: 500; opacity: 0.9;">🏆 Chủ đề hàng đầu: {top_sub_name}</p>
                <h2 style="margin:10px 0 0 0; font-size: 2.5rem; font-weight: 800; color: white;">{top_sub_val:,} Khóa học</h2>
            </div>
        """, unsafe_allow_html=True)

    st.write("") # Tạo khoảng cách

    # --- HÀNG 2: BIỂU ĐỒ THỐNG KÊ ---
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("##### 📐 Sự phân bổ nguồn lực đào tạo theo cấp độ chuyên môn")
        lvl_sub_data = df_f.groupby(['level', 'subject']).size().reset_index(name='count')
        fig1 = px.bar(lvl_sub_data, x='level', y='count', color='subject', barmode='group',
                      color_discrete_sequence=px.colors.qualitative.Pastel)
        fig1.update_traces(marker=dict(line=dict(width=0)))
        fig1.update_layout(height=300, showlegend=False, margin=dict(t=10, b=10, l=0, r=0), template='plotly_white', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.markdown("##### 🎯 Chúng ta đang 'bỏ quên' học viên ở trình độ nào?")
        heat_data = df_f.groupby(['subject', 'level'])['course_id'].count().reset_index(name='count')
        heat_pivot = heat_data.pivot(index='subject', columns='level', values='count').fillna(0)
        # Sắp xếp cột theo thứ tự hợp lý
        level_order = [l for l in ['Beginner Level', 'Intermediate Level', 'Expert Level', 'All Levels'] if l in heat_pivot.columns]
        heat_pivot = heat_pivot[level_order]

        fig_heat = go.Figure(go.Heatmap(
            z=heat_pivot.values,
            x=heat_pivot.columns.tolist(),
            y=heat_pivot.index.tolist(),
            colorscale=[[0, '#f0f4ff'], [0.4, '#68c9fe'], [0.75, '#7184fc'], [1, '#505fc8']],
            text=heat_pivot.values.astype(int),
            texttemplate='%{text}',
            textfont=dict(size=13, color='#1e293b'),
            hovertemplate='%{y} × %{x}<br>Số khóa học: %{z}<extra></extra>',
            showscale=False
        ))
        fig_heat.update_layout(
            height=300,
            margin=dict(t=10, b=10, l=0, r=0),
            xaxis=dict(title=None, tickfont=dict(size=11)),
            yaxis=dict(title=None, tickfont=dict(size=11)),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    with c3:
        st.markdown("##### 🚀 Bức tranh tăng trưởng: Xu hướng phát triển qua thời gian")
        growth_data = df_f.groupby(['year', 'subject']).size().reset_index(name='count')
        fig3 = px.area(growth_data, x='year', y='count', color='subject',
                       color_discrete_sequence=px.colors.qualitative.Pastel)
        fig3.update_traces(line=dict(width=2))
        fig3.update_layout(height=300, showlegend=False, margin=dict(t=10, b=10, l=0, r=0), template='plotly_white', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig3, use_container_width=True)

    # --- DASHBOARD: SEASONALITY & TIMING ---
    st.markdown("---")
    st.markdown("### ⏰ Phân tích Thời điểm 'Vàng' để Xuất bản Khóa học")

    month_names = {1:'Th1', 2:'Th2', 3:'Th3', 4:'Th4', 5:'Th5', 6:'Th6',
                   7:'Th7', 8:'Th8', 9:'Th9', 10:'Th10', 11:'Th11', 12:'Th12'}
    weekday_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    weekday_vi    = {'Monday':'T2','Tuesday':'T3','Wednesday':'T4',
                     'Thursday':'T5','Friday':'T6','Saturday':'T7','Sunday':'CN'}

    s1, s2, s3 = st.columns(3)

    with s1:
        st.markdown("##### 📅 Tháng nào các giảng viên đua nhau ra mắt khóa học mới?")
        month_count = df_f.groupby('month')['course_id'].count().reset_index()
        month_count['label'] = month_count['month'].map(month_names)
        fig_month = go.Figure()
        fig_month.add_trace(go.Scatter(
            x=month_count['label'], y=month_count['course_id'],
            mode='lines+markers',
            line=dict(color='#7184fc', width=3, shape='spline'),
            fill='tozeroy', fillcolor='rgba(113,132,252,0.15)',
            marker=dict(size=7, color='#7184fc'),
            hovertemplate='%{x}: %{y} khóa học<extra></extra>'
        ))
        fig_month.update_layout(
            height=300, yaxis=dict(visible=False),
            xaxis=dict(title=None, tickfont=dict(size=11)),
            margin=dict(t=20, b=10, l=0, r=0),
            template='plotly_white', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_month, use_container_width=True)

    with s2:
        st.markdown("##### 🍂 Ra mắt vào mùa nào thì dễ 'hốt' học viên nhất?")
        month_subs = df_f.groupby('month')['num_subscribers'].mean().reset_index()
        month_subs['label'] = month_subs['month'].map(month_names)
        fig_season = go.Figure()
        fig_season.add_trace(go.Scatter(
            x=month_subs['label'], y=month_subs['num_subscribers'],
            mode='lines+markers',
            line=dict(color='#fc970f', width=3, shape='spline'),
            fill='tozeroy', fillcolor='rgba(252,151,15,0.15)',
            marker=dict(size=7, color='#fc970f'),
            hovertemplate='%{x}: %{y:.2s} học viên TB<extra></extra>'
        ))
        fig_season.update_layout(
            height=300, yaxis=dict(visible=False),
            xaxis=dict(title=None, tickfont=dict(size=11)),
            margin=dict(t=20, b=10, l=0, r=0),
            template='plotly_white', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_season, use_container_width=True)

    with s3:
        st.markdown("##### 📆 Đăng khóa học vào cuối tuần hay đầu tuần thì tốt hơn?")
        wd_count = df_f.groupby('weekday')['course_id'].count().reset_index()
        wd_count['order'] = wd_count['weekday'].map({d: i for i, d in enumerate(weekday_order)})
        wd_count = wd_count.sort_values('order', ascending=False)
        wd_count['label'] = wd_count['weekday'].map(weekday_vi)
        colors = ['#68c9fe' if d in ['Saturday','Sunday'] else '#7184fc' for d in wd_count['weekday']]
        fig_wd = go.Figure(go.Bar(
            y=wd_count['label'], x=wd_count['course_id'],
            orientation='h',
            marker_color=colors, marker=dict(line=dict(width=0)),
            text=wd_count['course_id'], textposition='outside'
        ))
        fig_wd.update_layout(
            height=300, xaxis=dict(visible=False, range=[0, wd_count['course_id'].max()*1.25]),
            yaxis=dict(title=None, tickfont=dict(size=12)),
            margin=dict(t=20, b=10, l=0, r=40),
            template='plotly_white', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_wd, use_container_width=True)

    # --- HÀNG 3: BẢNG XẾP HẠNG TOP 5 ---
    st.markdown("---")
    st.markdown("#### Top 5 khóa học Udemy dựa trên:")
    
    # Tạo các nút bấm để chọn tiêu chí xếp hạng giống trong hình
    sort_criterion = st.radio("", ["Thời lượng", "Học viên", "Đánh giá", "Doanh thu"], horizontal=True)

    # Ánh xạ tên nút bấm với tên cột trong dataframe
    metric_map = {
        "Thời lượng": "duration_hours",
        "Học viên": "num_subscribers",
        "Đánh giá": "num_reviews",
        "Doanh thu": "sales"
    }

    # Lấy Top 5
    top_5 = df_f.sort_values(by=metric_map[sort_criterion], ascending=False).head(5)

    # Hiển thị bảng với các cột được định dạng đẹp
    display_cols = ['course_title', 'subject', 'level', 'duration_hours', 'price', 'num_subscribers', 'num_reviews', 'sales']
    df_display = top_5[display_cols].copy()
    
    # Đổi tên cột cho đẹp
    df_display.columns = ['Tên khóa học', 'Chủ đề', 'Trình độ', 'Thời lượng (Giờ)', 'Giá', 'Học viên', 'Đánh giá', 'Doanh thu']

    # Định dạng bảng
    st.dataframe(df_display.style.format({
        'Thời lượng (Giờ)': '{:.2f}',
        'Giá': '${:,.2f}',
        'Học viên': '{:,}',
        'Đánh giá': '{:,}',
        'Doanh thu': '${:,.0f}'
    }), use_container_width=True, hide_index=True)
elif page == "Dự đoán":
    import numpy as np
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline

    st.title("🔮 Dự đoán hiệu suất khóa học mới")
    st.markdown("<p style='color: #64748b; font-size: 1.1rem; margin-top: -15px;'>Mô phỏng Machine Learning để tối ưu hóa doanh thu, học viên và định giá khóa học mới trước khi xuất bản.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # 1. Caching & Training ML model on the active dataset
    @st.cache_resource
    def get_prediction_models(_df):
        # Drop rows with NaN in important fields
        train_df = _df.dropna(subset=['price', 'num_lectures', 'duration_hours', 'subject', 'level', 'num_subscribers', 'sales']).copy()
        
        # Features & Targets
        X = train_df[['subject', 'level', 'price', 'num_lectures', 'duration_hours', 'is_paid']]
        y_subs = train_df['num_subscribers']
        y_sales = train_df['sales']
        
        # Preprocessor for categorical columns
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(handle_unknown='ignore'), ['subject', 'level'])
            ],
            remainder='passthrough'
        )
        
        # Build Random Forest pipeline for Subscribers
        pipeline_subs = Pipeline([
            ('preprocessor', preprocessor),
            ('regressor', RandomForestRegressor(n_estimators=30, random_state=42, n_jobs=-1))
        ])
        pipeline_subs.fit(X, y_subs)
        
        # Build Random Forest pipeline for Sales
        pipeline_sales = Pipeline([
            ('preprocessor', preprocessor),
            ('regressor', RandomForestRegressor(n_estimators=30, random_state=42, n_jobs=-1))
        ])
        pipeline_sales.fit(X, y_sales)
        
        return pipeline_subs, pipeline_sales

    # Load ML pipelines
    with st.spinner("Đang tối ưu hóa mô hình AI..."):
        try:
            pipeline_subs, pipeline_sales = get_prediction_models(df)
        except Exception as e:
            st.error(f"Lỗi khi huấn luyện mô hình: {e}")
            st.stop()

    # 2. Main layout: Left for Inputs, Right for Results & AI recommendations
    col_inputs, col_results = st.columns([1, 2], gap="large")

    with col_inputs:
        with st.container(border=True):
            st.markdown("<h4 style='color: #1e1b4b; margin-bottom: 15px;'>📝 Thiết lập khóa học mới</h4>", unsafe_allow_html=True)
            
            # Select subject
            sub_options = sorted(list(df['subject'].dropna().unique()))
            subject = st.selectbox("Chủ đề khóa học", options=sub_options, index=sub_options.index('Web Development') if 'Web Development' in sub_options else 0)
            
            # Select level
            lvl_options = sorted(list(df['level'].dropna().unique()))
            level = st.selectbox("Trình độ hướng tới", options=lvl_options, index=lvl_options.index('All Levels') if 'All Levels' in lvl_options else 0)
            
            # Select price
            price = st.slider("Giá bán dự kiến ($)", min_value=0, max_value=200, value=40, step=10)
            
            # Select number of lectures
            num_lectures = st.slider("Số lượng bài giảng", min_value=5, max_value=300, value=35, step=5)
            
            # Select duration hours
            duration_hours = st.slider("Thời lượng video (Giờ)", min_value=1.0, max_value=120.0, value=8.0, step=0.5)

    with col_results:
        # 3. Running predictions
        input_data = pd.DataFrame([{
            'subject': subject,
            'level': level,
            'price': price,
            'num_lectures': num_lectures,
            'duration_hours': duration_hours,
            'is_paid': price > 0
        }])
        
        # Predict subscribers & sales
        pred_subs = max(0, pipeline_subs.predict(input_data)[0])
        pred_sales = max(0, pipeline_sales.predict(input_data)[0])
        
        # If price is 0, sales must be 0
        if price == 0:
            pred_sales = 0
            
        # Estimate reviews (approx 5.5% of subscribers based on historical mean)
        pred_reviews = pred_subs * 0.055

        # 4. Display Premium KPI Cards
        st.markdown(f"""
            <div style="display: flex; gap: 15px; margin-bottom: 25px;">
                <div style="flex: 1; background: linear-gradient(135deg, #ede9fe 0%, #fae8ff 100%); padding: 18px 24px; border-radius: 14px; border: 1.5px solid #d8b4fe; box-shadow: 0 4px 6px rgba(0,0,0,0.02); text-align: center;">
                    <div style="font-size: 0.8rem; color: #6d28d9; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 8px;">👥 HỌC VIÊN DỰ KIẾN</div>
                    <div style="font-size: 1.9rem; font-weight: 800; color: #4c1d95; line-height: 1.2;">{pred_subs:,.0f}</div>
                    <div style="font-size: 0.8rem; color: #7c3aed; margin-top: 5px;">Học viên / năm đầu</div>
                </div>
                <div style="flex: 1; background: linear-gradient(135deg, #dcfce7 0%, #ecfdf5 100%); padding: 18px 24px; border-radius: 14px; border: 1.5px solid #86efac; box-shadow: 0 4px 6px rgba(0,0,0,0.02); text-align: center;">
                    <div style="font-size: 0.8rem; color: #15803d; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 8px;">💰 DOANH THU DỰ KIẾN</div>
                    <div style="font-size: 1.9rem; font-weight: 800; color: #14532d; line-height: 1.2;">${pred_sales:,.0f}</div>
                    <div style="font-size: 0.8rem; color: #16a34a; margin-top: 5px;">Tổng doanh thu thu về</div>
                </div>
                <div style="flex: 1; background: linear-gradient(135deg, #eff6ff 0%, #f0f9ff 100%); padding: 18px 24px; border-radius: 14px; border: 1.5px solid #93c5fd; box-shadow: 0 4px 6px rgba(0,0,0,0.02); text-align: center;">
                    <div style="font-size: 0.8rem; color: #1d4ed8; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 8px;">⭐ ĐÁNH GIÁ DỰ KIẾN</div>
                    <div style="font-size: 1.9rem; font-weight: 800; color: #1e3a8a; line-height: 1.2;">{pred_reviews:,.0f}</div>
                    <div style="font-size: 0.8rem; color: #2563eb; margin-top: 5px;">Lượng reviews dự kiến</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # 5. Visual comparison container
        with st.container(border=True):
            st.markdown(f"<h5 style='color: #1e293b; margin-bottom: 10px;'>📊 Sức hút của khóa học so với trung bình chủ đề {subject}</h5>", unsafe_allow_html=True)
            
            # Fetch average subscribers for subject
            subj_avg = df[df['subject'] == subject]
            avg_subs = subj_avg['num_subscribers'].mean() if len(subj_avg) > 0 else 1000
            
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Bar(
                x=[f"Trung bình chủ đề", "Khóa của bạn (Dự đoán)"],
                y=[avg_subs, pred_subs],
                marker_color=["#cbd5e1", "#8b5cf6"],
                text=[f"{avg_subs:,.0f} học viên", f"{pred_subs:,.0f} học viên"],
                textposition='auto',
                width=0.4
            ))
            fig_comp.update_layout(
                height=220,
                margin=dict(t=10, b=10, l=10, r=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(showgrid=True, gridcolor='#f1f5f9', visible=False)
            )
            st.plotly_chart(fig_comp, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 6. AI recommendation engine
        st.markdown("<h5 style='color: #1e293b; margin-bottom: 10px;'>💡 Đánh giá & Khuyến nghị tối ưu hóa từ AI</h5>", unsafe_allow_html=True)
        
        # Build smart feedback rules
        feedback = []
        
        # Rule 1: Price / Value ratio
        if price > 150 and duration_hours < 10:
            feedback.append("""
            <div style="background-color: #fffbeb; border-left: 4px solid #d97706; padding: 12px 18px; border-radius: 6px; margin-bottom: 10px;">
                <span style="color: #b45309; font-weight: 700;">⚠️ Giá bán tương đối cao so với thời lượng:</span><br>
                <span style="color: #78350f; font-size: 0.9rem;">Khóa học của bạn có thời lượng tương đối ngắn (dưới 10 giờ) nhưng giá bán dự kiến khá cao. Giảng viên nên cân nhắc hạ giá bán xuống dưới $80 hoặc bổ sung thêm tài liệu bài học để tăng tính cạnh tranh.</span>
            </div>
            """)
        elif price <= 30 and duration_hours >= 30:
            feedback.append("""
            <div style="background-color: #ecfdf5; border-left: 4px solid #10b981; padding: 12px 18px; border-radius: 6px; margin-bottom: 10px;">
                <span style="color: #047857; font-weight: 700;">💎 Tỷ lệ Giá trị / Chi phí cực tốt:</span><br>
                <span style="color: #065f46; font-size: 0.9rem;">Thời lượng lớn trên 30 giờ với mức giá hấp dẫn dưới $30 sẽ tạo hiệu ứng thu hút học viên cực mạnh. Khóa học có tiềm năng bùng nổ đăng ký rất cao!</span>
            </div>
            """)
            
        # Rule 2: Optimal lecture count
        if num_lectures < 20:
            feedback.append("""
            <div style="background-color: #fffbeb; border-left: 4px solid #d97706; padding: 12px 18px; border-radius: 6px; margin-bottom: 10px;">
                <span style="color: #b45309; font-weight: 700;">⚠️ Số lượng bài giảng hơi ít:</span><br>
                <span style="color: #78350f; font-size: 0.9rem;">Khóa học dưới 20 bài giảng có thể khiến học viên cảm thấy nội dung chưa đủ sâu. Hãy cân nhắc chia nhỏ nội dung thành nhiều bài học ngắn hơn để tăng trải nghiệm học tập tốt hơn.</span>
            </div>
            """)
        elif 20 <= num_lectures <= 60:
            feedback.append("""
            <div style="background-color: #ecfdf5; border-left: 4px solid #10b981; padding: 12px 18px; border-radius: 6px; margin-bottom: 10px;">
                <span style="color: #047857; font-weight: 700;">🎯 Số lượng bài giảng tối ưu:</span><br>
                <span style="color: #065f46; font-size: 0.9rem;">Số bài giảng nằm trong khoảng 'vàng' (20-60 bài). Cấu trúc này giúp học viên dễ tiếp thu, không bị ngợp và duy trì tỷ lệ hoàn thành ở mức tối đa.</span>
            </div>
            """)
        else:
            feedback.append("""
            <div style="background-color: #eff6ff; border-left: 4px solid #3b82f6; padding: 12px 18px; border-radius: 6px; margin-bottom: 10px;">
                <span style="color: #1d4ed8; font-weight: 700;">ℹ️ Số lượng bài giảng đồ sộ:</span><br>
                <span style="color: #1e3a8a; font-size: 0.9rem;">Khóa học có lượng bài giảng lớn (trên 60 bài). Giảng viên nên chia khóa học thành các chương rõ ràng và cung cấp lộ trình cụ thể để tránh học viên bị nản giữa chừng.</span>
            </div>
            """)
            
        # Rule 3: Free vs Paid positioning
        if price == 0:
            feedback.append("""
            <div style="background-color: #eff6ff; border-left: 4px solid #3b82f6; padding: 12px 18px; border-radius: 6px; margin-bottom: 10px;">
                <span style="color: #1d4ed8; font-weight: 700;">💡 Chiến lược phễu thu hút học viên:</span><br>
                <span style="color: #1e3a8a; font-size: 0.9rem;">Đặt giá miễn phí là phương pháp tốt nhất để xây dựng danh tiếng và thu thập đánh giá 5 sao nhanh nhất. Bạn có thể sử dụng khóa học này làm phễu để chuyển đổi sang các khóa học trả phí khác.</span>
            </div>
            """)
        else:
            pct_higher_subs = (pred_subs - avg_subs) / avg_subs * 100 if avg_subs > 0 else 0
            if pct_higher_subs > 0:
                feedback.append(f"""
                <div style="background-color: #ecfdf5; border-left: 4px solid #10b981; padding: 12px 18px; border-radius: 6px; margin-bottom: 10px;">
                    <span style="color: #047857; font-weight: 700;">🚀 Ưu thế thị trường vượt trội:</span><br>
                    <span style="color: #065f46; font-size: 0.9rem;">Nhờ cấu trúc nội dung hợp lý, khóa học dự đoán sẽ thu hút học viên <b>cao hơn {pct_higher_subs:.1f}%</b> so với mặt bằng trung bình của chủ đề {subject}. Hãy giữ nguyên cấu hình này!</span>
                </div>
                """)
            else:
                feedback.append(f"""
                <div style="background-color: #fff1f2; border-left: 4px solid #f43f5e; padding: 12px 18px; border-radius: 6px; margin-bottom: 10px;">
                    <span style="color: #be123c; font-weight: 700;">📉 Sức cạnh tranh thấp hơn trung bình:</span><br>
                    <span style="color: #881337; font-size: 0.9rem;">Khóa học dự báo thu hút học viên thấp hơn trung bình chủ đề {subject}. Hãy thử kéo tăng nhẹ thời lượng học hoặc giảm giá dự kiến xuống 10-20$ để kiểm chứng hiệu năng bứt phá trên biểu đồ.</span>
                </div>
                """)
                
        # Print all recommendations
        for item in feedback:
            st.markdown(item, unsafe_allow_html=True)

    # 7. TIME-SERIES FORECASTING SECTION
    st.markdown("---")
    
    # Filter historical time-series data based on selections in Part 1 (subject & level)
    df_ts_init = df[(df['subject'] == subject) & (df['level'] == level)].copy()
    title_context = f"{subject} ({level})"
    
    # 1st Fallback: if too small, filter by subject only
    df_ts_init['ds'] = pd.to_datetime(df_ts_init['published_timestamp'])
    df_ts_init['year_month'] = df_ts_init['ds'].dt.to_period('M')
    
    if len(df_ts_init.groupby('year_month')) < 10:
        df_ts_init = df[df['subject'] == subject].copy()
        df_ts_init['ds'] = pd.to_datetime(df_ts_init['published_timestamp'])
        df_ts_init['year_month'] = df_ts_init['ds'].dt.to_period('M')
        title_context = f"{subject} (Tất cả trình độ)"
        
    # 2nd Fallback: if still too small, use entire dataset
    if len(df_ts_init.groupby('year_month')) < 10:
        df_ts_init = df.copy()
        df_ts_init['ds'] = pd.to_datetime(df_ts_init['published_timestamp'])
        df_ts_init['year_month'] = df_ts_init['ds'].dt.to_period('M')
        title_context = "Toàn bộ Udemy"

    st.markdown(f"<h3 style='color: #1e1b4b;'>📈 Dự báo xu hướng tăng trưởng phân khúc: {title_context}</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 1rem; margin-top: -10px;'>Phân tích và dự phóng chuỗi thời gian dựa trên Xu hướng tăng trưởng tuyến tính và Biến động mùa vụ (Trend + Seasonality).</p>", unsafe_allow_html=True)
    
    col_ts_controls, col_ts_blank = st.columns([2, 2])
    with col_ts_controls:
        ts_target = st.radio("Chọn chỉ số dự báo", ["Doanh thu ($)", "Lượng học viên đăng ký mới"], horizontal=True)
        ts_months = st.selectbox("Thời gian dự phóng", ["12 tháng tiếp theo", "24 tháng tiếp theo"], index=1)
        forecast_horizon = 12 if ts_months == "12 tháng tiếp theo" else 24

    # Target column mapping
    target_col = 'sales' if ts_target == "Doanh thu ($)" else 'num_subscribers'
    
    # Monthly groupby for filtered data
    monthly_data = df_ts_init.groupby('year_month').agg({target_col: 'sum'}).reset_index()
    monthly_data['ds'] = monthly_data['year_month'].dt.to_timestamp()
    monthly_data = monthly_data.sort_values('ds').reset_index(drop=True)
    
    # We only take historical data from 2018 onwards to get a cleaner, modern trend
    monthly_data = monthly_data[monthly_data['ds'].dt.year >= 2018].reset_index(drop=True)
    
    if len(monthly_data) > 6:
        # Build features for linear regression: Trend (t) + Month seasonality
        monthly_data['t'] = np.arange(len(monthly_data))
        monthly_data['month_num'] = monthly_data['ds'].dt.month
        
        # One-hot encoding of months for seasonality
        month_dummies = pd.get_dummies(monthly_data['month_num'], prefix='month', drop_first=False)
        # Ensure all 12 months columns are present in features
        for m in range(1, 13):
            col_name = f'month_{m}'
            if col_name not in month_dummies.columns:
                month_dummies[col_name] = 0
        
        X_hist = month_dummies.copy()
        X_hist['t'] = monthly_data['t']
        y_hist = monthly_data[target_col]
        
        from sklearn.linear_model import LinearRegression
        model_ts = LinearRegression()
        model_ts.fit(X_hist, y_hist)
        
        # Make predictions for historical data
        monthly_data['fitted'] = model_ts.predict(X_hist)
        
        # Generate Future Dataframe
        last_ds = monthly_data['ds'].iloc[-1]
        last_t = monthly_data['t'].iloc[-1]
        
        future_dates = [last_ds + pd.DateOffset(months=i) for i in range(1, forecast_horizon + 1)]
        future_df = pd.DataFrame({'ds': future_dates})
        future_df['t'] = last_t + np.arange(1, forecast_horizon + 1)
        future_df['month_num'] = future_df['ds'].dt.month
        
        future_dummies = pd.get_dummies(future_df['month_num'], prefix='month', drop_first=False)
        for m in range(1, 13):
            col_name = f'month_{m}'
            if col_name not in future_dummies.columns:
                future_dummies[col_name] = 0
                
        # Reorder columns to match historical dummies order
        future_dummies = future_dummies[month_dummies.columns]
        
        X_fut = future_dummies.copy()
        X_fut['t'] = future_df['t']
        
        future_df['forecast'] = model_ts.predict(X_fut)
        # Force non-negative
        future_df['forecast'] = future_df['forecast'].clip(lower=0)
        
        # Plotly visual representation
        col_ts_chart, col_ts_insights = st.columns([3, 2], gap="large")
        
        with col_ts_chart:
            fig_ts = go.Figure()
            
            # Historical line
            fig_ts.add_trace(go.Scatter(
                x=monthly_data['ds'], y=monthly_data[target_col],
                name="Thực tế (Lịch sử)",
                mode="lines",
                line=dict(color="#6366f1", width=2.5),
                fill='tozeroy',
                fillcolor='rgba(99,102,241,0.04)'
            ))
            
            # Future Forecast line (dashed)
            # Combine last point of historical to avoid visual gap
            conn_ds = [monthly_data['ds'].iloc[-1]] + list(future_df['ds'])
            conn_y = [monthly_data[target_col].iloc[-1]] + list(future_df['forecast'])
            
            fig_ts.add_trace(go.Scatter(
                x=conn_ds, y=conn_y,
                name="Dự báo tương lai",
                mode="lines",
                line=dict(color="#ec4899", width=2.5, dash='dash')
            ))
            
            fig_ts.update_layout(
                height=320,
                margin=dict(t=15, b=10, l=10, r=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#f1f5f9', tickformat=',.0f')
            )
            st.plotly_chart(fig_ts, use_container_width=True)
            
        with col_ts_insights:
            # Let's compute which level is growing fastest within this specific context
            level_ts = []
            sub_only_df = df_ts_init[df_ts_init['ds'].dt.year >= 2018]
            for lvl in sub_only_df['level'].unique():
                lvl_df = sub_only_df[sub_only_df['level'] == lvl]
                lvl_monthly = lvl_df.groupby('year_month').agg({'num_subscribers': 'sum'}).reset_index()
                if len(lvl_monthly) > 5:
                    lvl_monthly['t'] = np.arange(len(lvl_monthly))
                    lm = LinearRegression()
                    lm.fit(lvl_monthly[['t']], lvl_monthly['num_subscribers'])
                    slope = lm.coef_[0]
                    level_ts.append({'level': lvl, 'slope': slope})
            
            level_growth = pd.DataFrame(level_ts).sort_values('slope', ascending=False).reset_index(drop=True)
            fastest_lvl = level_growth.loc[0, 'level'] if len(level_growth) > 0 else "All Levels"
            
            # Forecasted total for next year
            next_year_total = future_df['forecast'].head(12).sum()
            
            unit = "$" if ts_target == "Doanh thu ($)" else "học viên"
            prefix = "$" if ts_target == "Doanh thu ($)" else ""
            
            st.markdown(f"""
                <div style="background-color: #fafaf9; padding: 22px; border-radius: 12px; border: 1.5px solid #e7e5e4; margin-top: 15px;">
                    <h5 style="color: #292524; font-weight: 700; margin-bottom: 12px;">📊 Nhận định xu hướng {subject}</h5>
                    <div style="font-size: 0.95rem; color: #44403c; margin-bottom: 15px; line-height: 1.5;">
                        🚀 <b>Tổng {ts_target} dự báo (12 tháng tới):</b><br>
                        Đạt khoảng <span style="color: #db2777; font-weight: 700; font-size: 1.15rem;">{prefix}{next_year_total:,.0f} {unit}</span>.
                    </div>
                    <div style="font-size: 0.95rem; color: #44403c; margin-bottom: 15px; line-height: 1.5;">
                        🔥 <b>Trình độ tăng trưởng nhanh nhất (Dự báo):</b><br>
                        Khóa học ở trình độ <span style="color: #6366f1; font-weight: 700; font-size: 1.05rem;">{fastest_lvl}</span> đang có tốc độ thu hút học viên phát triển mạnh mẽ nhất trong phân khúc này.
                    </div>
                    <div style="font-size: 0.88rem; color: #78716c; line-height: 1.4; border-top: 1px dashed #d6d3d1; padding-top: 12px;">
                        💡 <b>Lời khuyên chiến lược:</b><br>
                        Nếu bạn xuất bản khóa học mới về <b>{subject}</b>, hãy thiết kế nội dung hướng đến đối tượng <b>{fastest_lvl}</b> để tối ưu hóa khả năng thu hút học viên mới đăng ký.
                    </div>
                </div>
            """, unsafe_allow_html=True)