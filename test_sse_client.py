"""
测试 SSE 模式的 MCP 服务器
确保先启动服务器: python mcp_server.py --sse --port 8000
"""
import httpx
import json
import asyncio

SERVER_URL = "http://localhost:8000/sse"

async def call_tool(tool_name: str, arguments: dict):
    """调用 MCP 工具"""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(SERVER_URL, json=payload)
        return response.json()

async def list_tools():
    """列出所有可用工具"""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(SERVER_URL, json=payload)
        return response.json()

async def test_recommend_food():
    """测试推荐工具"""
    print("🍜 测试推荐工具 (recommend_food)")
    print("-" * 60)
    result = await call_tool(
        "recommend_food",
        {
            "address": "北京市海淀区上地十街10号",
            "cuisine_type": "火锅",
            "radius": 1000,
            "num_recommend": 3
        }
    )
    
    if "result" in result:
        content = result["result"]["content"]
        for item in content:
            if item["type"] == "text":
                data = json.loads(item["text"])
                print(f"\n查询地址: {data['query_address']}")
                print(f"菜系类型: {data['cuisine_type']}")
                print(f"推荐餐厅数量: {len(data['recommendations'])}\n")
                
                for i, restaurant in enumerate(data['recommendations'], 1):
                    print(f"{i}. {restaurant['name']}")
                    print(f"   评分: {restaurant['rating']} ⭐")
                    print(f"   距离: {restaurant['distance_m']}米")
                    print(f"   地址: {restaurant['address']}")
                    print(f"   电话: {restaurant['telephone']}")
                    print()
    else:
        print(f"错误: {result.get('error', '未知错误')}")
    print()

async def test_search_nearby_restaurants():
    """测试搜索工具"""
    print("🔍 测试搜索工具 (search_nearby_restaurants)")
    print("-" * 60)
    result = await call_tool(
        "search_nearby_restaurants",
        {
            "address": "北京市朝阳区三里屯",
            "keyword": "日料",
            "radius": 1000,
            "max_results": 5
        }
    )
    
    if "result" in result:
        content = result["result"]["content"]
        for item in content:
            if item["type"] == "text":
                data = json.loads(item["text"])
                print(f"\n搜索地址: {data['address']}")
                print(f"关键词: {data['keyword']}")
                print(f"找到 {len(data['results'])} 家餐厅\n")
                
                for i, restaurant in enumerate(data['results'], 1):
                    print(f"{i}. {restaurant['name']}")
                    print(f"   地址: {restaurant['address']}")
                    print()
    else:
        print(f"错误: {result.get('error', '未知错误')}")
    print()

async def test_compare_restaurants():
    """测试餐厅对比工具"""
    print("📊 测试餐厅对比工具 (compare_restaurants)")
    print("-" * 60)
    result = await call_tool(
        "compare_restaurants",
        {
            "uids": ["test_uid_1", "test_uid_2"]  # 示例UID，实际使用时需要替换为真实UID
        }
    )
    
    if "result" in result:
        content = result["result"]["content"]
        for item in content:
            if item["type"] == "text":
                data = json.loads(item["text"])
                print(f"\n对比餐厅数量: {data['count']}")
                print("对比结果:")
                for i, restaurant in enumerate(data['comparison'], 1):
                    print(f"{i}. {restaurant['name']}")
                    print(f"   综合评分: {restaurant['rating']} ⭐")
                    print(f"   口味评分: {restaurant['taste_rating']} ⭐")
                    print(f"   价格: {restaurant['price']} 元")
                    print()
    else:
        print(f"错误: {result.get('error', '未知错误')}")
    print()

async def test_generate_restaurant_map():
    """测试生成餐厅地图工具"""
    print("🗺️  测试生成餐厅地图工具 (generate_restaurant_map)")
    print("-" * 60)
    result = await call_tool(
        "generate_restaurant_map",
        {
            "uids": ["test_uid_1", "test_uid_2"],  # 示例UID，实际使用时需要替换为真实UID
            "width": 500,
            "height": 400,
            "zoom": 16
        }
    )
    
    if "result" in result:
        content = result["result"]["content"]
        for item in content:
            if item["type"] == "text":
                data = json.loads(item["text"])
                print(f"\n地图URL: {data['map_url']}")
                print(f"地图尺寸: {data['width']}x{data['height']}")
                print(f"缩放级别: {data['zoom']}")
                print(f"餐厅数量: {len(data['restaurants'])}")
                print()
    else:
        print(f"错误: {result.get('error', '未知错误')}")
    print()

async def main():
    print("=" * 60)
    print("测试 MCP 服务器 (SSE 模式)")
    print(f"服务器地址: {SERVER_URL}")
    print("=" * 60)
    print()
    
    try:
        # 1. 列出工具
        print("📋 1. 列出所有可用工具")
        print("-" * 60)
        tools = await list_tools()
        if "result" in tools:
            print(f"找到 {len(tools['result'].get('tools', []))} 个工具:")
            for tool in tools['result'].get('tools', []):
                print(f"  - {tool['name']}: {tool['description'][:50]}...")
        print()
        
        # 2. 测试各项功能
        await test_recommend_food()
        await test_search_nearby_restaurants()
        await test_compare_restaurants()
        await test_generate_restaurant_map()
        
        print("=" * 60)
        print("✅ 所有测试完成！")
        print("=" * 60)
        print("\n提示：")
        print("测试3和测试4使用的是示例UID，实际使用时需要替换为真实餐厅UID")
        
    except httpx.ConnectError:
        print("❌ 无法连接到服务器！")
        print("\n请确保服务器正在运行:")
        print("  python mcp_server.py --sse --port 8000")
        print()
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    asyncio.run(main())