/**
 * DragDropService
 * Handles global drag and drop operations for the WorldEditor
 */
export class DragDropService {
  constructor() {
    this.isDragging = false;
    this.draggedItem = null;
    this.dropTargets = new Set();
    this.eventListeners = new Map();

    // Bind the document drop handler to handle drops on unsupported elements
    this.handleDocumentDrop = this.handleDocumentDrop.bind(this);
    this.handleDocumentDragEnd = this.handleDocumentDragEnd.bind(this);

    // Initialize document event listeners
    document.addEventListener('drop', this.handleDocumentDrop);
    document.addEventListener('dragend', this.handleDocumentDragEnd);
  }

  /**
   * Start dragging an item
   * @param {Object} item - The item being dragged
   */
  startDrag(item) {
    console.log('DragDropService.startDrag called with item:', item);
    this.isDragging = true;
    this.draggedItem = item;
    this.emit('dragStart', item);

    // Add the dragging class to all drop targets
    console.log('Highlighting drop targets. Current targets:', this.dropTargets.size);
    this.highlightDropTargets();
  }

  /**
   * End dragging
   */
  endDrag() {
    console.log('DragDropService.endDrag called');
    this.isDragging = false;
    this.draggedItem = null;
    this.emit('dragEnd');

    // Remove the dragging class from all drop targets
    this.unhighlightDropTargets();
  }

  /**
   * Register a drop target element
   * @param {HTMLElement} element - The drop target element
   */
  registerDropTarget(element) {
    console.log('DragDropService.registerDropTarget called with element:', element);

    if (element && !this.dropTargets.has(element)) {
      this.dropTargets.add(element);
      console.log('Drop target registered. Total targets:', this.dropTargets.size);

      // If currently dragging, highlight this element immediately
      if (this.isDragging) {
        console.log('Currently dragging, highlighting element immediately');
        element.classList.add('drag-over-highlight');
      }
    } else {
      console.log('Element already registered or invalid');
    }
  }

  /**
   * Unregister a drop target element
   * @param {HTMLElement} element - The drop target element to unregister
   */
  unregisterDropTarget(element) {
    console.log('DragDropService.unregisterDropTarget called with element:', element);

    if (element) {
      this.dropTargets.delete(element);
      element.classList.remove('drag-over-highlight');
      console.log('Drop target unregistered. Remaining targets:', this.dropTargets.size);
    }
  }

  /**
   * Highlight all registered drop targets
   */
  highlightDropTargets() {
    console.log('DragDropService.highlightDropTargets called. Targets to highlight:', this.dropTargets.size);

    this.dropTargets.forEach(element => {
      console.log('Highlighting element:', element);
      element.classList.add('drag-over-highlight');
    });
  }

  /**
   * Remove highlight from all drop targets
   */
  unhighlightDropTargets() {
    console.log('DragDropService.unhighlightDropTargets called. Targets to unhighlight:', this.dropTargets.size);

    this.dropTargets.forEach(element => {
      console.log('Unhighlighting element:', element);
      element.classList.remove('drag-over-highlight');
    });
  }

  /**
   * Handle drops on unsupported elements
   * @param {Event} event - The drop event
   */
  handleDocumentDrop(event) {
    console.log('DragDropService.handleDocumentDrop called', {
      isDragging: this.isDragging,
      target: event.target,
      dropTargetsCount: this.dropTargets.size
    });

    // Only handle drops that aren't on registered drop targets
    const isDropTarget = Array.from(this.dropTargets).some(element =>
      element.contains(event.target) || element === event.target
    );

    console.log('Is drop target?', isDropTarget);

    if (!isDropTarget && this.isDragging) {
      event.preventDefault();
      console.warn('Drop failure: Unsupported drop target', {
        item: this.draggedItem,
        target: event.target
      });

      this.emit('dropFailure', {
        item: this.draggedItem,
        target: event.target,
        reason: 'Unsupported drop target'
      });

      this.endDrag();
    } else if (isDropTarget) {
      console.log('Drop on valid target, letting the target handle it');
      // Don't call endDrag here, let the component handle it
    }
  }

  /**
   * Handle drag end event (cleanup)
   * This is called when the drag operation ends without a drop
   * or when the drop is on an invalid target
   */
  handleDocumentDragEnd(event) {
    console.log('DragDropService.handleDocumentDragEnd called', {
      isDragging: this.isDragging,
      event: event
    });

    // Add a small delay to allow drop events to be processed first
    setTimeout(() => {
      if (this.isDragging) {
        console.log('Still dragging after delay, calling endDrag');
        this.endDrag();
      }
    }, 50);
  }

  /**
   * Clean up event listeners when service is destroyed
   */
  destroy() {
    document.removeEventListener('drop', this.handleDocumentDrop);
    document.removeEventListener('dragend', this.handleDocumentDragEnd);
    this.dropTargets.clear();
    this.eventListeners.clear();
  }

  /**
   * Event system for components to listen to changes
   */
  on(event, callback) {
    if (!this.eventListeners.has(event)) {
      this.eventListeners.set(event, []);
    }
    this.eventListeners.get(event).push(callback);
  }

  /**
   * Remove event listener
   */
  off(event, callback) {
    if (this.eventListeners.has(event)) {
      const listeners = this.eventListeners.get(event);
      const index = listeners.indexOf(callback);
      if (index > -1) {
        listeners.splice(index, 1);
      }
    }
  }

  /**
   * Emit event to listeners
   */
  emit(event, data) {
    if (this.eventListeners.has(event)) {
      this.eventListeners.get(event).forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`Error in event listener for ${event}:`, error);
        }
      });
    }
  }
}

// Export singleton instance
export const dragDropService = new DragDropService();
