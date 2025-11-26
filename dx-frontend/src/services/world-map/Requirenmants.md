# Interactive Map Editor - Requirements & Specifications
## AI-Friendly Technical Requirements Document

---

## Project Overview

**Project Name:** Zerra Planet Interactive Map Editor  
**Technology Stack:** Vue.js 3 + TypeScript + HTML5 Canvas  
**Purpose:** Create a layered, interactive map editing tool with infinite canvas wrapping  
**Primary Use Case:** Fantasy world map creation and editing for a game project

---

## Core Requirements

### 1. Canvas System

#### 1.1 Base Canvas Requirements
- **Canvas Element:** HTML5 Canvas as the primary rendering surface
- **Base Layer:** Support loading a background image (AI-generated or uploaded) as the bottom layer
- **Image Format Support:** PNG, JPEG, WebP
- **Image Loading:** Accept both local file upload and base64-encoded strings
- **Canvas Size:** Default 1920x1080, but should be configurable via metadata

#### 1.2 Infinite Canvas (Globe Wrapping)
**CRITICAL REQUIREMENT:** The canvas must behave like a globe surface with seamless wrapping.

**Horizontal Wrapping:**
- When panning right and reaching the right edge, continue seamlessly from the left edge
- When panning left and reaching the left edge, continue seamlessly from the right edge

**Vertical Wrapping:**
- When panning down and reaching the bottom edge, continue seamlessly from the top edge
- When panning up and reaching the top edge, continue seamlessly from the bottom edge

**Technical Implementation:**
- Use modulo operations to wrap coordinates
- Render multiple "tiles" of the map when near edges
- All geometric shapes (polygons, routes) must wrap correctly across edges
- Markers and labels must appear on wrapped instances when near edges

**Mathematical Formula:**
```
wrappedX = ((x % canvasWidth) + canvasWidth) % canvasWidth
wrappedY = ((y % canvasHeight) + canvasHeight) % canvasHeight
```

---

### 2. Layer System Architecture

The map consists of hierarchical layers, rendered in the following order (bottom to top):

#### Layer 1: Background Image
- Static image layer
- Cannot be edited, only replaced
- Serves as visual reference for mapping

#### Layer 2: Continents
- **Definition:** Large landmass polygons
- **Editable Properties:**
    - Polygon boundary (moveable vertices)
    - Fill color
    - Border color
    - Border width
    - Name/label
- **Visibility Controls:**
    - Toggle entire continent visibility
    - Toggle border visibility independently
    - Toggle fill visibility independently
- **Contains:** Array of Country objects

#### Layer 3: Countries
- **Definition:** Political boundaries within continents
- **Parent:** Must belong to a Continent
- **Editable Properties:**
    - Polygon boundary (moveable vertices)
    - Fill color
    - Border color
    - Border width
    - Name/label
- **Visibility Controls:**
    - Toggle entire country visibility
    - Toggle border visibility independently
    - Toggle fill visibility independently
- **Contains:** Array of City objects

#### Layer 4: Cities (Areas)
- **Definition:** Urban/settlement areas within countries
- **Parent:** Must belong to a Country
- **Two Types:**
    - **Area Type:** Polygon representing city boundaries
    - **Point Type:** Single point marker representing city location
- **Editable Properties:**
    - Polygon boundary OR point location
    - Fill color (area type only)
    - Border color
    - Marker color (point type)
    - Marker size (point type)
    - City type: 'major' | 'medium' | 'small'
    - Name/label
- **Visibility Controls:**
    - Toggle city visibility
    - Toggle border/area highlighting
    - Toggle label visibility

#### Layer 5: Routes/Paths
- **Definition:** Trade routes, roads, travel paths between locations
- **Data Structure:** Array of points forming a path
- **Editable Properties:**
    - Path points (add/remove/move vertices)
    - Line color
    - Line width
    - Line style: 'solid' | 'dashed' | 'dotted'
    - Route type: 'maritime' | 'aerial' | 'dimensional' | 'road'
    - Name/label
- **Visibility Controls:**
    - Toggle route visibility individually
    - Toggle all routes visibility
- **Rendering:** Lines connecting points, with appropriate styling

