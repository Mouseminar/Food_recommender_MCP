"""
测试 MCP 服务器功能的脚本
直接调用 mcp_server.py 中的工具函数来验证功能
"""
import asyncio
import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_server import recommend_food, search_nearby_restaurants, get_restaurant_details, compare_restaurants, generate_restaurant_map

async def test_recommend_food():
    """测试美食推荐功能"""
    print("=" * 60)
    print("测试 1: 推荐火锅店")
    print("=" * 60)
    
    result = await recommend_food(
        address="北京市海淀区上地十街10号",
        cuisine_type="火锅",
        radius=1000,
        num_recommend=3
    )
    print(result)
    print()

async def test_search_nearby():
    """测试附近餐厅搜索"""
    print("=" * 60)
    print("测试 2: 搜索附近餐厅")
    print("=" * 60)
    
    result = await search_nearby_restaurants(
        address="北京市朝阳区三里屯",
        keyword="日料",
        radius=1000,
        max_results=5
    )
    print(result)
    print()

async def test_compare_restaurants():
    """测试餐厅对比功能"""
    print("=" * 60)
    print("测试 3: 餐厅对比功能")
    print("=" * 60)
    
    # 注意：这里需要使用真实的餐厅UID进行测试
    result = await compare_restaurants(
        uids=["test_uid_1", "test_uid_2"]  # 示例UID，实际使用时需要替换为真实UID
    )
    print(result)
    print()

async def test_generate_restaurant_map():
    """测试生成餐厅地图功能"""
    print("=" * 60)
    print("测试 4: 生成餐厅地图")
    print("=" * 60)
    
    # 注意：这里需要使用真实的餐厅UID进行测试
    result = await generate_restaurant_map(
        uids=["test_uid_1", "test_uid_2"],  # 示例UID，实际使用时需要替换为真实UID
        width=500,
        height=400,
        zoom=16
    )
    print(result)
    print()

async def main():
    """运行所有测试"""
    print("\n开始测试 MCP 服务器功能...\n")
    
    try:
        await test_recommend_food()
        await test_search_nearby()
        await test_compare_restaurants()
        await test_generate_restaurant_map()
        
        print("=" * 60)
        print("所有测试完成！")
        print("=" * 60)
        print("\n提示：")
        print("1. 如果看到餐厅数据，说明 MCP 服务器工作正常")
        print("2. 可以将此服务器配置到 Claude Desktop 中使用")
        print("3. 配置方法请参考 README.md")
        print("注意：测试3和测试4使用的是示例UID，实际使用时需要替换为真实餐厅UID")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        print("\n请检查：")
        print("1. .env 文件中的 BAIDU_MAPS_API_KEY 是否正确配置")
        print("2. 网络连接是否正常")
        print("3. 百度地图 API 配额是否充足")

if __name__ == "__main__":
    asyncio.run(main())