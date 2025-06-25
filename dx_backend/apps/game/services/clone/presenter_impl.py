"""
Model Graph Presenters - Implementations
========================================

Concrete implementations of model dependency graph presenters for different output formats.
"""

import dataclasses
import json
import logging
import typing as t
from collections import defaultdict, deque

from .discovery_core import ModelGraph, ModelDependency, ModelRelation
from .presenter_core import (
    GraphAnalysisResult, ModelDistribution, RelationDistribution,
    DepthAnalysis, CircularDependency, SerializedModel, GraphAnalyzer,
    PresentationFormat, PresentationOptions, JsonGraphRepresentation,
    GraphStructure, GraphMetadata, SerializedModelRelation,
    SerializedRelationshipMetadata
)

logger = logging.getLogger("apps.game.services.clone")


class BasicGraphAnalyzer:
    """Basic implementation of model graph analysis functionality."""

    def analyze(self, graph: ModelGraph) -> GraphAnalysisResult:
        """Analyze model dependency graph and return comprehensive statistics."""
        logger.debug("Starting graph analysis for graph with %d models and %d relations",
                     len(graph.nodes), len(graph.edges))

        logger.debug("Analyzing model distribution")
        model_distribution = self._analyze_model_distribution(graph)

        logger.debug("Analyzing relation types")
        relation_distribution = self._analyze_relation_types(graph)

        logger.debug("Analyzing depth structure")
        depth_analysis = self._analyze_depth(graph)

        logger.debug("Detecting cycles")
        circular_dependencies = self._detect_cycles(graph)

        logger.debug("Finding orphaned models")
        orphaned_models = self._find_orphaned_models(graph)

        logger.debug("Analysis complete: %d models, %d relations, %d apps, %d relation types, %d cycles, %d orphans",
                     len(graph.nodes), len(graph.edges),
                     model_distribution.total_apps, relation_distribution.total_relation_types,
                     len(circular_dependencies), len(orphaned_models))

        return GraphAnalysisResult(
            total_nodes=len(graph.nodes),
            total_edges=len(graph.edges),
            has_root=len(graph.root_models) > 0,
            model_distribution=model_distribution,
            relation_distribution=relation_distribution,
            depth_analysis=depth_analysis,
            circular_dependencies=circular_dependencies,
            orphaned_models=orphaned_models
        )

    def _analyze_model_distribution(self, graph: ModelGraph) -> ModelDistribution:
        """Count models by app and type."""
        app_distribution = defaultdict(int)
        model_distribution = defaultdict(int)

        for model in graph.nodes:
            app_distribution[model.app_label] += 1
            model_distribution[f"{model.app_label}.{model.model_name}"] += 1

        return ModelDistribution(
            app_counts=dict(app_distribution),
            model_counts=dict(model_distribution)
        )

    def _analyze_relation_types(self, graph: ModelGraph) -> RelationDistribution:
        """Count relationships by type."""
        distribution = defaultdict(int)
        for relation in graph.edges:
            distribution[relation.relation_type] += 1
        return RelationDistribution(relation_counts=dict(distribution))

    def _analyze_depth(self, graph: ModelGraph) -> DepthAnalysis:
        """Analyze graph depth from root models."""
        if not graph.root_models:
            return DepthAnalysis(max_depth=0, depth_distribution={})

        depths = {}
        queue = deque()

        # Start from all root models
        for root_model in graph.root_models:
            queue.append((root_model, 0))

        visited = set()

        while queue:
            model, depth = queue.popleft()
            if model in visited:
                continue

            visited.add(model)
            depths[model] = depth

            # Find outgoing relations
            for relation in graph.edges:
                if relation.source == model and relation.target not in visited:
                    queue.append((relation.target, depth + 1))

        max_depth = max(depths.values()) if depths else 0
        depth_distribution = defaultdict(int)
        for depth in depths.values():
            depth_distribution[depth] += 1

        return DepthAnalysis(
            max_depth=max_depth,
            depth_distribution=dict(depth_distribution)
        )

    def _detect_cycles(self, graph: ModelGraph) -> t.List[CircularDependency]:
        """Detect circular dependencies using DFS."""
        visited = set()
        rec_stack = set()
        cycles = []

        def dfs(model, path):
            if model in rec_stack:
                # Found a cycle
                cycle_start = path.index(model)
                cycle_models = [self._serialize_model_for_analysis(m) for m in path[cycle_start:] + [model]]
                cycles.append(CircularDependency(cycle_models=cycle_models, cycle_length=len(cycle_models)))
                return

            if model in visited:
                return

            visited.add(model)
            rec_stack.add(model)

            # Find outgoing relations
            for relation in graph.edges:
                if relation.source == model:
                    dfs(relation.target, path + [model])

            rec_stack.remove(model)

        for model in graph.nodes:
            if model not in visited:
                dfs(model, [])

        return cycles

    def _find_orphaned_models(self, graph: ModelGraph) -> t.List[SerializedModel]:
        """Find models with no incoming or outgoing relationships."""
        models_with_relations = set()

        for relation in graph.edges:
            models_with_relations.add(relation.source)
            models_with_relations.add(relation.target)

        orphaned = [model for model in graph.nodes if model not in models_with_relations]
        return [self._serialize_model_for_analysis(model) for model in orphaned]

    def _serialize_model_for_analysis(self, model: ModelDependency) -> SerializedModel:
        """Serialize model dependency for analysis results."""
        verbose_name = None
        if hasattr(model.model_class, '_meta'):
            verbose_name = str(getattr(model.model_class._meta, 'verbose_name', ''))

        return SerializedModel(
            model_type=model.model_class.__name__,
            app_label=model.app_label,
            model_name=model.model_name,
            verbose_name=verbose_name
        )


