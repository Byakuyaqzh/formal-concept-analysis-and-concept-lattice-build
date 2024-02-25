

class concept:
    def __init__(self, x, a):
        self.X = x
        self.A = a
        self.father = []
        self.children = []

    #  这里的排序并不是偏序关系
    def __lt__(self, other):
        if isinstance(other, concept):
            if self.X == other.X:
                if len(self.A) == len(other.A):
                    return self.A > other.A
                else:
                    return len(self.A) > len(other.A)
            else:
                if len(self.X) == len(other.X):
                    return self.X < other.X
                else:
                    return len(self.X) < len(other.X)
        return False

    def __gt__(self, other):
        if isinstance(other, concept):
            if self.X == other.X:
                if len(self.A) == len(other.A):
                    return self.A < other.A
                else:
                    return len(self.A) < len(other.A)
            else:
                if len(self.X) == len(other.X):
                    return self.X > other.X
                else:
                    return len(self.X) > len(other.X)
        return False
        
    def __eq__(self, other) -> bool:
        if isinstance(other, concept):
            return self.X == other.X and self.A == other.A
        return False
    
    
    def __str__(self) -> str:
        s = ""
        x_size = len(self.X)
        a_size = len(self.A)
        s += "("
        if x_size == 0:
            s += " Ø"
        else:
            for j in range(x_size):
                s += " " + str(self.X[j])
        s += " , "
        if a_size == 0:
            s += " Ø"
        else:
            for j in range(a_size):
                s += " " + str(self.A[j])
        s += " )"
        return s
    
    
#  判断list1是否被list2包含
def is_sub(list1: list, list2: list) -> bool:
    n1, n2 = len(list1), len(list2)
    if n1 > n2:
        return False
    i = j = 0
    while i < n1 and j < n2:
        if list1[i] < list2[j]:
            return False
        elif list1[i] > list2[j]:
            j += 1
        else:
            i += 1
            j += 1
    return i == n1


#  并集
def union(a: list, b: list) -> list:
    len_1 = len(a)
    len_2 = len(b)
    res = []
    i = 0
    j = 0
    while i < len_1 and j < len_2:
        if a[i] < b[j]:
            res.append(a[i])
            i += 1
        elif a[i] > b[j]:
            res.append(b[j])
            j += 1
        else:
            res.append(a[i])
            i += 1
            j += 1
    while i < len_1:
        res.append(a[i])
        i += 1
    while j < len_2:
        res.append(b[j])
        j += 1
    return res


#  交集
def intersection(a: list, b: list) -> list:
    len_1 = len(a)
    len_2 = len(b)
    res: list = []
    i = 0
    j = 0
    while i < len_1 and j < len_2:
        if a[i] == b[j]:
            res.append(a[i])
            i += 1
            j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    return res


#  判断序列是否存在交集
def determine_intersection(a: list, b: list) -> bool:
    len_1 = len(a)
    len_2 = len(b)
    i = 0
    j = 0
    while i < len_1 and j < len_2:
        if a[i] == b[j]:
            return True
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    return False


#  输出一个序列中的所有概念
def print_list_of_concept(cpt: list) -> None:
    for c in cpt:
        print(c)


#  以显眼的方式输出二维数组
def out_two_dimensional_array(a: list[list]) -> None:
    n = len(a)
    m = len(a[0])
    for i in range(n):
        print(" |-->    ", end="")
        for j in range(m):
            print(a[i][j], end="  ")
        print()
    print()


#  根据形式背景获取基础概念
#  输入：二位数组
#  输出：基础概念
#  对象的命名从1开始，属性的命名从a开始，若属性数量大于26，则属性的命名调整为数字
#  digit = True  ->  强制属性使用数字命名
#  可以通过e1,e2调整开始的位置
#  例如，e1=20 对象从20开始；e2=t 属性从t开始，但要保证属性的最后一位不超过Z；e2=5 将属性的命名调整为数字，并从5开始
def get_base_concept(a, e1 = 1, e2 = 'a', digit = False) -> list:
    if str(e2).isdigit():
        digit = True
    else:
        #  a -> 1     b -> 2
        e2 = str(ord(e2) - ord('a') + 1)
    n = len(a)
    m = len(a[0])
    def get_attribute_name(o):
        if not digit:
            if m + int(e2) > 27:
                return o
            else:
                return chr(o + 96)
        else:
            return o
    base_cpt = []
    for i in range(n):
        cpt = concept([], [])
        cpt.X.append(i + e1)
        for j in range(m):
            if a[i][j] == 1:
                cpt.A.append(get_attribute_name(j + int(e2)))
        base_cpt.append(cpt)
    return base_cpt


