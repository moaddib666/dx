<template>
  <div class="info-section">
    <h4>Labels</h4>
    <div class="labels-container">
      <div class="label-list">
        <div
            v-for="(label, index) in localLabels"
            :key="index"
            class="label-item"
        >
          <input
              v-model="localLabels[index]"
              :disabled="!editable"
              class="label-input"
              @blur="onLabelsUpdated"
          />
          <button
              v-if="editable"
              class="remove-label-btn"
              title="Remove label"
              @click="removeLabel(index)"
          >
            <i class="icon-times"></i>
          </button>
        </div>
      </div>
      <button
          v-if="editable"
          class="add-label-btn"
          @click="addLabel"
      >
        <i class="icon-plus"></i> Add Label
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Labels',
  props: {
    labels: {
      type: Array,
      default: () => []
    },
    editable: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      localLabels: [...this.labels]
    };
  },
  watch: {
    labels: {
      handler(newLabels) {
        this.localLabels = [...newLabels];
      },
      deep: true
    }
  },
  methods: {
    addLabel() {
      this.localLabels.push('');
      this.$nextTick(() => {
        // Focus the newly added label input
        const inputs = this.$el.querySelectorAll('.label-input');
        if (inputs.length > 0) {
          inputs[inputs.length - 1].focus();
        }
      });
    },
    removeLabel(index) {
      this.localLabels.splice(index, 1);
      this.onLabelsUpdated();
    },
    onLabelsUpdated() {
      // Filter out empty labels
      const filteredLabels = this.localLabels.filter(label => label.trim() !== '');
      this.$emit('update:labels', filteredLabels);
    }
  }
};
</script>

<style scoped>
.info-section {

}

.labels-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.label-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.label-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.label-input {
  flex: 1;
  background: #444;
  border: 1px solid #555;
  color: #fff;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
}

.label-input:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.remove-label-btn {
  background: rgba(255, 0, 0, 0.2);
  border: 1px solid rgba(255, 0, 0, 0.3);
  color: #ff6666;
  width: 24px;
  height: 24px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-label-btn:hover {
  background: rgba(255, 0, 0, 0.3);
  border-color: rgba(255, 0, 0, 0.4);
}

.add-label-btn {
  background: rgba(0, 128, 255, 0.2);
  border: 1px solid rgba(0, 128, 255, 0.3);
  color: #66aaff;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  align-self: flex-start;
  margin-top: 0.5rem;
}

.add-label-btn:hover {
  background: rgba(0, 128, 255, 0.3);
  border-color: rgba(0, 128, 255, 0.4);
}
</style>