#### Layer 6: Markers/Points of Interest
- **Definition:** Single-point locations (cities, hazards, landmarks)
- **Types:**
    - City markers (when cities are point-type)
    - Hazard markers (dangerous locations)
    - Landmark markers (notable locations)
    - Custom markers
- **Editable Properties:**
    - Position (x, y)
    - Marker type
    - Marker size
    - Marker color
    - Icon/emoji
    - Name/label
    - Description
- **Visibility Controls:**
    - Toggle marker visibility individually
    - Toggle label visibility
    - Toggle by marker type (show/hide all hazards, etc.)
- **Visual Representation:**
    - Cities: Circles (size based on type)
    - Hazards: Triangles
    - Custom: Configurable shapes or icons

#### Layer 7: Labels/Text
- **Definition:** Text annotations overlaid on the map
- **Editable Properties:**
    - Text content
    - Position (x, y)
    - Font size
    - Font weight: 'normal' | 'bold'
    - Text color
    - Background enabled (boolean)
    - Background color
    - Alignment
- **Visibility Controls:**
    - Toggle label visibility individually
    - Toggle all labels visibility

---

### 3. Data Structure (JSON Format)

**REQUIREMENT:** All map data must be stored in a JSON structure that can be:
- Exported to file
- Imported from file
- Edited in real-time
- Validated against schema

**Coordinate System:**
- Use percentage-based coordinates (0-100 for both x and y)
- This makes the map resolution-independent
- Convert to pixels during rendering based on canvas size

**JSON Schema Structure:**
```typescript
interface MapData {
  metadata: {
    width: number;           // Canvas width in pixels
    height: number;          // Canvas height in pixels
    backgroundImage: string; // Base64 or URL
    version: string;         // Schema version
    created: string;         // ISO timestamp
    modified: string;        // ISO timestamp
  };
  
  continents: Array<{
    id: string;              // Unique identifier
    name: string;
    points: Array<{x: number, y: number}>; // Polygon vertices (% based)
    color: string;           // Hex color
    visible: boolean;
    borderVisible: boolean;
    fillVisible: boolean;
    borderWidth: number;
    borderColor: string;
    countries: Array<Country>;
  }>;
  
  routes: Array<{
    id: string;
    name: string;
    points: Array<{x: number, y: number}>;
    color: string;
    width: number;
    style: 'solid' | 'dashed' | 'dotted';
    visible: boolean;
    type: string;
  }>;
  
  markers: Array<{
    id: string;
    name: string;
    position: {x: number, y: number};
    type: string;
    color: string;
    icon: string;
    size: number;
    visible: boolean;
    labelVisible: boolean;
    description?: string;
  }>;
  
  labels: Array<{
    id: string;
    text: string;
    position: {x: number, y: number};
    fontSize: number;
    color: string;
    fontWeight: string;
    visible: boolean;
    background: boolean;
    backgroundColor?: string;
  }>;
}
```

---

### 4. Interaction Requirements

#### 4.1 Navigation Controls

**Zoom:**
- Mouse wheel to zoom in/out
- Zoom range: 0.1x to 5.0x
- Zoom should center on mouse cursor position
- Keyboard shortcuts: `+` to zoom in, `-` to zoom out

**Pan:**
- Click and drag to pan the canvas
- Arrow keys for keyboard panning
- Panning must respect infinite wrapping (edges loop)
- Smooth panning without lag

**Reset View:**
- Button or shortcut (`Home` key) to reset zoom to 1.0 and center map

#### 4.2 Tool System

**Required Tools:**

1. **Select Tool** (Default)
    - Click to select items (continents, countries, cities, markers, routes)
    - Show selection highlight
    - Display properties in side panel
    - Allow dragging selected items

2. **Draw Polygon Tool**
    - Click to add vertices
    - Double-click or press Enter to finish polygon
    - ESC to cancel
    - Use for creating continents, countries, city areas

3. **Draw Route Tool**
    - Click to add waypoints
    - Double-click to finish route
    - ESC to cancel

4. **Add Marker Tool**
    - Click to place marker
    - Prompt for marker type and properties

5. **Add Label Tool**
    - Click to place label
    - Prompt for text content and styling

6. **Edit Tool**
    - Select and drag vertices of polygons
    - Add new vertices by clicking on edges
    - Delete vertices by right-click or Delete key

