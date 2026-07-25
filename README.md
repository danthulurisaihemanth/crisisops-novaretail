# NovaRetail CrisisOps AI

NovaRetail CrisisOps AI is an enterprise-grade supply-chain operations assistant built with Streamlit, LangChain, LangGraph, and a synthetic enterprise dataset. It supports shipment tracking, inventory review, supplier lookup, incident creation, recovery planning, and digital-twin simulation.

## Features
- Conversational operations assistant
- Multi-agent routing for shipment, inventory, supplier, recovery, and reporting tasks
- Human-in-the-loop confirmation for risky actions
- Synthetic enterprise-grade datasets for suppliers, warehouses, inventory, shipments, orders, incidents, routes, partners, and recovery plans
- Digital twin scenarios for rerouting, supplier replacement, inventory redistribution, transportation cost comparison, delivery prediction, and business impact analysis

## Run locally
1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and set your environment values.
4. Generate datasets: `python data/generate_datasets.py`
5. Start the app: `streamlit run frontend/app.py`

## Architecture
- Frontend: Streamlit
- Backend: Python services and data store
- Agents: LangGraph-inspired workflow with supervisor and specialist agents
- Tools: shipment, inventory, supplier, incident, and digital-twin tools
- Observability: LangSmith-compatible tracing hooks
