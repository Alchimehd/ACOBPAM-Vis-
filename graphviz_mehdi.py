import json
import pydot
import time
start_time = time.time()
 
# Lire le fichier json

f = open('Graph_python.json')
graph_json = json.load(f)
f.close()

# Initialiser le graphe
graph = pydot.Dot('my_graph', graph_type='digraph')

# Creer les noeuds
for n in graph_json["behavioralPatternsList"]:
    id = n["id"]
    lab = n["id"] + "\n" + str(n["support"])
    wdth = 8.0 * n["support"] * n["support"]
    pwdth = 8.0 * n["support"] * n["support"]
    fsize = 80.0 * n["support"] * n["support"]
    imgScale = 2 * n["support"] * n["support"]
    
    graphTree = pydot.Dot('tree'+id)
    for treeNode in n['treePatt']['nodeSet']:
        labNode = treeNode['label']
        graphTree.add_node(pydot.Node(treeNode['idNode'], label = labNode, shape = 'circle'))
    
    for rel in n['treePatt']['relationSet']:
        graphTree.add_edge(pydot.Edge(rel[0], rel[1]))
        
    graphTree.write_png(id+"img.png")
    
    graph.add_node(pydot.Node(id, label="", image = "C:/Users/Mehdi/COBPAM VIS/"+ id+"img.png", imagescale = 2, shape='circle', penwidth=pwdth, width = wdth))
    
# Creer le arcs    
for e in graph_json["depGraph"]:
    id_ant = e['ant']
    id_cons = e['cons']
    pwdth = 7 * e['support']
    fsize = 80.0 * e["support"] * e["support"]
    asize = 6 * e['support']
    minln = 5 * e["support"] * e["support"]
    if e['dType'] == "ISPAN":
        col = 'firebrick1'
        ah = 'diamond'
    elif e['dType'] == "SPAN":
        col = 'dodgerblue'
        ah = 'normal'
    elif e['dType'] == "DFOL":
        col = 'chartreuse3'
        ah = 'dot'
    elif e['dType'] == "IDFOL":
        col = 'goldenrod1'
        ah = 'box'
    graph.add_edge(pydot.Edge(id_ant, id_cons, minlen = minln, label=e['support'], color=col, fontcolor=col, arrowhead=ah, penwidth=pwdth, arrowsize=asize, fontsize=fsize))
        
# Generer le resultat 
graph.write_svg('output.svg')
#print(graph.to_string())
#f = open("dotFile.dot", "w")
#f.write(graph.to_string())
#f.close()
end_time = time.time()
print("--- %s seconds ---" % (end_time - start_time))
