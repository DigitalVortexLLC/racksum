# Rack Diagram Tool - Development TODO List

## Phase 1: Project Setup & Foundation
- [ ] Decide on technology stack (vanilla JS vs framework)
- [ ] Answer open questions in claude.md
- [ ] Create project directory structure
- [ ] Initialize package.json (if using build tools)
- [ ] Set up HTML boilerplate (index.html)
- [ ] Create basic CSS structure
- [ ] Set up development environment

## Phase 2: Data Layer
- [ ] Define device schema (TypeScript interfaces or JSDoc)
- [ ] Create devices.json with default device library
  - [ ] Power devices (UPS, PDU)
  - [ ] Network devices (switches, routers, firewalls)
  - [ ] Servers (1U, 2U, 4U variants)
  - [ ] Storage devices (NAS, SAN)
- [ ] Create rack configuration schema
- [ ] Implement data loading from JSON file
- [ ] Implement state management for rack configurations

## Phase 3: Left Sidebar - Device Library
- [ ] Create sidebar HTML structure
- [ ] Implement accordion component
  - [ ] Expand/collapse functionality
  - [ ] Category sections
- [ ] Load and display devices by category
- [ ] Style device items in library
  - [ ] Show device name
  - [ ] Show RU size
  - [ ] Show power draw
  - [ ] Color indicator
- [ ] Make devices draggable
- [ ] Add search/filter functionality (optional enhancement)

## Phase 4: Main Area - Rack Display
- [ ] Create rack container component
- [ ] Implement single rack display
  - [ ] Render 42 RU slots (default)
  - [ ] Number each RU position
  - [ ] Style empty slots (outlined rectangles)
- [ ] Support configurable RU count per rack
- [ ] Implement multi-rack display
  - [ ] Layout multiple racks (horizontal/grid)
  - [ ] Label each rack
- [ ] Add rack headers with rack names
- [ ] Make rack slots drop targets
- [ ] Style occupied slots (filled rectangles with device color)

## Phase 5: Drag & Drop Functionality
- [ ] Set up drag and drop system (HTML5 DnD or library)
- [ ] Implement drag start from device library
  - [ ] Show drag preview
  - [ ] Store device data in drag event
- [ ] Implement drop zone logic
  - [ ] Highlight valid drop zones on drag over
  - [ ] Calculate if device fits in position
  - [ ] Collision detection (check if RUs are available)
- [ ] Handle drop event
  - [ ] Place device in rack at specified position
  - [ ] Update rack state
  - [ ] Render device in rack
- [ ] Implement device removal
  - [ ] Drag out to remove, OR
  - [ ] Delete button on hover, OR
  - [ ] Right-click context menu
- [ ] Support dragging between racks
- [ ] Add visual feedback
  - [ ] Highlight drop zones
  - [ ] Show invalid drop indicators
  - [ ] Animate device placement

## Phase 6: Configuration Menu
- [ ] Create settings/configuration UI
  - [ ] Modal dialog OR
  - [ ] Settings panel OR
  - [ ] Top menu bar
- [ ] Add rack configuration options
  - [ ] Number of racks (input field with validation)
  - [ ] RU per rack (input field, default 42)
  - [ ] Add/remove individual racks
- [ ] Add power configuration
  - [ ] Total power capacity input (watts)
  - [ ] Display unit selection (watts/kilowatts)
- [ ] Add HVAC configuration
  - [ ] Cooling capacity input (BTU/hr or watts)
  - [ ] Display unit selection
- [ ] Implement configuration save/apply
- [ ] Add validation for inputs
- [ ] Reset to defaults option

## Phase 7: Resource Utilization Tracking
- [ ] Calculate total power consumption
  - [ ] Sum power draw of all placed devices
  - [ ] Update in real-time on device add/remove
- [ ] Calculate heat load
  - [ ] Convert power to BTU/hr (1W = 3.41 BTU/hr)
  - [ ] Alternative: use watts for cooling capacity
- [ ] Create utilization display component (bottom-right)
  - [ ] Power utilization bar graph
  - [ ] HVAC utilization bar graph
  - [ ] Percentage and absolute values
- [ ] Implement color coding
  - [ ] Green: < 70% capacity
  - [ ] Yellow: 70-90% capacity
  - [ ] Red: > 90% capacity
- [ ] Add visual warnings when over capacity
- [ ] Show per-rack statistics (optional enhancement)

