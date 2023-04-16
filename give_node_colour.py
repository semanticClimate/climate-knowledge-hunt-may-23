import pandas as pd
from pyvis.network import Network
import json

SOURCE = "source"
TARGET = "target"
PACKAGE = "package"
SECTION = "section"

def cleaning_nan(df, list_of_columns):
    # dropping the rows having NaN values
    df = df.dropna(subset = list_of_columns)
    # To reset the indices
    df = df.reset_index(drop=True)
    return df

def get_package_names(df, file_name):
    with open(file_name) as f:
        package_dict = json.load(f)
    node_colour = []
    for package_extracted in df[PACKAGE]:
        try: 
            node_colour.append(package_dict[package_extracted]["colour"])
        except KeyError:
            node_colour.append("#87755d")
    df["node_colour"] = node_colour
    return df

def make_graph(df, source, target, colour):
    ipcc_net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", notebook=True)
    # set the physics layout of the network
    #ipcc_net.barnes_hut()
    sources = df[source]
    targets = df[target]
    colours = df[colour]
    edge_data = zip(sources, targets, colours)
    for e in edge_data:
        src = e[0]
        dst = e[1]
        clr = e[2]
        ipcc_net.add_node(src, src, title=src, color='#9F2B68')
        ipcc_net.add_node(dst, dst, title=dst, color=clr)
        ipcc_net.add_edge(src, dst)
    neighbor_map = ipcc_net.get_adj_list()
    # add neighbor data to node hover data
    for node in ipcc_net.nodes:
        node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
        node["value"] = len(neighbor_map[node["id"]])          
    ipcc_net.show_buttons(filter_=['physics'])          
    ipcc_net.show("ipcc_graph_coloured_2.html")




ipcc_table = pd.read_csv("knowledge_graph/edges.csv")
cleaned_ipcc_graph = cleaning_nan(ipcc_table, ['source', 'package','target', 'section'])
ipcc_graph_with_coloured_nodes = get_package_names(cleaned_ipcc_graph, "package.json")
ipcc_graph_with_coloured_nodes.to_csv('coloured.csv')
make_graph(ipcc_graph_with_coloured_nodes, source='source', target='target', colour ='node_colour')