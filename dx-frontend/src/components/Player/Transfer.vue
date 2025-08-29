<template>
  <div class="character-tool">
    <!-- Buttons -->
    <div class="button-group">
      <CompactButton @click="triggerImport" buttonType="default">
        Import
      </CompactButton>
      <CompactButton @click="openEditor" buttonType="default">
        Edit
      </CompactButton>
      <CompactButton @click="exportCharacter" buttonType="default">
        Export
      </CompactButton>

    </div>

    <!-- File Input (Hidden) -->
    <input
        type="file"
        ref="fileInput"
        @change="handleFileImport"
        accept="application/json"
        class="hidden"
    />

    <!-- Modal for JSON Editor -->
    <div v-if="editorVisible" class="modal">
      <div class="modal-content">
        <textarea
            v-model="editorContent"
            class="editor"
            :style="{ fontFamily: 'monospace' }"
        ></textarea>
        <div class="modal-buttons">
          <button @click="saveEditorChanges" class="button save">Save</button>
          <button @click="closeEditor" class="button cancel">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CompactButton from "@/components/btn/CompactButton.vue";

export default {
  name: "CharacterTool",
  components: {CompactButton},
  props: {
    character: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      editorVisible: false,
      editorContent: "", // JSON content for the editor
    };
  },
  methods: {
    triggerImport() {
      this.$refs.fileInput.click();
    },
    handleFileImport(event) {
      const file = event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const importedData = JSON.parse(e.target.result);
          this.$emit("import", importedData);
        } catch (error) {
          alert("Invalid JSON file.");
        }
      };
      reader.readAsText(file);
    },
    exportCharacter() {
      const dataStr = JSON.stringify(this.character, null, 2);
      const blob = new Blob([dataStr], { type: "application/json" });
      const url = URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = "character.json";
      a.click();
      URL.revokeObjectURL(url);
    },
    openEditor() {
      this.editorContent = JSON.stringify(this.character, null, 2);
      this.editorVisible = true;
    },
    saveEditorChanges() {
      try {
        const updatedData = JSON.parse(this.editorContent);
        this.$emit("import", updatedData); // Emit updated data
        this.editorVisible = false;
      } catch (error) {
        alert("Invalid JSON format. Please fix errors before saving.");
      }
    },
    closeEditor() {
      this.editorVisible = false;
    },
  },
};
</script>

<style scoped>
.character-tool {
  display: flex;
  justify-content: center;
  gap: 1rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.button-group {
  display: flex;
  gap: 1rem;
}

.button-group .button {
  padding: 0.75rem 1.5rem;
  font-size: 16px;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
  backdrop-filter: blur(2px);
}

.button {
  background: linear-gradient(45deg, rgba(250, 218, 149, 0.1), rgba(127, 255, 22, 0.1));
  color: #fada95;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 25px;
  padding: 0.75rem 1.5rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(2px);
}

.button:hover {
  background: linear-gradient(45deg, rgba(250, 218, 149, 0.2), rgba(127, 255, 22, 0.2));
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(127, 255, 22, 0.4);
  border-color: #7fff16;
}

.button:active {
  transform: translateY(1px);
  box-shadow: 0 2px 5px rgba(127, 255, 22, 0.2);
}

.hidden {
  display: none;
}

/* Modal */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: rgba(0, 0, 0, 0.4);
  padding: 2rem;
  border-radius: 0.5rem;
  width: 80%;
  max-height: 90%;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 20px rgba(127, 255, 22, 0.2);
  overflow: auto;
  border: 2px solid rgba(127, 255, 22, 0.3);
  backdrop-filter: blur(2px);
  position: relative;
}

/* Flow border effect for modal */
.modal-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 0.5rem;
  background: linear-gradient(45deg,
    transparent,
    rgba(127, 255, 22, 0.05),
    transparent,
    rgba(127, 255, 22, 0.05),
    transparent
  );
  background-size: 300% 300%;
  animation: flowBorder 8s ease-in-out infinite;
  opacity: 0.3;
  pointer-events: none;
}

@keyframes flowBorder {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.editor {
  width: 100%;
  height: 400px;
  padding: 1rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.25rem;
  font-size: 14px;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  resize: none;
  font-family: 'Courier New', monospace;
  backdrop-filter: blur(2px);
  position: relative;
  z-index: 2;
}

.editor:focus {
  outline: none;
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.05);
  box-shadow: 0 0 10px rgba(127, 255, 22, 0.2);
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
  position: relative;
  z-index: 2;
}

.save {
  background: linear-gradient(45deg, rgba(127, 255, 22, 0.2), rgba(250, 218, 149, 0.2));
  color: #fada95;
  border: 2px solid #7fff16;
}

.save:hover {
  background: linear-gradient(45deg, rgba(127, 255, 22, 0.3), rgba(250, 218, 149, 0.3));
  box-shadow: 0 4px 15px rgba(127, 255, 22, 0.4);
}

.cancel {
  background: rgba(255, 107, 107, 0.2);
  color: #ff6b6b;
  border: 2px solid rgba(255, 107, 107, 0.4);
}

.cancel:hover {
  background: rgba(255, 107, 107, 0.3);
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
  border-color: #ff6b6b;
}
</style>
