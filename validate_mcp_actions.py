#!/usr/bin/env python3
"""
MCP Actions Validation Script
Programmatically validates that all MCP actions are properly exposed in the DXT
"""
import json
import zipfile
import sys
import ast
import re
from pathlib import Path

def extract_mcp_tools_from_code(code_content):
    """Extract MCP tool definitions from Python code"""
    tools = []
    
    # Look for @mcp.tool() decorators
    tool_pattern = r'@mcp\.tool\(\)\s*(?:async\s+)?def\s+(\w+)\s*\([^)]*\)\s*(?:->\s*[^:]+)?\s*:\s*"""([^"]+)"""'
    matches = re.findall(tool_pattern, code_content, re.MULTILINE | re.DOTALL)
    
    for match in matches:
        func_name, docstring = match
        # Extract first line of docstring as description
        description = docstring.strip().split('\n')[0].strip()
        tools.append({
            "name": func_name,
            "description": description,
            "source": "code"
        })
    
    return tools

def extract_function_signatures(code_content):
    """Extract function signatures and parameters"""
    signatures = {}
    
    # Parse the AST to get function definitions
    try:
        tree = ast.parse(code_content)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check if it has @mcp.tool() decorator
                has_mcp_decorator = False
                for decorator in node.decorator_list:
                    if (isinstance(decorator, ast.Call) and 
                        isinstance(decorator.func, ast.Attribute) and
                        decorator.func.attr == 'tool'):
                        has_mcp_decorator = True
                        break
                
                if has_mcp_decorator:
                    # Extract parameters
                    params = []
                    for arg in node.args.args:
                        if arg.arg != 'self':  # Skip self parameter
                            param_info = {"name": arg.arg}
                            # Check for type annotations
                            if arg.annotation:
                                if isinstance(arg.annotation, ast.Name):
                                    param_info["type"] = arg.annotation.id
                                elif isinstance(arg.annotation, ast.Constant):
                                    param_info["type"] = str(arg.annotation.value)
                            params.append(param_info)
                    
                    # Extract defaults
                    defaults = node.args.defaults
                    if defaults:
                        # Apply defaults to the last N parameters
                        for i, default in enumerate(defaults):
                            param_idx = len(params) - len(defaults) + i
                            if param_idx >= 0 and param_idx < len(params):
                                if isinstance(default, ast.Constant):
                                    params[param_idx]["default"] = default.value
                                elif isinstance(default, ast.Name):
                                    params[param_idx]["default"] = default.id
                    
                    signatures[node.name] = {
                        "parameters": params,
                        "docstring": ast.get_docstring(node) or ""
                    }
    except Exception as e:
        print(f"Warning: Could not parse AST: {e}")
    
    return signatures

