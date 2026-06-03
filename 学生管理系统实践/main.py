"""
学生管理系统V1.0:主入口
功能：
1. 添加学生信息
2. 删除学生信息
3. 修改学生信息
4. 查询学生信息
5. 显示所有学生信息
6. 保存学生信息
7. 退出系统

"""
from utils import *

if __name__ == "__main__":
    student_cms = StudentCMS()
    student_cms.run()
