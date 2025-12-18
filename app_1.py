import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 1. 페이지 설정
st.set_page_config(page_title="Market Sentinel", layout="wide")

# 2. 사이드바 (파이프라인 상태)
with st.sidebar:
    st.title("⚙️ Control Panel")
    ticker = st.selectbox("Select Company", ["TSLA", "AAPL", "NVDA", "MSFT"])
    st.markdown("---")
    st.subheader("Pipeline Status")
    st.success("🟢 Data Collection (SEC)")
    st.success("🟢 LLM Processing (GPT-4o)")
    st.success("🟢 DB Injection (PostgreSQL)")
    st.info(f"Last Update: 2025-12-17")

# 3. 메인 헤더
st.title(f"📊 Market Sentinel: {ticker} Ontology Analysis")
st.markdown("LLM-driven Financial Knowledge Graph & Risk Assessment")

# 4. 핵심 지표 (KPI)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Current Price", "$245.30", "+1.2%")
col2.metric("Buffett Score", "8/10", "Strong")
col3.metric("ROE", "28.5%", "Excellent")
col4.metric("NPS Holding", "1.2M Shares", "▲ 2.5%")

# 5. 지식 그래프 (Ontology)
st.subheader("🕸️ Corporate Knowledge Graph")
col_graph, col_risk = st.columns([2, 1])

with col_graph:
    # (실제로는 PyVis 등을 써야 예쁘지만, 여기선 간단히 matplotlib 예시)
    G = nx.Graph()
    G.add_edge(ticker, "Rivian (Competitor)")
    G.add_edge(ticker, "Supply Chain (Risk)")
    G.add_edge(ticker, "AI Regulation (Risk)")
    G.add_edge("NVIDIA", "Supply Chain (Risk)")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=10)
    st.pyplot(fig)

with col_risk:
    st.subheader("🚨 Critical Risks (LLM Extracted)")
    # DB에서 가져온 데이터라고 가정
    risks = [
        {"title": "Supply Chain", "level": "HIGH", "desc": "Battery raw material shortage..."},
        {"title": "Regulatory", "level": "MED", "desc": "NHTSA investigation on FSD..."}
    ]
    for r in risks:
        with st.expander(f"{'🔴' if r['level']=='HIGH' else '🟡'} {r['title']}"):
            st.write(r['desc'])
            st.caption(f"Severity: {r['level']}")

# 6. 데이터 테이블 (DB 증명)
st.markdown("---")
st.subheader("💾 Structured Data (Gold Layer)")
df = pd.DataFrame({
    "entity_type": ["Competitor", "Risk", "Risk"],
    "entity_name": ["Rivian", "Supply Chain", "AI Regulation"],
    "confidence_score": [0.95, 0.88, 0.92],
    "source_doc": ["10-K Item 1", "10-K Item 1A", "10-K Item 1A"]
})
st.dataframe(df, use_container_width=True)