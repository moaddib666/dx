<template>
  <div class="reward-editor">
    <div class="reward-header">
      <h4>{{ title }}</h4>
      <button @click="$emit('cancel')" class="btn-close">
        <span class="icon">✖</span>
      </button>
    </div>

    <!-- Items Section -->
    <div class="reward-section">
      <div class="section-header">
        <h5>Items</h5>
        <button @click="addItem" class="btn-add">
          <span class="icon">+</span> Add Item
        </button>
      </div>

      <div v-if="!localReward.items?.length" class="empty-section-message">
        No items in this reward.
      </div>

      <div v-else class="items-list">
        <div
          v-for="(item, index) in localReward.items"
          :key="index"
          class="item-row"
        >
          <div class="item-details">
            <div class="form-group">
              <label :for="`item-id-${index}`">Item ID</label>
              <input
                :id="`item-id-${index}`"
                v-model="item.itemId"
                type="text"
                class="item-input"
                placeholder="Enter item ID"
              />
            </div>
            <div class="form-group">
              <label :for="`item-quantity-${index}`">Quantity</label>
              <input
                :id="`item-quantity-${index}`"
                v-model.number="item.quantity"
                type="number"
                min="1"
                class="quantity-input"
                placeholder="Quantity"
              />
            </div>
          </div>
          <button @click="removeItem(index)" class="btn-remove">
            <span class="icon">🗑️</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Tokens Section -->
    <div class="reward-section">
      <div class="section-header">
        <h5>Tokens</h5>
        <button @click="addToken" class="btn-add">
          <span class="icon">+</span> Add Token
        </button>
      </div>

      <div v-if="!localReward.tokens?.length" class="empty-section-message">
        No tokens in this reward.
      </div>

      <div v-else class="tokens-list">
        <div
          v-for="(token, index) in localReward.tokens"
          :key="index"
          class="token-row"
        >
          <div class="token-details">
            <div class="form-group">
              <label :for="`token-id-${index}`">Token Type</label>
              <select
                :id="`token-id-${index}`"
                v-model="token.tokenId"
                class="token-select"
              >
                <option value="xp">Experience (XP)</option>
                <option value="gold">Gold</option>
                <option value="reputation">Reputation</option>
                <option value="karma">Karma</option>
                <option value="custom">Custom</option>
              </select>
              <input
                v-if="token.tokenId === 'custom'"
                v-model="token.customTokenId"
                type="text"
                class="custom-token-input"
                placeholder="Enter custom token ID"
              />
            </div>
            <div class="form-group">
              <label :for="`token-amount-${index}`">Amount</label>
              <input
                :id="`token-amount-${index}`"
                v-model.number="token.amount"
                type="number"
                class="amount-input"
                placeholder="Amount"
              />
            </div>
          </div>
          <button @click="removeToken(index)" class="btn-remove">
            <span class="icon">🗑️</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Effects Section -->
    <div class="reward-section">
      <div class="section-header">
        <h5>Effects</h5>
        <button @click="addEffect" class="btn-add">
          <span class="icon">+</span> Add Effect
        </button>
      </div>

      <div v-if="!localReward.effects?.length" class="empty-section-message">
        No effects in this reward.
      </div>

      <div v-else class="effects-list">
        <div
          v-for="(effect, index) in localReward.effects"
          :key="index"
          class="effect-row"
        >
          <div class="effect-details">
            <div class="form-group">
              <label :for="`effect-id-${index}`">Effect ID</label>
              <input
                :id="`effect-id-${index}`"
                v-model="effect.effectId"
                type="text"
                class="effect-input"
                placeholder="Enter effect ID"
              />
            </div>
            <div class="form-group">
              <label :for="`effect-duration-${index}`">Duration (seconds)</label>
              <input
                :id="`effect-duration-${index}`"
                v-model.number="effect.duration"
                type="number"
                min="0"
                class="duration-input"
                placeholder="Duration in seconds (0 for permanent)"
              />
            </div>
          </div>
          <button @click="removeEffect(index)" class="btn-remove">
            <span class="icon">🗑️</span>
          </button>
        </div>
      </div>
    </div>

    <div class="form-actions">
      <button @click="saveReward" class="btn-save">
        Save Reward
      </button>
      <button @click="$emit('cancel')" class="btn-cancel">
        Cancel
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { Reward, ItemReward, TokenReward, EffectReward } from '@/api/dx-backend';

const props = defineProps<{
  reward?: Reward;
  title?: string;
}>();