class TextTreePresenter:
    """
    Presents model dependency graphs as hierarchical text trees.

    Outputs human-readable tree structures showing the relationships
    between model classes in a clear, indented format.
    """

    def __init__(self, analyzer: t.Optional[GraphAnalyzer] = None):
        """
        Initialize the text tree presenter.

        :param analyzer: Optional graph analyzer for statistics
        """
        logger.debug("Initializing TextTreePresenter")
        self.analyzer = analyzer or BasicGraphAnalyzer()
        logger.debug("Using analyzer: %r", self.analyzer)
        logger.debug("TextTreePresenter initialized")

    def get_format(self) -> PresentationFormat:
        """Return the TEXT format."""
        logger.debug("TextTreePresenter.get_format() called, returning TEXT format")
        return PresentationFormat.TEXT

    def present(self,
                graph: ModelGraph,
                options: t.Optional[PresentationOptions] = None) -> str:
        """
        Present model dependency graph as a hierarchical text tree.

        Creates a tree-like structure starting from the root models
        and showing all relationships with proper indentation.
        """
        logger.debug("TextTreePresenter.present() called with graph containing %d models and %d relations",
                     len(graph.nodes), len(graph.edges))

        if options is None:
            options = PresentationOptions()

        lines = []

        # Add header
        lines.append("Model Dependency Graph Tree")
        lines.append("=" * 60)
        lines.append("")

        # Add statistics if requested
        if options.include_statistics:
            lines.extend(self._format_statistics(graph))
            lines.append("")

        # Build the tree structure
        if graph.root_models:
            visited = set()
            logger.debug("Building tree from %d root models", len(graph.root_models))

            for root_model in sorted(graph.root_models, key=lambda m: (m.app_label, m.model_name)):
                self._build_tree_recursive(
                    graph,
                    root_model,
                    lines,
                    visited,
                    0,
                    options
                )
                lines.append("")  # Separate each root tree
        else:
            # No root - show all models
            lines.append("No root models found. Showing all models:")
            lines.append("")

            if options.sort_by_model_type:
                models = sorted(graph.nodes, key=lambda m: (m.app_label, m.model_name))
            else:
                models = list(graph.nodes)

            for model in models:
                lines.append(f"• {self._format_model(model, options)}")
                relations = graph.get_relations_for_model(model)
                for relation in relations:
                    lines.append(f"  └─ {self._format_relation(relation, options)}")

        return "\n".join(lines)

    def _build_tree_recursive(self,
                              graph: ModelGraph,
                              current_model: ModelDependency,
                              lines: t.List[str],
                              visited: t.Set[ModelDependency],
                              depth: int,
                              options: PresentationOptions) -> None:
        """Recursively build tree structure."""

        # Check depth limit
        if options.max_depth is not None and depth > options.max_depth:
            return

        # Format current model
        indent = "  " * depth
        prefix = "├─ " if depth > 0 else "• "

        if current_model in visited:
            lines.append(f"{indent}{prefix}{self._format_model(current_model, options)} [CIRCULAR]")
            return

        lines.append(f"{indent}{prefix}{self._format_model(current_model, options)}")
        visited.add(current_model)

        # Get relations from this model
        relations = graph.get_relations_for_model(current_model)

        # Filter relations if needed
        if not options.include_reverse_relations:
            relations = [r for r in relations if not r.is_reverse_relation]

        # Sort relations for consistent output
        relations = sorted(relations, key=lambda r: (
            r.relation_type,
            r.target.app_label,
            r.target.model_name
        ))

        for i, relation in enumerate(relations):
            child_indent = "  " * (depth + 1)

            if options.show_relation_types:
                relation_info = f"[{relation.relation_type}]"
                if options.show_metadata and relation.metadata.field_name:
                    relation_info += f" via {relation.metadata.field_name}"
                lines.append(f"{child_indent}│")
                lines.append(f"{child_indent}└─ {relation_info}")

            self._build_tree_recursive(
                graph,
                relation.target,
                lines,
                visited.copy(),  # Use copy to allow revisiting in different branches
                depth + 1,
                options
            )

    def _format_model(self, model: ModelDependency, options: PresentationOptions) -> str:
        """Format a model dependency for display."""
        return f"{model.app_label}.{model.model_name}"

    def _format_relation(self, relation: ModelRelation, options: PresentationOptions) -> str:
        """Format a relation for display."""
        target_str = self._format_model(relation.target, options)

        if options.show_relation_types:
            relation_str = f"[{relation.relation_type}] → {target_str}"
        else:
            relation_str = f"→ {target_str}"

        if options.show_metadata and relation.metadata.field_name:
            relation_str += f" (via {relation.metadata.field_name})"

        return relation_str

    def _format_statistics(self, graph: ModelGraph) -> t.List[str]:
        """Format graph statistics."""
        analysis = self.analyzer.analyze(graph)

        lines = [
            "Graph Statistics:",
            f"  Total Models: {analysis.total_nodes}",
            f"  Total Relations: {analysis.total_edges}",
            f"  Has Root Models: {analysis.has_root}",
            f"  Max Depth: {analysis.depth_analysis.max_depth}",
            f"  Average Depth: {analysis.depth_analysis.average_depth:.2f}",
            "",
            "App Distribution:"
        ]

        for app_label, count in sorted(analysis.model_distribution.app_counts.items()):
            lines.append(f"  {app_label}: {count}")

        lines.append("")
        lines.append("Model Distribution:")

        for model_name, count in sorted(analysis.model_distribution.model_counts.items()):
            lines.append(f"  {model_name}: {count}")

        lines.append("")
        lines.append("Relation Types:")

        for relation_type, count in sorted(analysis.relation_distribution.relation_counts.items()):
            lines.append(f"  {relation_type}: {count}")

        if analysis.has_cycles:
            lines.append("")
            lines.append(f"⚠️  Circular Dependencies Detected: {len(analysis.circular_dependencies)}")

        if analysis.has_orphans:
            lines.append(f"⚠️  Orphaned Models Found: {len(analysis.orphaned_models)}")

        return lines


