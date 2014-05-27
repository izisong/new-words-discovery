#-- encoding:utf-8 --
from __future__ import division
import argparse, math
"""
利用候选词序列词频文件，并计算每个候选词的凝固度
"""
parser = argparse.ArgumentParser()
parser.add_argument("freq_file", help="candidate words file")
parser.add_argument("-s", "--separator", help="field separator", default="\t")
parser.add_argument("-f", "--freq_limit", help="word minimun frequence", default=1, type=int)
parser.add_argument("-o", "--output", help="Candidate Sequence Solidification File")

args = parser.parse_args()

src_file, des_file, freq_limit = args.freq_file, args.output, args.freq_limit

def compute_ninggudu(word, freq, freq_limit):
    w_freq = freq.get(word, freq_limit)
    length = len(word)
    ninggudu = 0
    if length == 2:
        word1, word2 = word
        ninggudu = w_freq / (freq.get(word1, freq_limit)*freq.get(word2, freq_limit))
    elif length == 3:
        word1, word2 = word[:2], word[2:3]
        ninggudu1 = w_freq / (freq.get(word1, freq_limit)*freq.get(word2, freq_limit))
        word1, word2 = word[:1], word[1:3]
        ninggudu2 = w_freq / (freq.get(word1, freq_limit)*freq.get(word2, freq_limit))
        ninggudu = min(ninggudu1, ninggudu2)
    elif length == 4:
        word1, word2 = word[:1], word[1:4]
        ninggudu1 = w_freq / (freq.get(word1, freq_limit)*freq.get(word2, freq_limit))
        word1, word2 = word[:2], word[2:4]
        ninggudu2 = w_freq / (freq.get(word1, freq_limit)*freq.get(word2, freq_limit))
        word1, word2 = word[:3], word[3:4]
        ninggudu3 = w_freq / (freq.get(word1, freq_limit)*freq.get(word2, freq_limit))
        ninggudu = min(ninggudu1, ninggudu2, ninggudu3)
    return ninggudu

with open(src_file, 'r') as fs:
    #这里可以优化，只读入满足阈值的词就行
    freq = {}
    for line in fs:
        key, count = line.decode('utf-8').rstrip().split(args.separator)
        freq[key] = int(count)


with open(des_file, 'w') as fd:
    #只计算字长为2，3，4的词
    #如果只算词频超过阈值的词，那么组成词的字的词频也一定大于或等于阈值，所以先判断阈值效率会高很多。
    words = (word for word, count in freq.iteritems() if count>=freq_limit and 2<=len(word)<=4)
    ninggudus = [(word, freq[word], compute_ninggudu(word, freq, freq_limit)) for word in words]
    result = (("%s\t%d\t%.9f\n" % (word.encode('utf-8'), w_freq, ninggudu)) for (word, w_freq, ninggudu) in ninggudus)
    fd.writelines(result)

