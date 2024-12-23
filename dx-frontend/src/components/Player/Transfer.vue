<template>
  <div class="character-tool">
    <!-- Buttons -->
    <div class="button-group">
      <GlassButton @click="triggerImport" buttonType="default">
        Import
      </GlassButton>
      <GlassButton @click="openEditor" buttonType="default">
        Edit
      </GlassButton>
      <GlassButton @click="exportCharacter" buttonType="default">
        Export
      </GlassButton>

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
import GlassButton from "@/components/btn/Glass.vue";

export default {
  name: "CharacterTool",
  components: {GlassButton},
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
  gap: 10px;
}

.button-group .button {
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.button {
  background-color: #2196f3;
  color: white;
}

.button:hover {
  background-color: #1976d2;
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
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 80%;
  max-height: 90%;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
  overflow: auto;
}

.editor {
  width: 100%;
  height: 400px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  background: #f4f4f4;
  color: #333;
  resize: none;
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
}

.save {
  background-color: #4caf50;
  color: white;
}

.save:hover {
  background-color: #388e3c;
}

.cancel {
  background-color: #f44336;
  color: white;
}

.cancel:hover {
  background-color: #d32f2f;
}
</style>
