# Vibetest - Automated QA Testing DXT

Automated QA testing using Browser-Use agents to test websites for UI bugs, broken links, accessibility issues, and technical problems.

## Features

- **Multi-Agent Testing**: Launch multiple Browser-Use agents to comprehensively test websites
- **AI-Powered Analysis**: Uses Gemini 2.0 Flash for intelligent bug detection and categorization
- **Comprehensive Coverage**: Tests for UI bugs, broken links, accessibility issues, and technical problems
- **Flexible Testing**: Works with both live websites and localhost development sites
- **Detailed Reports**: Provides severity-classified bug reports with specific descriptions

## Requirements

- Python 3.11 or higher
- Google API Key for Gemini 2.0 Flash model

## Installation

This is a Desktop Extension (DXT) file that can be installed in Claude Desktop and other MCP-enabled applications.

### 🖥️ Claude Desktop
1. **Get a Google API Key** (free): [Google AI Studio](https://aistudio.google.com/app/apikey)
2. **Download** the `vibetest-use-mcp.dxt` file
3. **Install** by double-clicking the DXT file in Claude Desktop
4. **Configure** your Google API Key when prompted

### 🐳 MCPhub (Docker)
1. **Get a Google API Key** (free): [Google AI Studio](https://aistudio.google.com/app/apikey)
2. **Set environment variable**: `GOOGLE_API_KEY=your_key_here`
3. **Upload DXT** to MCPhub web interface
4. **Restart** MCPhub to load the extension

> 🔑 **Setup Guides:**  
> • [API_KEY_SETUP.md](API_KEY_SETUP.md) - Claude Desktop setup  
> • [MCPHUB_SETUP.md](MCPHUB_SETUP.md) - MCPhub Docker setup

## Usage

Once installed, you can use the following tools:

### `start` - Launch QA Testing
```
start(url: str, num_agents: int = 3, headless: bool = False) -> str
```
- `url`: The website URL to test
- `num_agents`: Number of QA agents to spawn (default: 3)
- `headless`: Whether to run browsers in headless mode (default: False)

Returns a test ID for retrieving results.

### `results` - Get Test Results
```
results(test_id: str) -> dict
```
- `test_id`: The test ID returned from the start function

Returns detailed test results with severity classification.

## Example Usage

```
# Start testing a website
test_id = start("https://example.com", num_agents=5, headless=True)

# Get the results
report = results(test_id)
```

## Configuration

The extension requires a Google API Key for the Gemini 2.0 Flash model. You can get one from:
https://developers.google.com/maps/api-security-best-practices

## License

MIT License - see the original vibetest-use repository for details.

## Source

Based on the vibetest-use project: https://github.com/browser-use/vibetest-use
