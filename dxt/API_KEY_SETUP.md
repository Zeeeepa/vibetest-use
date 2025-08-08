# 🔑 Google API Key Setup Guide

The Vibetest DXT requires a Google API key to use the Gemini 2.0 Flash model for AI-powered testing analysis.

## 🚀 Quick Setup

### Step 1: Get Your API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### Step 2: Configure in Claude Desktop

#### Method 1: DXT Settings (Recommended)
1. After installing the DXT, Claude Desktop should prompt you for the API key
2. Paste your API key when prompted
3. The key will be securely stored and used automatically

#### Method 2: Manual Configuration
If the automatic prompt doesn't appear:

1. Open Claude Desktop settings
2. Go to "Extensions" or "MCP Servers"
3. Find "vibetest-use" in the list
4. Click "Configure" or "Settings"
5. Enter your API key in the "Google API Key" field

### Step 3: Alternative Methods

#### Environment Variable (Advanced Users)
Set the environment variable before starting Claude Desktop:

**macOS/Linux:**
```bash
export GOOGLE_API_KEY="your_api_key_here"
# Then start Claude Desktop
```

**Windows:**
```cmd
set GOOGLE_API_KEY=your_api_key_here
# Then start Claude Desktop
```

#### Alternative Environment Variables
The DXT also checks these environment variables:
- `GEMINI_API_KEY`
- `GOOGLE_GENAI_API_KEY`

## 🔧 Troubleshooting

### "Google API Key not found" Error
If you see this error, try these solutions:

1. **Check DXT Configuration:**
   - Ensure the API key is properly set in Claude Desktop settings
   - Try removing and re-adding the DXT

2. **Verify API Key:**
   - Make sure your API key is valid and active
   - Check that billing is enabled in your Google Cloud project

3. **Manual Environment Setup:**
   ```bash
   # Test if your API key works
   export GOOGLE_API_KEY="your_key_here"
   python -c "import os; print('API Key:', os.getenv('GOOGLE_API_KEY'))"
   ```

### API Key Not Working
- Ensure your Google Cloud project has billing enabled
- Verify the Gemini API is enabled in your project
- Check API quotas and limits

### DXT Installation Issues
1. **Reinstall the DXT:**
   - Remove the current installation
   - Download the latest `vibetest-use-mcp.dxt`
   - Install again and configure the API key

2. **Check Python Dependencies:**
   - The DXT auto-installs dependencies
   - If this fails, manually install: `pip install mcp browser-use playwright langchain_google_genai`

## 📋 Configuration Examples

### Claude Desktop MCP Config (Manual)
If you need to manually configure the MCP server:

```json
{
  "mcpServers": {
    "vibetest-use": {
      "command": "python",
      "args": ["/path/to/dxt/server/main.py"],
      "env": {
        "GOOGLE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## 🔒 Security Notes

- Your API key is stored securely by Claude Desktop
- The key is only used for Gemini API calls
- Never share your API key publicly
- Regenerate your key if you suspect it's compromised

## 💡 Tips

- **Free Tier:** Google AI Studio provides a generous free tier
- **Rate Limits:** The DXT respects API rate limits automatically
- **Cost:** Gemini 2.0 Flash is very cost-effective for testing workloads
- **Monitoring:** Check your API usage in Google AI Studio

## 🆘 Still Having Issues?

1. Check the Claude Desktop logs for error messages
2. Verify your API key at [Google AI Studio](https://aistudio.google.com/app/apikey)
3. Try testing with a simple environment variable setup first
4. Create an issue in the repository with error details

---

**Need an API Key?** → [Get one here](https://aistudio.google.com/app/apikey) (Free tier available!)
