# AttributeBar Component Documentation

## Overview
The AttributeBar component is a cyberpunk-fantasy styled progress bar designed for the Dimension-X game. It displays character attributes (Health, Energy, Action Points, etc.) with interactive visual feedback and animations. The design is aligned with the Compass component to ensure visual consistency across the game interface.

## Features

### Visual Enhancements
- **Cyberpunk-Fantasy Design**: Matches the Compass component's aesthetic with gold accents and semi-transparent backgrounds
- **Glowing Effects**: Subtle gold glow on bars and interactive elements
- **Sharp Edges**: Angular, precise geometric shapes with minimal border-radius for a more technical look
- **Themed Gradients**: Different color schemes for different attribute types

### Interactive Feedback
- **Change Visualization**: Pulse animation when values change
- **Delta Display**: Shows the amount of change (+X or -X) with appropriate colors
- **Visual Indicators**:
  - Positive changes: Green glowing text
  - Negative changes: Red glowing text

### Animation Features
- **Enhanced Decrease Animation**: 
  - Shows preview of to-be-decreased portion in a lighter color
  - Scales the bar by 1.1x for emphasis
  - Adds a delay before the actual decrease for better visibility
  - Uses slower transitions (0.8s) for value changes
- **Bar Minimization**: Collapsible/expandable states (click to toggle)
- **Hover Effects**: Subtle lift (-2px) and brightness increase on hover with gold shadow
- **Pulse Effect**: Brightness and scaling animation when values change

### Accessibility
- ARIA labels for screen readers
- Support for reduced motion preferences
- High contrast text for readability
- Keyboard navigable

## Design Alignment with Compass
The AttributeBar component has been styled to match the Compass component's design language:

- **Color Scheme**: Uses the same gold accent color (--cyber-yellow, #ffd700)
- **Background**: Semi-transparent background with backdrop-filter blur
- **Border**: 1px border with rgba(255, 215, 0, 0.2) color
- **Sharp Edges**: Minimal border-radius (1-2px) for a more technical, angular look
- **Typography**: 
  - Font family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif
  - Font weight: 600
  - Letter spacing: 0.5px
- **Shadows**: Subtle box shadows (0 4px 8px rgba(0, 0, 0, 0.2))
- **Hover Effects**: Consistent hover behavior with Compass buttons
- **Transitions**: 
  - General transitions use "all 0.3s ease"
  - Value changes use slower 0.8s transitions for better visibility
  - Decrease animations include a delay for improved user perception

## Props

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| current | Number | Yes | - | Current value of the attribute |
| max | Number | Yes | - | Maximum value of the attribute |
| type | String | Yes | - | Attribute type ("Health", "Energy", "Action Points") |
| showDeltas | Boolean | No | true | Whether to show change indicators |
| compact | Boolean | No | false | Whether to use minimized view |
| theme | String | No | 'default' | Visual theme ('combat', 'exploration', 'default') |

## Usage

### Basic Usage
```vue
<AttributeBar
  :current="80"
  :max="100"
  type="Health"
/>
```

### With All Props
```vue
<AttributeBar
  :current="80"
  :max="100"
  type="Health"
  :showDeltas="true"
  :compact="false"
  theme="combat"
/>
```

### In a Loop
```vue
<div
  v-for="attribute in attributes"
  :key="attribute.name"
  class="attribute-row"
>
  <span class="attribute-name">{{ attribute.name }}</span>
  <AttributeBar
    :current="attribute.current"
    :max="attribute.max"
    :type="attribute.name"
    :showDeltas="true"
  />
</div>
```

## Events

The component automatically detects changes to the `current` prop and displays appropriate visual feedback. No manual event handling is required for basic functionality.

## CSS Variables

The component uses CSS variables for theming, aligned with the Compass component:

```css
:root {
  --cyber-yellow: #ffd700;
  --dx-primary-blue: #00BFFF;
  --dx-secondary-blue: #1E90FF;
  --dx-primary-green: #00FF00;
  --dx-secondary-green: #32CD32;
  --dx-primary-red: #FF0000;
  --dx-secondary-red: #DC143C;
  --dx-bg-dark: rgba(0, 0, 0, 0.3);
  --dx-bg-darker: #000000;
  --dx-text-light: rgba(255, 255, 255, 0.9);
  --dx-border-light: rgba(255, 215, 0, 0.2);
  --dx-glow-intensity: 0.3;
  --dx-animation-speed: 0.3s;
  /* Additional variables for decrease preview */
  --dx-decrease-preview-opacity: 0.7;
  --dx-decrease-delay: 800ms;
  --dx-value-transition-speed: 0.8s;
}
```

## Testing

A test component is available at `AttributeBarTest.vue` which demonstrates all features of the AttributeBar component and allows for interactive testing.