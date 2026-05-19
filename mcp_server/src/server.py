from mcp.server.fastmcp import FastMCP
from tools.csv_tools import load_csv, query_data

mcp = FastMCP("datapilot")

mcp.tool()(load_csv)
mcp.tool()(query_data)

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
