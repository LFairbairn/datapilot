# DataPilot TODO

## Project Setup
- [x] Create `pyproject.toml` with UV config and Taskipy shortcuts
- [x] Create sample data CSV in `data/` folder

## Docker
- [x] Create `docker-compose.yml` with ollama, mcp_server, and streamlit services
- [x] Create `mcp_server/Dockerfile`
- [x] Create `streamlit_app/Dockerfile`
- [ ] Run MCP server and Streamlit via Docker instead of locally

## MCP Server
- [x] Create `mcp_server/src/server.py` — MCP server entry point
- [x] Create `mcp_server/src/tools/csv_tools.py` — `load_csv` and `query_data` tools
- [ ] Create `mcp_server/src/tools/chart_tools.py` — `make_chart` tool (later phase)

## Streamlit UI
- [x] Create `streamlit_app/src/app.py` — Streamlit UI
- [ ] Add welcome message to Streamlit UI prompting user to upload a CSV 

## Tests & CI
- [ ] Create `tests/test_csv_tools.py`
- [ ] Create `tests/test_chart_tools.py`
- [ ] Create `.github/workflows/ci.yml` — GitHub Actions CI

## README
- [ ] Write How to Run section once project is working end-to-end

