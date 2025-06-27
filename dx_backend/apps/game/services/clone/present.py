from collections import defaultdict, deque
from typing import List, Set, Dict, Tuple, Optional, Any, Iterable

from apps.game.models import Campaign
from apps.game.services.clone.base import Dependency
from apps.game.services.clone.new import InstanceDependencyGraph


class DependencyGraph:
    """Represents the actual dependency graph structure"""

    def __init__(self):
        self.edges: Dict[str, List[Tuple[str, int]]] = defaultdict(list)  # model -> [(dependent_model, weight), ...]
        self.reverse_edges: Dict[str, List[Tuple[str, int]]] = defaultdict(list)  # dependent -> [(model, weight), ...]
        self.models: Dict[str, Any] = {}  # model_key -> actual model class
        self.weights: Dict[Tuple[str, str], int] = {}  # (from, to) -> weight

    def add_edge(self, from_model: str, to_model: str, weight: int, from_model_class: Any, to_model_class: Any):
        """Add an edge to the graph"""
        self.edges[from_model].append((to_model, weight))
        self.reverse_edges[to_model].append((from_model, weight))
        self.models[from_model] = from_model_class
        self.models[to_model] = to_model_class
        self.weights[(from_model, to_model)] = weight

    def get_dependencies(self, model_key: str) -> List[Tuple[str, int]]:
        """Get all models that depend on this model"""
        return self.edges[model_key]

    def get_dependents(self, model_key: str) -> List[Tuple[str, int]]:
        """Get all models this model depends on"""
        return self.reverse_edges[model_key]

    def get_all_models(self) -> Set[str]:
        """Get all model keys in the graph"""
        return set(self.models.keys())

    def topological_sort(self) -> List[str]:
        """Return models in topological order (dependencies first)"""
        in_degree = defaultdict(int)

        # Calculate in-degrees
        for model in self.get_all_models():
            in_degree[model] = len(self.get_dependents(model))

        # Start with models that have no dependencies
        queue = deque([model for model in self.get_all_models() if in_degree[model] == 0])
        result = []

        while queue:
            model = queue.popleft()
            result.append(model)

            # Remove this model from dependencies and update in-degrees
            for dependent, _ in self.get_dependencies(model):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        return result

    def find_root_models(self) -> List[str]:
        """Find models with no dependencies (potential root nodes)"""
        return [model for model in self.get_all_models() if not self.get_dependents(model)]

    def find_leaf_models(self) -> List[str]:
        """Find models with no dependents (leaf nodes)"""
        return [model for model in self.get_all_models() if not self.get_dependencies(model)]

    def get_shortest_path(self, from_model: str, to_model: str) -> Optional[List[Tuple[str, int]]]:
        """Find shortest weighted path between two models"""
        if from_model not in self.models or to_model not in self.models:
            return None

        # Dijkstra's algorithm
        distances = {model: float('inf') for model in self.get_all_models()}
        distances[from_model] = 0
        previous = {}
        unvisited = set(self.get_all_models())

        while unvisited:
            current = min(unvisited, key=lambda x: distances[x])
            if distances[current] == float('inf'):
                break

            unvisited.remove(current)

            if current == to_model:
                # Reconstruct path
                path = []
                while current != from_model:
                    prev = previous[current]
                    weight = self.weights[(prev, current)]
                    path.append((current, weight))
                    current = prev
                path.reverse()
                return path

            for neighbor, weight in self.get_dependencies(current):
                if neighbor in unvisited:
                    alt = distances[current] + weight
                    if alt < distances[neighbor]:
                        distances[neighbor] = alt
                        previous[neighbor] = current

        return None


class ShapeDistiller:

    def __init__(self):
        self.lookup_hash_store = set()

    def get_hash(self, dependency: Dependency) -> str:
        """Generate a unique hash for a dependency based on source and target"""
        return f"{dependency.source._meta.label}.{dependency.target._meta.label}.{dependency.field.name}"

    def _add_to_lookup(self, dependency: Dependency) -> bool:
        """Add a dependency to the lookup store if it's unique"""
        dep_hash = self.get_hash(dependency)
        if dep_hash in self.lookup_hash_store:
            return False
        self.lookup_hash_store.add(dep_hash)
        return True

    def _clear_lookup(self):
        """Clear the lookup store"""
        self.lookup_hash_store.clear()

    def distill(self, dependencies: Iterable[Dependency]) -> Set[Dependency]:
        """Distill dependencies to unique ones based on source and target"""
        result = {dep for dep in dependencies if self._add_to_lookup(dep)}
        self._clear_lookup()
        return result


