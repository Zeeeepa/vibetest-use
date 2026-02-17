# 🐳 MCPhub Docker Setup Guide

This guide shows how to configure the Vibetest DXT in **MCPhub** (MCP Hub) running in Docker.

## 🚀 Quick Setup for MCPhub

### Step 1: Get Your Google API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key (starts with `AIza...`)

### Step 2: Configure Environment Variables in MCPhub

#### Method 1: MCPhub Web Interface
1. Open your MCPhub web interface
2. Go to "MCP Servers" or "Extensions"
3. Find the Vibetest DXT server
4. Click "Configure" or "Environment Variables"
5. Add: `GOOGLE_API_KEY = your_api_key_here`
6. Save and restart the server

#### Method 2: Docker Environment Variables
If you're running MCPhub with Docker Compose:

```yaml
# docker-compose.yml
version: '3.8'
services:
  mcphub:
    image: mcphub/mcphub:latest
    environment:
      - GOOGLE_API_KEY=your_api_key_here
    # ... other config
```

#### Method 3: Docker Run Command
```bash
docker run -d \
  -e GOOGLE_API_KEY=your_api_key_here \
  -p 8080:8080 \
  mcphub/mcphub:latest
```

### Step 3: Install the DXT in MCPhub

1. **Upload DXT File:**
   - Download `vibetest-use-mcp.dxt` from this repository
   - In MCPhub web interface, go to "Extensions" or "Import"
   - Upload the DXT file
   - MCPhub will extract and configure it automatically

2. **Manual Installation (Alternative):**
   - Extract the DXT contents to MCPhub's extensions directory
   - Restart MCPhub to detect the new server

### Step 4: Verify Installation

1. Check MCPhub logs for any errors
2. Look for "vibetest-use" in the MCP servers list
3. Test with a simple command:
   ```
   start("https://example.com", num_agents=1, headless=True)
   ```

## 🔧 MCPhub-Specific Configuration

### Environment Variables
MCPhub supports these environment variables for Vibetest:

```bash
# Required
GOOGLE_API_KEY=your_api_key_here

# Optional
GEMINI_API_KEY=your_api_key_here          # Alternative name
GOOGLE_GENAI_API_KEY=your_api_key_here    # Alternative name
ANONYMIZED_TELEMETRY=false                # Disable telemetry
BROWSER_USE_LOGGING_LEVEL=CRITICAL        # Reduce logging
```

### MCPhub Docker Compose Example
```yaml
version: '3.8'
services:
  mcphub:
    image: mcphub/mcphub:latest
    ports:
      - "8080:8080"
    environment:
      # Vibetest Configuration
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - ANONYMIZED_TELEMETRY=false
      - BROWSER_USE_LOGGING_LEVEL=CRITICAL
    volumes:
      - ./extensions:/app/extensions
      - ./data:/app/data
    restart: unless-stopped
```

### .env File for Docker Compose
Create a `.env` file in your MCPhub directory:
```bash
# .env
GOOGLE_API_KEY=your_actual_api_key_here
```

## 🐛 Troubleshooting MCPhub Issues

### "Google API Key not found" Error
1. **Check Environment Variables:**
   ```bash
   # In MCPhub container
   docker exec -it mcphub_container env | grep GOOGLE
   ```

2. **Restart MCPhub:**
   ```bash
   docker-compose restart
   # or
   docker restart mcphub_container
   ```

3. **Check MCPhub Logs:**
   ```bash
   docker logs mcphub_container
   ```

### DXT Not Loading
1. **Verify DXT Installation:**
   - Check MCPhub extensions directory
   - Ensure all files are properly extracted

2. **Check Python Dependencies:**
   - MCPhub should auto-install dependencies
   - If not, manually install in the container:
   ```bash
   docker exec -it mcphub_container pip install mcp browser-use playwright langchain_google_genai
   ```

### Browser Issues in Docker
1. **Install Browser Dependencies:**
   ```bash
   docker exec -it mcphub_container playwright install chromium
   docker exec -it mcphub_container playwright install-deps
   ```

2. **Use Headless Mode:**
   - Always use `headless=True` in Docker environments
   - Non-headless mode won't work without display

## 📋 MCPhub Configuration Examples

### Basic MCPhub MCP Server Config
If MCPhub uses a JSON config file:
```json
{
  "servers": {
    "vibetest-use": {
      "command": "python",
      "args": ["/path/to/dxt/server/main.py"],
      "env": {
        "GOOGLE_API_KEY": "your_api_key_here",
        "ANONYMIZED_TELEMETRY": "false"
      }
    }
  }
}
```

### Advanced Docker Setup with Secrets
```yaml
version: '3.8'
services:
  mcphub:
    image: mcphub/mcphub:latest
    environment:
      - GOOGLE_API_KEY_FILE=/run/secrets/google_api_key
    secrets:
      - google_api_key
    # ... other config

secrets:
  google_api_key:
    file: ./secrets/google_api_key.txt
```

## 🧪 Testing in MCPhub

### Test API Key
```bash
# Inside MCPhub container
docker exec -it mcphub_container python -c "
import os
print('API Key found:', bool(os.getenv('GOOGLE_API_KEY')))
"
```

### Test Vibetest Tools
In MCPhub web interface or API:
```python
# Start a test
test_id = start("https://httpbin.org/html", num_agents=1, headless=True)

# Get results
report = results(test_id)
```

## 💡 MCPhub Best Practices

1. **Always use headless mode** in Docker
2. **Set resource limits** for browser processes
3. **Monitor memory usage** during testing
4. **Use environment files** for sensitive data
5. **Regular container restarts** to prevent memory leaks

## 🆘 Still Having Issues?

1. Check MCPhub documentation for MCP server configuration
2. Verify Docker container has internet access
3. Ensure sufficient memory allocation (2GB+ recommended)
4. Test with a simple website first (like httpbin.org)

---

**MCPhub Project:** [GitHub Repository](https://github.com/your-mcphub-repo)  
**Get API Key:** [Google AI Studio](https://aistudio.google.com/app/apikey)
