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


def get_rel_ground(qrelsFile):
    all_qr = {}
    with open(qrelsFile, "r", encoding="utf8") as qrel, open(
        "qrel_output", "w", encoding="utf8"
    ) as outfile:
        first_line = qrel.readline().split()
        prev_qr = first_line[0]
        curr_ground = {}
        curr_ground[first_line[2]] = int(first_line[3])
        for line in qrel:
            curr_line = line.split()
            if curr_line[0] != prev_qr:
                all_qr[prev_qr] = curr_ground
                prev_qr = curr_line[0]
                return all_qr
            else:
                curr_ground[curr_line[2]] = int(curr_line[3])
    return all_qr


def get_rel_real(trecrunFile, rel_ground):
    rel_real = []
    with open(trecrunFile, "r", encoding="utf8") as trecrun:
        for line in trecrun:
            curr_line = line.split()
            query = curr_line[0]
            docid = curr_line[2]
            rel_ground_qr = rel_ground[query]
            rel_real.append((docid, rel_ground_qr[docid]))
    return rel_real


rel_ground = get_rel_ground(
    "C:\\Users\\lemin\\P2python\\trainFiles\\msmarco.qrels"
)
print(
    get_rel_real(
        "C:\\Users\\lemin\\P2python\\trainFiles\\msmarcofull-bm25.trecrun",
        rel_ground,
    )
)


# ndcg = dcg / idcg
# need qrel to check relevance level, get all docid in trecrun, get their relevance level, sort


class Qr:
    def __init__(self, query, ground_rel_docs, trecrun_file) -> None:
        self.query = query
        self.ground_rel_docs = ground_rel_docs


def eval(trecrunFile, qrelsFile, outputFile):
    # Your function start here ...
    # trecrun is the file containing the systems to evaluate
    # qrels is the ground truth
    # Get all lines necessary for queries
    # for each query, get all relevant files, tuple with docid and their relevance
    # need to find: ndcg20, numRel in qrel, relFound in ranked list (trecrun),
    qrel = open(qrelsFile, "r", encoding="utf8")
    first_line = qrel.readline().split()
    prev_qr = first_line[0]
    curr_ground = []
    curr_ground.append((first_line[2], first_line[3]))
    for line in qrel:
        curr_line = line.split()
        if curr_line[0] != prev_qr:
            curr_qr = Qr(prev_qr, curr_ground)
        else:
            curr_ground.append((curr_line[2], curr_line[3]))

    return


if __name__ == "__main__":
    argv_len = len(sys.argv)
    runFile = sys.argv[1] if argv_len >= 2 else "msmarcosmall-bm25.trecrun"
    qrelsFile = sys.argv[2] if argv_len >= 3 else "msmarco.qrels"
    outputFile = sys.argv[3] if argv_len >= 4 else "my-msmarcosmall-bm25.eval"

    # eval(runFile, qrelsFile, outputFile)
    # Feel free to change anything here ...
