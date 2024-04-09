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
                if docid in curr_ground.keys():
                    docid = "N{id}".format(id=docid)
                curr_ground[docid] = rel_level
            cnt += 1
            all_qr[curr_query] = curr_ground
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
            cnt += 1
        all_qr[curr_query] = rel_real
    return all_qr


# print(
#     get_rel_real(
#         "trainFiles/ms2-bm25.trecrun",
#         get_rel_ground("trainFiles/msmarco.qrels"),
#     )
# )


def get_ndcg20(rel_real, rel_ground):
    rel_ideal = sorted(rel_ground.items(), key=lambda x: x[1], reverse=True)
    ndcg20 = 0
    dcg = rel_real[0][1]
    idcg = rel_ideal[0][1]
    for i in range(1, 20):
        dcg += rel_real[i][1] / math.log2(i + 1)
        idcg += rel_ideal[i][1] / math.log2(i + 1)
    if idcg == 0:
        return 0
    ndcg20 = dcg / idcg
    return ndcg20


def get_numRel(rel_ground_qr):
    cnt = 0
    for rel_level in rel_ground_qr.values():
        if rel_level > 0:
            cnt += 1
    return cnt


def get_relFound(rel_real, qr):
    cnt = 0
    res = []
    for pair in rel_real:
        if pair[1] > 0:
            cnt += 1
            res.append(pair[0])
    if qr == "118440":
        print(res)
    return cnt


def get_reciprocal_rank(rel_found, rel_real):
    if rel_found == 0:
        return 0
    cnt = 1
    res = 0
    for pair in rel_real:
        if pair[1] > 0:
            res = 1 / cnt
            break
        cnt += 1
    return res


def get_p10(rel_real):
    cnt = 0
    for i in range(10):
        if rel_real[i][1] > 0:
            cnt += 1
    if cnt == 0:
        return 0
    return cnt / 10


def get_r10(rel_real, num_rel):
    if num_rel == 0:
        return 0
    cnt = 0
    for i in range(10):
        if rel_real[i][1] > 0:
            cnt += 1
    if cnt == 0:
        return 0
    return cnt / num_rel


def get_f1(r10, p10):
    if r10 == 0 or p10 == 0:
        return 0
    return (2 * r10 * p10) / (r10 + p10)


def get_ap(rel_real):
    cnt_inc = 0
    cum = 0
    cnt_total = 0
    for pair in rel_real:
        cnt_total += 1
        if pair[1] > 0:
            cnt_inc += 1
            cum += cnt_inc / cnt_total
    if cnt_inc == 0:
        return 0
    return cum / cnt_inc


def write_file(output_file, all_queries):
    with open(output_file, "w", encoding="utf8") as out_file:
        for qr, res_eval in all_queries.items():
            for key, val in res_eval.items():
                if key in ("numRel", "relFound"):
                    out_file.write(
                        "{key} {qr} {val:d}\n".format(key=key, qr=qr, val=val)
                    )
                else:
                    out_file.write(
                        "{key} {qr} {val:6.4f}\n".format(
                            key=key, qr=qr, val=val
                        )
                    )
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
    cndcg20 = 0
    cnumRel = 0
    crelFound = 0
    crr = 0
    cp10 = 0
    cr10 = 0
    cf1_10 = 0
    cap = 0
    cnt = 0
    for qr, rankings in rel_real.items():
        cnt += 1
        ndcg20 = get_ndcg20(rankings, rel_ground[qr])
        numRel = get_numRel(rel_ground[qr])
        relFound = get_relFound(rankings, qr)
        rr = get_reciprocal_rank(relFound, rel_real=rankings)
        p10 = get_p10(rankings)
        r10 = get_r10(rankings, numRel)
        f1_10 = get_f1(r10, p10)
        ap = get_ap(rankings)
        all_qr[qr] = {
            "NDCG@20": ndcg20,
            "numRel": numRel,
            "relFound": relFound,
            "RR": rr,
            "P@10": p10,
            "R@10": r10,
            "F1@10": f1_10,
            "AP": ap,
        }
        cndcg20 += ndcg20
        cnumRel += numRel
        crelFound += relFound
        crr += rr
        cp10 += p10
        cr10 += r10
        cf1_10 += f1_10
        cap += ap
    all_qr["all"] = {
        "NDCG@20": cndcg20 / cnt,
        "numRel": round(cnumRel / cnt),
        "relFound": round(crelFound / cnt),
        "MRR": crr / cnt,
        "P@10": cp10 / cnt,
        "R@10": cr10 / cnt,
        "F1@10": cf1_10 / cnt,
        "AP": cap / cnt,
    }
    write_file(outputFile, all_qr)
    return all_qr


# bm25 = eval(
#     "C:\\Users\\lemin\\P2python\\P2eval\\msmarcofull-bm25.trecrun",
#     "C:\\Users\\lemin\\P2python\\trainFiles\\msmarco.qrels",
#     "C:\\Users\\lemin\\P2python\\msmarcofull-bm25.eval",
# )
# dpr = eval(
#     "C:\\Users\\lemin\\P2python\\P2eval\\msmarcofull-dpr.trecrun",
#     "C:\\Users\\lemin\\P2python\\trainFiles\\msmarco.qrels",
#     "C:\\Users\\lemin\\P2python\\msmarcofull-dpr.eval",
# )
# ql = eval(
#     "C:\\Users\\lemin\\P2python\\P2eval\\msmarcofull-ql.trecrun",
#     "C:\\Users\\lemin\\P2python\\trainFiles\\msmarco.qrels",
#     "C:\\Users\\lemin\\P2python\\msmarcofull-ql.eval",
# )


# def write_table(output_file, bm25, dpr, ql):
#     with open(output_file, "w", encoding="utf8") as outfile:
#         key1 = "AP"
#         for qr in bm25.keys():
#             outfile.write("{qr}\n".format(qr=qr))
#         for qr in bm25.keys():
#             outfile.write("{qr:6.4f}\n".format(qr=bm25[qr][key1]))
#         for qr in dpr.keys():
#             outfile.write("{qr:6.4f}\n".format(qr=dpr[qr][key1]))
#         for qr in ql.keys():
#             outfile.write("{qr:6.4f}\n".format(qr=ql[qr][key1]))


# write_table("table.txt", bm25, dpr, ql)

if __name__ == "__main__":
    argv_len = len(sys.argv)
    runFile = (
        sys.argv[1]
        if argv_len >= 2
        else "/trainFiles/msmarcosmall-bm25.trecrun"
    )
    qrelsFile = sys.argv[2] if argv_len >= 3 else "../trainFiles/msmarco.qrels"
    outputFile = sys.argv[3] if argv_len >= 4 else "my-msmarcosmall-bm25.eval"
    eval(runFile, qrelsFile, outputFile)


# Feel free to change anything here ...
