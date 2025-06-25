"""
DOT Graph Presenter - Visualization Adapter
Distance-based node sizing for hierarchical model graphs.
"""

import dataclasses
import typing as t
from abc import abstractmethod
from enum import StrEnum
from collections import deque

# Import domain models (assumes discovery_module.py exists)
from .discovery_core import ModelGraph, ModelDependency, ModelRelation, RelationType


# ============================================================================
# Presentation Contracts
# ============================================================================

class PresentationFormat(StrEnum):
    TEXT = "text"
    JSON = "json"
    DOT = "dot"
    HTML = "html"


class GraphLayout(StrEnum):
    DOT = "dot"
    NEATO = "neato"
    FDP = "fdp"
    CIRCO = "circo"


@dataclasses.dataclass(frozen=True)
class PresentationOptions:
    graph_layout: GraphLayout = GraphLayout.DOT
    show_node_details: bool = True
    show_edge_labels: bool = True
    include_reverse_relations: bool = False
    cluster_by_distance: bool = True
    max_distance: int = 6


class ModelGraphPresenter(t.Protocol):
    @abstractmethod
    def present(self, graph: ModelGraph, options: t.Optional[PresentationOptions] = None) -> str:
        ...

    @abstractmethod
    def get_format(self) -> PresentationFormat:
        ...


# ============================================================================
# DOT Presenter Implementation
# ============================================================================

class DotGraphPresenter:
    """DOT format presenter with distance-based sizing."""

    def present(self, graph: ModelGraph, options: t.Optional[PresentationOptions] = None) -> str:
        opts = options or PresentationOptions()
        distances = self._calculate_distances_from_roots(graph)

        lines = [
            f"digraph ModelGraph {{",
            f"    layout={opts.graph_layout.value};",
            f"    rankdir=TB;",
            f"    ranksep=1.5;",
            f"    nodesep=0.8;",
            ""
        ]

        # Nodes with distance-based sizing
        for node in graph.nodes:
            lines.append(self._create_node(node, distances, graph.root_models, opts))

        lines.append("")

        # Edges with relation styling
        for edge in graph.edges:
            if opts.include_reverse_relations or not edge.is_reverse_relation:
                lines.append(self._create_edge(edge, opts))

        # Distance-based ranks
        if opts.cluster_by_distance:
            lines.extend(self._create_distance_ranks(distances, opts.max_distance))

        lines.append("}")
        return "\n".join(lines)

    def get_format(self) -> PresentationFormat:
        return PresentationFormat.DOT

    def _calculate_distances_from_roots(self, graph: ModelGraph) -> t.Dict[ModelDependency, int]:
        """BFS distance calculation from root models."""
        distances = {}
        queue = deque()

        # Initialize roots at distance 0
        for root in graph.root_models:
            distances[root] = 0
            queue.append((root, 0))

        # BFS traversal
        while queue:
            current, dist = queue.popleft()

            for relation in graph.get_relations_for_model(current):
                target = relation.target
                if target not in distances:
                    distances[target] = dist + 1
                    queue.append((target, dist + 1))

        # Handle orphaned nodes
        for node in graph.nodes:
            if node not in distances:
                distances[node] = 999

        return distances

    def _create_node(self, node: ModelDependency, distances: t.Dict[ModelDependency, int],
                     root_models: t.Set[ModelDependency], opts: PresentationOptions) -> str:
        """Create node with distance-based sizing."""
        distance = distances.get(node, 999)

        # Size scaling by distance
        if distance == 0:
            size_factor = 2.0  # Root models largest
        elif distance <= 2:
            size_factor = 1.5
        elif distance <= 4:
            size_factor = 1.0
        else:
            size_factor = 0.7  # Far models smallest

        # App-based color
        color = self._get_app_color(node.app_label)

        # Node attributes
        attrs = [
            f'label="{self._get_node_label(node, opts)}"',
            f'fontsize={int(12 * size_factor)}',
            f'width={size_factor}',
            f'height={size_factor * 0.6}',
            f'style=filled',
            f'fillcolor="{color}"',
            f'shape=box'
        ]

        # Highlight root models
        if node in root_models:
            attrs.extend(['penwidth=3', 'color=red'])

        node_id = self._get_node_id(node)
        return f'    "{node_id}" [{", ".join(attrs)}];'

    def _create_edge(self, edge: ModelRelation, opts: PresentationOptions) -> str:
        """Create edge with relation type styling."""
        source_id = self._get_node_id(edge.source)
        target_id = self._get_node_id(edge.target)

        # Edge styling by relation type
        attrs = []

        if edge.relation_type == RelationType.FOREIGN_KEY:
            attrs.extend(['color=blue', 'penwidth=2'])
        elif edge.relation_type == RelationType.MANY_TO_MANY:
            attrs.extend(['color=green', 'penwidth=2', 'style=dashed'])
        elif edge.relation_type == RelationType.ONE_TO_ONE:
            attrs.extend(['color=purple', 'penwidth=2'])
        elif edge.is_reverse_relation:
            attrs.extend(['color=gray', 'penwidth=1', 'style=dotted'])

        # Edge labels
        if opts.show_edge_labels and edge.metadata.field_name:
            attrs.append(f'label="{edge.metadata.field_name}"')

        attrs_str = f' [{", ".join(attrs)}]' if attrs else ''
        return f'    "{source_id}" -> "{target_id}"{attrs_str};'

    def _create_distance_ranks(self, distances: t.Dict[ModelDependency, int], max_distance: int) -> t.List[str]:
        """Group nodes by distance for hierarchical layout."""
        ranks = {}
        for node, distance in distances.items():
            if distance <= max_distance:
                if distance not in ranks:
                    ranks[distance] = []
                ranks[distance].append(node)

        constraints = []
        for distance in sorted(ranks.keys()):
            node_ids = [f'"{self._get_node_id(node)}"' for node in ranks[distance]]
            constraints.append(f"    {{ rank=same; {'; '.join(node_ids)}; }}")

        return constraints

    def _get_node_id(self, node: ModelDependency) -> str:
        return f"{node.app_label}_{node.model_name}"

    def _get_node_label(self, node: ModelDependency, opts: PresentationOptions) -> str:
        if opts.show_node_details:
            return f"{node.app_label}\\n{node.model_name}"
        return node.model_name

    def _get_app_color(self, app_label: str) -> str:
        """Consistent app colors."""
        colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightpink',
                  'lightcoral', 'lightgray', 'lightcyan', 'lavender']
        return colors[hash(app_label) % len(colors)]


# ============================================================================
# Usage Example
# ============================================================================

def create_dot_visualization(graph: ModelGraph, layout: GraphLayout = GraphLayout.DOT) -> str:
    """Simple factory for DOT visualization."""
    presenter = DotGraphPresenter()
    options = PresentationOptions(
        graph_layout=layout,
        show_node_details=True,
        show_edge_labels=True,
        include_reverse_relations=False,
        cluster_by_distance=True
    )
    return presenter.present(graph, options)


def save_dot_file(graph: ModelGraph, filename: str = "model_graph.dot") -> None:
    """Save graph to DOT file for Graphviz rendering."""
    dot_output = create_dot_visualization(graph)
    with open(filename, "w") as f:
        f.write(dot_output)
    print(f"Saved: {filename}")
    print(f"Render: dot -Tpng {filename} -o {filename.replace('.dot', '.png')}")
