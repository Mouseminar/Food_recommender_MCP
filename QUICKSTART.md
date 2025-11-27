# 快速开始

本指南将帮助您快速配置和使用美食推荐 MCP 服务器，支持 Stdio 和 SSE 两种模式。

## 1. 环境准备

### 1.1 安装 Python

确保已安装 Python 3.11 或更高版本。

```bash
python --version
# 或
python3 --version
```

### 1.2 安装依赖

```bash
pip install fastmcp httpx python-dotenv
```

或者使用 requirements.txt（如果存在）：

```bash
pip install -r requirements.txt
```

## 2. 配置 API Key

### 2.1 获取百度地图 API Key

1. 访问 [百度地图开放平台](https://lbsyun.baidu.com/)
2. 注册账号并登录
3. 进入控制台，创建应用并获取 API Key

### 2.2 配置环境变量

在项目根目录创建 `.env` 文件：

```env
BAIDU_MAPS_API_KEY=your_actual_api_key_here
```

将 `your_actual_api_key_here` 替换为您自己的百度地图 API Key。

## 3. 配置 Claude Desktop

### 3.1 找到配置文件

Claude Desktop 配置文件位于：

- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

## 4. 运行模式选择

本服务器支持两种运行模式：

### 4.1 Stdio 模式（推荐日常使用）

**特点：** Claude Desktop 自动启动和管理，无需手动操作

在配置文件中添加以下内容：

```json
{
  "mcpServers": {
    "food-recommender": {
      "command": "python",
      "args": [
        "g:\\food_mcp\\mcp_server.py"
      ]
    }
  }
}
```

**注意事项：**
- 确保 Python 路径正确（如果使用 conda 环境，需要使用完整路径）
- 确保项目路径正确（这里是 `g:\food_mcp\mcp_server.py`）
- 配置完成后重启 Claude Desktop

如果使用 conda 环境，配置应该是：

```json
{
  "mcpServers": {
    "food-recommender": {
      "command": "C:/ProgramData/Anaconda3/envs/your_env_name/python.exe",
      "args": [
        "g:\\food_mcp\\mcp_server.py"
      ]
    }
  }
}
```

### 4.2 SSE 模式（推荐开发测试）

**特点：** 通过 HTTP 端口访问，方便调试和测试

1. 启动 SSE 服务器：
```bash
python mcp_server.py --sse --port 8000
# 或双击 run_sse_server.bat
```

2. 在配置文件中添加以下内容：
```json
{
  "mcpServers": {
    "food-recommender": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

3. 配置完成后重启 Claude Desktop

## 5. 测试配置

### 5.1 快速测试

运行测试脚本验证配置：

```bash
# 测试 Stdio 模式
python test_mcp.py

# 测试 SSE 模式
python test_sse_simple.py
```

### 5.2 在 Claude Desktop 中测试

重启 Claude Desktop，然后尝试以下对话：

```
请在"北京市海淀区上地十街10号"附近推荐5家火锅店
```

Claude 应该会自动调用 recommend_food 工具并返回推荐结果。

## 6. 可用工具

本 MCP 服务器提供以下工具：

1. **recommend_food** - 推荐附近餐厅
2. **search_nearby_restaurants** - 搜索附近餐厅
3. **get_restaurant_details** - 获取餐厅详情
4. **compare_restaurants** - 对比多个餐厅
5. **generate_restaurant_map** - 生成餐厅地图

详细参数说明请参考 [README.md](README.md)。

## 7. 故障排除

### 7.1 常见问题

1. **无法找到模块**
   - 确保已安装所有依赖
   - 检查 Python 路径是否正确

2. **API Key 错误**
   - 检查 `.env` 文件中的 API Key 是否正确
   - 确保 API Key 在百度地图控制台中已启用相应服务

3. **Claude Desktop 无法连接**
   - 确保配置文件格式正确
   - 重启 Claude Desktop
   - 检查项目路径是否正确（Stdio 模式）
   - 检查服务器是否正在运行（SSE 模式）

### 7.2 日志查看

查看 `food_mcp.log` 文件获取详细日志信息。

## 8. 进阶配置

### 8.1 自定义参数

您可以根据需要调整各种参数，如搜索半径、推荐数量等。

### 8.2 开发测试技巧

对于开发测试，推荐使用 SSE 模式，因为：
- 可以独立启动和停止服务器
- 方便查看实时日志输出
- 便于使用各种 HTTP 客户端进行调试