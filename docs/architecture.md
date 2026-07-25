# Architecture Overview

NovaRetail CrisisOps AI uses a layered architecture:
- Streamlit UI for conversation and dashboarding.
- Backend data store for synthetic enterprise data.
- Tool layer for shipment, inventory, supplier, incident, and digital twin operations.
- LangGraph-inspired agent graph for routing.
- Human-loop confirmation for risky actions.
- Tracing hooks for LangSmith-style observability.
