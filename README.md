new-words-discovery
===================

这是完成了新词发现功能的python脚本。

##使用方法
###1. 输入语料，计算出长度为1~5个字的所有候选词的词频
```bash
python compute_candidate_freq.py [-h] [-r] [-o OUTPUT] corpus_file
```
加上参数`-r`，会将语料文件的句子都翻转后，再统计所有逆序候选词的词频。

###2. 输入候选词词频文件，计算出长度为2~4个字的所有候选词的凝固度
```bash
python compute_solidation.py [-h] [-s SEPARATOR] [-f FREQ_LIMIT] [-o OUTPUT] freq_file
```
可通过参数`-s`设置词频文件的分隔符，默认是`\t`；设置`-f`可只计算词频大于等于词频阈值的候选词，默认为1。

###3. 输入候选词词频文件，计算出长度为2~4个字的所有候选词的右邻字信息熵
```bash
python compute_freedegree.py [-h] [-s SEPARATOR] [-f FREQ_LIMIT] [-r] [-o OUTPUT] freq_file
```
可通过参数`-s`设置词频文件的分隔符，默认是`\t`；设置`-f`可只计算词频大于等于词频阈值的候选词，默认为1；加上`-r`时，需要输入是逆序候选词词频文件，输出的是正序候选词的左邻字信息熵。

###4. 将词频文件，凝固度文件，左右邻字信息熵文件，合并到一起，然后导入Excel，通过设置词频阈值，凝固度阈值，自由度阈值刷选出新词。
