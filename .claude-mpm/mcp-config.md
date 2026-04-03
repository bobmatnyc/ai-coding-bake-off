# MCP Server Configuration for Bake-Off

## Required MCP Servers (Claude MPM runs)

### kuzu-memory
- **Purpose**: Persistent memory across challenge levels and evaluation phases
- **Key uses**: Store/recall architecture decisions, timing patterns, quality findings
- **Config**: Standard kuzu-memory setup, project-scoped to ai-coding-bake-off

### mcp-vector-search  
- **Purpose**: Semantic search across challenges, solutions, and evaluations
- **Key uses**: Compare solutions, find patterns, search challenge context
- **Config**: Auto-indexes project directory, stored in .mcp-vector-search/

## Optional MCP Servers

### gworkspace-mcp
- **Purpose**: Publish results to Google Docs/Sheets for the article
- **When needed**: Article writing phase only

## Configuration Notes
- Both kuzu-memory and mcp-vector-search should be configured in the Claude Code MCP settings for this project
- The .mcp-vector-search/ directory is gitignored
- kuzu-memory data persists across sessions in its standard location
