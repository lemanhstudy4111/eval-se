# import package ...
import sys
import math


"""
def find_ndcg20_each(rel_rank):
    rel_ideal = sorted(rel_rank, reverse=True)
    dcg_curr = rel_rank[0]
    idcg_curr = rel_ideal[0]
    for i in range(1, 20):
        dcg_curr += rel_rank[i] / math.log2(i + 1)
        idcg_curr += rel_ideal[i] / math.log2(i + 1)
    if idcg_curr == 0:
        return 0
    return dcg_curr / idcg_curr


def find_ndcg20_all(qrelsFile):
    f = open(qrelsFile, "r", encoding="utf8")
    ndcg_20 = []
    rel_rank = []
    first_line = f.readline().split()
    prev_qr = first_line[0]
    rel_rank.append(int(first_line[3]))
    for line in f:
        arr_curr = line.split()
        if arr_curr[0] != prev_qr:
            ndcg_20.append((prev_qr, find_ndcg20_each(rel_rank=rel_rank)))
            rel_rank = []
            rel_rank.append(int(arr_curr[3]))
            prev_qr = arr_curr[0]
        else:
            rel_rank.append(int(arr_curr[3]))
    return ndcg_20
"""

"""
trecrun: 1. queryname 2. skip 3. docid 4. rank 5. score 6. some text to describe the run (same for every line)
qrels: 1. queryname 2. skip 3. docid 4. relevance
NDCG: DCG / IDCG
"""


"""    all_qr = {}
    with open(qrelsFile, "r", encoding="utf8") as qrel:
        first_line = qrel.readline().split()
        prev_qr = first_line[0]
        curr_ground = {}
        curr_ground[first_line[2]] = int(first_line[3])
        for line in qrel:
            curr_line = line.split()
            if curr_line[0] != prev_qr:
                all_qr[prev_qr] = curr_ground
                curr_ground = {}
                curr_ground[curr_line[2]] = int(curr_line[3])
                prev_qr = curr_line[0]
            else:
                curr_ground[curr_line[2]] = int(curr_line[3])
            all_qr[prev_qr] = curr_ground
    return all_qr"""


def get_rel_ground(qrelsFile):
    all_qr = {}
    cnt = 0
    curr_ground = {}
    curr_query = "0"
    with open(qrelsFile, "r", encoding="utf8") as qrel:
        for line in qrel:
            curr_line = line.split()
            query = curr_line[0]
            docid = curr_line[2]
            rel_level = int(curr_line[3])
            if cnt == 0:
                curr_query = query
            if query != curr_query:
                all_qr[query] = curr_ground
                curr_ground = {}
                curr_query = query
            else:
                curr_ground[docid] = rel_level
            all_qr[curr_query] = curr_ground
            cnt += 1
    return all_qr


def get_rel_real(trecrunFile, rel_ground):
    all_qr = {}
    curr_query = "0"
    cnt = 0
    rel_real = []
    with open(trecrunFile, "r", encoding="utf8") as trecrun:
        for line in trecrun:
            curr_line = line.split()
            query = curr_line[0]
            if cnt == 0:
                curr_query = query
            docid = curr_line[2]
            rel_ground_qr = rel_ground[query]
            if query != curr_query:
                all_qr[curr_query] = rel_real
                rel_real = []
                curr_query = query
            if docid not in rel_ground_qr:
                rel_real.append((docid, 0))
            else:
                rel_real.append((docid, rel_ground_qr[docid]))
            all_qr[curr_query] = rel_real
            cnt += 1
    return all_qr


"""
def test(filename):
    res = []
    cnt = 0
    with open(filename, "r", encoding="utf8") as f:
        for line in f:
            curr_line = line.split()
            if cnt != 0 and int(curr_line[1]) > 0:
                res.append(curr_line[0])
            cnt += 1
    return res
"""


def get_numRel(rel_ground_qr):
    cnt = 0
    for rel_level in rel_ground_qr.values():
        if rel_level > 0:
            cnt += 1
    return cnt


def get_relFound(rel_real):
    cnt = 0
    for pair in rel_real:
        if pair[1] > 0:
            cnt += 1
    return cnt


"""
def test_trec(filename, rel_items):
    with open(
        "C:\\Users\\lemin\\P2python\\{file}".format(file=filename),
        "w",
        encoding="utf8",
    ) as outFile:
        for qr, rank in rel_items.items():
            outFile.write("{query} \n".format(query=qr))
            for docid, rel in rank:
                rel_w = str(rel)
                outFile.write(
                    "{docid} {rel_w} \n".format(docid=docid, rel_w=rel_w)
                )

"""


def get_ndcg20(rel_real, rel_ground):
    # rel_ground = get_rel_ground(qrelsFile)
    # rel_real = get_rel_real(trecrunFile, rel_ground)
    # test_trec("relreal-test-smallbm25.txt", rel_real)
    rel_ideal = sorted(rel_ground.items(), key=lambda x: x[1], reverse=True)
    # test_trec("relideal-test-smallbm25.txt", rel_ideal)
    # dcg_all = {}
    # idcg_all = {}
    ndcg20 = 0
    dcg = rel_real[0][1]
    idcg = rel_ideal[0][1]
    for i in range(1, 20):
        dcg += rel_real[i][1] / math.log2(i + 1)
        idcg += rel_ideal[i][1] / math.log2(i + 1)
    ndcg20 = dcg / idcg
    return ndcg20


# ndcg20 = get_ndcg20(
#     "C:\\Users\\lemin\\P2python\\trainFiles\\msmarcosmall-bm25.trecrun",
#     "C:\\Users\\lemin\\P2python\\trainFiles\\msmarco.qrels",
# )
# print(ndcg20)


# ndcg = dcg / idcg
# need qrel to check relevance level, get all docid in trecrun, get their relevance level, sort


def write_file(output_file, res, query):
    return 0


def eval(trecrunFile, qrelsFile, outputFile):
    # Your function start here ...
    # trecrun is the file containing the systems to evaluate
    # qrels is the ground truth
    # Get all ground truth for all queries
    # Get all real system runs for all queries
    # for each query, calculate ndcg@20, numRel, relFound, RR (reciprocal rank), P@10 (precision), R@10(recall), F1@(10) (f measure), AP(average precision)
    rel_ground = get_rel_ground(qrelsFile)
    rel_real = get_rel_real(trecrunFile, rel_ground)
    all_qr = {}
    for qr, rankings in rel_real.items():
        ndcg20 = get_ndcg20(rankings, rel_ground[qr])
        numRel = get_numRel(rel_ground[qr])
        relFound = get_relFound(rankings)

        all_qr[qr] = {"ndcg20": ndcg20, "numRel": numRel, "relFound": relFound}
    return all_qr


all_queries = eval(
    "C:\\Users\\lemin\\P2python\\trainFiles\\msmarcosmall-bm25.trecrun",
    "C:\\Users\\lemin\\P2python\\trainFiles\\msmarco.qrels",
    "outputFile.txt",
)
print(all_queries)


if __name__ == "__main__":
    argv_len = len(sys.argv)
    runFile = sys.argv[1] if argv_len >= 2 else "msmarcosmall-bm25.trecrun"
    qrelsFile = sys.argv[2] if argv_len >= 3 else "msmarco.qrels"
    outputFile = sys.argv[3] if argv_len >= 4 else "my-msmarcosmall-bm25.eval"

    # eval(runFile, qrelsFile, outputFile)
    # Feel free to change anything here ...
