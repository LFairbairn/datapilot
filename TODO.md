# DataPilot TODO

## Project Setup
- [x] Create `pyproject.toml` with UV config and Taskipy shortcuts
- [x] Create sample data CSV in `data/` folder

## Docker
- [x] Create `docker-compose.yml` with ollama, mcp_server, and streamlit services
- [x] Create `mcp_server/Dockerfile`
- [x] Create `streamlit_app/Dockerfile`
- [x] Run MCP server and Streamlit via Docker instead of locally

## MCP Server
- [x] Create `mcp_server/src/server.py` — MCP server entry point
- [x] Create `mcp_server/src/tools/csv_tools.py` — `load_csv` and `query_data` tools

## Streamlit UI
- [x] Create `streamlit_app/src/app.py` — Streamlit UI
- [x] Add welcome message to Streamlit UI prompting user to upload a CSV

## Tests & CI
- [x] Create `tests/test_csv_tools.py`
- [x] Create `.github/workflows/ci.yml` — GitHub Actions CI

## README
- [x] Write How to Run section once project is working end-to-end

