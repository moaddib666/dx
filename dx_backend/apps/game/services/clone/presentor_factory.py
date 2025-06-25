"""
Model Graph Presenter Factory
=============================

Factory for creating model dependency graph presenters based on format requirements.
"""

import logging
import typing as t

from .presentor_core import PresentationFormat, ModelGraphPresenter, GraphAnalyzer
from .presentor_dot import DotPresenter
from .presentor_impl import TextTreePresenter, JsonPresenter

logger = logging.getLogger("apps.game.services.clone")


class PresenterFactory:
    """Factory for creating model graph presenters based on format requirements."""

    _presenters: t.Dict[PresentationFormat, t.Type[ModelGraphPresenter]] = {
        PresentationFormat.TEXT: TextTreePresenter,
        PresentationFormat.JSON: JsonPresenter,
        PresentationFormat.DOT: DotPresenter,
    }

    @classmethod
    def create_presenter(cls,
                         format_type: PresentationFormat,
                         analyzer: t.Optional[GraphAnalyzer] = None) -> ModelGraphPresenter:
        """
        Create a presenter for the specified format.

        :param format_type: The desired presentation format
        :param analyzer: Optional graph analyzer
        :return: Configured presenter instance
        """
        logger.debug("Creating presenter for format: %s", format_type)

        if format_type not in cls._presenters:
            logger.error("Unsupported presentation format: %s", format_type)
            raise ValueError(f"Unsupported presentation format: {format_type}")

        presenter_class = cls._presenters[format_type]
        logger.debug("Using presenter class: %s", presenter_class.__name__)

        if analyzer:
            logger.debug("Using provided analyzer: %r", analyzer)
        else:
            logger.debug("No analyzer provided, presenter will use default")

        presenter = presenter_class(analyzer=analyzer)
        logger.debug("Created presenter instance: %r", presenter)
        return presenter

    @classmethod
    def get_supported_formats(cls) -> t.List[PresentationFormat]:
        """Get list of supported presentation formats."""
        formats = list(cls._presenters.keys())
        logger.debug("Supported presentation formats: %r", formats)
        return formats
