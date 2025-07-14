import logging
from typing import Dict, Any, Optional

from apps.story.models import Story
from .loader import StoryLoader
from .dumper import StoryDumper


class StoryService:
    """
    Typed service that provides unified interface for Story JSON operations.
    Combines StoryLoader and StoryDumper functionality with smart trigger handling.
    """

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.loader: Optional[StoryLoader] = None
        self.dumper: Optional[StoryDumper] = None

    def load_from_file(self, json_file_path: str) -> Story:
        """
        Load a Story from JSON file.
        
        Args:
            json_file_path: Path to the JSON file containing story data
            
        Returns:
            Story: The loaded Story instance
            
        Raises:
            ValidationError: If JSON structure is invalid
            FileNotFoundError: If JSON file doesn't exist
        """
        self.loader = StoryLoader(json_file_path)
        return self.loader.load()

    def load_from_dict(self, data: Dict[str, Any]) -> Story:
        """
        Load a Story from dictionary data.
        
        Args:
            data: Dictionary containing story data in QuestStoryTaller.MD format
            
        Returns:
            Story: The loaded Story instance
            
        Raises:
            ValidationError: If data structure is invalid
        """
        # Use a temporary loader for dict loading
        temp_loader = StoryLoader("")
        return temp_loader.load_from_dict(data)

    def dump_to_file(self, story: Story, output_file_path: str) -> None:
        """
        Dump a Story to JSON file.
        
        Args:
            story: The Story instance to dump
            output_file_path: Path where the JSON file will be saved
        """
        self.dumper = StoryDumper(output_file_path)
        self.dumper.dump(story)

    def dump_to_dict(self, story: Story) -> Dict[str, Any]:
        """
        Convert a Story to dictionary format.
        
        Args:
            story: The Story instance to convert
            
        Returns:
            Dict containing the story data in QuestStoryTaller.MD format
        """
        dumper = StoryDumper()
        return dumper.to_dict(story)

    def dump_to_json_string(self, story: Story) -> str:
        """
        Convert a Story to JSON string.
        
        Args:
            story: The Story instance to convert
            
        Returns:
            JSON string representation of the story
        """
        dumper = StoryDumper()
        return dumper.to_json_string(story)

    def convert_file_to_file(self, input_file_path: str, output_file_path: str) -> Story:
        """
        Load a Story from JSON file and dump it to another JSON file.
        Useful for format validation and normalization.
        
        Args:
            input_file_path: Path to the input JSON file
            output_file_path: Path where the output JSON file will be saved
            
        Returns:
            Story: The processed Story instance
        """
        story = self.load_from_file(input_file_path)
        self.dump_to_file(story, output_file_path)
        return story

    def validate_json_structure(self, json_file_path: str) -> bool:
        """
        Validate if a JSON file has the correct structure for Story loading.
        
        Args:
            json_file_path: Path to the JSON file to validate
            
        Returns:
            bool: True if structure is valid, False otherwise
        """
        try:
            self.load_from_file(json_file_path)
            return True
        except Exception as e:
            self.logger.error(f"JSON structure validation failed: {e}")
            return False

    def validate_dict_structure(self, data: Dict[str, Any]) -> bool:
        """
        Validate if a dictionary has the correct structure for Story loading.
        
        Args:
            data: Dictionary to validate
            
        Returns:
            bool: True if structure is valid, False otherwise
        """
        try:
            self.load_from_dict(data)
            return True
        except Exception as e:
            self.logger.error(f"Dictionary structure validation failed: {e}")
            return False

    def get_loader_stats(self) -> Optional[Dict[str, int]]:
        """
        Get statistics from the last loader operation.
        
        Returns:
            Dict with object creation counts or None if no loader operation performed
        """
        if self.loader:
            return self.loader.created_objects.copy()
        return None

    def get_dumper_stats(self) -> Optional[Dict[str, int]]:
        """
        Get statistics from the last dumper operation.
        
        Returns:
            Dict with object processing counts or None if no dumper operation performed
        """
        if self.dumper:
            return self.dumper.processed_objects.copy()
        return None

    def get_custom_triggers_count(self) -> int:
        """
        Get the count of CUSTOM triggers created during the last load operation.
        This indicates how many unknown trigger types were encountered.
        
        Returns:
            int: Number of CUSTOM triggers created, 0 if no loader operation performed
        """
        if self.loader and 'custom_triggers' in self.loader.created_objects:
            return self.loader.created_objects['custom_triggers']
        return 0
