qr_infile = "C:\\Users\\lemin\\P2python\\trainFiles\\msmarco.qrels"
qr_outfile = "query.txt"


def write_qr(filename, outputfile):
    with open(filename, "r", encoding="utf8") as infile, open(
        outputfile, "w", encoding="utf8"
    ) as outfile:
        curr_query = "0"
        for line in infile:
            curr_line = line.split()
            query = curr_line[0]
            if query != curr_query:
                outfile.write("{qr}\n".format(qr=query))
                curr_query = query
    return 0


bm25_in = "C:/Users/lemin/P2python/p2-submission/bm25.eval"
dpr_in = "C:/Users/lemin/P2python/p2-submission/dpr.eval"
ql_in = "C:/Users/lemin/P2python/p2-submission/ql.eval"


def write_ap(filename, outputfile):
    with open(filename, "r", encoding="utf8") as infile, open(
        outputfile, "w", encoding="utf8"
    ) as outfile:
        for line in infile:
            curr_line = line.split()
            ap = curr_line[0]
            if ap == "AP":
                outfile.write("{ap}\n".format(ap=curr_line[2]))


# write_qr(qr_infile, qr_outfile)
write_ap(bm25_in, "bm25_table.txt")
write_ap(dpr_in, "dpr_table.txt")
write_ap(ql_in, "ql_table.txt")
