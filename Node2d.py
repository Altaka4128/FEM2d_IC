class Node2d:
    # コンストラクタ
    # no : 節点番号
    # x  : x座標
    # y  : y座標
    def __init__(self, no, x, y):
        self.no = no   # 節点番号
        self.x = x     # x座標
        self.y = y     # y座標

    # 節点の情報を表示する
    def printNode(self):
        print("Node No: %d, x: %f, y: %f" % (self.no, self.x, self.y))

# テスト用
if __name__ == '__main__':
    p1 = Node2d(1, 1.0, 1.0)
    p2 = Node2d(2, 2.0, 2.0)

    print("Point1(%f, %f)" % (p1.x, p1.y))
    print("Point2(%f, %f)" % (p2.x, p2.y))
    print(p1.printNode())
    print(p2.printNode())