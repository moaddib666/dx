# Knowledge Base Importer

This document describes how to use the Knowledge Base Importer service to import documents and timeline events into the DX Backend system.

## Overview

The Knowledge Base Importer allows you to organize your knowledge base documents in a structured folder hierarchy and import them into the database with a single command. The importer supports:

- Document creation with title, content, and categories
- Image attachments for documents
- Timeline events with date/time information
- Automatic validation of JSON data
- Dry-run mode for validation without importing
- Detailed error reporting

## Folder Structure

The importer expects a specific folder structure:

```
docs/knowlage_base/
├── {category}/
│   ├── {document_name}/
│   │   ├── document.json  (required)
│   │   └── image.png      (optional)
│   └── {another_document}/
│       ├── document.json
│       └── image.png
└── {another_category}/
    └── ...
```

### Valid Categories

The category folder name must match one of the following valid categories:

- `events` - Events
- `rules` - Rules
- `lore` - Lore
- `stories` - Stories
- `guides` - Guides
- `items` - Items
- `characters` - Characters
- `locations` - Locations
- `places` - Places
- `factions` - Factions
- `creatures` - Creatures
- `skills` - Skills
- `spells` - Spells
- `abilities` - Abilities
- `other` - Other

### Document Folder

Each document must be in its own folder within a category folder. The folder name is used for identification purposes but doesn't affect the imported data.

### Required Files

- **document.json** (required): Contains the document metadata and content
- **image.png** (optional): An image to attach to the document

## JSON Format

### Basic Document Format

The `document.json` file must contain the following structure:

```json
{
  "title": "Document Title",
  "content": "The full content of the document. This can be multiple paragraphs and include detailed information.",
  "categories": ["events", "lore"]
}
```

#### Fields

- **title** (required, string, max 255 characters): The title of the document
- **content** (required, string): The full content/body of the document
- **categories** (optional, array of strings): Additional categories to assign to the document. The folder category is automatically added.

### Document with Timeline Event

To create a timeline event associated with the document, add a `timeline_event` field:

```json
{
  "title": "The Great Battle of Active Glow",
  "content": "A historic battle that changed the course of history. The forces of light clashed with the darkness in an epic confrontation that lasted for three sols.",
  "categories": ["events", "lore", "stories"],
  "timeline_event": {
    "active_glow": true,
    "sol": 150,
    "solar_year": 42
  }
}
```

#### Timeline Event Fields

- **active_glow** (required, boolean): Whether this event occurred during the Active Glow epoch (true) or Before Active Glow (false)
- **sol** (required, integer, >= 0): The sol number when the event occurred
- **solar_year** (required, integer, >= 0): The solar year when the event occurred

## Usage

### Basic Import

To import all documents from the knowledge base folder:

```bash
python manage.py import_knowledge_base /path/to/docs/knowlage_base
```

### Dry Run (Validation Only)

To validate the folder structure and JSON files without actually importing:

```bash
python manage.py import_knowledge_base /path/to/docs/knowlage_base --dry-run
```

This is useful for:
- Testing your folder structure
- Validating JSON files
- Checking for errors before importing

### Verbose Output

To see detailed logging information:

```bash
python manage.py import_knowledge_base /path/to/docs/knowlage_base --verbosity 2
```

Verbosity levels:
- `0`: Minimal output (errors only)
- `1`: Normal output (default)
- `2`: Verbose output (includes debug information)

### Combined Options

```bash
python manage.py import_knowledge_base /path/to/docs/knowlage_base --dry-run --verbosity 2
```

## Examples

### Example 1: Simple Document

**Folder structure:**
```
docs/knowlage_base/
└── rules/
    └── combat_basics/
        ├── document.json
        └── image.png
```

**document.json:**
```json
{
  "title": "Combat Basics",
  "content": "Combat in DX follows a turn-based system. Each character can perform one action per turn, including attacking, defending, or using abilities.",
  "categories": ["rules", "guides"]
}
```

### Example 2: Event with Timeline

**Folder structure:**
```
docs/knowlage_base/
└── events/
    └── active_glow/
        ├── document.json
        └── image.png
```

**document.json:**
```json
{
  "title": "The Active Glow Phenomenon",
  "content": "The Active Glow is a mysterious phenomenon that began in solar year 1, sol 1. It manifests as a luminous energy that permeates the dimension, affecting all living beings and magical constructs. The phenomenon is characterized by increased magical potency and dimensional instability.",
  "categories": ["events", "lore"],
  "timeline_event": {
    "active_glow": true,
    "sol": 1,
    "solar_year": 1
  }
}
```

### Example 3: Character Lore

**Folder structure:**
```
docs/knowlage_base/
└── characters/
    └── elder_sage/
        ├── document.json
        └── image.png
```

**document.json:**
```json
{
  "title": "Elder Sage Moaddib",
  "content": "Elder Sage Moaddib is a legendary figure who witnessed the beginning of the Active Glow. Known for his wisdom and mastery of dimensional magic, he has guided countless adventurers through the perils of the unstable dimensions.",
  "categories": ["characters", "lore"]
}
```

## Import Behavior

### Document Creation

- Documents are matched by **title**
- If a document with the same title exists, its content is **updated**
- Categories are **replaced** (not merged) on update

### Category Assignment

- The folder category is automatically added to the document
- Additional categories from the JSON `categories` field are also added
- Invalid categories are logged as warnings but don't stop the import

### Image Handling

- Images are copied to Django's media storage
- If a document already has an image, it will be replaced
- Only `image.png` files are currently supported

### Timeline Events

- Timeline events are matched by document + date/time
- If a timeline event already exists for the same document and date/time, it won't be duplicated
- DateTimeInfo records are reused if they match existing records

### Error Handling

The importer will:
- Continue processing even if individual documents fail
- Log all errors with file paths
- Provide a summary of successes, errors, and skipped items
- Exit with an error code if any errors occurred

## Validation

The importer performs comprehensive validation:

### JSON Validation
- Valid JSON syntax
- Required fields present
- Field types correct
- String length constraints
- Integer range constraints

### Category Validation
- Category folder names must be valid
- Categories in JSON must be valid
- Invalid categories are logged but don't stop import

### File Validation
- `document.json` must exist in each document folder
- `image.png` is optional

## Troubleshooting

### Common Errors

**"Missing document.json"**
- Ensure each document folder contains a `document.json` file

**"Invalid JSON"**
- Check your JSON syntax (use a JSON validator)
- Ensure proper quotes and commas

**"Validation error"**
- Check that all required fields are present
- Verify field types (strings, integers, booleans)
- Check string length constraints (title max 255 characters)

**"Invalid category"**
- Ensure category folder names match valid categories exactly
- Check spelling and case (must be lowercase)

**"Invalid categories in JSON"**
- Verify categories in the `categories` array are valid
- Check spelling and case

### Tips

1. **Use dry-run first**: Always test with `--dry-run` before importing
2. **Check verbosity**: Use `--verbosity 2` to see detailed logs
3. **One category per folder**: Don't mix categories in the same folder
4. **Unique titles**: Use unique document titles to avoid unintended updates
5. **Backup first**: Backup your database before large imports

## API Integration

After importing, documents are available through the REST API:

- **List documents**: `GET /api/knowledge-base/documents/`
- **Get document**: `GET /api/knowledge-base/documents/{id}/`
- **List timeline events**: `GET /api/knowledge-base/timeline-events/`
- **Get timeline event**: `GET /api/knowledge-base/timeline-events/{id}/`

See the API documentation for filtering, searching, and pagination options.
