#-- encoding:utf-8 --
from __future__ import division
import argparse, math
"""
利用候选词序列词频文件，并计算每个候选词的右(左)邻字熵
由于此脚本只负责算词的邻熵，freq_file可以只包含两字及以上的词
"""
parser = argparse.ArgumentParser()
parser.add_argument("freq_file", help="candidate words file")
parser.add_argument("-s", "--separator", help="field separator", default="\t")
parser.add_argument("-f", "--freq_limit", help="word minimun frequence", default=1, type=int)
parser.add_argument("-r", "--reverse", help="when freq_file is reversed", action="store_true")
parser.add_argument("-o", "--output", help="Candidate Sequence Solidification File")

args = parser.parse_args()

src_file, des_file, freq_limit = args.freq_file, args.output, args.freq_limit

def compute_entropy(neighbours):
    if neighbours:
        right_sum = sum(neighbours)
        #TODO 计算改词的右领字熵，可以怎么优化呢？
        right_prob = map(lambda x:x/right_sum, neighbours)
        right_entropy = sum(map(lambda x:-(x)*math.log(x), right_prob))
        return right_entropy
    else:
        return 0

freq = {}
with open(src_file, 'r') as fs:
    #这里可以优化，只读入满足阈值的词就行
    for line in fs:
        key, count = line.decode('utf-8').rstrip().split(args.separator)
        freq[key] = int(count)

#只计算字长为2，3，4的词
#如果只算词频超过阈值的词，那么组成词的字的词频也一定大于或等于阈值，所以先判断阈值效率会高很多。
words = {word for word, count in freq.iteritems() if count>=freq_limit and 2<=len(word)<=4}
right_distribution = {}
for key, count in freq.iteritems():
    length = len(key)
    if length >= 3 and key[:length-1] in words:
        right_distribution.setdefault(key[:length-1], []).append(count)


entropys = map(lambda x:compute_entropy(right_distribution.get(x, None)), words)
if not args.reverse:
    result = ("%s\t%.9f\n" % (word.encode('utf-8'), entropy) for (word, entropy) in zip(words, entropys))
else:
    result = ("%s\t%.9f\n" % (word[::-1].encode('utf-8'), entropy) for (word, entropy) in zip(words, entropys))
with open(des_file, 'w') as fd:
    fd.writelines(result)

