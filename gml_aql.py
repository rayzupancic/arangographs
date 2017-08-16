#######################################################
# name: gml_aql.py
# purpose:  exercise some AQL queries against database
# input: strings username, password, database (default is _system)
#
# author:  Ray Zupancic
#######################################################

import sys
import getopt
from pyArango.connection import *
from pyArango.graph import *
from pyArango.collection import *



#######################################################
# name: get_length
# purpose: get length of collection
# input: string collection - name of collection
# ouput: int length
#
#######################################################
def get_length(db,collection):
    aql = "RETURN LENGTH(" + collection +")"
    query_result = db.AQLQuery(aql, rawResults=True, batchSize=100)
    return query_result.result


#######################################################
# name: get_conn
# purpose: get connection to db
# input: string database, username, password
# ouput: db connection object
#
#######################################################
def get_conn(db,user,pw):
    conn = Connection(username=user, password=pw)
    db = conn[db]
    return db


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
    
    dbconn = get_conn(db,username,password)

   
    # exercise the db
    print("number of edges: {}".format(get_length(dbconn,"paths")))
    print("number of nodes: {}".format(get_length(dbconn,"nodes")))



if __name__ == "__main__":
    main(sys.argv[1:])