def validate_mcp_actions(dxt_file):
    """Validate MCP actions in the DXT file"""
    print(f"🔍 Validating MCP actions in {dxt_file}...")
    
    try:
        with zipfile.ZipFile(dxt_file, 'r') as zf:
            # Read manifest
            manifest_data = zf.read('manifest.json')
            manifest = json.loads(manifest_data)
            
            print(f"📋 Manifest tools declared: {len(manifest.get('tools', []))}")
            manifest_tools = {tool['name']: tool for tool in manifest.get('tools', [])}
            
            # Find and read the MCP server file
            server_files = [f for f in zf.namelist() if f.endswith('mcp_server.py')]
            if not server_files:
                print("❌ No mcp_server.py file found!")
                return False
            
            server_file = server_files[0]
            server_code = zf.read(server_file).decode('utf-8')
            
            # Extract tools from code
            code_tools = extract_mcp_tools_from_code(server_code)
            print(f"🐍 Code tools found: {len(code_tools)}")
            
            # Extract function signatures
            signatures = extract_function_signatures(server_code)
            
            # Validation checks
            validation_passed = True
            
            print("\n📊 Tool Validation Results:")
            print("=" * 50)
            
            # Check if all manifest tools are implemented
            for tool_name, tool_info in manifest_tools.items():
                code_tool = next((t for t in code_tools if t['name'] == tool_name), None)
                if code_tool:
                    print(f"✅ {tool_name}: Declared in manifest ✓ Implemented in code ✓")
                    
                    # Check if descriptions match or are reasonable
                    manifest_desc = tool_info.get('description', '').lower()
                    code_desc = code_tool.get('description', '').lower()
                    
                    if manifest_desc and code_desc:
                        # Simple similarity check
                        common_words = set(manifest_desc.split()) & set(code_desc.split())
                        if len(common_words) >= 2:
                            print(f"   📝 Description consistency: Good")
                        else:
                            print(f"   ⚠️  Description mismatch:")
                            print(f"      Manifest: {tool_info.get('description')}")
                            print(f"      Code: {code_tool.get('description')}")
                    
                    # Show function signature if available
                    if tool_name in signatures:
                        sig = signatures[tool_name]
                        params = sig['parameters']
                        if params:
                            print(f"   🔧 Parameters: {', '.join([f'{p['name']}:{p.get('type', 'any')}' + ('=' + str(p['default']) if 'default' in p else '') for p in params])}")
                        else:
                            print(f"   🔧 Parameters: None")
                        
                        # Show docstring summary
                        if sig['docstring']:
                            first_line = sig['docstring'].split('\n')[0].strip()
                            print(f"   📖 Docstring: {first_line}")
                else:
                    print(f"❌ {tool_name}: Declared in manifest ✗ Missing in code")
                    validation_passed = False
            
            # Check for tools implemented but not declared
            for code_tool in code_tools:
                if code_tool['name'] not in manifest_tools:
                    print(f"⚠️  {code_tool['name']}: Implemented in code but not declared in manifest")
                    print(f"   📝 Description: {code_tool['description']}")
            
            print("\n🔍 Detailed Function Analysis:")
            print("=" * 50)
            
            for func_name, sig in signatures.items():
                print(f"\n🔧 Function: {func_name}")
                print(f"   📖 Docstring: {sig['docstring'][:100]}..." if len(sig['docstring']) > 100 else f"   📖 Docstring: {sig['docstring']}")
                
                if sig['parameters']:
                    print("   📋 Parameters:")
                    for param in sig['parameters']:
                        param_str = f"      - {param['name']}"
                        if 'type' in param:
                            param_str += f": {param['type']}"
                        if 'default' in param:
                            param_str += f" = {param['default']}"
                        print(param_str)
                else:
                    print("   📋 Parameters: None")
            
            print(f"\n{'✅ VALIDATION PASSED' if validation_passed else '❌ VALIDATION FAILED'}")
            print(f"📊 Summary:")
            print(f"   - Manifest tools: {len(manifest_tools)}")
            print(f"   - Code tools: {len(code_tools)}")
            print(f"   - Function signatures: {len(signatures)}")
            
            return validation_passed
            
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False

def validate_dxt_structure(dxt_file):
    """Validate basic DXT structure"""
    print(f"🔍 Validating DXT structure...")
    
    try:
        with zipfile.ZipFile(dxt_file, 'r') as zf:
            files = zf.namelist()
            
            # Check required files
            required_files = ['manifest.json']
            for req_file in required_files:
                if req_file not in files:
                    print(f"❌ Missing required file: {req_file}")
                    return False
            
            # Validate manifest
            manifest_data = zf.read('manifest.json')
            manifest = json.loads(manifest_data)
            
            # Check entry point exists
            entry_point = manifest.get('server', {}).get('entry_point')
            if entry_point and entry_point not in files:
                print(f"❌ Entry point file not found: {entry_point}")
                return False
            
            print("✅ DXT structure validation passed")
            return True
            
    except Exception as e:
        print(f"❌ Structure validation failed: {e}")
        return False

if __name__ == "__main__":
    dxt_file = "dxt/vibetest-use-mcp.dxt"
    
    if not Path(dxt_file).exists():
        print(f"❌ DXT file not found: {dxt_file}")
        sys.exit(1)
    
    print("🚀 Starting MCP Actions Validation")
    print("=" * 60)
    
    # Validate structure first
    structure_ok = validate_dxt_structure(dxt_file)
    if not structure_ok:
        sys.exit(1)
    
    # Validate MCP actions
    actions_ok = validate_mcp_actions(dxt_file)
    
    print("\n" + "=" * 60)
    if structure_ok and actions_ok:
        print("🎉 ALL VALIDATIONS PASSED!")
        print("✅ DXT is ready for distribution")
        sys.exit(0)
    else:
        print("❌ VALIDATION FAILED!")
        print("🔧 Please fix the issues above before distributing")
        sys.exit(1)
