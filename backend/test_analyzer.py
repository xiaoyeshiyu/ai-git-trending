import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.analyzer import analyze_trends, get_trend_by_tag

def test_analyzer():
    print("开始测试analyzer模块...")
    try:
        # 测试analyze_trends函数（使用1天的数据减少运行时间）
        print("\n测试analyze_trends函数...")
        trends = analyze_trends(days=1)
        print(f"测试成功！获取到的趋势数据：")
        print(f"- 热门项目数量: {len(trends['most_frequent_projects'])}")
        print(f"- 热门语言数量: {len(trends['most_frequent_languages'])}")
        print(f"- 上升项目数量: {len(trends['surging_projects'])}")
        
        # 测试get_trend_by_tag函数（使用较短时间窗口）
        print("\n测试get_trend_by_tag函数...")
        tag_trend = get_trend_by_tag("ai", days=7)
        print(f"标签'trend'的趋势数据点数: {len(tag_trend)}")
        
        print("\n所有测试通过！analyzer模块工作正常。")
        return True
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_analyzer()