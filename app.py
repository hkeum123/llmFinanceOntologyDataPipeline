import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# 1. 페이지 설정 (Wide Mode & Title)
st.set_page_config(
    page_title="Market Sentinel",
    layout="wide",
    page_icon="📈",
    initial_sidebar_state="expanded"
)

# 2. Toss Style CSS 주입 (핵심!)
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 설정 */
    .stApp {
        background-color: #FFFFFF;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* 사이드바 스타일 */
    section[data-testid="stSidebar"] {
        background-color: #F9FAFB;
        border-right: 1px solid #E5E8EB;
    }
    
    /* 제목 스타일 */
    h1 {
        color: #191F28;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    h2, h3 {
        color: #333D4B;
        font-weight: 600;
    }
    
    /* Toss 스타일 카드 (KPI Metric) */
    .toss-card {
        background-color: #F2F4F6;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 10px;
        transition: transform 0.2s;
    }
    .toss-card:hover {
        transform: translateY(-2px);
    }
    .metric-label {
        color: #8B95A1;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 4px;
    }
    .metric-value {
        color: #191F28;
        font-size: 1.6rem;
        font-weight: 700;
    }
    .metric-delta-up {
        color: #F04452; /* Toss Red for Rising/Risk */
        font-size: 0.9rem;
        font-weight: 600;
    }
    .metric-delta-down {
        color: #3182F6; /* Toss Blue for Safe/Down */
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    /* 데이터프레임 스타일 */
    .stDataFrame {
        border: 1px solid #E5E8EB;
        border-radius: 12px;
    }
    
    /* 인사이트 박스 */
    .insight-box {
        background-color: #E8F3FF; /* 연한 블루 */
        border-radius: 16px;
        padding: 20px;
        color: #1B64DA;
        font-weight: 500;
        border: 1px solid #3182F6;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 모의 생성
def get_ontology_data(ticker):
    data = {
        "source": ["TSLA", "TSLA", "TSLA", "TSLA", "TSLA", "Rivian", "Lucid", "NVIDIA", "Panasonic"],
        "target": ["Rivian", "Lucid", "Supply Chain", "AI Regulation", "NVIDIA", "Supply Chain", "Supply Chain", "TSLA", "TSLA"],
        "relation": ["Competitor", "Competitor", "Risk", "Risk", "Supplier", "Risk_Exposure", "Risk_Exposure", "Supplier", "Supplier"],
        "type": ["Company", "Company", "Risk", "Risk", "Company", "Risk", "Risk", "Company", "Company"]
    }
    return pd.DataFrame(data)

# 4. PyVis 그래프 생성 (Toss Color 적용)
def draw_knowledge_graph(df, main_ticker):
    # 배경을 흰색으로, 폰트는 검정으로 변경
    net = Network(height="550px", width="100%", bgcolor="#FFFFFF", font_color="#191F28", notebook=False)
    net.force_atlas_2based(gravity=-50, central_gravity=0.01, spring_length=100, spring_strength=0.08)
    
    sources = df['source']
    targets = df['target']
    relations = df['relation']
    
    edge_data = zip(sources, targets, relations)
    
    for src, dst, rel in edge_data:
        # --- Toss Color Logic ---
        # Main Ticker: Toss Blue (#3182F6)
        # Risk: Toss Red (#F04452)
        # Competitor/Others: Grey (#8B95A1) or Dark Grey (#333D4B)
        
        if src == main_ticker:
            src_color = "#3182F6" 
            src_size = 45
            src_label = src
        else:
            src_color = "#8B95A1"
            src_size = 20
            src_label = src

        if dst in ["Supply Chain", "AI Regulation"]: # Risk Factors
            dst_color = "#F04452" # Risk Red
            dst_shape = "dot"
            dst_size = 30
        elif rel == "Competitor":
            dst_color = "#333D4B" # Dark Grey
            dst_shape = "dot"
            dst_size = 25
        else:
            dst_color = "#B0B8C1" # Light Grey
            dst_shape = "dot"
            dst_size = 20

        net.add_node(src, label=src_label, title=src, color=src_color, size=src_size, borderWidth=0)
        net.add_node(dst, label=dst, title=dst, color=dst_color, size=dst_size, borderWidth=0)
        
        # 엣지 색상은 연한 회색
        net.add_edge(src, dst, title=rel, color="#E5E8EB", width=2)

    net.save_graph("toss_graph.html")
    return "toss_graph.html"

# --- 메인 UI 구성 ---

# 사이드바
with st.sidebar:
    st.title("Market Sentinel")
    st.markdown("### AI Financial Ontology")
    
    st.markdown("<br>", unsafe_allow_html=True)
    selected_ticker = st.selectbox("분석할 종목을 선택하세요", ["TSLA", "AAPL", "NVDA"], index=0)
    
    st.markdown("---")
    st.caption("Pipeline Status")
    st.markdown("✅ **SEC 10-K** 수집 완료")
    st.markdown("✅ **LLM (GPT-4o)** 분석 완료")
    st.markdown("✅ **DB (PostgreSQL)** 적재 완료")
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.caption("Powered by Data Engineering Team")

# 메인 헤더
st.title(f"{selected_ticker} 분석 리포트")
st.markdown(f"**{selected_ticker}**의 공시 데이터와 시장 관계를 분석했습니다.")
st.markdown("<br>", unsafe_allow_html=True)

# Toss Style KPI Cards (HTML 커스텀)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="toss-card">
        <div class="metric-label">Buffett Score</div>
        <div class="metric-value">8.5<span style="font-size:1rem; color:#8B95A1;">/10</span></div>
        <div class="metric-delta-up">Excellent</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="toss-card">
        <div class="metric-label">Risk Factors</div>
        <div class="metric-value">2<span style="font-size:1rem; color:#8B95A1;">건</span></div>
        <div class="metric-delta-up">High Severity</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="toss-card">
        <div class="metric-label">Competitors</div>
        <div class="metric-value">5<span style="font-size:1rem; color:#8B95A1;">개사</span></div>
        <div class="metric-delta-down">식별됨</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="toss-card">
        <div class="metric-label">NPS Holding</div>
        <div class="metric-value">1.2M</div>
        <div class="metric-delta-up">▲ 2.5%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 그래프 및 인사이트 영역
col_graph, col_insight = st.columns([2, 1])

with col_graph:
    st.subheader("지식 그래프 (Knowledge Graph)")
    st.caption("기업과 리스크 간의 연결 관계를 시각화했습니다.")
    
    # 그래프 생성 및 로드
    df_ontology = get_ontology_data(selected_ticker)
    graph_html_path = draw_knowledge_graph(df_ontology, selected_ticker)
    
    with open(graph_html_path, 'r', encoding='utf-8') as f:
        html_string = f.read()
        # Toss 스타일의 둥근 테두리 적용
        components.html(html_string, height=500, scrolling=False)

with col_insight:
    st.subheader("AI 핵심 요약")
    st.caption("10-K 공시 기반 LLM 분석 결과입니다.")
    
    st.markdown("""
    <div class="insight-box">
        <span style="font-size: 1.2rem;">💡 Supply Chain Risk</span><br><br>
        LLM 분석 결과, <b>배터리 원자재 공급망</b> 이슈가 감지되었습니다.<br>
        이는 경쟁사인 <b>Rivian</b>과 <b>Lucid</b>에도 공통적으로 영향을 미치는 시스템 리스크입니다.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 리스크 목록 (심플한 리스트 스타일)
    st.markdown("**상세 리스크 요인**")
    st.markdown("""
    - 🔴 **AI Regulation** (High): 자율주행 규제 강화 가능성
    - 🟠 **Interest Rate** (Med): 고금리로 인한 할부 수요 감소
    """)

# 하단 데이터 테이블
st.markdown("---")
st.subheader("구조화된 데이터 (Structured Data)")
st.caption("DB(Gold Layer)에 적재된 실제 데이터입니다.")
st.dataframe(df_ontology, use_container_width=True, hide_index=True)