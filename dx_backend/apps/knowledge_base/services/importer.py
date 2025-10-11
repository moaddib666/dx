"""
Knowledge Base Importer Service

This service handles importing documents and timeline events from a structured folder hierarchy.
Expected folder structure: {base_folder}/{category}/{document_name}/document.json + optional image.png

The service validates JSON data using Pydantic models and creates/updates Document and TimeLineEvent records.
"""

import json
import logging
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ValidationError, field_validator
from django.core.files import File
from django.db import transaction

from apps.knowledge_base.models import Document, DocumentCategory, TimeLineEvent, DateTimeInfo

logger = logging.getLogger(__name__)


class DateTimeInfoSchema(BaseModel):
    """Schema for DateTimeInfo data in JSON"""
    active_glow: bool = Field(..., description="Whether this is in the Active Glow epoch")
    sol: int = Field(..., ge=0, description="Number of sols since the start of the calendar")
    solar_year: int = Field(..., ge=0, description="Number of solar years since the start of the calendar")


class DocumentSchema(BaseModel):
    """Schema for Document data in JSON"""
    title: str = Field(..., min_length=1, max_length=255, description="Document title")
    content: str = Field(..., min_length=1, description="Document content")
    categories: List[str] = Field(default_factory=list, description="List of category names")
    timeline_event: Optional[DateTimeInfoSchema] = Field(None, description="Optional timeline event data")
    
    @field_validator('categories')
    @classmethod
    def validate_categories(cls, v):
        """Validate that all categories exist in DocumentCategoryEnum"""
        from apps.knowledge_base.models import DocumentCategoryEnum
        valid_categories = [choice[0] for choice in DocumentCategoryEnum.choices]
        invalid = [cat for cat in v if cat not in valid_categories]
        if invalid:
            raise ValueError(f"Invalid categories: {invalid}. Valid categories are: {valid_categories}")
        return v


class ImportResult:
    """Result of an import operation"""
    def __init__(self):
        self.success_count = 0
        self.error_count = 0
        self.skipped_count = 0
        self.errors: List[Dict[str, Any]] = []
        self.imported_documents: List[str] = []
    
    def add_success(self, document_title: str):
        self.success_count += 1
        self.imported_documents.append(document_title)
    
    def add_error(self, path: str, error: str):
        self.error_count += 1
        self.errors.append({'path': path, 'error': error})
    
    def add_skip(self):
        self.skipped_count += 1
    
    def __str__(self):
        return (
            f"Import Results:\n"
            f"  Success: {self.success_count}\n"
            f"  Errors: {self.error_count}\n"
            f"  Skipped: {self.skipped_count}\n"
        )


