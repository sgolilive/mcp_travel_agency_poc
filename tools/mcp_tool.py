def mcp_tool(func):
    func._is_mcp_tool = True
    return func