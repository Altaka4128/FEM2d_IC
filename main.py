from Node2d import Node2d
from d2cps4i import d2cps4i
from Boundary2d import Boundary2d
from FEM2d import FEM2d

def main():

    # 節点リストを定義する
    node1 = Node2d(1, 0.0, 0.0)
    node2 = Node2d(2, 10.0, 0.0)
    node3 = Node2d(3, 20.0, 0.0)
    node4 = Node2d(4, 30.0, 0.0)
    node5 = Node2d(5, 40.0, 0.0)
    node6 = Node2d(6, 50.0, 0.0)
    node7 = Node2d(7, 60.0, 0.0)
    node8 = Node2d(8, 70.0, 0.0)
    node9 = Node2d(9, 80.0, 0.0)
    node10 = Node2d(10, 90.0, 0.0)
    node11 = Node2d(11, 100.0, 0.0)
    node12 = Node2d(12, 0.0, 10.0)
    node13 = Node2d(13, 10.0, 10.0)
    node14 = Node2d(14, 20.0, 10.0)
    node15 = Node2d(15, 30.0, 10.0)
    node16 = Node2d(16, 40.0, 10.0)
    node17 = Node2d(17, 50.0, 10.0)
    node18 = Node2d(18, 60.0, 10.0)
    node19 = Node2d(19, 70.0, 10.0)
    node20 = Node2d(20, 80.0, 10.0)
    node21 = Node2d(21, 90.0, 10.0)
    node22 = Node2d(22, 100.0, 10.0)
    node23 = Node2d(23, 0.0, 20.0)
    node24 = Node2d(24, 10.0, 20.0)
    node25 = Node2d(25, 20.0, 20.0)
    node26 = Node2d(26, 30.0, 20.0)
    node27 = Node2d(27, 40.0, 20.0)
    node28 = Node2d(28, 50.0, 20.0)
    node29 = Node2d(29, 60.0, 20.0)
    node30 = Node2d(30, 70.0, 20.0)
    node31 = Node2d(31, 80.0, 20.0)
    node32 = Node2d(32, 90.0, 20.0)
    node33 = Node2d(33, 100.0, 20.0)
    node34 = Node2d(34, 0.0, 30.0)
    node35 = Node2d(35, 10.0, 30.0)
    node36 = Node2d(36, 20.0, 30.0)
    node37 = Node2d(37, 30.0, 30.0)
    node38 = Node2d(38, 40.0, 30.0)
    node39 = Node2d(39, 50.0, 30.0)
    node40 = Node2d(40, 60.0, 30.0)
    node41 = Node2d(41, 70.0, 30.0)
    node42 = Node2d(42, 80.0, 30.0)
    node43 = Node2d(43, 90.0, 30.0)
    node44 = Node2d(44, 100.0, 30.0)
    node45 = Node2d(45, 0.0, 40.0)
    node46 = Node2d(46, 10.0, 40.0)
    node47 = Node2d(47, 20.0, 40.0)
    node48 = Node2d(48, 30.0, 40.0)
    node49 = Node2d(49, 40.0, 40.0)
    node50 = Node2d(50, 50.0, 40.0)
    node51 = Node2d(51, 60.0, 40.0)
    node52 = Node2d(52, 70.0, 40.0)
    node53 = Node2d(53, 80.0, 40.0)
    node54 = Node2d(54, 90.0, 40.0)
    node55 = Node2d(55, 100.0, 40.0)
    nodes = [node1, node2, node3, node4, node5, node6, node7, node8, node9, node10,
             node11, node12, node13, node14, node15, node16, node17, node18, node19, node20,
             node21, node22, node23, node24, node25, node26, node27, node28, node29, node30,
             node31, node32, node33, node34, node35, node36, node37, node38, node39, node40,
             node41, node42, node43, node44, node45, node46, node47, node48, node49, node50,
             node51, node52, node53, node54, node55]
    nodes1 = [node1, node2, node13, node12]
    nodes2 = [node2, node3, node14, node13]
    nodes3 = [node3, node4, node15, node14]
    nodes4 = [node4, node5, node16, node15]
    nodes5 = [node5, node6, node17, node16]
    nodes6 = [node6, node7, node18, node17]
    nodes7 = [node7, node8, node19, node18]
    nodes8 = [node8, node9, node20, node19]
    nodes9 = [node9, node10, node21, node20]
    nodes10 = [node10, node11, node22, node21]
    nodes11 = [node12, node13, node24, node23]
    nodes12 = [node13, node14, node25, node24]
    nodes13 = [node14, node15, node26, node25]
    nodes14 = [node15, node16, node27, node26]
    nodes15 = [node16, node17, node28, node27]
    nodes16 = [node17, node18, node29, node28]
    nodes17 = [node18, node19, node30, node29]
    nodes18 = [node19, node20, node31, node30]
    nodes19 = [node20, node21, node32, node31]
    nodes20 = [node21, node22, node33, node32]
    nodes21 = [node23, node24, node35, node34]
    nodes22 = [node24, node25, node36, node35]
    nodes23 = [node25, node26, node37, node36]
    nodes24 = [node26, node27, node38, node37]
    nodes25 = [node27, node28, node39, node38]
    nodes26 = [node28, node29, node40, node39]
    nodes27 = [node29, node30, node41, node40]
    nodes28 = [node30, node31, node42, node41]
    nodes29 = [node31, node32, node43, node42]
    nodes30 = [node32, node33, node44, node43]
    nodes31 = [node34, node35, node46, node45]
    nodes32 = [node35, node36, node47, node46]
    nodes33 = [node36, node37, node48, node47]
    nodes34 = [node37, node38, node49, node48]
    nodes35 = [node38, node39, node50, node49]
    nodes36 = [node39, node40, node51, node50]
    nodes37 = [node40, node41, node52, node51]
    nodes38 = [node41, node42, node53, node52]
    nodes39 = [node42, node43, node54, node53]
    nodes40 = [node43, node44, node55, node54]
    
    # 要素セットを定義する
    thickness = 1.5
    young = 210000
    poisson = 0.3
    elem1 = d2cps4i(1, nodes1, thickness, young, poisson)
    elem2 = d2cps4i(2, nodes2, thickness, young, poisson)
    elem3 = d2cps4i(3, nodes3, thickness, young, poisson)
    elem4 = d2cps4i(4, nodes4, thickness, young, poisson)
    elem5 = d2cps4i(5, nodes5, thickness, young, poisson)
    elem6 = d2cps4i(6, nodes6, thickness, young, poisson)
    elem7 = d2cps4i(7, nodes7, thickness, young, poisson)
    elem8 = d2cps4i(8, nodes8, thickness, young, poisson)
    elem9 = d2cps4i(9, nodes9, thickness, young, poisson)
    elem10 = d2cps4i(10, nodes10, thickness, young, poisson)
    elem11 = d2cps4i(11, nodes11, thickness, young, poisson)
    elem12 = d2cps4i(12, nodes12, thickness, young, poisson)
    elem13 = d2cps4i(13, nodes13, thickness, young, poisson)
    elem14 = d2cps4i(14, nodes14, thickness, young, poisson)
    elem15 = d2cps4i(15, nodes15, thickness, young, poisson)
    elem16 = d2cps4i(16, nodes16, thickness, young, poisson)
    elem17 = d2cps4i(17, nodes17, thickness, young, poisson)
    elem18 = d2cps4i(18, nodes18, thickness, young, poisson)
    elem19 = d2cps4i(19, nodes19, thickness, young, poisson)
    elem20 = d2cps4i(20, nodes20, thickness, young, poisson)
    elem21 = d2cps4i(21, nodes21, thickness, young, poisson)
    elem22 = d2cps4i(22, nodes22, thickness, young, poisson)
    elem23 = d2cps4i(23, nodes23, thickness, young, poisson)
    elem24 = d2cps4i(24, nodes24, thickness, young, poisson)
    elem25 = d2cps4i(25, nodes25, thickness, young, poisson)
    elem26 = d2cps4i(26, nodes26, thickness, young, poisson)
    elem27 = d2cps4i(27, nodes27, thickness, young, poisson)
    elem28 = d2cps4i(28, nodes28, thickness, young, poisson)
    elem29 = d2cps4i(29, nodes29, thickness, young, poisson)
    elem30 = d2cps4i(30, nodes30, thickness, young, poisson)
    elem31 = d2cps4i(31, nodes31, thickness, young, poisson)
    elem32 = d2cps4i(32, nodes32, thickness, young, poisson)
    elem33 = d2cps4i(33, nodes33, thickness, young, poisson)
    elem34 = d2cps4i(34, nodes34, thickness, young, poisson)
    elem35 = d2cps4i(35, nodes35, thickness, young, poisson)
    elem36 = d2cps4i(36, nodes36, thickness, young, poisson)
    elem37 = d2cps4i(37, nodes37, thickness, young, poisson)
    elem38 = d2cps4i(38, nodes38, thickness, young, poisson)
    elem39 = d2cps4i(39, nodes39, thickness, young, poisson)
    elem40 = d2cps4i(40, nodes40, thickness, young, poisson)
    elems = [elem1, elem2, elem3, elem4, elem5, elem6, elem7, elem8, elem9, elem10,
             elem11, elem12, elem13, elem14, elem15, elem16, elem17, elem18, elem19, elem20,
             elem21, elem22, elem23, elem24, elem25, elem26, elem27, elem28, elem29, elem30,
             elem31, elem32, elem33, elem34, elem35, elem36, elem37, elem38, elem39, elem40]

    # 境界条件を設定する
    bound = Boundary2d(len(nodes))
    bound.addSPC(1, 0.0, 0.0)
    bound.addSPC(12, 0.0, 0.0)
    bound.addSPC(23, 0.0, 0.0)
    bound.addSPC(34, 0.0, 0.0)
    bound.addSPC(45, 0.0, 0.0)
    bound.addForce(33, 0.0, -1000.0)

    # 解析を行う
    fem = FEM2d(nodes, elems, bound)
    fem.analysis()

    # Text形式で結果を出力する
    fem.outputTxt("output")


main()