## Phase 8: JSON Import/Export
- [ ] Implement export functionality
  - [ ] Serialize current rack configuration to JSON
  - [ ] Download as file
  - [ ] Copy to clipboard option
- [ ] Implement import functionality
  - [ ] File upload input
  - [ ] Parse and validate JSON
  - [ ] Handle parse errors gracefully
- [ ] Add paste/text input import
  - [ ] Text area for pasting JSON
  - [ ] Validate and load
- [ ] Implement POST endpoint (if backend needed)
  - [ ] Create minimal API server (Express/Flask)
  - [ ] POST /api/load-configuration endpoint
  - [ ] Accept JSON body and return success/error
  - [ ] Update UI with posted configuration
- [ ] Add example JSON configurations
- [ ] Document JSON schema for users

## Phase 9: UI/UX Polish
- [ ] Responsive layout
  - [ ] Desktop optimization
  - [ ] Tablet support (optional)
  - [ ] Mobile support (optional)
- [ ] Add device tooltips
  - [ ] Show full device info on hover
  - [ ] Position, power draw, name
- [ ] Add device labels in rack
  - [ ] Show device name
  - [ ] Truncate long names
  - [ ] Optional toggle for labels
- [ ] Implement undo/redo (optional)
- [ ] Add keyboard shortcuts (optional)
  - [ ] Delete key to remove selected device
  - [ ] Ctrl+Z for undo
  - [ ] Ctrl+Y for redo
- [ ] Add loading states
- [ ] Error handling and user feedback
  - [ ] Toast notifications or alerts
  - [ ] Validation messages
- [ ] Accessibility improvements
  - [ ] ARIA labels
  - [ ] Keyboard navigation
  - [ ] Screen reader support

## Phase 10: Additional Features (Optional)
- [ ] Device customization
  - [ ] Edit device properties
  - [ ] Create custom devices
  - [ ] Save custom devices to library
- [ ] Device instance naming
  - [ ] Rename devices when placed in rack
  - [ ] Show custom names instead of defaults
- [ ] Print/Export
  - [ ] Print-friendly CSS
  - [ ] Export as PNG/SVG image
  - [ ] Export as PDF
- [ ] Multiple configuration management
  - [ ] Save multiple layouts
  - [ ] Switch between configurations
  - [ ] Configuration history
- [ ] Collaboration features (if backend added)
  - [ ] Share configurations via URL
  - [ ] Real-time collaboration
- [ ] Cable management tracking (advanced)
  - [ ] Track connections between devices
  - [ ] Visualize cable paths
- [ ] Cost tracking
  - [ ] Add cost per device
  - [ ] Calculate total cost
- [ ] Asset management
  - [ ] Serial numbers
  - [ ] Purchase dates
  - [ ] Warranty tracking

## Phase 11: Testing & Deployment
- [ ] Cross-browser testing
  - [ ] Chrome
  - [ ] Firefox
  - [ ] Safari
  - [ ] Edge
- [ ] Responsive testing (if applicable)
- [ ] Performance optimization
  - [ ] Large rack configurations (10+ racks)
  - [ ] Many devices (100+ devices)
- [ ] Write README.md
  - [ ] Installation instructions
  - [ ] Usage guide
  - [ ] JSON schema documentation
  - [ ] Screenshots
- [ ] Choose deployment platform
  - [ ] GitHub Pages (static)
  - [ ] Netlify (static)
  - [ ] Vercel (static or with API)
  - [ ] Traditional web host
- [ ] Deploy application
- [ ] Set up CI/CD (optional)

## Critical Decisions Needed Before Starting

1. **Framework**: Vanilla JS, React, Vue, or Svelte?
2. **Styling**: Plain CSS, Sass/SCSS, Tailwind, or CSS-in-JS?
3. **Backend**: Fully static or minimal server for POST endpoint?
4. **Storage**: localStorage, file download/upload, or backend database?
5. **Drag & Drop Library**: HTML5 native, react-dnd, interact.js, or dnd-kit?

## Recommended Starting Point

### Minimal Viable Product (MVP):
1. Vanilla JS or React (for faster development)
2. Single rack with 42 RU
3. Fixed device library (5-10 devices)
4. Basic drag and drop
5. Simple power/HVAC calculation and display
6. JSON export only (no import initially)
7. localStorage for persistence

### Then iterate to add:
- Multiple racks
- Full device library
- JSON import
- Configuration menu
- Polish and additional features
