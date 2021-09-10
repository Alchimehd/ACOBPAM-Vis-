#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

import xdot
import json
import pydot



threshSpan = [0.7]
threshFol = [0.7]
threshISpan = [0.7]
threshIFol = [0.7]

activeSpan = [True]
activeFol = [True]
activeISpan = [True]
activeIFol = [True]

class MyDotWindow(xdot.DotWindow):

    def __init__(self):
        xdot.DotWindow.__init__(self, width = 1000, height = 500)
        widge = self.dotwidget
        self.get_child().remove(self.dotwidget)
        builder = Gtk.Builder()
        builder.add_from_file('/home/hh/interface.glade')
        self.builder = builder
        fhbox = builder.get_object('fhbox')
        fhbox.pack_end(widge, True, True, 0)
        self.get_child().pack_start(fhbox, True, True, 0)
        builder.connect_signals(Handler(self))
        
    def on_open(self, action):
        chooser = Gtk.FileChooserDialog(parent=self,
                                        title="Open Pattern File",
                                        action=Gtk.FileChooserAction.OPEN,
                                        buttons=(Gtk.STOCK_CANCEL,
                                                 Gtk.ResponseType.CANCEL,
                                                 Gtk.STOCK_OPEN,
                                                 Gtk.ResponseType.OK))
        chooser.set_default_response(Gtk.ResponseType.OK)
        chooser.set_current_folder(self.last_open_dir)
        filter = Gtk.FileFilter()
        filter.set_name('COBPAM Patterns File')
        filter.add_pattern("*.json")
        chooser.add_filter(filter)
        filter = Gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        chooser.add_filter(filter)
        if chooser.run() == Gtk.ResponseType.OK:
            filename = chooser.get_filename()
            self.last_open_dir = chooser.get_current_folder()
            chooser.destroy()
            open_file(filename, self)
        else:
            chooser.destroy()

        
 
# Lire le fichier json
    


# Initialiser le graphe
graph = pydot.Dot('my_graph', graph_type='digraph')
graphSpan = pydot.Dot('g_span', graph_type='digraph')
graphFol = pydot.Dot('g_fol', graph_type='digraph')
graph_json = None


def open_file(filename, window):
    
    f = open(filename)
    global graph_json
    graph_json = json.load(f)
    f.close()
    
    # Creer les noeuds
    for n in graph_json["behavioralPatternsList"]:
        id = n["id"]
        wdth = 10.0 * n["support"] * n["support"]
        pwdth = 8.0 * n["support"] * n["support"]
        
        graphTree = pydot.Dot('tree'+id)
        for treeNode in n['treePatt']['nodeSet']:
            labNode = treeNode['label']
            graphTree.add_node(pydot.Node(treeNode['idNode'], label = labNode, shape = 'circle'))
        
        for rel in n['treePatt']['relationSet']:
            graphTree.add_edge(pydot.Edge(rel[0], rel[1]))
            
        graphTree.write_png(id+"img.png")
        pydot.Node()
        graph.add_node(pydot.Node(id, label="", image = "./"+ id+"img.png", tooltip = n["support"], imagescale = True, shape='circle', penwidth=pwdth, width = wdth))
        graphSpan.add_node(pydot.Node(id))
        graphFol.add_node(pydot.Node(id)) 
        
    updateGraph()
    window.set_dotcode(bytes(graph.to_string(), 'utf_8'))
    window.show_all()