#  获取所有概念
#  输入：是一个二维数组a；或由二维数组得到的基础概念get_base_concept(a)
#      额外的输入用于 get_base_concept()
#  输出：所有概念
def get_all_concept(base_cpt: list, e1 = 1, e2 = 'a', digit = False) -> list:
    if isinstance(base_cpt[0], list):
        base_cpt = get_base_concept(base_cpt, e1, e2, digit)

    num_of_cpt = len(base_cpt)
    if num_of_cpt == 1:
        return base_cpt

    #  检查顶部概念
    top_flg = False
    attribute_list = base_cpt[0].A
    for cpt in base_cpt:
        attribute_list = intersection(attribute_list, cpt.A)
    if len(attribute_list) == 0:
        top_flg = True
    def get_top_concept():
        top_cpt = concept([], [])
        for cpt in base_cpt:
            top_cpt.X = union(top_cpt.X, cpt.X)
        return top_cpt
    
    #  使用两个数组交替存放上一轮的结果
    all_cpt = [[], []]

    #  首先插入底部的（phi，all）元素和第一个元素
    bottom_cpt = concept([], [])
    for i in range(num_of_cpt):
        bottom_cpt.A = union(bottom_cpt.A, base_cpt[i].A)
    all_cpt[0].append(bottom_cpt)
    all_cpt[0].append(base_cpt[0])

    #  使用两个数组交替存放结果, 每次循环后 交换两个数组的作用
    #  使用cur、res表示两个数组，每次循环后交换位置
    #  *首次循环时，所有概念存放在0中，循环结束后结果存放在1中
    #  *在程序循环中，始终操作/计算cur中的概念，将结果存放在res中
    cur, res = 1, 0
    for i in range(1, num_of_cpt):
        cur, res = res, cur

        #  当前需要插入的概念
        insert_cpt = base_cpt[i]

        #  遍历所有概念 （R）
        size_of_R = len(all_cpt[cur])
        for j in range(size_of_R):
            #  当前正在访问的概念
            cpt = all_cpt[cur][j]
            #  判断属性是否存在交集
            if determine_intersection(insert_cpt.A, cpt.A):
                #  存在交集，将两者合并得到新概念
                new_cpt = concept(union(cpt.X, insert_cpt.X), intersection(cpt.A, insert_cpt.A))
                #  遍历已生成的所有概念，判断是否存在一个概念，其内涵等于new_cpt的内涵    有 ：True  没有 ： False
                flg = False
                size_of_L = len(all_cpt[res])
                for k in range(size_of_L):
                    if new_cpt.A == all_cpt[res][k].A:
                        #  若有，更新这个概念的对象
                        if all_cpt[res][k].X != new_cpt.X:
                            all_cpt[res][k].X = union(all_cpt[res][k].X, new_cpt.X)
                        #  保存当前访问的概念
                        if all_cpt[res][k].A != cpt.A:
                            all_cpt[res].append(cpt)
                        flg = True
                        break
                #  end for
                #  若没有，则插入合并后的概念
                if not flg:
                    all_cpt[res].append(new_cpt)
                    #  保存当前访问的概念
                    if new_cpt.A != cpt.A:
                        all_cpt[res].append(cpt)
            # end if
            #  不存在交集
            else:
                all_cpt[res].append(cpt)
        #  end for
        #  本次循环结束，清空R，用于下次存放结果
        all_cpt[cur].clear()
    #  end for

    #  检查顶部概念
    if top_flg:
        all_cpt[res].append(get_top_concept())

    all_cpt[res].sort()

    return all_cpt[res]


#  建立父子关系
def lattice_build(all_cpt: list):
    n = len(all_cpt)
    for i in range(n):
        for j in range(i + 1, n):
            flg = True
            if is_sub(all_cpt[i].X, all_cpt[j].X):
                #  判断这个概念是否是父概念的父概念
                for father_cpt in all_cpt[i].father:
                    if is_sub(father_cpt.X, all_cpt[j].X):
                        flg = False
                        break
                if flg:
                    all_cpt[i].father.append(all_cpt[j])
                    all_cpt[j].children.append(all_cpt[i])


def main():

    #  输入二维数组
    a = [
         [1, 1, 0, 1, 1],
         [1, 1, 1, 0, 0],
         [0, 0, 0, 1, 0],
         [1, 1, 1, 0, 0],
    ]

    #  获取所有概念
    all_cpt = get_all_concept(a)

    print("---------------")
    print_list_of_concept(all_cpt)
    print("概念总数是：", len(all_cpt))


    #  建立父子关系
    # lattice_build(all_cpt)

    # for cpt in all_cpt:
    #     print("---------------")
    #     print("当前概念是：", end="")
    #     print(cpt)
    #     print("父概念是：")
    #     print_list_of_concept(cpt.father)
    #     print("子概念是：")
    #     print_list_of_concept(cpt.children)


if __name__ == '__main__':
    main()