class DependencyGraphPresenter:
    """Presents Django model dependency graphs"""

    def __init__(self, dependencies: List[Dependency], distiller: ShapeDistiller = None):
        if distiller:
            dependencies = distiller.distill(dependencies)
        self.dependencies = dependencies
        self.graph = self._build_graph()

    def _get_model_key(self, model: Any) -> str:
        """Get a unique key for a Django model"""
        if hasattr(model, '_meta'):
            # Django model
            return f"{model._meta.app_label}.{model._meta.model_name}"
        elif hasattr(model, '__name__'):
            # Regular class
            return model.__name__
        else:
            # Fallback
            return str(model)

    def _get_model_label(self, model: Any) -> str:
        """Get a human-readable label for a Django model"""
        if hasattr(model, '_meta'):
            if hasattr(model._meta, 'verbose_name'):
                return model._meta.verbose_name.title()
            else:
                return model._meta.model_name.replace('_', ' ').title()
        elif hasattr(model, '__name__'):
            return model.__name__
        else:
            return str(model)

    def _build_graph(self) -> DependencyGraph:
        """Build the dependency graph from the dependency list"""
        graph = DependencyGraph()

        for dep in self.dependencies:
            source_key = self._get_model_key(dep.source)
            target_key = self._get_model_key(dep.target)

            if dep.reverse:
                # If reverse=True, the actual dependency is target -> source
                # target depends on source (source is required for target)
                graph.add_edge(source_key, target_key, dep.layer, dep.source, dep.target)
            else:
                # Normal dependency: source -> target
                # source depends on target (target is required for source)
                graph.add_edge(target_key, source_key, dep.layer, dep.target, dep.source)

        return graph

    def analyze_graph(self) -> Dict[str, Any]:
        """Analyze the dependency graph structure"""
        analysis = {
            'total_models': len(self.graph.get_all_models()),
            'total_dependencies': sum(len(deps) for deps in self.graph.edges.values()),
            'root_models': self.graph.find_root_models(),
            'leaf_models': self.graph.find_leaf_models(),
            'topological_order': self.graph.topological_sort(),
            'cycles': self._detect_cycles(),
            'max_depth': self._calculate_max_depth(),
            'dependency_layers': self._group_by_dependency_distance()
        }
        return analysis

    def _detect_cycles(self) -> List[List[str]]:
        """Detect cycles in the dependency graph"""
        visited = set()
        rec_stack = set()
        cycles = []

        def dfs(node, path):
            if node in rec_stack:
                # Found a cycle
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return

            if node in visited:
                return

            visited.add(node)
            rec_stack.add(node)

            for neighbor, _ in self.graph.get_dependencies(node):
                dfs(neighbor, path + [neighbor])

            rec_stack.remove(node)

        for model in self.graph.get_all_models():
            if model not in visited:
                dfs(model, [model])

        return cycles

    def _calculate_max_depth(self) -> int:
        """Calculate the maximum dependency depth"""
        root_models = self.graph.find_root_models()
        if not root_models:
            return 0

        max_depth = 0
        for root in root_models:
            depth = self._dfs_max_depth(root, set())
            max_depth = max(max_depth, depth)

        return max_depth

    def _dfs_max_depth(self, node: str, visited: Set[str]) -> int:
        """DFS to find maximum depth from a node"""
        if node in visited:
            return 0  # Avoid infinite recursion in cycles

        visited.add(node)
        max_child_depth = 0

        for neighbor, weight in self.graph.get_dependencies(node):
            child_depth = self._dfs_max_depth(neighbor, visited.copy())
            max_child_depth = max(max_child_depth, child_depth + weight)

        return max_child_depth

    def _group_by_dependency_distance(self) -> Dict[int, List[str]]:
        """Group models by their dependency distance from root"""
        root_models = self.graph.find_root_models()
        if not root_models:
            return {}

        distances = {}

        def calculate_distance(node, current_distance):
            if node not in distances or distances[node] > current_distance:
                distances[node] = current_distance
                for neighbor, weight in self.graph.get_dependencies(node):
                    calculate_distance(neighbor, current_distance + weight)

        for root in root_models:
            calculate_distance(root, 0)

        # Group by distance
        groups = defaultdict(list)
        for model, distance in distances.items():
            groups[distance].append(model)

        return dict(groups)

    def generate_dot(self,
                     graph_name: str = "dependency_graph",
                     show_weights: bool = True,
                     color_by_layer: bool = True,
                     rankdir: str = "TB") -> str:
        """Generate DOT format representation"""

        dot_lines = [f'digraph {graph_name} {{']
        dot_lines.append(f'    rankdir={rankdir};')
        dot_lines.append('    node [shape=box, style="rounded,filled", fontname="Arial"];')
        dot_lines.append('    edge [fontname="Arial", fontsize="10"];')
        dot_lines.append('')

        # Color palette for layers
        colors = ["lightblue", "lightgreen", "lightyellow", "lightcoral",
                  "lightpink", "lightgray", "lightsalmon", "lightcyan"]

        # Add nodes with layer-based coloring
        if color_by_layer:
            layer_groups = self._group_by_dependency_distance()
            for layer, models in layer_groups.items():
                color = colors[layer % len(colors)]
                dot_lines.append(f'    // Layer {layer}')
                for model in models:
                    label = self._get_model_label(self.graph.models[model])
                    dot_lines.append(f'    "{model}" [label="{label}", fillcolor="{color}"];')
                dot_lines.append('')
        else:
            for model_key, model_class in self.graph.models.items():
                label = self._get_model_label(model_class)
                dot_lines.append(f'    "{model_key}" [label="{label}"];')

        # Add edges
        dot_lines.append('    // Dependencies')
        for from_model in self.graph.get_all_models():
            for to_model, weight in self.graph.get_dependencies(from_model):
                if show_weights:
                    dot_lines.append(f'    "{from_model}" -> "{to_model}" [label="{weight}"];')
                else:
                    dot_lines.append(f'    "{from_model}" -> "{to_model}";')

        dot_lines.append('}')
        return '\n'.join(dot_lines)

    def render_image(self,
                     output_path: str = "dependency_graph",
                     format: str = "png",
                     cleanup: bool = True,
                     **dot_kwargs) -> str:
        """Render the dependency graph as an image"""
        try:
            import graphviz
        except ImportError:
            raise ImportError("graphviz package is required. Install with: pip install graphviz")

        dot_content = self.generate_dot(**dot_kwargs)
        dot = graphviz.Source(dot_content)
        output_file = dot.render(output_path, format=format, cleanup=cleanup, view=True)
        return output_file

    def print_analysis(self):
        """Print detailed analysis of the dependency graph"""
        analysis = self.analyze_graph()

        print("=== Dependency Graph Analysis ===")
        print(f"Total Models: {analysis['total_models']}")
        print(f"Total Dependencies: {analysis['total_dependencies']}")
        print(f"Maximum Depth: {analysis['max_depth']}")
        print()

        print("Root Models (no dependencies):")
        for model in analysis['root_models']:
            label = self._get_model_label(self.graph.models[model])
            print(f"  - {label} ({model})")
        print()

        print("Leaf Models (no dependents):")
        for model in analysis['leaf_models']:
            label = self._get_model_label(self.graph.models[model])
            print(f"  - {label} ({model})")
        print()

        print("Dependency Layers:")
        for layer in sorted(analysis['dependency_layers'].keys()):
            models = analysis['dependency_layers'][layer]
            print(f"  Layer {layer} ({len(models)} models):")
            for model in models:
                label = self._get_model_label(self.graph.models[model])
                print(f"    - {label} ({model})")
        print()

        if analysis['cycles']:
            print("⚠️  Detected Dependency Cycles:")
            for i, cycle in enumerate(analysis['cycles']):
                print(f"  Cycle {i + 1}: {' -> '.join(cycle)}")
        else:
            print("✅ No dependency cycles detected")
        print()

        print("Topological Order (dependencies first):")
        for i, model in enumerate(analysis['topological_order']):
            label = self._get_model_label(self.graph.models[model])
            print(f"  {i + 1}. {label} ({model})")

    def get_dependency_path(self, from_model: Any, to_model: Any) -> Optional[List[str]]:
        """Get the dependency path between two models"""
        from_key = self._get_model_key(from_model)
        to_key = self._get_model_key(to_model)

        path = self.graph.get_shortest_path(from_key, to_key)
        if path:
            return [from_key] + [step[0] for step in path]
        return None


if __name__ == '__main__':
    campaign = Campaign.objects.get(name="The Test Campaign")
    campaign = Campaign.objects.get(name="First Campaign")
    graph = InstanceDependencyGraph(campaign)
    dependencies = graph.discover()
    presenter = DependencyGraphPresenter(dependencies)
    presenter.print_analysis()
    presenter.render_image(output_path="campaign_dependency_graph", format="png", show_weights=True,
                           color_by_layer=True)
