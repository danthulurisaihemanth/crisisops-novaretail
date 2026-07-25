import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from config.settings import settings

from backend.agent_orchestrator import CrisisOpsAgent
from backend.data_store import DataStore
from backend.memory import ConversationMemory

st.set_page_config(page_title="NovaRetail CrisisOps AI", page_icon="📦", layout="wide")
st.markdown("<style>body{background:#0f172a;color:#f8fafc;} .stTextInput>div>div>input{background:#111827;color:white;} .stSidebar{background:#111827;} .stAlert{background:#1f2937;}</style>", unsafe_allow_html=True)


def main() -> None:
    data_store = DataStore("data")
    memory = ConversationMemory()
    agent = CrisisOpsAgent(data_store, memory)

    if not getattr(settings, "gemini_api_key", "") and not getattr(settings, "openai_api_key", ""):
        st.warning("No LLM key is configured. The assistant is running in fallback mode with basic guidance only. Add GEMINI_API_KEY or OPENAI_API_KEY in Streamlit secrets for full AI responses.")

    if "session_id" not in st.session_state:
        st.session_state.session_id = "session-1"

    st.title("NovaRetail CrisisOps AI")
    st.caption("A multi-agent supply chain operations assistant for disruption management and digital-twin planning")

    with st.sidebar:
        st.header("Operations Overview")
        suppliers = len(data_store.suppliers())
        warehouses = len(data_store.warehouses())
        shipments = len(data_store.shipments())
        orders = len(data_store.orders())
        incidents = len(data_store.incidents())
        st.metric("Active Suppliers", suppliers)
        st.metric("Warehouses", warehouses)
        st.metric("Shipments", shipments)
        st.metric("Orders", orders)
        st.metric("Incidents", incidents)
        st.button("Reset Chat", on_click=lambda: memory.clear(st.session_state.session_id))

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Conversation")
        if "messages" not in st.session_state:
            st.session_state.messages = []
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        prompt = st.chat_input("Ask about shipments, inventory, suppliers, incidents, or recovery options")
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.spinner("Agent is reasoning..."):
                result = agent.handle_message(st.session_state.session_id, prompt)
            response = result.get("response", "")
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    with col2:
        st.subheader("Operational Snapshot")
        st.info("The agent can route requests to specialized workflows and ask for confirmation before taking risky actions.")
        if data_store.shipments():
            shipment_statuses = {}
            for shipment in data_store.shipments()[:10]:
                shipment_statuses[shipment["id"]] = shipment.get("delay_hours", 0)
            st.write("Recent shipment delays")
            st.json(shipment_statuses)


if __name__ == "__main__":
    main()
