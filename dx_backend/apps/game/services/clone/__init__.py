"""
Django Model Dependency Discovery and Cloning Services
=====================================================

This package provides a comprehensive system for discovering and analyzing
dependencies between Django model classes. It focuses on schema-level analysis
to understand relationships between models without touching the database.

Main Components:
- Model Discovery: Analyze Django model relationships
- Graph Presentation: Visualize dependency graphs in various formats
- Filtering System: Control which models and relationships to include

Example Usage:
    # Basic model discovery
    from apps.game.services.clone import DjangoModelDiscoveryService

    discovery_service = DjangoModelDiscoveryService()
    graph = discovery_service.discover_model_dependencies([BlogPost, User])

    # Present as text tree
    from apps.game.services.clone import PresenterFactory, PresentationFormat

    presenter = PresenterFactory.create_presenter(PresentationFormat.TEXT)
    output = presenter.present(graph)
    print(output)

    # Generate DOT for Graphviz
    dot_presenter = PresenterFactory.create_presenter(PresentationFormat.DOT)
    dot_output = dot_presenter.present(graph)
"""

# =============================================================================
# CORE DISCOVERY TYPES AND PROTOCOLS
# =============================================================================

from .discovery_core import (
    # Core Types
    RelationType,
    ModelDependency,
    ModelRelation,
    ModelGraph,
    RelationshipMetadata,

    # Protocols
    FilterModel,
    ModelDiscoveryService,

    # Basic Filters
    AcceptAllModels,
    ExcludeModelTypes,
    ExcludeRelationTypes,
    CompositeFilter,
    TagsFilter,
)
from .discovery_impl import (
    # Main Django Implementation
    DjangoModelDiscoveryService,

    # Django-specific Metadata
    DjangoRelationshipMetadata,
)
from .presenter_core import (
    # Presentation Types
    PresentationFormat,
    PresentationOptions,
    GraphLayout,

    # Analysis Results
    GraphAnalysisResult,
    ModelDistribution,
    RelationDistribution,
    DepthAnalysis,
    CircularDependency,

    # Protocols
    ModelGraphPresenter,
    GraphAnalyzer,
)
from .presenter_dot import (
    DotPresenter,
)
from .presenter_factory import (
    PresenterFactory,
)
from .presenter_impl import (
    # Presenters
    TextTreePresenter,
    JsonPresenter,

    # Analyzer
    BasicGraphAnalyzer,
)

# =============================================================================
# DJANGO IMPLEMENTATION
# =============================================================================
# =============================================================================
# PRESENTATION CORE
# =============================================================================
# =============================================================================
# PRESENTATION IMPLEMENTATIONS
# =============================================================================
# =============================================================================
# FACTORY
# =============================================================================

# =============================================================================
# PUBLIC API
# =============================================================================

__all__ = [
    # === DISCOVERY ===
    # Core Types
    'RelationType',
    'ModelDependency',
    'ModelRelation',
    'ModelGraph',
    'RelationshipMetadata',

    # Protocols
    'FilterModel',
    'ModelDiscoveryService',

    # Filters
    'AcceptAllModels',
    'ExcludeModelTypes',
    'ExcludeRelationTypes',
    'CompositeFilter',
    'TagsFilter',

    # Django Implementation
    'DjangoModelDiscoveryService',
    'DjangoRelationshipMetadata',

    # === PRESENTATION ===
    # Core Types
    'PresentationFormat',
    'PresentationOptions',
    'GraphLayout',

    # Analysis
    'GraphAnalysisResult',
    'ModelDistribution',
    'RelationDistribution',
    'DepthAnalysis',
    'CircularDependency',

    # Protocols
    'ModelGraphPresenter',
    'GraphAnalyzer',

    # Implementations
    'TextTreePresenter',
    'JsonPresenter',
    'DotPresenter',
    'BasicGraphAnalyzer',

    # Factory
    'PresenterFactory',
]


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def discover_model_dependencies(root_models,
                                filter_func=None,
                                include_reverse_relations=True):
    """
    Convenience function to discover model dependencies.

    :param root_models: List of Django model classes to analyze
    :param filter_func: Optional filter for models/relations
    :param include_reverse_relations: Whether to include reverse relationships
    :return: ModelGraph of discovered dependencies
    """
    service = DjangoModelDiscoveryService(include_reverse_relations=include_reverse_relations)
    return service.discover_model_dependencies(
        root_models=root_models,
        filter_func=filter_func,
        include_reverse_relations=include_reverse_relations
    )


def present_graph(graph, format_type=PresentationFormat.TEXT, **options):
    """
    Convenience function to present a model graph.

    :param graph: ModelGraph to present
    :param format_type: Desired presentation format
    :param options: Additional presentation options
    :return: String representation of the graph
    """
    presenter = PresenterFactory.create_presenter(format_type)
    presentation_options = PresentationOptions(**options) if options else None
    return presenter.present(graph, presentation_options)


def analyze_models(*model_classes,
                   filter_func=None,
                   format_type=PresentationFormat.TEXT,
                   **presentation_options):
    """
    One-stop function to discover and present model dependencies.

    :param model_classes: Django model classes to analyze
    :param filter_func: Optional filter for models/relations
    :param format_type: Desired presentation format
    :param presentation_options: Options for presentation
    :return: String representation of the dependency graph

    Example:
        output = analyze_models(BlogPost, User, Comment,
                               format_type=PresentationFormat.DOT,
                               show_metadata=True)
    """
    # Discover dependencies
    graph = discover_model_dependencies(
        root_models=list(model_classes),
        filter_func=filter_func
    )

    # Present results
    return present_graph(graph, format_type, **presentation_options)