def updateGraph():

    for e in graph.get_edges():
        graph.del_edge(e.get_source(), e.get_destination())
        
    for e in graphSpan.get_edges():
        graphSpan.del_edge(e.get_source(), e.get_destination())
        
    for e in graphFol.get_edges():
        graphFol.del_edge(e.get_source(), e.get_destination())
    
    for e in graph_json["depGraph"]:
    
        id_ant = e['ant']
        id_cons = e['cons']
    
        pwdth = 7 * e['support']
        fsize = 80.0 * e["support"] * e["support"]
        asize = 6 * e['support']
        minln = 5 * e["support"] * e["support"]
    
    
        if e['dType'] == "SPAN" and e['support'] > threshSpan[0] and activeSpan[0]:
            graphSpan.add_edge(pydot.Edge(id_ant, id_cons, label = e['support']))
        elif e['dType'] == "DFOL" and e['support'] > threshFol[0] and activeFol[0]:
            graphFol.add_edge(pydot.Edge(id_ant, id_cons, label = e['support']))
        elif e['dType'] == "ISPAN" and e['support'] > threshISpan[0] and not graphSpan.get_edge([e['ant'], e['cons']]) and activeISpan[0]:
            col = 'firebrick1'
            ah = 'diamond'
            graph.add_edge(pydot.Edge(id_ant, id_cons, minlen = minln, label=e['support'], color=col, fontcolor=col, arrowhead=ah, penwidth=pwdth, arrowsize=asize, fontsize=fsize))
        elif e['dType'] == "IDFOL" and e['support'] > threshIFol[0] and not graphFol.get_edge([e['ant'], e['cons']]) and activeIFol[0]:
            col = 'goldenrod1'
            ah = 'box'
            graph.add_edge(pydot.Edge(id_ant, id_cons, minlen = minln, label=e['support'], color=col, fontcolor=col, arrowhead=ah, penwidth=pwdth, arrowsize=asize, fontsize=fsize))
            
        
    # Generer le resultat 
    
    #print(graphSpan.to_string())
    if activeSpan[0]:
        graphSpan.write('graphSpan.dot')
        redSpanDot = pydot.call_graphviz("tred", ['graphSpan.dot'], './')[0]
        redSpanG = pydot.graph_from_dot_data(redSpanDot.decode('utf-8'))[0]
        for e in redSpanG.get_edges():
       
            id_ant = e.get_source()
            id_cons = e.get_destination()
    
            pwdth = 7 * float(e.get('label'))
            fsize = 80.0 * float(e.get('label')) * float(e.get('label'))
            asize = 6 * float(e.get('label'))
            minln = 5 * float(e.get('label')) * float(e.get('label'))
            col = 'dodgerblue'
            ah = 'normal'
            graph.add_edge(pydot.Edge(id_ant, id_cons, minlen = minln, label=e.get('label'), color=col, fontcolor=col, arrowhead=ah, penwidth=pwdth, arrowsize=asize, fontsize=fsize))
    
    if activeFol[0]:
        graphFol.write('graphFol.dot')
    
        redFolDot = pydot.call_graphviz("tred", ['graphFol.dot'], './')[0]
    
    
        redFolG = pydot.graph_from_dot_data(redFolDot.decode('utf-8'))[0]
        for e in redFolG.get_edges():
            id_ant = e.get('points')[0]
            id_cons = e.get('points')[1]
    
            pwdth = 7 * float(e.get('label'))
            fsize = 80.0 * float(e.get('label')) * float(e.get('label'))
            asize = 6 * float(e.get('label'))
            minln = 5 * float(e.get('label')) * float(e.get('label'))
            col = 'chartreuse3'
            ah = 'dot'
            graph.add_edge(pydot.Edge(id_ant, id_cons, minlen = minln, label=e.get('label'), color=col, fontcolor=col, arrowhead=ah, penwidth=pwdth, arrowsize=asize, fontsize=fsize))
    
    
   

class Handler:
     
    def __init__(self, window):
        self.window = window
        
    def onDestroy(self, *args):
        Gtk.main_quit()

    def on_spancheck_toggled(self, button):
        if(button.get_active()):
            activeSpan[0] = True
        else:
            activeSpan[0] = False
        self.update()
        
    def on_ispancheck_toggled(self, button):
        if(button.get_active()):
            activeISpan[0] = True
        else:
            activeISpan[0] = False
        self.update()
        
    def on_folcheck_toggled(self, button):
        if(button.get_active()):
            activeFol[0] = True
        else:
            activeFol[0] = False
        self.update()
        
    def on_ifolcheck_toggled(self, button):
        if(button.get_active()):
            activeIFol[0] = True
        else:
            activeIFol[0] = False
        self.update()
        
    def on_adjSp_value_changed(self, adj):
        threshSpan[0] = adj.get_value()
        self.update()
        
    def on_adjISp_value_changed(self, adj):
        threshISpan[0] = adj.get_value()
        self.update()
        
    def on_adjFol_value_changed(self, adj):
        threshFol[0] = adj.get_value()
        self.update()
    
    def on_adjIFol_value_changed(self, adj):
        threshIFol[0] = adj.get_value()
        self.update()
    
    def update(self):
        updateGraph()
        self.window.set_dotcode(bytes(graph.to_string(), 'utf_8'))
        self.window.show_all()
        
        
        

    

def main():
 
    
    window = MyDotWindow()
    window.set_dotcode(bytes(graph.to_string(), 'utf_8'))
    window.connect('delete-event', Gtk.main_quit)
    act = window.actiongroup.get_action('Open')
    window.actiongroup.remove_action(act)
    window.actiongroup.add_actions([('Open', Gtk.STOCK_OPEN, None, None, None, window.on_open)])
    window.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()


