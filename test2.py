# 示例1：执行简单的数学计算
# code = 'result = 5 + 10'
# exec(code)
# print(result)  # 输出：15

# # 示例2：在不同的命名空间中执行代码
# global_vars = {'a': 1, 'b': 2}
# local_vars = {'a': 10, 'b': 20}
# exec('c = a + b', global_vars, local_vars)
# print(global_vars)  # 输出：{'a': 1, 'b': 2}
# print(local_vars)   # 输出：{'a': 10, 'b': 20, 'c': 30}



# 示例3：定义函数并调用
def main():
    exec('def foo():\n\treturn "bar"')
    print(foo())  # 输出："bar"


if __name__ == '__main__':
    main()
