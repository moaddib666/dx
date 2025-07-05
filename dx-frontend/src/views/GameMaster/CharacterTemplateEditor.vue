<template>
  <div class="character-template-editor">
    <!-- Top Row (1) -->
    <div class="top-row">
      <h1>Character Template Editor</h1>
      <div class="toolbar">
        <button class="save-btn">Save Template</button>
        <button class="cancel-btn">Cancel</button>
      </div>
    </div>

    <!-- Center Row (8) -->
    <div class="center-row">
      <!-- Left Column (1) -->
      <div class="left-column">
        <div class="sidebar-section">
          <h3>Template Categories</h3>
          <ul class="category-list">
            <li class="category-item">Warriors</li>
            <li class="category-item">Mages</li>
            <li class="category-item">Rogues</li>
            <li class="category-item">Clerics</li>
            <li class="category-item">Custom</li>
          </ul>
        </div>
      </div>

      <!-- Center Column (2) -->
      <div class="center-column">
        <!-- This column is divided into 1,8 for columns -->
        <div class="center-content">
          <!-- Left part (1) -->
          <div class="template-list">
            <h3>Available Templates</h3>
            <div class="template-item">Warrior Captain</div>
            <div class="template-item">Elite Guard</div>
            <div class="template-item">Berserker</div>
            <div class="template-item">Paladin</div>
            <div class="template-item">Knight</div>
          </div>

          <!-- Right part (8) -->
          <div class="template-editor">
            <h3>Template Details</h3>

            <div class="form-group">
              <label>Template Name</label>
              <input type="text" placeholder="Enter template name" />
            </div>

            <div class="form-group">
              <label>Base Stats</label>
              <div class="stats-grid">
                <div class="stat-item">
                  <label>Strength</label>
                  <input type="number" value="10" />
                </div>
                <div class="stat-item">
                  <label>Dexterity</label>
                  <input type="number" value="10" />
                </div>
                <div class="stat-item">
                  <label>Constitution</label>
                  <input type="number" value="10" />
                </div>
                <div class="stat-item">
                  <label>Intelligence</label>
                  <input type="number" value="10" />
                </div>
                <div class="stat-item">
                  <label>Wisdom</label>
                  <input type="number" value="10" />
                </div>
                <div class="stat-item">
                  <label>Charisma</label>
                  <input type="number" value="10" />
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>Description</label>
              <textarea placeholder="Enter template description"></textarea>
            </div>

            <div class="form-group">
              <label>Starting Equipment</label>
              <textarea placeholder="Enter starting equipment"></textarea>
            </div>

            <div class="form-group">
              <label>Special Abilities</label>
              <textarea placeholder="Enter special abilities"></textarea>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column (1) -->
      <div class="right-column">
        <div class="sidebar-section">
          <h3>Preview</h3>
          <div class="preview-card">
            <h4>Character Preview</h4>
            <div class="preview-image">
              [Character Image Placeholder]
            </div>
            <div class="preview-stats">
              <p>STR: 10</p>
              <p>DEX: 10</p>
              <p>CON: 10</p>
              <p>INT: 10</p>
              <p>WIS: 10</p>
              <p>CHA: 10</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Row (1) -->
    <div class="bottom-row">
      <div class="status-bar">
        <span>Last saved: Never</span>
        <span>Status: Editing</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CharacterTemplateEditor',
  data() {
    return {
      // Data will be added as needed
    };
  },
  methods: {
    // Methods will be added as needed
  }
};
</script>

<style scoped>
.character-template-editor {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
  background: #1e1e1e;
  color: #ffffff;
  font-family: 'Roboto', sans-serif;
  max-height: 100vh;
}

/* Top Row - 1 part of vertical layout */
.top-row {
  height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background: #2d2d2d;
  border-bottom: 1px solid #444;
  min-height: 60px;
  color: white;
}

.toolbar {
  display: flex;
  gap: 1rem;
}

.toolbar button {
  padding: 0.5rem 1rem;
  background: #444;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-btn {
  background: #4CAF50;
  color: white;
}

.save-btn:hover {
  background: #3d8b40;
}

.cancel-btn {
  background: #f44336;
  color: white;
}

.cancel-btn:hover {
  background: #d32f2f;
}

/* Center Row - 8 parts of vertical layout */
.center-row {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* Left Column - 1 part of horizontal layout */
.left-column {
  width: 300px;
  background: #2d2d2d;
  border-right: 1px solid #444;
  padding: 20px;
  overflow-y: auto;
}

.sidebar-section h3 {
  color: #1E90FF;
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 1.2rem;
}

.template-list h3, .template-editor h3 {
  color: #1E90FF;
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.2rem;
}

.preview-card h4 {
  color: #1E90FF;
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.category-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.category-item {
  padding: 10px;
  margin: 5px 0;
  background: #444;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.category-item:hover {
  background: #555;
}

/* Center Column - 2 parts of horizontal layout */
.center-column {
  flex: 1;
  position: relative;
  overflow: hidden;
  background: #1e1e1e;
}

.center-content {
  display: flex;
  height: 100%;
}

/* Left part of center column - 1 part */
.template-list {
  width: 200px;
  border-right: 1px solid #444;
  padding: 20px;
  overflow-y: auto;
  background: #2d2d2d;
}

.template-item {
  padding: 10px;
  margin: 5px 0;
  background: #444;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.template-item:hover {
  background: #555;
}

/* Right part of center column - 8 parts */
.template-editor {
  flex: 8;
  padding: 20px;
  overflow-y: auto;
  background: #1e1e1e;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #ccc;
}

.form-group input[type="text"],
.form-group input[type="number"],
.form-group textarea {
  width: 100%;
  padding: 8px;
  background: #333;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.form-group input[type="text"]:focus,
.form-group input[type="number"]:focus,
.form-group textarea:focus {
  border-color: #1E90FF;
  outline: none;
}

.form-group textarea {
  height: 100px;
  resize: vertical;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-item label {
  margin-bottom: 5px;
  color: #ccc;
}

.stat-item input {
  width: 100%;
  padding: 8px;
  background: #333;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.stat-item input:focus {
  border-color: #1E90FF;
  outline: none;
}

/* Right Column - 1 part of horizontal layout */
.right-column {
  width: 300px;
  background: #2d2d2d;
  border-left: 1px solid #444;
  padding: 20px;
  overflow-y: auto;
}

.preview-card {
  background: #333;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  border: 1px solid #444;
}

.preview-image {
  height: 150px;
  background: #444;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 10px 0;
  border-radius: 4px;
  color: #ccc;
}

.preview-stats {
  font-size: 14px;
  color: #ccc;
}

.preview-stats p {
  margin: 5px 0;
}

/* Bottom Row - 1 part of vertical layout */
.bottom-row {
  height: 40px;
  background: #2d2d2d;
  color: white;
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border-top: 1px solid #444;
  min-height: 40px;
  font-size: 0.9rem;
}

.status-bar {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.status-bar span {
  color: #ccc;
}
</style>