7. **Delete Tool**
    - Click items to delete them
    - Confirmation dialog for deletion

#### 4.3 Selection and Editing

**Selection Behavior:**
- Click on item to select it
- Selected item shows highlight (glow effect or different stroke)
- Properties panel updates to show selected item properties
- Click on empty space to deselect

**Multi-Select:**
- Hold Ctrl/Cmd to select multiple items
- Drag to create selection box (optional feature)

**Editing Vertices:**
- When polygon is selected, show vertex handles
- Drag vertex handles to reshape polygon
- Click on edge to add new vertex
- Right-click vertex to delete it

**Keyboard Shortcuts:**
- `Delete` or `Backspace`: Delete selected item
- `Ctrl+Z`: Undo
- `Ctrl+Y` or `Ctrl+Shift+Z`: Redo
- `Ctrl+S`: Save/Export
- `Ctrl+C`: Copy selected item
- `Ctrl+V`: Paste copied item
- `ESC`: Deselect / Cancel current operation

---

### 5. UI Components Requirements

#### 5.1 Main Editor Layout

```
┌─────────────────────────────────────────────────────┐
│  Tool Panel                    Export/Import         │
├──────────┬─────────────────────────────┬────────────┤
│          │                             │            │
│  Layer   │                             │ Properties │
│ Controls │      Canvas Area            │   Panel    │
│          │                             │            │
│          │                             │            │
├──────────┴─────────────────────────────┴────────────┤
│  Status Bar (zoom level, coordinates, etc.)         │
└─────────────────────────────────────────────────────┘
```

#### 5.2 Layer Controls Panel (Left Side)

**Features:**
- Hierarchical tree view of all layers
- Checkboxes to toggle visibility
- Sub-controls for border/fill visibility
- Eye icon to toggle visibility
- Collapsible sections for each continent
- Show/hide nested countries and cities

**Example Structure:**
```
Layers
├─ 🖼️ Background Image
├─ 🌍 Continents
│  ├─ ☑️ Mainland Primus
│  │  ├─ ☑️ Border  ☑️ Fill
│  │  └─ 📁 Countries (3)
│  ├─ ☑️ TechnoEdge
│  └─ ☑️ Mystory Heaven
├─ 🛣️ Routes (5)
│  ├─ ☑️ Maritime Route 1
│  └─ ☑️ Aerial Route 2
├─ 📍 Markers (12)
│  ├─ ☑️ Show Cities
│  ├─ ☑️ Show Hazards
│  └─ ☑️ Show Landmarks
└─ 🏷️ Labels (8)
```

#### 5.3 Tool Panel (Top)

**Buttons:**
- Select Tool (cursor icon)
- Draw Polygon (polygon icon)
- Draw Route (path icon)
- Add Marker (pin icon)
- Add Label (text icon)
- Edit Tool (pencil icon)
- Delete Tool (trash icon)

**Active tool should be highlighted**

#### 5.4 Properties Panel (Right Side)

**Content varies based on selection:**

**When Continent Selected:**
- Name input field
- Color picker (fill)
- Border color picker
- Border width slider
- Visibility checkboxes

**When City Selected:**
- Name input field
- Type dropdown (major/medium/small)
- Color picker
- Size slider (if point type)
- Label visibility checkbox

**When Marker Selected:**
- Name input field
- Type dropdown
- Icon/emoji picker
- Color picker
- Size slider
- Description text area

**When Nothing Selected:**
- Show map statistics (number of continents, cities, etc.)
- Quick actions (new continent, etc.)

#### 5.5 Export/Import Controls

**Buttons:**
- "Import JSON" - Load map data from file
- "Export JSON" - Save map data to file
- "Export PNG" - Export rendered map as image
- "Upload Background" - Change base image

#### 5.6 Status Bar (Bottom)

**Display Information:**
- Current zoom level (e.g., "Zoom: 150%")
- Mouse coordinates in percentage (e.g., "X: 45.2%, Y: 67.8%")
- Selected item info (e.g., "Continent: Mainland Primus")
- Tool hint (e.g., "Click to add vertex")

---

### 6. Rendering Requirements

#### 6.1 Performance Requirements