class JsonPresenter:
    """
    Presents model dependency graphs as structured JSON data.

    Outputs machine-readable JSON format suitable for APIs,
    serialization, or further processing by other systems.
    """

    def __init__(self, analyzer: t.Optional[GraphAnalyzer] = None):
        """
        Initialize the JSON presenter.

        :param analyzer: Optional graph analyzer for statistics
        """
        logger.debug("Initializing JsonPresenter")
        self.analyzer = analyzer or BasicGraphAnalyzer()
        logger.debug("JsonPresenter initialized")

    def get_format(self) -> PresentationFormat:
        """Return the JSON format."""
        return PresentationFormat.JSON

    def present(self,
                graph: ModelGraph,
                options: t.Optional[PresentationOptions] = None) -> str:
        """
        Present model dependency graph as structured JSON.

        Creates a comprehensive JSON representation including models,
        relations, metadata, and optional statistics.
        """
        logger.debug("JsonPresenter.present() called with graph containing %d models and %d relations",
                     len(graph.nodes), len(graph.edges))

        if options is None:
            options = PresentationOptions()

        # Build JSON structure
        graph_structure = self._create_graph_structure(graph, options)
        metadata = self._create_graph_metadata(graph, options)

        json_representation = JsonGraphRepresentation(
            graph=graph_structure,
            metadata=metadata,
            statistics=self.analyzer.analyze(graph) if options.include_statistics else None
        )

        return json.dumps(
            dataclasses.asdict(json_representation),
            indent=options.indent_size,
            default=self._json_serializer
        )

    def _create_graph_structure(self, graph: ModelGraph, options: PresentationOptions) -> GraphStructure:
        """Create the core graph structure."""
        models = self._serialize_models(graph, options)
        relations = self._serialize_relations(graph, options)
        root_models = [self._serialize_model(model, options) for model in graph.root_models]

        return GraphStructure(models=models, relations=relations, root_models=root_models)

    def _create_graph_metadata(self, graph: ModelGraph, options: PresentationOptions) -> GraphMetadata:
        """Create graph metadata."""
        return GraphMetadata(
            total_models=len(graph.nodes),
            total_relations=len(graph.edges),
            has_root=len(graph.root_models) > 0,
            presentation_options=options
        )

    def _serialize_models(self, graph: ModelGraph, options: PresentationOptions) -> t.List[SerializedModel]:
        """Serialize graph models to structured format."""
        models = []

        for model in graph.nodes:
            serialized_model = self._serialize_model(model, options)
            models.append(serialized_model)

        # Sort models for consistent output
        if options.sort_by_model_type:
            models.sort(key=lambda m: (m.app_label, m.model_name))

        return models

    def _serialize_relations(self, graph: ModelGraph, options: PresentationOptions) -> t.List[SerializedModelRelation]:
        """Serialize graph relations to structured format."""
        relations = []

        for relation in graph.edges:
            # Filter reverse relations if not requested
            if not options.include_reverse_relations and relation.is_reverse_relation:
                continue

            serialized_relation = SerializedModelRelation(
                source=self._serialize_model(relation.source, options),
                target=self._serialize_model(relation.target, options),
                relation_type=relation.relation_type,
                is_reverse=relation.is_reverse_relation,
                is_many=relation.is_many_relation,
                metadata=self._serialize_metadata(relation.metadata) if options.show_metadata else None
            )

            relations.append(serialized_relation)

        return relations

    def _serialize_model(self, model: ModelDependency, options: PresentationOptions) -> SerializedModel:
        """Serialize a single model dependency to structured format."""
        verbose_name = None
        if hasattr(model.model_class, '_meta'):
            verbose_name = str(getattr(model.model_class._meta, 'verbose_name', ''))

        return SerializedModel(
            model_type=model.model_class.__name__,
            app_label=model.app_label,
            model_name=model.model_name,
            verbose_name=verbose_name
        )

    def _serialize_metadata(self, metadata) -> SerializedRelationshipMetadata:
        """Serialize relationship metadata to structured format."""
        return SerializedRelationshipMetadata(
            field_name=metadata.field_name,
            related_name=metadata.related_name,
            through_model=metadata.through_model.__name__ if metadata.through_model else None,
            null=metadata.null,
            blank=metadata.blank,
            on_delete=metadata.on_delete,
            db_column=metadata.db_column
        )

    def _json_serializer(self, obj: t.Any) -> t.Any:
        """Custom JSON serializer for non-standard types."""
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        elif hasattr(obj, '__str__'):
            return str(obj)
        else:
            return f"<{type(obj).__name__} object>"
