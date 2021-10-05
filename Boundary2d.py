import numpy as np

class Boundary2d:
    # コンストラクタ
    # nodeNum : 節点数
    def __init__(self, nodeNum):
        # インスタンス変数を定義する
        self.nodeNum = nodeNum  # 全節点数
        self.dispNodeNo = []    # 単点拘束の節点番号
        self.dispX = []         # 単点拘束の強制変位x
        self.dispY = []         # 単点拘束の強制変位y
        self.forceNodeNo = []   # 荷重が作用する節点番号
        self.forceX = []        # x方向の荷重
        self.forceY = []        # y方向の荷重
        self.matC = np.empty((0, self.nodeNum * 2))   # 多点拘束用のCマトリクス
        self.vecd = np.empty(0)                       # 多点拘束用のdベクトル

    # 単点拘束を追加する
    def addSPC(self, nodeNo, x, y):

        self.dispNodeNo.append(nodeNo)
        self.dispX.append(x)
        self.dispY.append(y)

    # 多点拘束を追加する
    # 条件式 : vecC x u = d
    def addMPC(self, vecC, d):
        self.matC = np.vstack((self.matC, vecC))
        self.vecd = np.hstack((self.vecd, d))

    # 単点拘束条件から変位ベクトルを作成する
    def makeDispVector(self):

        vecd = np.array([None] * self.nodeNum * 2)
        for i in range(len(self.dispNodeNo)):
            vecd[(self.dispNodeNo[i] - 1) * 2] = self.dispX[i]
            vecd[(self.dispNodeNo[i] - 1) * 2 + 1] = self.dispY[i]
        
        return vecd
    
    # 荷重を追加する
    def addForce(self, nodeNo, fx, fy):
        
        self.forceNodeNo.append(nodeNo)
        self.forceX.append(fx)
        self.forceY.append(fy)
    
    # 境界条件から荷重ベクトルを作成する
    def makeForceVector(self):

        vecf = np.array(np.zeros([self.nodeNum * 2]))
        for i in range(len(self.forceNodeNo)):
            vecf[(self.forceNodeNo[i] - 1) * 2] += self.forceX[i]
            vecf[(self.forceNodeNo[i] - 1) * 2 + 1] += self.forceY[i]
        
        return vecf

    # 多点拘束の境界条件を表すCマトリクス、dベクトルを作成する
    def makeMPCmatrixes(self):
        
        return self.matC, self.vecd

    # 拘束条件を出力する
    def printBoundary(self):
        print("Node Number: ", self.nodeNum)
        print("SPC Constraint Condition")
        for i in range(len(self.dispNodeNo)):
            print("Node No: " + str(self.dispNodeNo[i]) + ", x: " + str(self.dispX[i]) + ", y: " + str(self.dispY[i]))
        print("Force Condition")
        for i in range(len(self.forceNodeNo)):
            print("Node No: " + str(self.forceNodeNo[i]) + ", x: " + str(self.forceX[i]) + ", y: " + str(self.forceY[i]))
        print("MPC Constraint Condition")
        print("C x u = q")
        print("C Matrix")
        print(self.matC)
        print("q vector")
        print(self.vecd)

# テスト用
def test1():
    NodeNum = 8
    bound = Boundary2d(NodeNum)
    bound.addSPC(1, 0.0, 0.0)
    bound.addSPC(4, 0.0, 0.0)
    bound.addForce(5, 100.0, 0.0)
    
    bound.printBoundary()
    print("Disp Vector(SPC)")
    print(bound.makeDispVector())
    print("Force Vector")
    print(bound.makeForceVector())

def test2():
    NodeNum = 4
    bound = Boundary2d(NodeNum)
    bound.addSPC(1, 0.0, None)
    bound.addSPC(2, None, 10.0)
    bound.addSPC(3, 0.0, 10.0)
    bound.addForce(4, 100.0, 0.0)
    bound.addForce(4, 0.0, 10.0)
    
    bound.printBoundary()
    print("Disp Vector(SPC)")
    print(bound.makeDispVector())
    print("Force Vector")
    print(bound.makeForceVector())

def test3():
    NodeNum = 4
    bound = Boundary2d(NodeNum)
    mpc1 = np.array([1, 1, 0, 0, 0, 0, 0, 0])   # mpcの条件式1
    d1 = 0.0
    mpc2 = np.array([0, 0, 1, 0, 0, 0, 0, 0])
    d2 = 10.0
    bound.addMPC(mpc1, d1)
    bound.addMPC(mpc2, d2)
    bound.addForce(4, 100.0, 0.0)
    
    bound.printBoundary()

if __name__ == '__main__':
    test1()
    test2()
    test3()