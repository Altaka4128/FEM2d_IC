import numpy as np
import numpy.linalg as LA
from Dmatrix2d import Dmatrix2d

# 2次元平面応力4節点不適合要素のクラス
class d2cps4i:
    # コンストラクタ
    # no          : 要素番号
    # nodes       : 節点の集合(Node2d型のリスト)
    # thickness   : 厚さ
    # young       : ヤング率
    # poisson     : ポアソン比
    def __init__(self, no, nodes, thickness, young, poisson):

        # インスタンス変数を定義する
        self.no = no                           # 要素番号
        self.nodes = nodes                     # nodesは反時計回りの順番になっている前提(Node2d型のリスト形式)
        self.thickness = thickness             # 厚さ
        self.young = young                     # ヤング率
        self.poisson = poisson                 # ポアソン比
        self.ipNum = 4                         # 積分点の数
        self.w1 = [1.0, 1.0, 1.0, 1.0]         # 積分点の重み係数1
        self.w2 = [1.0, 1.0, 1.0, 1.0]         # 積分点の重み係数2
        self.ai = [-np.sqrt(1.0 / 3.0), np.sqrt(1.0 / 3.0), -np.sqrt(1.0 / 3.0), np.sqrt(1.0 / 3.0)]   # 積分点の座標(a,b座標系)
        self.bi = [-np.sqrt(1.0 / 3.0), -np.sqrt(1.0 / 3.0), np.sqrt(1.0 / 3.0), np.sqrt(1.0 / 3.0)]   # 積分点の座標(a,b座標系)

        # Dマトリクスを計算する
        self.matD = self.makeDmatrix()

        # ヤコビ行列を計算する
        self.matJ = []
        for i in range(self.ipNum):
            self.matJ.append(self.makeJmatrix(self.ai[i], self.bi[i]))

        # Bマトリクスを計算する
        self.matB = []
        for i in range(self.ipNum):
            self.matB.append(self.makeBmatrix(self.ai[i], self.bi[i], self.matJ[i]))

        # Biマトリクスを計算する
        self.matBi = self.makeBimatirixes()

        # Kciマトリクスを計算する
        self.matKci = self.makeKcimatrix()

        # Kiiマトリクスを計算する
        self.matKii = self.makeKiimatrix()
    
    # Keマトリクスを作成する
    def makeKematrix(self):
        
        # Kccマトリクスをガウス積分で計算する
        matKcc = np.matrix(np.zeros([8, 8]))
        for i in range(self.ipNum):
            matKcc += self.w1[i] * self.w2[i] * self.matB[i].T * self.matD * self.matB[i] * LA.det(self.matJ[i])
        matKcc *= self.thickness

        # Keマトリクスを計算する
        matKe = matKcc - self.matKci * LA.inv(self.matKii) * self.matKci.T

        return matKe

    # kiiマトリクスを作成する
    def makeKiimatrix(self):

        matKii = np.matrix(np.zeros([4, 4]))
        for i in range(self.ipNum):
            matKii += self.w1[i] * self.w2[i] * self.matBi[i].T * self.matD * self.matBi[i] * LA.det(self.matJ[i])
        matKii *= self.thickness

        return matKii
    
    # Kciマトリクスを作成する
    def makeKcimatrix(self):

        matKci = np.matrix(np.zeros([8, 4]))
        for i in range(self.ipNum):
            matKci += self.w1[i] * self.w2[i] * self.matB[i].T * self.matD * self.matBi[i] * LA.det(self.matJ[i])
        matKci *= self.thickness

        return matKci

    # ヤコビ行列を計算する
    # ai : a座標値
    # bi : b座標値
    def makeJmatrix(self, ai, bi):

         # dNdabを計算する
        dNdab = self.makedNdab(ai, bi)
        
        # xi, yiの行列を計算する
        matxiyi = np.matrix([[self.nodes[0].x, self.nodes[0].y],
                             [self.nodes[1].x, self.nodes[1].y],
                             [self.nodes[2].x, self.nodes[2].y],
                             [self.nodes[3].x, self.nodes[3].y]])

        # ヤコビ行列を計算する
        matJ = dNdab * matxiyi

        # ヤコビアンが負にならないかチェックする
        if LA.det(matJ) < 0:
            raise ValueError("要素の計算に失敗しました")
        
        return matJ

    # Dマトリクスを作成する
    def makeDmatrix(self):

        d2dmat = Dmatrix2d(self.young, self.poisson)
        matD = d2dmat.makeDcpsmatrix()

        return matD

    # Bマトリクスを作成する
    # a   : a座標値
    # b   : b座標値
    # matJ : 座標(a,b)のヤコビ行列(np.matrix型)
    def makeBmatrix(self, a, b, matJ):

        # dNdabを計算する
        dNdab = self.makedNdab(a, b)

        #dNdxy = matJinv * matdNdab
        dNdxy = LA.solve(matJ, dNdab)
        
        # Bマトリクスを計算する
        matB = np.matrix([[dNdxy[0, 0], 0.0, dNdxy[0, 1], 0.0, dNdxy[0, 2], 0.0, dNdxy[0, 3], 0.0],
                          [0.0, dNdxy[1, 0], 0.0, dNdxy[1, 1], 0.0, dNdxy[1, 2], 0.0, dNdxy[1, 3]],
                          [dNdxy[1, 0], dNdxy[0, 0], dNdxy[1, 1], dNdxy[0, 1], dNdxy[1, 2], dNdxy[0, 2], dNdxy[1, 3], dNdxy[0, 3]]])
        
        return matB

    # dNdabの行列を計算する
    # a   : a座標値
    # b   : b座標値
    def makedNdab(self, a, b):

        # dNi/da, dNi/dbを計算する
        dN1da = -0.25 * (1 - b)
        dN2da = 0.25 * (1 - b)
        dN3da = 0.25 * (1 + b)
        dN4da = -0.25 * (1 + b)
        dN1db = -0.25 * (1 - a)
        dN2db = -0.25 * (1 + a)
        dN3db = 0.25 * (1 + a)
        dN4db = 0.25 * (1 - a)

        # dNdabを計算する
        dNdab = np.matrix([[dN1da, dN2da, dN3da, dN4da],
                           [dN1db, dN2db, dN3db, dN4db]])
        
        return dNdab

    # 補正されたBiマトリクスのリストを作成する
    def makeBimatirixes(self):

         # Biマトリクスを計算する
        matBi = []
        sumdetJ = 0
        sumMatBidetJ = np.zeros((3, 4))
        for i in range(self.ipNum):
            matJinv = LA.inv(self.matJ[i])
            dadx = matJinv[0,0]
            dbdx = matJinv[0,1]
            dady = matJinv[1,0]
            dbdy = matJinv[1,1]
            matBiTmp = np.matrix([[-2 * self.ai[i] * dadx, -2 * self.bi[i] * dbdx, 0, 0],
                                  [0, 0, -2 * self.ai[i] * dady, -2 * self.bi[i] * dbdy],
                                  [-2 * self.ai[i] * dady, -2 * self.bi[i] * dbdy, -2 * self.ai[i] * dadx, -2 * self.bi[i] * dbdx]])
            matBi.append(matBiTmp)

            # 補正項を求めるためにガウス積分を計算する
            sumdetJ += self.w1[i] * self.w2[i] * LA.det(self.matJ[i])
            sumMatBidetJ += self.w1[i] * self.w2[i] * matBiTmp * LA.det(self.matJ[i])

        # Biマトリクスに補正項を追加する
        matBic = -sumMatBidetJ / sumdetJ
        for i in range(self.ipNum):
            matBi[i] += matBic

        return matBi

    # 要素の出力データを作成する
    # vecElemDisp : 要素節点の変位のリスト
    def makeOutputData(self, vecElemDisp):
        
        # 積分点の応力、ひずみを計算する
        vecIpStrains = []    # 積分点のひずみベクトルのリスト(np.array型のリスト)
        vecIpStresses = []   # 積分点の応力ベクトルのリスト(np.array型のリスト)
        ipMises = []         # 積分点のミーゼス応力のリスト
        for i in range(self.ipNum):

            # 積分点のひずみベクトルを計算する
            vec1 = np.array(self.matB[i] @ vecElemDisp).flatten()
            vec2 = np.array(self.matBi[i] * LA.inv(self.matKii) * self.matKci.T @ vecElemDisp).flatten()
            vecIpStrain = vec1 - vec2
            vecIpStrains.append(vecIpStrain) 

            # 積分点の応力ベクトルを計算する
            vecIpStress = np.array(self.matD @ vecIpStrains[i]).flatten()
            vecIpStresses.append(vecIpStress)

            # 積分点のミーゼス応力を計算する
            tmp = np.square(vecIpStress[0] - vecIpStress[1]) + np.square(vecIpStress[0]) + np.square(vecIpStress[1]) + 6 * np.square(vecIpStress[2])
            mises = np.sqrt(0.5 * tmp)
            ipMises.append(mises)

        return vecIpStrains, vecIpStresses, ipMises
        
# テスト用
from Node2d import Node2d

if __name__ == '__main__':
    node1 = Node2d(1, 0.0, 0.0)
    node2 = Node2d(2, 1.0, 0.0)
    node3 = Node2d(3, 1.0, 1.0)
    node4 = Node2d(4, 0.0, 1.0)
    nodes = [node1, node2, node3, node4]
    thickness = 2.0
    young = 210000
    poisson = 0.3

    elem1 = d2cps4i(1, nodes, thickness, young, poisson)
    matKe1 = elem1.makeKematrix()

    vecDisp = [0.0, 0.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5]
    vecIpStrains, vecIpStresses, ipMises = elem1.makeOutputData(vecDisp)

    print(matKe1)
    print(vecIpStrains)
    print(vecIpStresses)
    print(ipMises)