class KnowledgeBaseImporter:
    """
    Service for importing knowledge base documents from a folder structure.
    
    Expected folder structure:
        base_folder/
            {category}/
                {document_name}/
                    document.json  (required)
                    image.png      (optional)
    
    The document.json file should contain:
    {
        "title": "Document Title",
        "content": "Document content...",
        "categories": ["category1", "category2"],
        "timeline_event": {  // optional
            "active_glow": true,
            "sol": 150,
            "solar_year": 42
        }
    }
    """
    
    def __init__(self, base_folder: str, dry_run: bool = False):
        """
        Initialize the importer.
        
        Args:
            base_folder: Path to the base folder containing category folders
            dry_run: If True, validate but don't actually import
        """
        self.base_folder = Path(base_folder)
        self.dry_run = dry_run
        self.result = ImportResult()
        
        if not self.base_folder.exists():
            raise ValueError(f"Base folder does not exist: {base_folder}")
        if not self.base_folder.is_dir():
            raise ValueError(f"Base folder is not a directory: {base_folder}")
    
    def import_all(self) -> ImportResult:
        """
        Import all documents from the base folder.
        
        Returns:
            ImportResult with statistics and errors
        """
        logger.info(f"Starting import from: {self.base_folder}")
        logger.info(f"Dry run mode: {self.dry_run}")
        
        # Iterate through category folders
        for category_folder in self.base_folder.iterdir():
            if not category_folder.is_dir():
                logger.debug(f"Skipping non-directory: {category_folder}")
                continue
            
            category_name = category_folder.name
            logger.info(f"Processing category: {category_name}")
            
            # Validate category exists
            if not self._validate_category(category_name):
                logger.warning(f"Invalid category: {category_name}, skipping folder")
                self.result.add_skip()
                continue
            
            # Iterate through document folders
            for document_folder in category_folder.iterdir():
                if not document_folder.is_dir():
                    logger.debug(f"Skipping non-directory: {document_folder}")
                    continue
                
                self._import_document(category_name, document_folder)
        
        logger.info(f"Import completed: {self.result}")
        return self.result
    
    def _validate_category(self, category_name: str) -> bool:
        """Check if category exists in DocumentCategoryEnum"""
        from apps.knowledge_base.models import DocumentCategoryEnum
        valid_categories = [choice[0] for choice in DocumentCategoryEnum.choices]
        return category_name in valid_categories
    
    def _import_document(self, category_name: str, document_folder: Path):
        """
        Import a single document from a folder.
        
        Args:
            category_name: Name of the category
            document_folder: Path to the document folder
        """
        document_name = document_folder.name
        json_file = document_folder / "document.json"
        image_file = document_folder / "image.png"
        
        logger.info(f"  Processing document: {category_name}/{document_name}")
        
        # Check if document.json exists
        if not json_file.exists():
            error_msg = f"Missing document.json in {document_folder}"
            logger.error(f"    {error_msg}")
            self.result.add_error(str(document_folder), error_msg)
            return
        
        try:
            # Load and validate JSON
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # Validate with Pydantic
            document_schema = DocumentSchema(**json_data)
            
            # Check if image exists
            has_image = image_file.exists()
            if has_image:
                logger.info(f"    Found image: {image_file.name}")
            
            # Import the document
            if not self.dry_run:
                self._create_or_update_document(
                    document_schema,
                    category_name,
                    image_file if has_image else None
                )
            
            self.result.add_success(document_schema.title)
            logger.info(f"    ✓ Successfully imported: {document_schema.title}")
            
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON: {e}"
            logger.error(f"    {error_msg}")
            self.result.add_error(str(json_file), error_msg)
        except ValidationError as e:
            error_msg = f"Validation error: {e}"
            logger.error(f"    {error_msg}")
            self.result.add_error(str(json_file), error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            logger.error(f"    {error_msg}", exc_info=True)
            self.result.add_error(str(document_folder), error_msg)
    
    @transaction.atomic
    def _create_or_update_document(
        self,
        document_schema: DocumentSchema,
        category_name: str,
        image_path: Optional[Path]
    ):
        """
        Create or update a document in the database.
        
        Args:
            document_schema: Validated document data
            category_name: Name of the category folder
            image_path: Path to the image file (if exists)
        """
        # Get or create the document
        document, created = Document.objects.get_or_create(
            title=document_schema.title,
            defaults={'content': document_schema.content}
        )
        
        # Update content if document already exists
        if not created:
            document.content = document_schema.content
            document.save()
            logger.info(f"    Updated existing document: {document.title}")
        else:
            logger.info(f"    Created new document: {document.title}")
        
        # Handle categories
        document.categories.clear()
        
        # Add the folder category
        try:
            category = DocumentCategory.objects.get(name=category_name)
            document.categories.add(category)
            logger.debug(f"    Added category from folder: {category_name}")
        except DocumentCategory.DoesNotExist:
            logger.warning(f"    Category not found in database: {category_name}")
        
        # Add additional categories from JSON
        for cat_name in document_schema.categories:
            if cat_name != category_name:  # Avoid duplicates
                try:
                    category = DocumentCategory.objects.get(name=cat_name)
                    document.categories.add(category)
                    logger.debug(f"    Added category from JSON: {cat_name}")
                except DocumentCategory.DoesNotExist:
                    logger.warning(f"    Category not found in database: {cat_name}")
        
        # Handle image
        if image_path and image_path.exists():
            with open(image_path, 'rb') as img_file:
                document.image.save(
                    image_path.name,
                    File(img_file),
                    save=True
                )
            logger.info(f"    Saved image: {image_path.name}")
        
        # Handle timeline event if present
        if document_schema.timeline_event:
            self._create_timeline_event(document, document_schema.timeline_event)
    
    def _create_timeline_event(self, document: Document, timeline_data: DateTimeInfoSchema):
        """
        Create a timeline event for the document.
        
        Args:
            document: The document to link to
            timeline_data: Validated timeline event data
        """
        # Get or create DateTimeInfo
        date_time, created = DateTimeInfo.objects.get_or_create(
            active_glow=timeline_data.active_glow,
            sol=timeline_data.sol,
            solar_year=timeline_data.solar_year
        )
        
        if created:
            logger.info(f"    Created new DateTimeInfo: {date_time}")
        else:
            logger.debug(f"    Using existing DateTimeInfo: {date_time}")
        
        # Get or create TimeLineEvent
        timeline_event, created = TimeLineEvent.objects.get_or_create(
            document=document,
            date_time=date_time
        )
        
        if created:
            logger.info(f"    Created new TimeLineEvent: {timeline_event}")
        else:
            logger.debug(f"    TimeLineEvent already exists: {timeline_event}")
