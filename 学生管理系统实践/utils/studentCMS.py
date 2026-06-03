"""
该文件用于记录学生管理类，包含添加学生信息，删除学生信息，修改学生信息，查询学生信息，展示所有学生信息
保存学生信息，退出系统
"""
import time
from . import student as s

class StudentCMS:
    def __init__(self):
        #创建列表，存储学生对象信息
        self.student_list: list[s.Student] = []

    #添加学生信息
    def add_student_info(self):
        #包含学生姓名，学号，性别，年龄，手机号，描述信息
        name = input("请输入学生姓名：")
        id = input("请输入学生学号：")
        gender = input("请输入学生性别：")
        age = input("请输入学生年龄：")
        phone = input("请输入学生手机号：")
        desc = input("请输入学生信息：")

        student_info = s.Student(name, id, gender, age, phone, desc)
        self.student_list.append(student_info)
        print(f"学生{name}信息添加成功\n")

    #删除学生信息
    def del_student_info(self):
        name = input("请输入要删除的学生姓名：")
        for student_info in self.student_list:
            if name in student_info.name:
                self.student_list.remove(student_info)
                print(f"学生{name}信息删除成功\n")
                break
            else:
                print("学生不存在\n")

    #修改学生信息
    def update_student_info(self):
        id = input("请输入要修改的学生学号：")
        for student_info in self.student_list:
            if id in student_info.id:
                print("学生存在,请输入修改后的信息：")
                student_info.name = input("请输入学生姓名：")
                student_info.gender = input("请输入学生性别：")
                student_info.age = input("请输入学生年龄：")
                student_info.phone = input("请输入学生手机号：")
                student_info.desc = input("请输入学生信息：")
                print(f"学生{student_info.name}信息修改成功\n")
                break
        else:
            print("学生不存在\n")

    #查询单个学生信息
    def show_student_info(self):
        name = input("请输入要查询的学生姓名：")
        if len(self.student_list)==0:
            print("没有学生信息")
        else:
            for student_info in self.student_list:
                if name in student_info.name:
                    print(student_info)

    #显示所有学生信息
    def show_all_student_info(self):
        if len(self.student_list) == 0:
            print("没有学生信息")
        else:
            for student_info in self.student_list:
                print(student_info)

    def save_student_info(self):
        with open("date/student_info.txt", "w",encoding="utf-8") as f:
            stu_dict=[student_info.__dict__ for student_info in self.student_list]
            f.write(str(stu_dict))

    #加载学生信息
    def load_student_info(self):
        try:
            with open("date/student_info.txt", "r",encoding="utf-8") as f:
                stu_dict = f.read()
                stu_list = eval(stu_dict)
                if  len(stu_list)==0:
                    self.student_list = []
                self.student_list = [s.Student(**stu_dict) for stu_dict in stu_list]
        except:
            with open("date/student_info.txt", "w",encoding="utf-8") as f:
                f.write("[]")

    @staticmethod
    def state_view():
        print("学生管理系统V1.0")
        print("1. 添加学生信息")
        print("2. 删除学生信息")
        print("3. 修改学生信息")
        print("4. 查询单个学生信息")
        print("5. 显示所有学生信息")
        print("6. 保存学生信息")
        print("7. 退出系统")


    def run(self):
        #主程序运行时先加载文件，再显示菜单
        self.load_student_info()

        while True:
            time.sleep(1)

            self.state_view()

            choice = int(input("请选择要执行的操作（1-7）："))
            try:
                match choice:
                    case 1:
                        self.add_student_info()
                        continue
                    case 2:
                        self.del_student_info()
                        continue
                    case 3:
                        self.update_student_info()
                        continue
                    case 4:
                        self.show_student_info()
                        continue
                    case 5:
                        self.show_all_student_info()
                        continue
                    case 6:
                        self.save_student_info()
                        print("学生信息保存成功\n")
                        continue
                    case 7:
                        ex=input("确定要退出系统吗？y/n : ")
                        if ex.lower() == "y" or ex.lower() == "n":
                            print("退出系统，欢迎下次使用\n")
                            exit()
                        else:
                            print("取消退出系统\n")
                            continue
                    case _:
                        print("输入错误，请重新输入\n")

            except Exception as e:
                print("输入错误，请重新输入\n")


