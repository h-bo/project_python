import numpy as np
def load_str_data(filename):
    f = open(filename)
    data = [line.strip().split('\t') for line in f.readlines()]
    return data

def cal_entropy(data, result):
    N = len(data)
    entropy = 0
    for r in result:
        p = (data == r).sum() / float(N)
        entropy += -p * np.log2(p) if p != 0 else 0
    return entropy

def select_feature(data_a):
    N, data_n = data_a.shape
    feat_n = data_n - 1
    data_set = [list(set([feat for feat in data_a[:, i].tolist()])) for i in xrange(data_n)]
    feat = data_set[:-1]
    result = data_set[-1]
    if len(result) == 1:
        # only one list means the end of dividing
        # and best_feat_name becomes the end class
        best_feat_name = result[0]
        best_feat_list = []
    else:
        # select feature and cal_entropy
        entropy_data = np.zeros((feat_n))
        feat_list = []
        for i in xrange(feat_n):
            feat_list.append([])
            f_c = len(feat[i])
            for j in xrange(f_c):
                index = data_a[:, i] == feat[i][j]
                entropy_data[i] += cal_entropy(data_a[index, -1], result)
                feat_list[i].append(data_a[index])
        best_feat = entropy_data.argmin()
        best_feat_name = feat[best_feat]
        best_feat_list = [np.delete(sublist,best_feat,1) for sublist in feat_list[best_feat]]

    return best_feat_name, best_feat_list

class tree_node(object):

    def __init__(self, name):
        self.name = name
        self.subtree = []

    def print_tree(self):
        print 'tree: %s' %self.name
        print 'subtree: '
        for subname, subtree in self.subtree:
            print 'subname',
        print
        for subname, subtree in self.subtree:
            self.print_tree(subtree)

    def get_depth(self):
        if len(self.subtree) == 0:
            return 1
        else:
            return 1 + max([subtree[1].get_depth() for subtree in self.subtree])

    def get_width(self):
        if len(self.subtree) == 0:
            return 1
        else:
            return sum([subtree[1].get_width() for subtree in self.subtree])

# code below are transformed from machinelearninginaction

def cal(data_a):
    best_feat_name, best_feat_list = select_feature(data_a)
    node = tree_node(best_feat_name)
    for i in xrange(len(best_feat_list)):
        sub_node_name, sub_node = cal(best_feat_list[i])
        node.subtree.append((best_feat_name[i], sub_node))
    return best_feat_name, node

# plot the decision tree
import matplotlib.pyplot as plt

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt,  xycoords='axes fraction',
             xytext=centerPt, textcoords='axes fraction',
             va="center", ha="center", bbox=nodeType, arrowprops=arrow_args )

def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)

def plotTree(tree, parentPt, nodeTxt):#if the first key tells you what feat was split on
    numLeafs = tree.get_width()  #this determines the x width of this tree
    depth = tree.get_depth()
    firstStr = tree.name     #the text label for this node should be this
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    subtree= tree.subtree
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
    for st in subtree:
        if len(st[1].subtree) > 0:    #test to see if the nodes are dictonaires, if not they are leaf nodes
            plotTree(st[1],cntrPt,st[0])        #recursion
        else:   #it's a leaf node print the leaf node
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(st[1].name, (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, st[0])
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD

def createPlot(tree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False)
    plotTree.totalW = tree.get_width()
    plotTree.totalD = tree.get_depth()
    plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0;
    plotTree(tree, (0.5,1.0), '')
    plt.show()

# demo
filename = 'lenses.txt'
data = load_str_data(filename)
data_a = np.array(data)

_, tree = cal(data_a)
createPlot(tree)






