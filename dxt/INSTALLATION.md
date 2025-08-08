# Vibetest DXT Installation Guide

## What is this DXT?

This is a Desktop Extension (DXT) package for the **Vibetest** automated QA testing tool. It allows you to install and use the vibetest-use MCP server with one click in Claude Desktop and other MCP-enabled applications.

## Features

- ✅ **One-click installation** - No manual configuration required
- 🤖 **Multi-agent testing** - Launch multiple Browser-Use agents simultaneously
- 🧠 **AI-powered analysis** - Uses Gemini 2.0 Flash for intelligent bug detection
- 🔍 **Comprehensive testing** - UI bugs, broken links, accessibility, technical issues
- 📊 **Detailed reports** - Severity-classified findings with specific descriptions
- 🌐 **Flexible targets** - Test live websites or localhost development sites

## Installation Steps

### 1. Prerequisites
- **Python 3.11+** installed on your system
- **Google API Key** for Gemini 2.0 Flash model
  - Get one from: https://developers.google.com/maps/api-security-best-practices

### 2. Install the DXT
1. Download `vibetest-use-mcp.dxt`
2. Double-click the file to open with Claude Desktop
3. Click "Install" when prompted
4. Enter your Google API Key when requested

### 3. Verify Installation
After installation, you should see "vibetest-use" in your MCP servers list in Claude Desktop.

## Usage Examples

### Basic Website Testing
```
Please test my website with vibetest: https://example.com
```

### Advanced Testing with Multiple Agents
```
Run vibetest on localhost:3000 with 5 agents in headless mode
```

### Get Detailed Results
```
Show me the detailed results for test ID: abc123-def456
```

## Tools Available

### `start` - Launch QA Testing
- **url** (required): Website URL to test
- **num_agents** (optional): Number of agents (default: 3)
- **headless** (optional): Run in headless mode (default: false)

### `results` - Get Test Results  
- **test_id** (required): Test ID from start command

## Troubleshooting

### Dependencies Not Installing
If dependencies fail to install automatically:
```bash
pip install mcp[cli] browser-use playwright langchain_google_genai langchain_core pydantic screeninfo
playwright install chromium
```

### Google API Key Issues
- Ensure your API key has access to Gemini 2.0 Flash
- Check that the key is properly configured in the DXT settings
- Verify billing is enabled for your Google Cloud project

### Browser Issues
- Make sure Chromium is installed: `playwright install chromium`
- On Linux, you may need additional dependencies: `playwright install-deps`

## Technical Details

- **DXT Version**: 0.1
- **Python Version**: 3.11+
- **MCP Protocol**: Uses FastMCP framework
- **Browser Engine**: Playwright with Chromium
- **AI Model**: Google Gemini 2.0 Flash

## Support

For issues and questions:
- Original project: https://github.com/browser-use/vibetest-use
- DXT specification: https://github.com/anthropics/dxt

## License

MIT License - Based on the vibetest-use project by the Browser-Use team.
