"""
简单测试 - 使用 MCP SDK 连接 SSE 服务器
"""
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client

async def test_sse_connection():
    """测试 SSE 连接"""
    print("=" * 60)
    print("连接到 MCP 服务器 (SSE 模式)")
    print("服务器地址: http://localhost:8000/sse")
    print("=" * 60)
    print()
    
    try:
        # 使用 SSE 客户端连接
        async with sse_client("http://localhost:8000/sse") as (read, write):
            async with ClientSession(read, write) as session:
                # 初始化会话
                await session.initialize()
                
                # 1. 列出工具
                print("📋 列出所有可用工具:")
                print("-" * 60)
                tools = await session.list_tools()
                for tool in tools.tools:
                    print(f"✓ {tool.name}")
                    print(f"  描述: {tool.description}")
                    print()
                
                # 2. 调用推荐工具
                print("🍜 测试推荐工具:")
                print("-" * 60)
                result = await session.call_tool(
                    "recommend_food",
                    arguments={
                        "address": "北京市海淀区上地十街10号",
                        "cuisine_type": "火锅",
                        "num_recommend": 3
                    }
                )
                
                print("✅ 获取到推荐结果:")
                for content in result.content:
                    if hasattr(content, 'text'):
                        print(content.text[:500])
                        print("...")
                
                # 3. 调用搜索工具
                print("\n🔍 测试搜索工具:")
                print("-" * 60)
                result = await session.call_tool(
                    "search_nearby_restaurants",
                    arguments={
                        "address": "北京市朝阳区三里屯",
                        "keyword": "日料",
                        "max_results": 5
                    }
                )
                
                print("✅ 获取到搜索结果:")
                for content in result.content:
                    if hasattr(content, 'text'):
                        print(content.text[:500])
                        print("...")
                
                # 4. 调用对比工具
                print("\n📊 测试对比工具:")
                print("-" * 60)
                result = await session.call_tool(
                    "compare_restaurants",
                    arguments={
                        "uids": ["test_uid_1", "test_uid_2"]  # 示例UID，实际使用时需要替换为真实UID
                    }
                )
                
                print("✅ 获取到对比结果:")
                for content in result.content:
                    if hasattr(content, 'text'):
                        print(content.text[:500])
                        print("...")
                
                # 5. 调用地图工具
                print("\n🗺️  测试地图工具:")
                print("-" * 60)
                result = await session.call_tool(
                    "generate_restaurant_map",
                    arguments={
                        "uids": ["test_uid_1", "test_uid_2"],  # 示例UID，实际使用时需要替换为真实UID
                        "width": 500,
                        "height": 400
                    }
                )
                
                print("✅ 获取到地图结果:")
                for content in result.content:
                    if hasattr(content, 'text'):
                        print(content.text[:500])
                        print("...")
                
                print("\n" + "=" * 60)
                print("✅ 测试成功！SSE 服务器工作正常")
                print("=" * 60)
                print("\n提示：测试4和测试5使用的是示例UID，实际使用时需要替换为真实餐厅UID")
                
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        print("\n请确保服务器正在运行:")
        print("  python mcp_server.py --sse --port 8000")

if __name__ == "__main__":
    asyncio.run(test_sse_connection())