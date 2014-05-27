#-- encoding:utf-8 --
import argparse, re
from collections import Counter
"""
从语料中提取候选词序列，并计算词频
"""
parser = argparse.ArgumentParser()
parser.add_argument("corpus_file", help="corpus file")
parser.add_argument("-r", "--reverse", help="reverse the corpus", action="store_true")
parser.add_argument("-o", "--output", help="Candidate Sequence Frequency File")

args = parser.parse_args()

src_file, des_file = args.corpus_file, args.output

with open(src_file, 'r') as fs:
    freq = Counter()
    freq_update = freq.update
    re_chinese = re.compile(u'[^a-zA-Z0-9\u4e00-\u9fa5]+')
    for line in fs:
        sentence = re_chinese.sub('', line.decode('utf-8').rstrip())
        #下面这句放到循环里，合理吗？
        sentence = sentence if not args.reverse else sentence[::-1]
        sen_len = len(sentence)
        freq_update(sentence[i:i+1] for i in xrange(sen_len-1, -1, -1))
        freq_update(sentence[i:i+2] for i in xrange(sen_len-2, -1, -1))
        freq_update(sentence[i:i+3] for i in xrange(sen_len-3, -1, -1))
        freq_update(sentence[i:i+4] for i in xrange(sen_len-4, -1, -1))
        freq_update(sentence[i:i+5] for i in xrange(sen_len-5, -1, -1))

with open(des_file, 'w') as fd:
    for key, value in freq.iteritems():
            fd.write("%s\t%d\n" % (key.encode('utf-8'), value))
