<script setup lang="ts">
import {Reward, TokenReward, ItemReward, EffectReward} from "@/api/dx-backend";
import {itemsService} from '@/services/ItemsService';
import {computed} from "vue";
import DXCell from "@/components/DXCell.vue";

interface Props {
  reward: Reward;
}

const props = defineProps<Props>();

// Resolve item details for item rewards
const resolveItemDetails = (itemReward: ItemReward) => {
  if (!itemReward.item) {
    return null;
  }

  const itemInstance = itemsService.getItemById(itemReward.item);
  if (!itemInstance) {
    return null;
  }

  return {
    id: itemReward.item,
    title: itemInstance.name,
    image: itemInstance.icon,
    description: `Quantity: ${itemReward.quantity || 1}`,
  };
};

// Computed properties for different reward types
const hasExperience = computed(() => props.reward.experience && props.reward.experience > 0);
const hasTokens = computed(() => props.reward.tokens && props.reward.tokens.length > 0);
const hasItems = computed(() => props.reward.items && props.reward.items.length > 0);
const hasEffects = computed(() => props.reward.effects && props.reward.effects.length > 0);

// Resolve all item rewards
const resolvedItems = computed(() => {
  if (!hasItems.value) return [];

  return props.reward.items
    .map(itemReward => resolveItemDetails(itemReward))
    .filter(item => item !== null);
});
</script>

<template>
  <div class="reward-container">
    <div class="reward-description" v-if="props.reward.description">
      {{ props.reward.description }}
    </div>

    <!-- Experience reward -->
    <div class="reward-section" v-if="hasExperience">
      <div class="reward-section-header">
        <span class="reward-type-label">XP</span>
        <span class="reward-value">{{ props.reward.experience }}</span>
      </div>
    </div>

    <!-- Token rewards -->
    <div class="reward-section" v-if="hasTokens">
      <div class="reward-section-header">
        <span class="reward-type-label">Tokens</span>
      </div>
      <div class="reward-items">
        <div v-for="token in props.reward.tokens" :key="token.id" class="token-reward">
          <span class="token-name">{{ token.token }}</span>
          <span class="token-quantity">{{ token.quantity }}</span>
        </div>
      </div>
    </div>

    <!-- Item rewards -->
    <div class="reward-section" v-if="hasItems">
      <div class="reward-section-header">
        <span class="reward-type-label">Items</span>
      </div>
      <div class="reward-items">
        <div v-for="(item, index) in resolvedItems" :key="index" class="item-reward">
          <DXCell
            :image="item.image"
            :title="item.title"
            :subtitle="item.description"
          />
        </div>
        <!-- Fallback for unresolved items -->

        <div v-for="(item, index) in props.reward.items" :key="`unresolved-${index}`" class="item-reward"
           >
          <div class="placeholder-item"   v-if="item && !resolvedItems.some(resolved => resolved && resolved.id && item.item && resolved.id === item.item)">
            <div class="placeholder-icon">?</div>
            <div class="placeholder-text">Item ID: {{ item.item }}</div>
            <div class="placeholder-text">Qty: {{ item.quantity || 1 }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Effect rewards -->
    <div class="reward-section" v-if="hasEffects">
      <div class="reward-section-header">
        <span class="reward-type-label">Effects</span>
      </div>
      <div class="reward-items">
        <div v-for="effect in props.reward.effects" :key="effect.id" class="effect-reward">
          <div class="effect-details">
            <span class="effect-name">{{ effect.effect }}</span>
            <span v-if="effect.duration" class="effect-duration">Duration: {{ effect.duration }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- No rewards message -->
    <div class="no-rewards" v-if="!hasExperience && !hasTokens && !hasItems && !hasEffects">
      No rewards specified
    </div>
  </div>
</template>

<style scoped>
/* Import the same fonts as in the parent components */
@import url('https://fonts.googleapis.com/css2?family=Cinzel&family=Inter&family=Source+Code+Pro&display=swap');

.reward-container {
  position: relative;
  margin: 0.5rem 0;
  font-family: 'Inter', sans-serif;
  color: #bcbbbb;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
}

.reward-description {
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  width: 100%;
}

.reward-section {
  margin-bottom: 0.5rem;
  width: 100%;
  border-left: 2px solid #d6b97b;
  padding-left: 0.5rem;
}

.reward-section-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.3rem;
}

.reward-type-label {
  background-color: #1a1c1f;
  color: #d6b97b;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  border: 1px solid #d6b97b;
  text-shadow: 0 0 4px rgba(214, 185, 123, 0.3);
  font-weight: bold;
  font-family: 'Cinzel', serif;
  margin-right: 0.5rem;
}

.reward-value {
  font-size: 0.9rem;
  color: #d6b97b;
  font-weight: bold;
}

.reward-items {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.token-reward, .effect-reward {
  background-color: #1a1c1f;
  border: 1px solid #d6b97b;
  border-radius: 4px;
  padding: 0.3rem 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.token-name, .effect-name {
  font-weight: bold;
  color: #d6b97b;
  font-size: 0.8rem;
}

.token-quantity {
  background-color: rgba(214, 185, 123, 0.2);
  padding: 0.1rem 0.3rem;
  border-radius: 3px;
  font-size: 0.7rem;
}

.effect-duration {
  font-size: 0.7rem;
  opacity: 0.8;
}

.item-reward {
  width: 4rem;
  height: 4rem;
}

.placeholder-item {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #1a1c1f;
  color: #d6b97b;
  text-align: center;
  padding: 0.15rem;
  border: 0.15rem solid transparent;
  border-image-slice: 60 60 60 60;
  border-image-width: 10px 10px 10px 10px;
  border-image-outset: 0px 0px 0px 0px;
  border-image-repeat: stretch stretch;
  border-image-source: url("@/assets/images/border/borderassets.png");
}

.placeholder-icon {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0.15rem;
  font-family: 'Cinzel', serif;
  text-shadow: 0 0 4px rgba(214, 185, 123, 0.5);
}

.placeholder-text {
  font-family: 'Source Code Pro', monospace;
  font-size: 0.6rem;
  opacity: 0.9;
  word-break: break-word;
  max-width: 100%;
}

.no-rewards {
  font-style: italic;
  font-size: 0.9rem;
  opacity: 0.7;
  padding: 0.5rem;
  text-align: center;
  width: 100%;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .reward-items {
    gap: 0.3rem;
  }

  .item-reward {
    width: 3.5rem;
    height: 3.5rem;
  }
}
</style>