**Target Performance:**
- Maintain 60 FPS during pan/zoom
- Smooth rendering with up to 1000 elements
- No lag when toggling layer visibility
- Efficient re-rendering (only redraw when needed)

**Optimization Strategies:**
- Use dirty checking (only re-render when data changes)
- Implement viewport culling (only render visible items)
- Use requestAnimationFrame for smooth animations
- Consider OffscreenCanvas for background layer caching

#### 6.2 Visual Requirements

**Polygon Rendering:**
- Fill color with opacity support
- Border stroke with configurable width and color
- Smooth anti-aliasing

**Line Rendering (Routes):**
- Support solid, dashed, and dotted line styles
- Configurable width (1-10 pixels)
- Line caps: rounded

**Marker Rendering:**
- Circles for cities (filled with border)
- Triangles for hazards (filled with border)
- Support for custom shapes
- Scale appropriately with zoom

**Text Rendering:**
- Clear, readable fonts (Arial, sans-serif)
- Optional background box for contrast
- Text should not pixelate when zoomed

**Selection Highlight:**
- Selected items show glow effect or thicker border
- Color: bright cyan or yellow
- Vertex handles shown as small circles on selected polygons

#### 6.3 Color System

**Default Colors:**
- Continents: Dark theme colors (#2a2a3e, #1a3a4a, #2a4a2a)
- Countries: Slightly lighter than parent continent
- Major Cities: Gold (#fbbf24)
- Medium Cities: Blue (#60a5fa)
- Small Cities: Light blue (#93c5fd)
- Hazards: Red (#ef4444)
- Routes: Blue with opacity (#60a5fa with 60% opacity)
- Labels: White (#ffffff) with dark background

**All colors should be customizable via properties panel**

---

### 7. File Operations

#### 7.1 Import JSON

**Requirements:**
- Accept .json file via file input
- Validate JSON structure before loading
- Show error message if invalid JSON
- Replace current map data with imported data
- Ask for confirmation if current data exists (unsaved changes)

#### 7.2 Export JSON

**Requirements:**
- Serialize entire MapData object to JSON
- Format with proper indentation (2 spaces)
- Trigger browser download
- Default filename: `map-data-[timestamp].json`
- Include all metadata (version, timestamps)

#### 7.3 Export PNG

**Requirements:**
- Render current canvas view to PNG
- Include all visible layers
- Maintain current zoom and pan position
- Resolution: Same as canvas size
- Trigger browser download
- Default filename: `map-export-[timestamp].png`

#### 7.4 Background Image Upload

**Requirements:**
- Accept PNG, JPG, WebP files
- Convert to base64 for storage in JSON
- Resize if too large (max 4096x4096)
- Update canvas to match image dimensions
- Show preview before applying

#### 7.5 Auto-save

**Optional Feature:**
- Save to localStorage every 30 seconds
- Show "Auto-saved" indicator
- Restore from auto-save on page reload
- Clear auto-save after manual export

---

### 8. Data Validation Rules

#### 8.1 Geometric Constraints

**Polygons:**
- Minimum 3 vertices required
- Vertices must be within 0-100 range (percentage)
- No self-intersecting polygons (optional validation)

**Points:**
- Must be within 0-100 range for both x and y

**Routes:**
- Minimum 2 waypoints required
- Waypoints must be within valid range

#### 8.2 Hierarchical Constraints

**Countries:**
- Must belong to a Continent
- Country boundaries should be within parent Continent (soft rule)

**Cities:**
- Must belong to a Country
- City locations should be within parent Country (soft rule)

#### 8.3 Naming Rules

**All Named Elements:**
- Name cannot be empty
- Maximum length: 100 characters
- Trim whitespace
- Unique IDs within their type

---

### 9. Edge Cases and Error Handling

#### 9.1 Canvas Edge Wrapping Edge Cases

**Problem:** When a polygon spans the edge of the canvas

**Solution:**
- Split polygon rendering across wrapped instances
- Example: If a continent polygon has points at x: 95% and x: 5%, render it twice:
    - Once at its actual position
    - Once offset by 100% to show wrapped portion

**Implementation:**
```typescript
// Check if polygon spans edge
if (maxX - minX > 50) {
  // Polygon likely wraps around
  // Render with offset
}
```

#### 9.2 Invalid JSON Import

**Handling:**
- Try-catch block around JSON.parse()
- Validate structure against schema
- Show user-friendly error message
- Do not modify current map data if import fails

#### 9.3 Performance Degradation

**If map has > 1000 elements:**
- Show warning message
- Implement viewport culling automatically
- Reduce rendering quality (optional)
- Suggest splitting into multiple maps

#### 9.4 Browser Compatibility

**Minimum Requirements:**
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Fallbacks:**
- Check for Canvas support
- Check for FileReader API support
- Show unsupported browser message if needed

---

### 10. Testing Requirements

#### 10.1 Unit Tests

**Test Coverage:**
- All composables (useCanvas, useLayerRenderer, etc.)
- Geometric utility functions
- Coordinate conversion functions
- Wrapping logic

**Test Framework:** Vitest

#### 10.2 Integration Tests

**Scenarios:**
- Load map data from JSON
- Export map data to JSON
- Add/remove/edit each type of element
- Toggle layer visibility
- Zoom and pan operations
- Selection and editing

#### 10.3 Visual Regression Tests

**Tool:** Playwright or Cypress

**Test Cases:**
- Render map with known data
- Compare screenshot to baseline
- Test at different zoom levels
- Test with different viewport sizes

#### 10.4 Manual Testing Checklist

- [ ] Infinite wrapping works in all directions
- [ ] All layer types render correctly
- [ ] Selection and editing works for all element types
- [ ] Import/Export preserves all data
- [ ] Zoom and pan are smooth
- [ ] Keyboard shortcuts work
- [ ] Undo/Redo works correctly
- [ ] All visibility toggles work
- [ ] Performance is acceptable with large datasets

---

## Implementation Priority

### Phase 1: MVP (Must Have)
1. Canvas with background image
2. Basic continent rendering (polygons)
3. Zoom and pan (without wrapping first)
4. Layer visibility toggles
5. Basic selection
6. JSON import/export

### Phase 2: Core Features (Should Have)
1. Infinite canvas wrapping
2. Countries and cities layers
3. Draw polygon tool
4. Edit polygon vertices
5. Markers and routes
6. Properties panel

### Phase 3: Enhancement (Nice to Have)
1. Labels layer
2. Undo/Redo
3. Keyboard shortcuts
4. Auto-save
5. PNG export
6. Copy/paste

### Phase 4: Polish (Could Have)
1. Minimap
2. Grid snapping
3. Multi-select
4. Touch support
5. Themes (dark/light mode)
6. Localization

---

## Success Criteria

**The project is considered successful when:**

1. ✅ User can upload a background image
2. ✅ User can draw continents, countries, and cities as polygons
3. ✅ User can add markers for cities and hazards
4. ✅ User can draw routes between locations
5. ✅ User can toggle visibility of all layer types
6. ✅ Canvas wraps infinitely like a globe (edges loop)
7. ✅ User can zoom and pan smoothly
8. ✅ User can select and edit all elements
9. ✅ User can export complete map as JSON
10. ✅ User can import previously exported JSON
11. ✅ All data matches the specified JSON schema
12. ✅ Performance is smooth with realistic map data (50-100 continents/countries, 200+ cities)

---

## Technical Constraints

1. **Must use Vue.js 3 with Composition API** (not Options API)
2. **Must use TypeScript** for type safety
3. **Must use HTML5 Canvas** (not SVG or WebGL)
4. **Must work in modern browsers** (Chrome, Firefox, Safari, Edge - latest versions)
5. **Must store all data in JSON format** (no proprietary formats)
6. **Must use percentage-based coordinates** (0-100 range)
7. **Must implement infinite wrapping** (not optional)
8. **Must be responsive** (work on different screen sizes)

---

## Non-Functional Requirements

1. **Code Quality:**
    - Follow Vue.js style guide
    - Use ESLint and Prettier
    - Write clear comments
    - Use meaningful variable names

2. **Accessibility:**
    - Keyboard navigation support
    - ARIA labels where appropriate
    - Sufficient color contrast

3. **Documentation:**
    - README with setup instructions
    - Component documentation
    - API documentation for composables

4. **Maintainability:**
    - Modular code structure
    - Reusable composables
    - Clear separation of concerns

---