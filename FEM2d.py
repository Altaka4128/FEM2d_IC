import numpy as np
import numpy.linalg as LA
from Boundary2d import Boundary2d

class FEM2d:
    # コンストラクタ
    # nodes    : 全節点のリスト(節点は1から始まる順番で並んでいる前提, Node2d型のリスト)
    # elements : 全要素のリスト(d2cps4iのリスト)
    # bound    : 境界条件(d2Boundary型)
    def __init__(self, nodes, elements, bound):
        self.nodes = nodes         # 全節点のリスト(Node2d型のリスト)
        self.elements = elements   # 全要素のリスト(d2cps4iのリスト)
        self.bound = bound         # 境界条件(d2Boundary型)

    # 解析を行う
    def analysis(self):

        # 境界条件を考慮しないKマトリクスを作成する
        matK = self.makeKmatrix()

        # 節点に負荷する荷重ベクトルを作成する
        vecf = self.bound.makeForceVector()

        # 境界条件を考慮したKマトリクス、荷重ベクトルを作成する
        matKc, vecfc, condiNum = self.setBoundCondition(matK, vecf)

        # 変位ベクトルを計算する
        vecTmp = LA.solve(matKc, vecfc)
        vecDisp = np.delete(vecTmp, slice(len(vecTmp) - condiNum, len(vecTmp)))
        self.vecDisp = vecDisp

        # 変位ベクトルから要素の出力データを計算する
        vecIpStrainsList = []
        vecIpStressList = []
        ipMisesList = []
        for elem in self.elements:
            vecElemDisp = np.zeros(len(elem.nodes) * 2)
            for i in range(len(elem.nodes)):
                vecElemDisp[i * 2] = vecDisp[(elem.nodes[i].no - 1) * 2]
                vecElemDisp[i * 2 + 1] = vecDisp[(elem.nodes[i].no - 1) * 2 + 1]
            vecIpStrains, vecIpStresses, ipMises = elem.makeOutputData(vecElemDisp)
            vecIpStrainsList.append(vecIpStrains)
            vecIpStressList.append(vecIpStresses)
            ipMisesList.append(ipMises)
        self.vecIpStrainsList = vecIpStrainsList
        self.vecIpStressList = vecIpStressList
        self.ipMisesList = ipMisesList

        # 節点反力を計算する
        vecRF = np.array(matK @ vecDisp - vecf).flatten()
        self.vecRF = vecRF
    
    # 境界条件を考慮しないKマトリクスを作成する
    def makeKmatrix(self):

        matK = np.matrix(np.zeros((len(self.nodes) * 2, len(self.nodes) * 2)))
        for elem in self.elements:
            # keマトリクスを計算する
            matKe = elem.makeKematrix()

            # Kマトリクスに代入する
            for c in range(len(elem.nodes) * 2):
                ct = (elem.nodes[c // 2].no - 1) * 2 + c % 2
                for r in range(len(elem.nodes) * 2):
                    rt = (elem.nodes[r // 2].no - 1) * 2 + r % 2
                    matK[ct, rt] += matKe[c, r]
        return matK

    # Kマトリクス、荷重ベクトルに境界条件を考慮する
    def setBoundCondition(self, matK, vecf):

        matKc = np.copy(matK)
        vecfc = np.copy(vecf)

        # 単点拘束条件を考慮したKマトリクス、荷重ベクトルを作成する
        vecDisp = self.bound.makeDispVector()
        for i in range(len(vecDisp)):
            if not vecDisp[i] == None:
                # Kマトリクスからi列を抽出する
                vecx = np.array(matK[:, i]).flatten()

                # 変位ベクトルi列の影響を荷重ベクトルに適用する
                vecfc = vecfc - vecDisp[i] * vecx

                # Kマトリクスのi行、i列を全て0にし、i行i列の値を1にする
                matKc[:, i] = 0.0
                matKc[i, :] = 0.0
                matKc[i, i] = 1.0
        for i in range(len(vecDisp)):
            if not vecDisp[i] == None:
                vecfc[i] = vecDisp[i]

        # 多節点拘束条件を考慮したKマトリクス、荷重ベクトルを作成する
        matC, vecd = self.bound.makeMPCmatrixes()
        mpcNum = len(vecd)   # 多節点拘束の条件式の数を求める
        if mpcNum > 0:
            matKc = np.hstack((matKc, matC.T))
            tmpMat = np.hstack((matC, np.zeros((matC.shape[0], matC.shape[0]))))
            matKc = np.vstack((matKc, tmpMat))
            vecfc = np.hstack((vecf, vecd))

        return matKc, vecfc, mpcNum

    # 解析結果をテキストファイルに出力する
    def outputTxt(self, filePath):

        # ファイルを作成し、開く
        f = open(filePath + ".txt", 'w')

        # 出力する文字の情報を定義する
        columNum = 18
        floatDigits = ".10g"

        # 入力データのタイトルを書きこむ
        f.write("*********************************\n")
        f.write("*          Input Data           *\n")
        f.write("*********************************\n")
        f.write("\n")

        # 節点情報を出力する
        f.write("***** Node Data ******\n")
        f.write("No".rjust(columNum) + "X".rjust(columNum) + "Y".rjust(columNum) +  "\n")
        f.write("-" * columNum * 3 + "\n")
        for node in self.nodes:
            strNo = str(node.no).rjust(columNum)
            strX = str(format(node.x, floatDigits).rjust(columNum))
            strY = str(format(node.y, floatDigits).rjust(columNum))
            f.write(strNo + strX + strY + "\n")
        f.write("\n")

        # 要素情報を出力する
        f.write("***** Element Data ******\n")
        f.write("No".rjust(columNum) + "Type".rjust(columNum) + "Node No".rjust(columNum) + 
                "Thickness".rjust(columNum) + "Young".rjust(columNum) + "Poisson".rjust(columNum) + "\n")
        f.write("-" * columNum * 6 + "\n")
        for elem in self.elements:
            strNo = str(elem.no).rjust(columNum)
            strType = str(elem.__class__.__name__ ).rjust(columNum)
            strNodeNo = ""
            for node in elem.nodes:
                strNodeNo += " " + str(node.no)
            strNodeNo = strNodeNo.rjust(columNum)
            strThickness = str(format(elem.thickness, floatDigits).rjust(columNum))
            strYoung = str(format(elem.young, floatDigits).rjust(columNum))
            strPoisson = str(format(elem.poisson, floatDigits).rjust(columNum))
            f.write(strNo + strType + strNodeNo + strThickness + strYoung + strPoisson + "\n")
        f.write("\n")

        # 単点拘束情報を出力する
        f.write("***** SPC Constraint Data ******\n")
        f.write("NodeNo".rjust(columNum) + "X Displacement".rjust(columNum) + "Y Displacement".rjust(columNum) + "\n")
        f.write("-" * columNum * 3 + "\n")
        for i in range(len(self.bound.dispNodeNo)):
            strNo = str(self.bound.dispNodeNo[i]).rjust(columNum)
            strXDisp = "None".rjust(columNum)
            if not self.bound.dispX[i] is None:
                strXDisp = str(format(self.bound.dispX[i], floatDigits).rjust(columNum))
            strYDisp = "None".rjust(columNum)
            if not self.bound.dispY[i] is None:
                strYDisp = str(format(self.bound.dispY[i], floatDigits).rjust(columNum))
            f.write(strNo + strXDisp + strYDisp + "\n")
        f.write("\n")

        # 多点拘束情報を出力する
        matC, vecd = self.bound.makeMPCmatrixes()
        f.write("***** MPC Constraint Data ******\n")
        f.write("-" * columNum * 1 + "\n")
        for i in range(matC.shape[0]):
            strRow = ""
            for j in range(matC.shape[1]):
                if not matC[i, j] == 0:
                    strTmp = " " + str(format(matC[i, j], "+.3g"))
                    if (j % 2) == 0:
                        strTmp += " u" + str(j // 2 + 1)
                    else :
                        strTmp += " v" + str(j // 2 + 1)
                    strRow += strTmp.rjust(5)
            strRow += "= " + str(format(vecd[i], ".3g"))
            f.write(strRow + "\n")
        f.write("\n")

        # 荷重条件を出力する
        f.write("***** Nodal Force Data ******\n")
        f.write("NodeNo".rjust(columNum) + "X Force".rjust(columNum) + "Y Force".rjust(columNum) + "\n")
        f.write("-" * columNum * 3 + "\n")
        vecf = self.bound.makeForceVector()
        for i in range(len(self.nodes)):
            if not vecf[2 * i] == 0 or not vecf[2 * i + 1] == 0:
                strNo = str(i + 1).rjust(columNum)
                strXForce = str(format(vecf[2 * i], floatDigits).rjust(columNum))
                strYForce = str(format(vecf[2 * i + 1], floatDigits).rjust(columNum))
                f.write(strNo + strXForce + strYForce + "\n")
        f.write("\n")

        # 結果データのタイトルを書きこむ
        f.write("**********************************\n")
        f.write("*          Result Data           *\n")
        f.write("**********************************\n")
        f.write("\n")

        # 変位のデータを出力する
        f.write("***** Displacement Data ******\n")
        f.write("NodeNo".rjust(columNum) + "Magnitude".rjust(columNum) + "X Displacement".rjust(columNum) +
                "Y Displacement".rjust(columNum) + "\n")
        f.write("-" * columNum * 4 + "\n")
        for i in range(len(self.nodes)):
            strNo = str(i + 1).rjust(columNum)
            mag = np.linalg.norm(np.array((self.vecDisp[2 * i], self.vecDisp[2 * i + 1])))
            strMag = str(format(mag, floatDigits).rjust(columNum))
            strXDisp = str(format(self.vecDisp[2 * i], floatDigits).rjust(columNum))
            strYDisp = str(format(self.vecDisp[2 * i + 1], floatDigits).rjust(columNum))
            f.write(strNo + strMag + strXDisp + strYDisp + "\n")            
        f.write("\n")

        # 応力データを出力する
        f.write("***** Stress Data ******\n")
        f.write("Element No".rjust(columNum) + "Integral No".rjust(columNum) + "Stress XX".rjust(columNum) + "Stress YY".rjust(columNum) + 
                "Stress XY".rjust(columNum) + "Mises".rjust(columNum) + "\n")
        f.write("-" * columNum * 6 + "\n")
        
        for i in range(len(self.elements)):
            elem = self.elements[i]
            strElemNo = str(elem.no).rjust(columNum)
            for j in range(elem.ipNum):
                strIntNo = str(j + 1).rjust(columNum)
                vecIpStresses = self.vecIpStressList[i]
                strStressXX = str(format(vecIpStresses[j][0], floatDigits).rjust(columNum))
                strStressYY = str(format(vecIpStresses[j][1], floatDigits).rjust(columNum))
                strStressXY = str(format(vecIpStresses[j][2], floatDigits).rjust(columNum))
                ipMises = self.ipMisesList[i]
                strMises = str(format(ipMises[j], floatDigits).rjust(columNum))
                f.write(strElemNo + strIntNo + strStressXX + strStressYY + strStressXY + strMises + "\n")
        f.write("\n")

        # ひずみデータを出力する
        f.write("***** Strain Data ******\n")
        f.write("Element No".rjust(columNum) + "Integral No".rjust(columNum) + "Strain XX".rjust(columNum) + "Strain YY".rjust(columNum) + 
                "Strain XY".rjust(columNum) + "\n")
        f.write("-" * columNum * 5 + "\n")
        
        for i in range(len(self.elements)):
            elem = self.elements[i]
            strElemNo = str(elem.no).rjust(columNum)
            for j in range(elem.ipNum):
                strIntNo = str(j + 1).rjust(columNum)
                vecIpStrains = self.vecIpStrainsList[i]
                strStrainXX = str(format(vecIpStrains[j][0], floatDigits).rjust(columNum))
                strStrainYY = str(format(vecIpStrains[j][1], floatDigits).rjust(columNum))
                strStrainXY = str(format(vecIpStrains[j][2], floatDigits).rjust(columNum))
                f.write(strElemNo + strIntNo + strStrainXX + strStrainYY + strStrainXY + "\n")
        f.write("\n")

        # 反力のデータを出力する
        f.write("***** Reaction Force Data ******\n")
        f.write("NodeNo".rjust(columNum) + "Magnitude".rjust(columNum) + "X Force".rjust(columNum) + "Y Force".rjust(columNum) + "\n")
        f.write("-" * columNum * 4 + "\n")
        for i in range(len(self.nodes)):
            strNo = str(i + 1).rjust(columNum)
            mag = np.linalg.norm(np.array((self.vecRF[2 * i], self.vecRF[2 * i + 1])))
            strMag = str(format(mag, floatDigits).rjust(columNum))
            strXForce = str(format(self.vecRF[2 * i], floatDigits).rjust(columNum))
            strYForce = str(format(self.vecRF[2 * i + 1], floatDigits).rjust(columNum))
            f.write(strNo + strMag + strXForce + strYForce + "\n")            
        f.write("\n")

        # ファイルを閉じる
        f.close()


# テスト用
from Node2d import Node2d
from d2cps4i import d2cps4i

# d2cps4iのテスト
def test():
    node1 = Node2d(1, 0.0, 0.0)
    node2 = Node2d(2, 10.0, 0.0)
    node3 = Node2d(3, 0.0, 10.0)
    node4 = Node2d(4, 10.0, 10.0)
    nodes = [node1, node2, node3, node4]
    nodes1 = [node1, node2, node4, node3]

    thickness = 1.5
    young = 210000.0
    poisson = 0.3
    elem1 = d2cps4i(1, nodes1, thickness, young, poisson)
    elems = [elem1]

    bound = Boundary2d(len(nodes))
    bound.addSPC(1, 0.0, 0.0)
    bound.addSPC(3, 0.0, 0.0)
    bound.addForce(2, 0.0, -100.0)
    bound.addForce(4, 0.0, -100.0)

    fem = FEM2d(nodes, elems, bound)
    fem.analysis()
    fem.outputTxt("D:\ParaViewFile\\FEM2dtest12")


if __name__ == '__main__':
    test()