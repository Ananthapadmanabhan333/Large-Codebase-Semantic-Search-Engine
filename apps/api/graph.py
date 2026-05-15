import networkx as nx
from typing import List, Dict, Any, Set
import json

class GraphEngine:
    def __init__(self):
        self.graph = nx.MultiDiGraph()

    def add_file(self, file_path: str, metadata: Dict[str, Any]):
        self.graph.add_node(
            file_path, 
            type="file", 
            **metadata
        )

    def add_symbol(self, symbol_name: str, file_path: str, metadata: Dict[str, Any]):
        symbol_id = f"{file_path}:{symbol_name}"
        self.graph.add_node(
            symbol_id, 
            type="symbol", 
            name=symbol_name,
            file=file_path,
            **metadata
        )
        self.graph.add_edge(file_path, symbol_id, relation="contains")

    def add_dependency(self, source_path: str, target_path: str, dep_type: str = "import"):
        self.graph.add_edge(source_path, target_path, relation=dep_type)

    def get_dependencies(self, node_id: str, direction: str = "outgoing") -> List[Dict]:
        if direction == "outgoing":
            edges = self.graph.out_edges(node_id, data=True)
        else:
            edges = self.graph.in_edges(node_id, data=True)
            
        return [
            {
                "from": u,
                "to": v,
                "relation": data.get("relation")
            }
            for u, v, data in edges
        ]

    def get_subgraph(self, center_node: str, radius: int = 1) -> Dict[str, Any]:
        """
        Returns a subgraph around a center node for visualization.
        """
        if center_node not in self.graph:
            return {"nodes": [], "links": []}

        nodes = set([center_node])
        for _ in range(radius):
            new_nodes = set()
            for node in nodes:
                new_nodes.update(self.graph.neighbors(node))
                if isinstance(self.graph, nx.DiGraph):
                    new_nodes.update(self.graph.predecessors(node))
            nodes.update(new_nodes)

        sub = self.graph.subgraph(nodes)
        
        return {
            "nodes": [
                {"id": n, **sub.nodes[n]}
                for n in sub.nodes
            ],
            "links": [
                {"source": u, "target": v, "relation": data.get("relation")}
                for u, v, data in sub.edges(data=True)
            ]
        }

    def serialize(self) -> str:
        return json.dumps(nx.node_link_data(self.graph))

    def load(self, data_str: str):
        data = json.loads(data_str)
        self.graph = nx.node_link_graph(data)
