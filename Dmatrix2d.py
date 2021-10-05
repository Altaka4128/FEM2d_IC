import numpy as np

class Dmatrix2d:
    # コンストラクタ
    # young   : ヤング率
    # poisson : ポアソン比
    def __init__(self, young, poisson):
        self.young = young
        self.poisson = poisson
    
    # 平面応力状態のDマトリクスを作成する
    def makeDcpsmatrix(self):
        coef = self.young / (1 - self.poisson * self.poisson)
        matD = np.matrix([[1.0, self.poisson, 0.0],
                          [self.poisson, 1.0, 0.0],
                          [0.0, 0.0, 0.5 * (1 - self.poisson)]])
        matD *= coef

        return matD

    # 平面ひずみ状態のDマトリクスを作成する
    def makeDcpematrix(self):
        coef = self.young / ((1.0 - 2 * self.poisson) * (1.0 + self.poisson))
        matD = np.matrix([[1.0 - self.poisson, self.poisson, 0.0],
                          [self.poisson, 1.0 - self.poisson, 0.0],
                          [0.0, 0.0, 0.5 * (1 - 2 * self.poisson)]])
        matD *= coef

        return matD

# テスト用
if __name__ == '__main__':
    mat = Dmatrix2d(210000, 0.3)
    print(mat.makeDcpsmatrix())
    print(mat.makeDcpematrix())
