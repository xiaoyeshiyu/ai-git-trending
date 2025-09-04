from datetime import date, timedelta
from database import ProjectDatabase

# 创建一个简单的测试函数
def test_function():
    try:
        db = ProjectDatabase()
        conn = db._get_connection()
        cursor = conn.cursor()
        
        # 简单查询测试
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        conn.close()
        
        print(f"测试成功！查询结果: {result}")
        return True
    except Exception as e:
        print(f"测试失败: {e}")
        return False

if __name__ == "__main__":
    test_function()