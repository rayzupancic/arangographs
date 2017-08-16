##############################################################
# name: cond-gml.py
# purpose: utility routine to harvest nodes and edges from GML
# notes: this splits a gml file into an edges file and a nodes files (two files): edges.txt and nodes.txt
# output: two files: edges.txt and nodes.txt, which can be used to load with pyrango
#
#
# author: Ray Zupancic
##############################################################
import re

##############################################################
# name: edgeparser.py
# purpose: utility routine to harvest edges from GML
# input: list ary  # ary contains the raw data
# output: results # list of tuplets is a list of tuplets 
##############################################################
def edgeparser(ary):

    # create a source and target list, then push them into a result list of tuplets
    result,source,target = [],[],[]
    for item in ary:
        if 'source' in item:
            num = re.findall('\d+',item)
            # use join and int to get rid of brackets and quotes
            source.append(int(''.join(num)))
        if 'target' in item:
            num = re.findall('\d+',item)
            target.append(int(''.join(num)))
    for i in range(len(source)):
        result.append((source[i],target[i]))
    return result

##############################################################
# name: nodeparser.py
# purpose: utility routine to harvest nodes from GML
# input: list ary  # ary contains the raw data
# output: results # list of tuplets is a list of tuplets # (<node id>, <node label>
##############################################################
def nodeparser(ary):

    # create a source and target list, then push them into a result list of tuplets
    result,ident,label = [],[],[]
    for item in ary:
        if 'id' in item:
            num = re.findall('\d+',item)
            # use join and int to get rid of brackets and quotes
            ident.append(int(''.join(num)))
        if 'label' in item: # label is the actual node name
            num = re.findall('\d+',item)
            label.append(int(''.join(num)))
    for i in range(len(label)):
        result.append((ident[i],label[i]))
    return result


##############################################################
# name: main routine
# purpose:  harvest nodes and edges from GML into separate files consisting
# of simply tuples
##############################################################
def main():
    # read in the nodes and edges, and translate into a tuplet: (<node-id>, <node-label>) 
    # eg. (53,879)
    gml_file = 'as-22july06.gml'

    with open(gml_file) as f:
            lines = f.readlines()
    
    # find the nodes and write to a file 
    noderesults = nodeparser(lines)

    with open("nodes.txt", 'w') as f:
        for item in noderesults:
            f.write("{},{}\n".format(item[0],item[1]))


    # find the edges and write to a file 
    edgeresults = edgeparser(lines)

    with open("edges.txt", 'w') as f:
        for item in edgeresults:
            f.write("{},{}\n".format(item[0],item[1]))



#  call main routine
main()
