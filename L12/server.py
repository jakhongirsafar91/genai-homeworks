import json
from pathlib import Path

from mcp.server import MCPServer

mcp = MCPServer("my-session-directory")


@mcp.tool()
def get_session(session_id: str) -> dict:
    """Read a session from the local sessions.json file. Returns found=false if absent."""
    file_path = Path(__file__).resolve().parent / "sessions.json"
    data = json.loads(file_path.read_text(encoding="utf-8-sig"))
    records = data.get("sessions", [])
    for record in records:
        if record.get("id") == session_id:
            return {"found": True, "session": record}
    return {"found": False, "session_id": session_id, "message": "Session not found"}


if __name__ == "__main__":
    mcp.run(transport="stdio")