const emit = defineEmits<{
  (e: 'save', reward: Reward): void;
  (e: 'cancel'): void;
}>();

// Computed properties
const title = computed(() => props.title || 'Edit Reward');

// Create a local copy of the reward for editing
const localReward = ref<Reward>(props.reward ? { ...props.reward } : {
  id: '',
  items: [],
  tokens: [],
  effects: []
});

// Reset local reward when props change
watch(() => props.reward, (newReward) => {
  if (newReward) {
    localReward.value = { ...newReward };
  }
}, { deep: true });

// Event handlers
const addItem = () => {
  if (!localReward.value.items) {
    localReward.value.items = [];
  }

  const newItem: ItemReward = {
    itemId: '',
    quantity: 1
  };

  localReward.value.items.push(newItem);
};

const removeItem = (index: number) => {
  if (localReward.value.items) {
    localReward.value.items.splice(index, 1);
  }
};

const addToken = () => {
  if (!localReward.value.tokens) {
    localReward.value.tokens = [];
  }

  const newToken: TokenReward = {
    tokenId: 'xp',
    amount: 0
  };

  localReward.value.tokens.push(newToken);
};

const removeToken = (index: number) => {
  if (localReward.value.tokens) {
    localReward.value.tokens.splice(index, 1);
  }
};

const addEffect = () => {
  if (!localReward.value.effects) {
    localReward.value.effects = [];
  }

  const newEffect: EffectReward = {
    effectId: '',
    duration: 0
  };

  localReward.value.effects.push(newEffect);
};

const removeEffect = (index: number) => {
  if (localReward.value.effects) {
    localReward.value.effects.splice(index, 1);
  }
};

const saveReward = () => {
  // Process custom token IDs
  if (localReward.value.tokens) {
    localReward.value.tokens.forEach(token => {
      if (token.tokenId === 'custom' && token.customTokenId) {
        token.tokenId = token.customTokenId;
        delete token.customTokenId;
      }
    });
  }

  emit('save', localReward.value);
};
</script>

<style scoped>
.reward-editor {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border: 1px solid rgba(255, 215, 0, 0.2);
}

.reward-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
  padding-bottom: 0.75rem;
}

.reward-header h4 {
  font-size: 1.2rem;
  color: var(--cyber-yellow, #ffd700);
  margin: 0;
}

.btn-close {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.btn-close:hover {
  color: white;
}

.reward-section {
  margin-bottom: 1.5rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h5 {
  font-size: 1rem;
  color: white;
  margin: 0;
}

.btn-add {
  background: rgba(255, 215, 0, 0.2);
  color: var(--cyber-yellow, #ffd700);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
}

.btn-add:hover {
  background: rgba(255, 215, 0, 0.3);
  transform: translateY(-2px);
}

.empty-section-message {
  text-align: center;
  padding: 1rem;
  color: rgba(255, 255, 255, 0.5);
  font-style: italic;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  font-size: 0.9rem;
}

.items-list, .tokens-list, .effects-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.item-row, .token-row, .effect-row {
  display: flex;
  align-items: flex-start;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  padding: 1rem;
}

.item-details, .token-details, .effect-details {
  flex: 1;
  display: flex;
  gap: 1rem;
}

.form-group {
  flex: 1;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: white;
  font-weight: bold;
}

.item-input, .quantity-input, .token-select, .custom-token-input, .amount-input, .effect-input, .duration-input {
  width: 100%;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 4px;
  padding: 0.75rem;
  color: white;
  font-size: 1rem;
}

.custom-token-input {
  margin-top: 0.5rem;
}

.btn-remove {
  background: rgba(0, 0, 0, 0.3);
  border: none;
  border-radius: 4px;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-left: 1rem;
}

.btn-remove:hover {
  background: rgba(255, 0, 0, 0.3);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-save {
  background: var(--cyber-yellow, #ffd700);
  color: black;
  border: none;
  border-radius: 4px;
  padding: 0.75rem 1.5rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-save:hover {
  background: #ffdf33;
  transform: translateY(-2px);
}

.btn-cancel {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel:hover {
  background: rgba(255, 255, 255, 0.2);
}

.icon {
  font-size: 1rem;
  margin-right: 0.25rem;
}

@media (max-width: 768px) {
  .reward-editor {
    padding: 1rem;
  }

  .item-details, .token-details, .effect-details {
    flex-direction: column;
    gap: 0.5rem;
  }

  .form-actions {
    flex-direction: column;
    gap: 0.5rem;
  }

  .btn-save, .btn-cancel {
    width: 100%;
  }
}
</style>