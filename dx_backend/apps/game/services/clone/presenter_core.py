"""
Model Graph Presenters - Core Abstractions
==========================================

This module provides abstract protocols for presenting model dependency graphs
and concrete implementations for different output formats with proper typing.
"""

import dataclasses
import logging
import typing as t
from abc import abstractmethod
from enum import StrEnum

from .discovery_core import ModelGraph, ModelDependency, ModelRelation, RelationType

logger = logging.getLogger("apps.game.services.clone")


class PresentationFormat(StrEnum):
    """Supported presentation formats."""
    TEXT = "text"
    JSON = "json"
    HTML = "html"
    DOT = "dot"
    CSV = "csv"


class GraphLayout(StrEnum):
    """Supported graph layout algorithms for DOT presenter."""
    DOT = "dot"  # Hierarchical layout (default)
    NEATO = "neato"  # Spring model layout
    FDP = "fdp"  # Force-directed placement
    CIRCO = "circo"  # Circular layout
    TWOPI = "twopi"  # Radial layout
    SFDP = "sfdp"  # Scalable force-directed placement


@dataclasses.dataclass(frozen=True)
class PresentationOptions:
    """Configuration options for presentation."""
    show_metadata: bool = True
    show_relation_types: bool = True
    max_depth: t.Optional[int] = None
    include_reverse_relations: bool = True
    sort_by_model_type: bool = False
    indent_size: int = 2
    include_statistics: bool = False
    # DOT-specific options
    graph_layout: GraphLayout = GraphLayout.DOT
    show_node_details: bool = True
    use_model_colors: bool = True
    show_edge_labels: bool = True
    cluster_by_model: bool = False
    highlight_cycles: bool = True


@dataclasses.dataclass(frozen=True)
class ModelDistribution:
    """Distribution of models by app."""
    app_counts: t.Dict[str, int]
    model_counts: t.Dict[str, int]

    @property
    def total_apps(self) -> int:
        result = len(self.app_counts)
        logger.debug("ModelDistribution.total_apps: %d", result)
        return result

    @property
    def total_models(self) -> int:
        result = len(self.model_counts)
        logger.debug("ModelDistribution.total_models: %d", result)
        return result


@dataclasses.dataclass(frozen=True)
class RelationDistribution:
    """Distribution of relationships by type."""
    relation_counts: t.Dict[str, int]

    @property
    def total_relation_types(self) -> int:
        result = len(self.relation_counts)
        logger.debug("RelationDistribution.total_relation_types: %d", result)
        return result

    @property
    def total_relations(self) -> int:
        result = sum(self.relation_counts.values())
        logger.debug("RelationDistribution.total_relations: %d", result)
        return result


@dataclasses.dataclass(frozen=True)
class DepthAnalysis:
    """Analysis of graph depth structure."""
    max_depth: int
    depth_distribution: t.Dict[int, int]

    @property
    def average_depth(self) -> float:
        logger.debug("Calculating average depth")
        if not self.depth_distribution:
            logger.debug("Empty depth distribution, returning 0.0")
            return 0.0
        total_nodes = sum(self.depth_distribution.values())
        weighted_sum = sum(depth * count for depth, count in self.depth_distribution.items())
        result = weighted_sum / total_nodes
        logger.debug("Average depth: %.2f (total nodes: %d, weighted sum: %d)",
                     result, total_nodes, weighted_sum)
        return result


@dataclasses.dataclass(frozen=True)
class CircularDependency:
    """Represents a circular dependency cycle."""
    cycle_models: t.List['SerializedModel']
    cycle_length: int

    def __post_init__(self):
        cycle_length = len(self.cycle_models)
        logger.debug("Initializing CircularDependency with %d models", cycle_length)
        object.__setattr__(self, 'cycle_length', cycle_length)


@dataclasses.dataclass(frozen=True)
class GraphAnalysisResult:
    """Complete analysis result of a model dependency graph."""
    total_nodes: int
    total_edges: int
    has_root: bool
    model_distribution: ModelDistribution
    relation_distribution: RelationDistribution
    depth_analysis: DepthAnalysis
    circular_dependencies: t.List[CircularDependency]
    orphaned_models: t.List['SerializedModel']

    @property
    def has_cycles(self) -> bool:
        result = len(self.circular_dependencies) > 0
        logger.debug("GraphAnalysisResult.has_cycles: %r (found %d cycles)",
                     result, len(self.circular_dependencies))
        return result

    @property
    def has_orphans(self) -> bool:
        result = len(self.orphaned_models) > 0
        logger.debug("GraphAnalysisResult.has_orphans: %r (found %d orphaned models)",
                     result, len(self.orphaned_models))
        return result


@dataclasses.dataclass(frozen=True)
class SerializedModel:
    """Serialized representation of a model dependency."""
    model_type: str
    app_label: str
    model_name: str
    verbose_name: t.Optional[str] = None


@dataclasses.dataclass(frozen=True)
class SerializedRelationshipMetadata:
    """Serialized relationship metadata."""
    field_name: t.Optional[str]
    related_name: t.Optional[str]
    through_model: t.Optional[str]
    null: bool
    blank: bool
    on_delete: t.Optional[str]
    db_column: t.Optional[str]


@dataclasses.dataclass(frozen=True)
class SerializedModelRelation:
    """Serialized representation of a model relation."""
    source: SerializedModel
    target: SerializedModel
    relation_type: str
    is_reverse: bool
    is_many: bool
    metadata: t.Optional[SerializedRelationshipMetadata] = None


@dataclasses.dataclass(frozen=True)
class GraphStructure:
    """Core graph structure for JSON serialization."""
    models: t.List[SerializedModel]
    relations: t.List[SerializedModelRelation]
    root_models: t.List[SerializedModel]


@dataclasses.dataclass(frozen=True)
class GraphMetadata:
    """Metadata about the graph presentation."""
    total_models: int
    total_relations: int
    has_root: bool
    presentation_options: PresentationOptions


@dataclasses.dataclass(frozen=True)
class JsonGraphRepresentation:
    """Complete JSON representation of a model dependency graph."""
    graph: GraphStructure
    metadata: GraphMetadata
    statistics: t.Optional[GraphAnalysisResult] = None


# =============================================================================
# ABSTRACT PRESENTATION PROTOCOLS
# =============================================================================

class ModelGraphPresenter(t.Protocol):
    """Protocol for presenting model dependency graphs in various formats."""

    @abstractmethod
    def present(self,
                graph: ModelGraph,
                options: t.Optional[PresentationOptions] = None) -> str:
        """
        Present a model dependency graph in a specific format.

        :param graph: The model dependency graph to present
        :param options: Optional presentation configuration
        :return: String representation of the graph
        """
        ...

    @abstractmethod
    def get_format(self) -> PresentationFormat:
        """Return the format this presenter outputs."""
        ...


class GraphAnalyzer(t.Protocol):
    """Protocol for analyzing model dependency graphs before presentation."""

    @abstractmethod
    def analyze(self, graph: ModelGraph) -> GraphAnalysisResult:
        """
        Analyze a model dependency graph and return statistics.

        :param graph: The model dependency graph to analyze
        :return: Complete analysis results
        """
        ...
