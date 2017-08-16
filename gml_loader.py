#######################################################
# name: gml_loader.py
# purpose: load graphs into arangodb based on conditioned files from a GML 
# need an edges.txt and a nodes.txt file - see cond-gml.py for creating these
# input: strings username, password, database (default is _system)
#
# author: adapted from pyrango example by Ray Zupancic
#######################################################

import sys
import getopt
from pyArango.connection import *
from pyArango.graph import *
from pyArango.collection import *


class AS(object):
        class nodes(Collection) :
            _fields = {
                "name" : Field()
            }
            
            
        class paths(Edges) :
            _fields = {
                "number" : Field()
            }
            
        class as2006(Graph) :

            _edgeDefinitions = (EdgeDefinition ('paths',
                                                fromCollections = ["nodes"],
                                                toCollections = ["nodes"]),)
            _orphanedCollections = []


        def __init__(self,nodes_tup,edges_tup, user, pw, db = "_system"):

               self.nodes_tuples = nodes_tup
               self.edges_tuples = edges_tup
               self.conn = Connection(username=user, password=pw)
               ndict = {}
        
               self.db = self.conn[db]

               self.nodes   = self.db.createCollection(className = "nodes")
               
               self.paths = self.db.createCollection(className ="paths")
               
               g = self.db.createGraph(db)

               for item in self.nodes_tuples:
                   # uncomment if you want to watch the routine load
                   #print("id:", item[0]," label:", item[1])
               
                   n =  g.createVertex('nodes', {"name": item[1],  "_key": str(item[0])})
                   n.save()
                   ndict[item[0]] = n

               for item in self.edges_tuples:

                   print(item)
                   strval = str(item[0]) + "_" + str(item[1])
                   g.link('paths', ndict[item[0]],ndict[item[1]], {"type": 'number', "_key": strval})


#####################
# name: stub to run AS - Autonomous System Graphing Class
#####################
def main(argv):


    if len(sys.argv) <3:
        print('usage: gml_loader.py -d database -u <arangodb_username> -p <arangodb_password>')
        sys.exit()

    try:
        opts, args = getopt.getopt(argv,"hd:u:p:",["username=","password="])
    except getopt.GetoptError:
        print('gml_loader.py -d database -u <arangodb_username> -p <arangodb_password>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('gml_loader.py -d database -u <arangodb_username> -p <arangodb_password>')
            sys.exit()
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-d", "--database"):
             db= arg
    print( 'database: ', db)
    print( 'username: ', username)
    print( 'password: ', password[0:2] + '*****')

    # read in the paths and nodes as tuplets 
    with open('edges.txt') as f:
        edges_col = []
        for line in f:
            #strip new-line, split into a tuple, and append as integer rather than string
            val1,val2 = line.rstrip('\n').split(',')
            edges_col.append((int(val1),int(val2)))

    with open('nodes.txt') as f:
        nodes_col = []
        for line in f:
            #strip new-line, split into a tuple, and append as integer rather than string
            val1,val2 = line.rstrip('\n').split(',')
            nodes_col.append((int(val1),int(val2)))

    AS(nodes_col, edges_col, username, password, db)



if __name__ == "__main__":
    main(sys.argv[1:])
