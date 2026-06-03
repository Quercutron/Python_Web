"""
该文件用于记录学生类，包含学生姓名，学号，性别，年龄，手机号，描述信息
"""
class Student:
    def __init__(self, name, id, gender, age, phone, desc):
        """
        初始化方法,定义学生类
        Args:
            name: 学生姓名
            id: 学生学号
            gender: 学生性别
            age: 学生年龄
            phone: 学生手机号
            desc:
        """
        self.name = name
        self.id = id
        self.gender = gender
        self.age = age
        self.phone = phone
        self.desc = desc

    def __str__(self):
        return f"姓名：{self.name} ，学号：{self.id} ，性别：{self.gender} ，年龄：{self.age} ，手机号：{self.phone}，信息： {self.desc}"