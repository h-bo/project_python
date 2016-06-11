import numpy as np
def load_str_data(filename):
    f = open(filename)
    data = [line.strip().split('\t') for line in f.readlines()]
    return np.array(data)
    
def test_load_str_data():
    filename = 'D:/CsTech/Python/project_python/decision_tree/lenses.txt'
    data = load_str_data(filename)
    print data

test_load_str_data()