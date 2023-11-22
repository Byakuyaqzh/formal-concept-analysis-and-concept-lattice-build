class concept:
    def __init__(self, x, y):
        self.X = x
        self.Y = y
    
    def __lt__(self, other):
        if isinstance(other, concept):
            if(self.X == other.X):
                return True if self.Y > other.Y else False
            else:
                return True if self.X < other.X else False
        return False
        

    def __gt__(self, other):
        if isinstance(other, concept):
            if(self.X == other.X):
                return True if self.Y < other.Y else False
            else:
                return True if self.X > other.X else False
        return False
    
    def __eq__(self, other):
        if isinstance(other, concept):
            return self.X == other.X and self.Y == other.Y
        return False
    
    def __str__(self) -> str:
        s = ""
        s += "("
        for x in self.X:
            s += "  " + str(x)
        s += "  ),  ("
        for y in self.Y:
            s += "  " + str(y)
        s += "  )"
        return s


#  输出一个序列中的所有概念
def output_concept_list(all_cpt):
    cnt = 1
    for cpt in all_cpt:
        print(cnt, end=" -> \t")
        print(cpt)
        cnt += 1
    print()


#  第一个值是对象个数， 第二个值： 3 ->  [0, 0.5, 1],  5 -> [0, 0.25, 0.5, 0.75, 1]
def get_table(t):
    ans = [[0 for _ in range(t)] for _ in range(t)]
    val = []
    if t == 3:
        val = [0, 0.5, 1]
    if t == 5:
        val = [0, 0.25, 0.5, 0.75, 1]
    if t == 9:
        val = [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]

    for i in range(t):
        for j in range(t):
            ans[i][j] = min(1, 1 - val[i] + val[j])
    return ans


#  获取x所有可能的排列
def get_all_sort_x(n, t):
    val = []
    if t == 3:
        val = [0, 0.5, 1]
    if t == 5:
        val = [0, 0.25, 0.5, 0.75, 1]
    if t == 9:
        val = [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]
    ans = []
    cur = []
    def dfs(i):
        if i == n:
            ans.append(cur.copy())
            return
        for x in val:
            cur.append(x)
            dfs(i+1)
            cur.pop()
    dfs(0)
    return ans


#  查表
def judge_xy(table, x, y):
    if len(table) == 3:
        return table[int(x * 2)][int(y * 2)]
    if len(table) == 5:
        return table[int(x * 4)][int(y * 4)]
    if len(table) == 9:
        return table[int(x * 6)][int(y * 6)]


#  获取所有概念
def get_all_cpt(table, a, x_list):
    #  all_cpt 存放最后的结果
    all_cpt = []
    n = len(a)
    m = len(a[0])
    num = len(x_list)

    #  遍历所有x的组合
    for i in range(num):
        #  生成的新概念
        cpt = concept([], [])
        cpt.X = x_list[i]
        for j in range(m):
            tmp = []
            for k in range(n):
                tmp.append(judge_xy(table, x_list[i][k], a[k][j]))
            cpt.Y.append(min(tmp))

        #  不去重
        all_cpt.append(cpt)

        #  去重 
        # #  插入总集
        # sizeof_all = len(all_cpt)
        # #  插入第一个
        # if sizeof_all == 0:
        #     all_cpt.append(cpt)
        # #  遍历，检查是否重复   flg :  True -> 不重复   False -> 重复
        # else:
        #     flg = True
        #     for k in range(sizeof_all):
        #         #  重复
        #         if cpt.Y == all_cpt[k].Y:
        #             for g in range(n):
        #                 all_cpt[k].X[g] = max(all_cpt[k].X[g], cpt.X[g])
        #             flg = False
        #             break
        #     #  无重复
        #     if flg:
        #         all_cpt.append(cpt)

    return all_cpt


def main():
    a = [
        [1, 0, 0.5],
        [0.5, 0, 1],
        [0, 0.5, 1],
    ]
    t = 3
    #  t 代表模糊分析的等级    3 ->  [0, 0.5, 1]  ,  5 -> [0, 0.25, 0.5, 0.75, 1]

    n = len(a)

    #  表
    table = get_table(t)

    #  x 所有可能的排列
    x_list = get_all_sort_x(n, t)

    #  通过 表、模糊形式背景、x所有可能的排列，计算所有概念
    all_cpt = get_all_cpt(table, a, x_list)

    #  输出所有概念
    output_concept_list(all_cpt)


if __name__ == "__main__":
    main()
