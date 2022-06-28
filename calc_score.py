# -*- coding: UTF-8 -*-

import statistics
import argparse

import numpy

parser = argparse.ArgumentParser()
parser.add_argument('--fa-file', '-fa', help='sentence file in fa-format')
parser.add_argument('--src-file', '-src', help='sentence file in fa-format')
parser.add_argument('--trg-file', '-trg', help='sentence file in fa-format')
parser.add_argument('--alignments-file', '-a', required=True, help='alignments')
parser.add_argument('--out-file', '-o', required=True, help='name of outfile')
args = parser.parse_args()

alignFile = open(args.alignments_file, 'r')
alignLines = alignFile.readlines()
alignFile.close()

#setja reglu sem tryggir að annaðhvort src/trg eða fa sé ákveðið
sentLines = []
if args.fa_file:
    faFile = open(args.fa_file, 'r')
    faLines = faFile.readlines()
    faFile.close()
    assert len(faLines) == len(alignLines)
    sentLines = faLines
else:
    srcFile = open(args.src_file, 'r')
    srcLines = srcFile.readlines()
    srcFile.close()
    trgFile = open(args.trg_file, 'r')
    trgLines = trgFile.readlines()
    trgFile.close()
    assert len(srcLines) == len(trgLines) == len(alignLines)
    sentLines = [str(x[0].strip() + '|||' + x[1].strip()) for x in zip(srcLines, trgLines)]

lengthDict = {}
allvalues = []

with open(args.out_file, 'w') as fo:
    for i in range(len(sentLines)):
        WAScore = 0
        src_sent, trg_sent = sentLines[i].strip().split('|||')
        src_num = len(src_sent.strip().split())
        trg_num = len(trg_sent.strip().split())

        alignments = alignLines[i].strip().split()
        src_aligned = []
        trg_aligned = []
        for a in alignments:
            src_a, trg_a = a.split('-')
            src_aligned.append(src_a)
            trg_aligned.append(trg_a)
        src_a_num = len(set(src_aligned))
        trg_a_num = len(set(trg_aligned))

        if (src_num > 0) and (trg_num > 0):
            WAScore = round((src_a_num / src_num) * (trg_a_num / trg_num), 2)

        allvalues.append(WAScore)

        fo.write(src_sent.strip() + '\t' + trg_sent.strip() + '\t' + str(WAScore) + '\n')


print("The population standard deviation of data is : ",end="")
print(statistics.pstdev(allvalues))
print("The standard deviation of data is : ",end="")
data_stddev = statistics.stdev(allvalues)
print(data_stddev)
print("The mean of data is : ",end="")
data_mean = statistics.mean(allvalues)
print(data_mean)

suggestedcutoffscore = round(data_mean-data_stddev, 2)
print("The mean-1stddev is : ",end="")
print(suggestedcutoffscore)

print("Total number of values: ",end="")
print(len(allvalues))
nvals = numpy.asarray(allvalues)
values = nvals[nvals>data_mean]
print("Total number above mean: ",end="")
print(len(values))
values = nvals[nvals>suggestedcutoffscore]
print("Total number above threshold: ",end="")
print(len(values))


lowrange = data_mean - data_stddev
highrange = data_mean + data_stddev

