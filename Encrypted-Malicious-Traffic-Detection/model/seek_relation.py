import pandas as pd
import time
from sklearn.utils import shuffle

# 将两个分类随机抽样成1：1的比例
data = pd.read_csv(r"D:\Encrypted-Malicious-Traffic-Detection\total\csv\test\content.csv")
data['label'] = data['label'].replace([0, 1], ['white', 'black'])
print(data['label'])
data0 = data[data['label'] == 'white']
print(data0.shape)
data1 = data[data['label'] == 'black']
print(data1.shape)
n = min(data0.shape[0], data1.shape[0])
print(n)
data1 = data1.sample(n, random_state=123, axis=0)
data_train = pd.concat([data0, data1], axis=0)
data_train = shuffle(data_train)
data_train.to_csv(r"D:\Encrypted-Malicious-Traffic-Detection\total\csv\test\content.csv", index=False)

# 寻求训练集节点中的关联，两个流有公共IP即为有关联
data = pd.read_csv(r"D:\Encrypted-Malicious-Traffic-Detection\total\csv\test\content.csv")

edges1 = []
edges2 = []
src = data['ip.src']
dst = data['ip.dst']

data.index = data.index + 1
data = data.reset_index()
data = data.rename(columns={'index': 'ID'})

ID = data['ID']
for i in range(data.shape[0]):
    # start = time.process_time()
    for j in range(data.shape[0]):
        if i != j and (set([src[j], dst[j]]) & set([src[i], dst[i]]) != set()):
            edges1.append(ID[i])
            edges2.append(ID[j])
    # end = time.process_time()
    # print('Running time: %s Seconds' % (end - start))
    print(i)
edges_unordered = pd.DataFrame({'ID': edges1, 'relative_ID': edges2})
edges_unordered.to_csv(r"D:\Encrypted-Malicious-Traffic-Detection\total\csv\test\adjacency.csv", index=False)

