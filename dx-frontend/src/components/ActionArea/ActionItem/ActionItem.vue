<script setup lang="ts">
import {defineProps} from 'vue';
import {TypeC27Enum} from "@/api/dx-backend";
// TODO: decode emitted events

const props = defineProps({
  id: {
    type: String,
    default: ''
  },
  ctaType: {
    type: TypeC27Enum,
    default: TypeC27Enum.Defense
  },
  image: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  }
});

</script>

<template>
  <div class="cta__holder"
       @click="$emit('select')"
       :class="{
         'cta__holder--disabled': id === '' || disabled,
       }"
  >
    <img
        :title="title"
        :class="{
         'cta__icon__attack': ctaType === TypeC27Enum.Attack,
         'cta__icon__defense': ctaType === TypeC27Enum.Defense,
         'cta__icon__heal': ctaType === TypeC27Enum.Heal,
         'cta__icon__buff': ctaType === TypeC27Enum.Buff,
         'cta__icon__debuff': ctaType === TypeC27Enum.Debuff,
         'cta__icon__utility': ctaType === TypeC27Enum.Utility,
         'cta__icon__special': ctaType === TypeC27Enum.Special,
         'cta__icon--disabled': disabled
       }"
        src="@/assets/images/action/anomaly.png"
        alt="Action Icon"
        class="cta__icon"
        v-if="image"
    />
  </div>
</template>
<style scoped>
.cta__holder {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background: url("@/assets/images/action-area/Cell.png") no-repeat center center;
  background-size: cover;
}

.cta__icon {
  width: 85%;
  height: 85%;
  object-fit: contain;
}

.cta__holder--disabled {
  pointer-events: none;
}

.cta__icon__attack {
  border: 0 solid #ff1744;
  box-shadow: 0 0 5px #ff1744;
}

.cta__icon__defense {
  border: 0 solid #00e5ff;
  box-shadow: 0 0 0.3rem #00e5ff;
}

.cta__icon__heal {
  border: 0 solid #00ff00;
  box-shadow: 0 0 5px #00ff00;
}

.cta__icon__buff {
  border: 0 solid #ffc107;
  box-shadow: 0 0 5px #ffc107;
}

.cta__icon__debuff {
  border: 0 solid #b71c1c;
  box-shadow: 0 0 5px #b71c1c;
}

.cta__icon__utility {
  border: 0 solid #9e9e9e;
  box-shadow: 0 0 5px #9e9e9e;
}

.cta__icon__special {
  border: 0 solid #673ab7;
  box-shadow: 0 0 5px #673ab7;
}

.cta__icon:hover {
  transform: scale(1.1);
  transition: transform 0.2s ease-in-out;
  border-width: 0.1rem;
}

.cta__icon:active {
  transform: scale(1);
  transition: transform 0.1s ease-in-out;
}

.cta__icon--disabled {
  filter: grayscale(100%);
}

.cta__icon:focus {
  outline: none;
  box-shadow: 0 0 0.3rem rgba(255, 255, 255, 0.5);
}
.cta__icon[title] {
  cursor: pointer;
}

.cta__icon[title]:hover {
  box-shadow: 0 0 0.3rem rgba(255, 255, 255, 0.7);
}

</style>