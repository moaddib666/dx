"""
DOT Graph Presenter for Model Dependencies
==========================================

DOT format presenter for visualizing model dependency graphs using Graphviz.
"""

import dataclasses
import logging
import typing as t
from collections import defaultdict

from .discovery_core import ModelGraph, ModelDependency, ModelRelation
from .presentor_core import (
    GraphAnalyzer, PresentationFormat, PresentationOptions, GraphAnalysisResult,
    GraphLayout
)
from .presentor_impl import BasicGraphAnalyzer

logger = logging.getLogger("apps.game.services.clone")


@dataclasses.dataclass(frozen=True)
class NodeStyle:
    """Visual styling for DOT graph nodes."""
    shape: str = "box"
    color: str = "black"
    fillcolor: str = "lightblue"
    style: str = "filled"
    fontname: str = "Arial"
    fontsize: str = "12"


@dataclasses.dataclass(frozen=True)
class EdgeStyle:
    """Visual styling for DOT graph edges."""
    color: str = "black"
    style: str = "solid"
    arrowhead: str = "normal"
    fontname: str = "Arial"
    fontsize: str = "10"
    penwidth: str = "1.0"


class DotPresenter:
    """
    Presents model dependency graphs as DOT format for Graphviz visualization.

    Generates DOT language output that can be rendered into visual graphs
    using Graphviz tools (dot, neato, fdp, etc.).
    """

    # Color palette for different apps
    APP_COLORS = [
        "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
        "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9",
        "#F8C471", "#82E0AA", "#F1948A", "#85CDBA", "#D7BDE2"
    ]

    # Colors for different relation types
    RELATION_COLORS = {
        "foreign_key": "#2C3E50",
        "one_to_one": "#8E44AD",
        "many_to_many": "#E67E22",
        "reverse_foreign_key": "#34495E",
        "reverse_one_to_one": "#9B59B6",
        "reverse_many_to_many": "#F39C12",
        "many_to_many_through": "#D35400"
    }

    # Edge styles for different relation types
    RELATION_STYLES = {
        "foreign_key": EdgeStyle(penwidth="2.0"),
        "one_to_one": EdgeStyle(penwidth="2.0", style="bold"),
        "many_to_many": EdgeStyle(penwidth="1.5", style="dashed"),
        "reverse_foreign_key": EdgeStyle(penwidth="1.0", style="dotted"),
        "reverse_one_to_one": EdgeStyle(penwidth="1.0", style="dotted", arrowhead="odot"),
        "reverse_many_to_many": EdgeStyle(penwidth="1.0", style="dotted", arrowhead="crow"),
        "many_to_many_through": EdgeStyle(penwidth="1.5", style="dashed", arrowhead="diamond")
    }

    def __init__(self, analyzer: t.Optional[GraphAnalyzer] = None):
        """
        Initialize the DOT presenter.

        :param analyzer: Optional graph analyzer for enhanced visualization
        """
        logger.debug("Initializing DotPresenter")
        self.analyzer = analyzer or BasicGraphAnalyzer()
        logger.debug("Using analyzer: %r", self.analyzer)
        self._app_color_map: t.Dict[str, str] = {}
        self._color_index = 0
        logger.debug("DotPresenter initialized")

    def get_format(self) -> PresentationFormat:
        """Return the DOT format."""
        logger.debug("DotPresenter.get_format() called, returning DOT format")
        return PresentationFormat.DOT

    def present(self,
                graph: ModelGraph,
                options: t.Optional[PresentationOptions] = None) -> str:
        """
        Present model dependency graph as DOT format for Graphviz.

        Creates a complete DOT graph description with models, relations,
        styling, and optional clustering by app.
        """
        logger.debug("DotPresenter.present() called with graph containing %d models and %d relations",
                     len(graph.nodes), len(graph.edges))

        if options is None:
            logger.debug("No options provided, using defaults")
            options = PresentationOptions()

        # Analyze graph for enhanced visualization
        logger.debug("Analyzing graph for enhanced visualization")
        analysis = self.analyzer.analyze(graph)
        logger.debug("Graph analysis complete: %d models, %d relations, has_cycles=%r",
                     analysis.total_nodes, analysis.total_edges, analysis.has_cycles)

        # Build DOT content
        logger.debug("Building DOT content")
        lines = []

        # Graph header
        logger.debug("Adding graph header")
        lines.append('digraph ModelDependencyGraph {')
        lines.append(f'    layout="{options.graph_layout}";')
        lines.append('    rankdir="TB";')
        lines.append('    node [fontname="Arial"];')
        lines.append('    edge [fontname="Arial"];')
        lines.append('')

        # Graph attributes for better visualization
        logger.debug("Generating graph attributes")
        lines.extend(self._generate_graph_attributes(options))
        lines.append('')

        # Generate clusters if requested
        if options.cluster_by_model:
            logger.debug("Generating clusters by app")
            lines.extend(self._generate_clusters(graph, analysis, options))
        else:
            # Generate individual models
            logger.debug("Generating individual models")
            lines.extend(self._generate_models(graph, analysis, options))

        lines.append('')

        # Generate relations
        logger.debug("Generating relations")
        lines.extend(self._generate_relations(graph, analysis, options))

        # Add legend if using colors
        if options.use_model_colors or options.show_relation_types:
            logger.debug("Generating legend")
            lines.append('')
            lines.extend(self._generate_legend(analysis, options))

        lines.append('}')

        logger.debug("DOT content generation complete, returning %d lines", len(lines))
        return '\n'.join(lines)

    def _generate_graph_attributes(self, options: PresentationOptions) -> t.List[str]:
        """Generate global graph attributes."""
        logger.debug("Generating graph attributes with layout: %s", options.graph_layout)

        lines = [
            '    // Graph styling',
            '    bgcolor="white";',
            '    pad="0.5";',
            '    nodesep="1.0";',
            '    ranksep="1.5";',
        ]

        if options.graph_layout == GraphLayout.DOT:
            logger.debug("Using DOT layout with orthogonal splines")
            lines.append('    splines="ortho";')
        elif options.graph_layout in [GraphLayout.NEATO, GraphLayout.FDP]:
            logger.debug("Using force-directed layout with overlap prevention")
            lines.append('    overlap="false";')
            lines.append('    sep="+25";')

        logger.debug("Generated %d lines of graph attributes", len(lines))
        return lines

    def _generate_clusters(self,
                           graph: ModelGraph,
                           analysis: GraphAnalysisResult,
                           options: PresentationOptions) -> t.List[str]:
        """Generate subgraph clusters grouped by app."""
        logger.debug("Generating clusters grouped by app")
        lines = []
        cluster_id = 0

        # Group models by app
        app_models: t.Dict[str, t.List[ModelDependency]] = defaultdict(list)
        for model in graph.nodes:
            app_models[model.app_label].append(model)

        logger.debug("Grouped models into %d apps", len(app_models))

        for app_label, models in sorted(app_models.items()):
            logger.debug("Processing app %s with %d models", app_label, len(models))

            if len(models) > 1:  # Only cluster if multiple models
                logger.debug("Creating cluster for app %s with %d models", app_label, len(models))
                lines.append(f'    subgraph cluster_{cluster_id} {{')
                lines.append(f'        label="{app_label}";')
                lines.append('        style="rounded,filled";')
                lines.append('        fillcolor="lightgrey";')
                lines.append('        fontsize="14";')
                lines.append('        fontweight="bold";')
                lines.append('')

                for model in sorted(models, key=lambda m: m.model_name):
                    logger.debug("Adding model %r to cluster %s", model, app_label)
                    model_lines = self._generate_single_model(model, analysis, options, indent="        ")
                    lines.extend(model_lines)

                lines.append('    }')
                lines.append('')
                cluster_id += 1
                logger.debug("Completed cluster %d for app %s", cluster_id - 1, app_label)
            else:
                # Single model, don't cluster
                logger.debug("Single model for app %s, not clustering", app_label)
                model_lines = self._generate_single_model(models[0], analysis, options)
                lines.extend(model_lines)

        logger.debug("Generated %d lines for %d clusters", len(lines), cluster_id)
        return lines

    def _generate_models(self,
                         graph: ModelGraph,
                         analysis: GraphAnalysisResult,
                         options: PresentationOptions) -> t.List[str]:
        """Generate all graph model nodes."""
        logger.debug("Generating all graph models for %d models", len(graph.nodes))
        lines = ['    // Models']

        for model in sorted(graph.nodes, key=lambda m: (m.app_label, m.model_name)):
            logger.debug("Generating definition for model %r", model)
            model_lines = self._generate_single_model(model, analysis, options)
            lines.extend(model_lines)

        logger.debug("Generated %d lines for models", len(lines))
        return lines

    def _generate_single_model(self,
                               model: ModelDependency,
                               analysis: GraphAnalysisResult,
                               options: PresentationOptions,
                               indent: str = "    ") -> t.List[str]:
        """Generate a single model definition."""
        model_id = self._get_model_id(model)
        label = self._create_model_label(model, options)
        style = self._get_model_style(model, analysis, options)

        # Check if model is part of a cycle
        is_in_cycle = any(
            any(cycle_model.app_label == model.app_label and cycle_model.model_name == model.model_name
                for cycle_model in cycle.cycle_models)
            for cycle in analysis.circular_dependencies
        )

        attributes = [f'label="{label}"']
        attributes.append(f'shape="{style.shape}"')
        attributes.append(f'fillcolor="{style.fillcolor}"')
        attributes.append(f'style="{style.style}"')
        attributes.append(f'fontname="{style.fontname}"')
        attributes.append(f'fontsize="{style.fontsize}"')

        if is_in_cycle and options.highlight_cycles:
            attributes.append('color="red"')
            attributes.append('penwidth="3.0"')
        else:
            attributes.append(f'color="{style.color}"')

        # Special styling for root models
        if model in analysis.total_nodes:  # This needs to be checked properly
            attributes.append('penwidth="2.0"')

        attr_string = ', '.join(attributes)
        return [f'{indent}{model_id} [{attr_string}];']

    def _generate_relations(self,
                            graph: ModelGraph,
                            analysis: GraphAnalysisResult,
                            options: PresentationOptions) -> t.List[str]:
        """Generate all graph relations."""
        logger.debug("Generating all graph relations for %d relations", len(graph.edges))
        lines = ['    // Relations']

        for relation in graph.edges:
            # Filter reverse relations if not requested
            if not options.include_reverse_relations and relation.is_reverse_relation:
                logger.debug("Skipping reverse relation %r (not requested)", relation)
                continue

            logger.debug("Generating edge for relation %r", relation)
            edge_lines = self._generate_single_relation(relation, analysis, options)
            lines.extend(edge_lines)

        logger.debug("Generated %d lines for relations", len(lines))
        return lines

    def _generate_single_relation(self,
                                  relation: ModelRelation,
                                  analysis: GraphAnalysisResult,
                                  options: PresentationOptions) -> t.List[str]:
        """Generate a single relation definition."""
        source_id = self._get_model_id(relation.source)
        target_id = self._get_model_id(relation.target)

        # Get edge styling
        style = self.RELATION_STYLES.get(relation.relation_type, EdgeStyle())
        color = self.RELATION_COLORS.get(relation.relation_type, "#2C3E50")

        attributes = [f'color="{color}"']
        attributes.append(f'style="{style.style}"')
        attributes.append(f'arrowhead="{style.arrowhead}"')
        attributes.append(f'penwidth="{style.penwidth}"')
        attributes.append(f'fontname="{style.fontname}"')
        attributes.append(f'fontsize="{style.fontsize}"')

        # Add edge label if requested
        if options.show_edge_labels:
            label_parts = []
            if options.show_relation_types:
                label_parts.append(relation.relation_type.replace('_', ' ').title())
            if options.show_metadata and relation.metadata and relation.metadata.field_name:
                label_parts.append(f"via {relation.metadata.field_name}")

            if label_parts:
                label = "\\n".join(label_parts)
                attributes.append(f'label="{label}"')

        attr_string = ', '.join(attributes)
        return [f'    {source_id} -> {target_id} [{attr_string}];']

    def _generate_legend(self,
                         analysis: GraphAnalysisResult,
                         options: PresentationOptions) -> t.List[str]:
        """Generate a legend for the graph."""
        lines = [
            '    // Legend',
            '    subgraph cluster_legend {',
            '        label="Legend";',
            '        style="rounded,filled";',
            '        fillcolor="lightyellow";',
            '        fontsize="12";',
            '        fontweight="bold";',
            '        rank="sink";',
            ''
        ]

        # App legend
        if options.use_model_colors:
            lines.append('        // Apps')
            for app_label in sorted(analysis.model_distribution.app_counts.keys()):
                color = self._get_app_color(app_label)
                legend_id = f'legend_{app_label.replace(".", "_")}'
                lines.append(
                    f'        {legend_id} [label="{app_label}", shape="box", fillcolor="{color}", style="filled"];')

        # Relation type legend
        if options.show_relation_types:
            lines.append('        // Relation Types')
            for relation_type in sorted(analysis.relation_distribution.relation_counts.keys()):
                color = self.RELATION_COLORS.get(relation_type, "#2C3E50")
                style = self.RELATION_STYLES.get(relation_type, EdgeStyle())
                legend_id = f'legend_rel_{relation_type}'
                display_name = relation_type.replace('_', ' ').title()

                # Create invisible nodes for edge legend
                lines.append(f'        {legend_id}_src [style="invis"];')
                lines.append(f'        {legend_id}_dst [label="{display_name}", shape="plaintext"];')
                lines.append(
                    f'        {legend_id}_src -> {legend_id}_dst [color="{color}", style="{style.style}", penwidth="{style.penwidth}"];')

        lines.append('    }')
        return lines

    def _get_model_id(self, model: ModelDependency) -> str:
        """Generate a unique DOT identifier for a model."""
        return f'{model.app_label}_{model.model_name}'.replace('.', '_').replace('-', '_')

    def _create_model_label(self, model: ModelDependency, options: PresentationOptions) -> str:
        """Create a display label for a model."""
        if not options.show_node_details:
            return f"{model.app_label}.{model.model_name}"

        label_parts = [model.model_class.__name__]
        label_parts.append(f"{model.app_label}.{model.model_name}")

        # Add verbose name if available
        if hasattr(model.model_class, '_meta'):
            verbose_name = str(getattr(model.model_class._meta, 'verbose_name', ''))
            if verbose_name and verbose_name != model.model_name:
                label_parts.append(f"({verbose_name})")

        return "\\n".join(label_parts)

    def _get_model_style(self,
                         model: ModelDependency,
                         analysis: GraphAnalysisResult,
                         options: PresentationOptions) -> NodeStyle:
        """Get styling for a model based on its properties."""

        # Base style
        style = NodeStyle()

        # Color by app if requested
        if options.use_model_colors:
            fillcolor = self._get_app_color(model.app_label)
            style = dataclasses.replace(style, fillcolor=fillcolor)

        # Special styling for root models
        if model in analysis.total_nodes:  # This needs proper checking
            style = dataclasses.replace(style, shape="ellipse", style="filled,bold")

        return style

    def _get_app_color(self, app_label: str) -> str:
        """Get a consistent color for an app."""
        if app_label not in self._app_color_map:
            color = self.APP_COLORS[self._color_index % len(self.APP_COLORS)]
            self._app_color_map[app_label] = color
            self._color_index += 1

        return self._app_color_map[app_label]
