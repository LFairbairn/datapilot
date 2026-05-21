import asyncio
import json
import os

import httpx
import streamlit as st
from mcp import ClientSession
from mcp.client.sse import sse_client

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/sse")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = "llama3.1"
DATA_DIR = os.getenv("DATA_DIR", "data")


# --- MCP helpers ---


async def get_mcp_tools() -> list[dict]:
    """Fetch available tools from the MCP server and convert to Ollama format."""
    async with sse_client(MCP_SERVER_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.list_tools()
            return [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.inputSchema,
                    },
                }
                for t in result.tools
            ]


async def call_mcp_tool(name: str, arguments: dict) -> str:
    """Call a single MCP tool and return its text output."""
    async with sse_client(MCP_SERVER_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(name, arguments)
            return result.content[0].text


# --- Ollama helpers ---


async def run_conversation(messages: list[dict], tools: list[dict]) -> list[dict]:
    """
    Send messages to Ollama and handle tool calls in a loop until
    Ollama returns a plain text response with no further tool calls.
    """
    async with httpx.AsyncClient(timeout=120) as client:
        while True:
            response = await client.post(
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": MODEL,
                    "messages": messages,
                    "tools": tools,
                    "stream": False,
                },
            )
            response.raise_for_status()
            assistant_message = response.json()["message"]
            messages.append(assistant_message)

            if not assistant_message.get("tool_calls"):
                break

            for tool_call in assistant_message["tool_calls"]:
                fn = tool_call["function"]
                tool_result = await call_mcp_tool(fn["name"], fn["arguments"])
                messages.append({"role": "tool", "content": tool_result})

    return messages


# --- Streamlit UI ---


def main():
    st.title("DataPilot")
    st.caption("Upload a CSV and ask questions about your data")

    # File upload
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    if uploaded_file:
        os.makedirs(DATA_DIR, exist_ok=True)
        save_path = os.path.join(DATA_DIR, uploaded_file.name)

        if st.session_state.get("csv_path") != save_path:
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            result = asyncio.run(call_mcp_tool("load_csv", {"file_path": save_path}))
            st.session_state.csv_path = save_path
            st.session_state.messages = [
                {
                    "role": "system",
                    "content": "You are a data analyst providing insights into data in a friendly and professional way. "
                    "Your goal is to answer users questions about contents of a csv file, "
                    "summerise results concisely rather than listing every row and do not return raw JSON, use plain english. "
                    "If you do not know the answer, or the answer is not present in the data, "
                    "state 'I am not sure' rather than making up information. "
                    "Do not discuss any other topic other than what is contained within the csv file.",
                }
            ]
            st.success(result)
            st.session_state.messages.append({"role": "system", "content": result})

    if not st.session_state.get("csv_path"):
        st.info("Upload a CSV file above to get started.")
        return

    for msg in st.session_state.messages:
        if msg["role"] in ("user", "assistant"):
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    if prompt := st.chat_input("Ask a question about your data..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Thinking..."):
            tools = asyncio.run(get_mcp_tools())
            updated = asyncio.run(
                run_conversation(list(st.session_state.messages), tools)
            )
            st.session_state.messages = updated

        st.rerun()


if __name__ == "__main__":
    main()
