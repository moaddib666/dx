<template>
  <div>
    <button @click="$emit('add-room')">Add Room</button>
    <button @click="$emit('start-connection')">Start Connection</button>
    <button @click="onImport">Import Map</button>
    <button @click="$emit('export-map')">Export Map</button>
    <input ref="fileInput" style="display: none;" type="file" @change="onFileChange"/>
  </div>
</template>

<script>
export default {
  methods: {
    onImport() {
      this.$refs.fileInput.click();
    },
    onFileChange(event) {
      const file = event.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (e) => this.$emit("import-map", JSON.parse(e.target.result));
      reader.readAsText(file);
    },
  },
};
</script>
