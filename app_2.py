import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# 1. 페이지 설정 (Wide Mode)
st.set_page_config(page_title="Market Sentinel Pro", layout="wide", page_icon="🕸️")

# 2. 스타일링 (CSS)
st.markdown("""
    <style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 모의 생성 (DB에서 가져왔다고 가정)
# 실제로는 PostgreSQL에서 쿼리한 결과를 DataFrame으로 변환하면 됩니다.
def get_ontology_data(ticker):
    # 예시 데이터: 테슬라(TSLA) 중심의 온톨로지
    data = {
        "source": ["TSLA", "TSLA", "TSLA", "TSLA", "TSLA", "Rivian", "Lucid", "NVIDIA", "Panasonic"],
        "target": ["Rivian", "Lucid", "Supply Chain", "AI Regulation", "NVIDIA", "Supply Chain", "Supply Chain", "TSLA", "TSLA"],
        "relation": ["Competitor", "Competitor", "Risk", "Risk", "Supplier", "Risk_Exposure", "Risk_Exposure", "Supplier", "Supplier"],
        "type": ["Company", "Company", "Risk", "Risk", "Company", "Risk", "Risk", "Company", "Company"]
    }
    return pd.DataFrame(data)

# 4. PyVis 그래프 생성 함수
def draw_knowledge_graph(df, main_ticker):
    # PyVis 네트워크 초기화 (Dark Theme)
    net = Network(height="600px", width="100%", bgcolor="#1E1E1E", font_color="white", notebook=False)
    
    # 물리 엔진 설정 (부드러운 움직임)
    net.force_atlas_2based()
    
    sources = df['source']
    targets = df['target']
    relations = df['relation']
    
    edge_data = zip(sources, targets, relations)
    
    for src, dst, rel in edge_data:
        # --- 노드 스타일링 로직 (Ontology의 핵심) ---
        
        # 1. Source Node 스타일
        src_color = "#00C853" if src == main_ticker else "#2979FF" # 메인은 초록, 나머진 파랑
        src_size = 40 if src == main_ticker else 20
        src_shape = "star" if src == main_ticker else "dot"
        
        # 2. Target Node 스타일 (타입에 따라 색상 변경)
        if dst in ["Supply Chain", "AI Regulation", "Interest Rate"]: # 리스크 요인
            dst_color = "#FF5252" # 빨강 (위험)
            dst_shape = "triangle"
            dst_size = 25
        elif rel == "Competitor":
            dst_color = "#FF9100" # 주황 (경쟁)
            dst_shape = "dot"
            dst_size = 20
        else:
            dst_color = "#2979FF" # 파랑 (일반)
            dst_shape = "dot"
            dst_size = 20

        # 노드 추가
        net.add_node(src, label=src, title=f"{src} (Source)", color=src_color, size=src_size, shape=src_shape)
        net.add_node(dst, label=dst, title=f"{dst} (Target)", color=dst_color, size=dst_size, shape=dst_shape)
        
        # 엣지(관계) 추가
        net.add_edge(src, dst, title=rel, label=rel, color="#9E9E9E")

    # HTML로 저장 후 읽어오기
    net.save_graph("pyvis_graph.html")
    return "pyvis_graph.html"

# --- 메인 UI 구성 ---

# 사이드바
with st.sidebar:
    st.title("🚀 Market Sentinel")
    st.caption("LLM-driven Financial Ontology")
    
    selected_ticker = st.selectbox("Select Ticker", ["TSLA", "AAPL", "NVDA"])
    
    st.markdown("---")
    st.subheader("Pipeline Status")
    st.success("✅ SEC 10-K Parsed")
    st.success("✅ Entity Extracted (GPT-4o)")
    st.success("✅ Graph Built")

# 메인 헤더
st.title(f"🕸️ {selected_ticker} Knowledge Graph Explorer")
st.markdown(f"**{selected_ticker}**의 공시 데이터를 분석하여 추출한 **기업-리스크-경쟁사** 관계도입니다.")

# 상단 지표 (KPI)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Risk Factors", "2 Critical", "High Severity")
col2.metric("Competitors", "5 Identified", "+1 New")
col3.metric("Suppliers", "3 Key Partners", "Stable")
col4.metric("Sentiment", "Neutral", "-0.5 Score")

# 그래프 영역
st.subheader("Interactive Ontology View")
st.caption("💡 노드를 드래그하거나 휠로 확대/축소해보세요. 마우스를 올리면 상세 정보가 뜹니다.")

# 데이터 로드 및 그래프 생성
df_ontology = get_ontology_data(selected_ticker)
graph_html_path = draw_knowledge_graph(df_ontology, selected_ticker)

# Streamlit에 HTML 임베딩 (핵심!)
with open(graph_html_path, 'r', encoding='utf-8') as f:
    html_string = f.read()
    components.html(html_string, height=610, scrolling=False)

# 하단: 구조화된 데이터 테이블 (DB 증명용)
st.markdown("---")
col_table, col_detail = st.columns([2, 1])

with col_table:
    st.subheader("💾 Structured Data (Gold Layer)")
    st.dataframe(df_ontology, use_container_width=True)

with col_detail:
    st.subheader("🤖 LLM Insight")
    st.info(f"""
    **[Supply Chain Risk]**
    
    LLM 분석 결과, **{selected_ticker}**는 배터리 원자재 공급망 이슈에 노출되어 있습니다. 
    이는 경쟁사인 **Rivian**과 **Lucid**에도 공통적으로 영향을 미치는 **Systemic Risk**로 식별됩니다.
    """)