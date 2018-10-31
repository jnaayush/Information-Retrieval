import sys
from collections import OrderedDict


d = 0.85

outlinks = {}
inlinks = {}
PR = {}
newPR = {}
allDocID = {}
sinkDocID = {}
sourceDocID ={}

inlinkNum = 0
outlinkNum = 0
sink_num = 0
source_num = 0

l1Norm = 1000
numDocIDs = 0
iteration = 0

l1_3last = 0
l1_2last = 0
l1_4last = 0
l1_last = 0
l1Str = ""

"""
Checks if the li norm has reached the condition for convergence
"""
def converge(l1):
    global l1_3last
    global l1_2last
    global l1_last
    global l1_4last
    if iteration > 3:
        l1_4last = l1_3last
    if iteration > 2:
        l1_3last = l1_2last
    if iteration > 1:
        l1_2last = l1_last
    l1_last = l1
    if (l1_last < 0.001 and l1_2last < 0.001 and l1_3last < 0.001 and l1_4last < 0.001):
        return False
    else:
        return True


"""
Populates all the dictionaries that are used to calculate the page ranks
"""
def populate_sets():
    global inlinkNum
    global numDocIDs
    global outlinkNum

    for line in graph_file:
        line = line.strip()
        nodes = line.split(" ")    #list of nodes from each line
        inlinkNum += 1
        inlinks[nodes[0]] = tuple(nodes[1:])
        if not allDocID.has_key(nodes[0]):
            allDocID[nodes[0]] = 1
            numDocIDs += 1
        for node in nodes[1:]:
            if outlinks.has_key(node):
                outlinks[node] += 1
            else:
                outlinks[node] = 1
                outlinkNum += 1
            if not allDocID.has_key(node):
                allDocID[node] = 1;
                numDocIDs += 1
    for key in allDocID.keys():
        if not inlinks.has_key(key):
            inlinks[key] = ()
            sourceDocID[key] = 1
        if not outlinks.has_key(key):
            sinkDocID[key] = 1


"""
actual page rank algorithm that is used to assign page ranks
"""
def assignRanks():
    global iteration
    global l1Norm
    global l1Str
    for p in allDocID.keys():
        PR[p] = 1.0 / numDocIDs
    while converge(l1Norm):
        l1Norm = 0
        sinkPR = 0
        for p in sinkDocID.keys():
            sinkPR += PR[p]

        for p in allDocID.keys():
            newPR[p] = (1 - d) / numDocIDs
            newPR[p] += d * sinkPR / numDocIDs
            for inlink in inlinks[p]:
                newPR[p] += d * PR[inlink] / outlinks[inlink]

        for p in newPR.keys():
            l1Norm += abs(newPR[p] - PR[p])
            PR[p] = newPR[p]

        iteration += 1
        l1Str = l1Str + "L1 norm " + str(l1Norm) + "\titeration: " + str(iteration) + "\tTotal PR: %.2f \n" %sum(PR.values())


"""
writes the inlinks counts to the files in a sorted order
"""
def inLinksToFIle():
    outfileInlinks = open(graph_name.replace(".txt","") + "_inlinks" +".txt","w")
    pageAndInlinks = OrderedDict(sorted(inlinks.viewitems(), key=lambda (k,v):len(v), reverse=True))
    i = 0
    for key,value in pageAndInlinks.items():
        outfileInlinks.write(str(i)+" "+ key + "\t"+str(len(value))+"\n")
        if i > 18:
            break
        i += 1
    outfileInlinks.close()

"""
write the top50 DocIDs, L1 norm and graph statistics to the file
"""
def toFile():
    numUrl = 0
    outfile = open(graph_name.replace(".txt","") + "_output_"+str(d)+ "_"+str(iteration)+".txt","w")
    for key,value in sorted(newPR.iteritems(), key=lambda (v,k): (k, v), reverse=True):
        if (numUrl > 50):
            break
        outfile.write("" + str(PR[key]) + "\thttps://en.wikipedia.org/wiki/" + key + "\n")
        numUrl += 1
        print "" + str(PR[key]) + "\thttps://en.wikipedia.org/wiki/" + key + "\n"
    outfile.write(l1Str)
    maxInDegree = len(inlinks[max(inlinks, key = lambda x: len(inlinks.get(x)))])
    maxOutDegree = outlinks[max(outlinks, key = lambda x: outlinks.values())]


    outfile.write("Number of sinks: " + str(len(sinkDocID)) + "\n")
    outfile.write("Number of sources: " + str(len(sourceDocID)) + "\n")
    outfile.write("Maximum in-degree: " + str(maxInDegree) + "\n")
    outfile.write("Maximum out-degree: " + str(maxOutDegree) + "\n")
    outfile.close()

if __name__ == "__main__":
    graph_name = sys.argv[1]
    graph_file = open(graph_name, "r")
    populate_sets()
    assignRanks()
    inLinksToFIle()
    toFile()
    graph_file.close()



