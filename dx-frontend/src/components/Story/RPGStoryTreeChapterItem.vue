<script setup lang="ts">
import {defineProps, ref, computed} from 'vue';
import {Chapter} from '@/api/dx-backend';
import RPGStoryTreeQuestItem from "@/components/Story/RPGStoryTreeQuestItem.vue";

interface Props {
  chapter: Chapter;
  selectedItem: string;
  selected: boolean;
  collapsed: boolean;
}

const props = defineProps<Props>();
const isCollapsed = ref(props.collapsed);

// Toggle collapse state
const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value;
};

// Determine if this chapter is active
const isActive = computed(() => {
  return props.selectedItem === props.chapter.id;
});

</script>

<template>
  <div class="chapter-item" :class="{ 'active': isActive }">
    <div class="chapter-container" @click="toggleCollapse">
      <div class="chapter-image-container">
        <div class="chapter-image-gradient" :style="props.chapter.image ? { backgroundImage: `url(${props.chapter.image})` } : {}"></div>
      </div>
      <div class="chapter-number-frame">
        <div class="chapter-number">{{ props.chapter.order || 1 }}</div>
      </div>
      <h1 class="chapter-title">{{ props.chapter.title }}</h1>
    </div>

    <div class="chapter-quests" v-if="!isCollapsed">
      <RPGStoryTreeQuestItem
          v-for="quest in props.chapter.quests"
          :key="quest.id"
          :quest="quest"
          :selectedItem="props.selectedItem"
          :selected="props.selected"
          :collapsed="props.collapsed"
      >
      </RPGStoryTreeQuestItem>
    </div>
  </div>
</template>

<style scoped>
.chapter-item {
  margin-bottom: 0.75rem;
  border-radius: 0.4rem;
  background: linear-gradient(145deg, rgba(13, 25, 35, 0.8), rgba(20, 35, 50, 0.6));
  padding: 0.6rem;
  border: 0.1rem solid rgba(0, 196, 255, 0.3);
  box-shadow:
      0 0.25rem 0.75rem rgba(0, 0, 0, 0.4),
      inset 0 0.05rem 0 rgba(0, 196, 255, 0.1);
  transition: border-color 0.3s ease, box-shadow 0.3s ease, background 0.3s ease;
  position: relative;
  backdrop-filter: blur(0.6rem);
}

.chapter-item.active {
  border-color: #00e6ff;
  background: linear-gradient(145deg, rgba(13, 25, 35, 0.9), rgba(25, 45, 65, 0.8));
  box-shadow:
      0 0 1rem rgba(0, 230, 255, 0.4),
      0 0.25rem 0.75rem rgba(0, 0, 0, 0.4),
      inset 0 0.05rem 0 rgba(0, 230, 255, 0.2);
}

.chapter-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background:
      radial-gradient(circle at 20% 80%, rgba(0, 255, 127, 0.08) 0%, transparent 50%),
      radial-gradient(circle at 80% 20%, rgba(0, 196, 255, 0.12) 0%, transparent 50%),
      radial-gradient(circle at 60% 40%, rgba(138, 43, 226, 0.06) 0%, transparent 60%);
  pointer-events: none;
  z-index: -1;
  border-radius: 0.4rem;
}

.chapter-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
  cursor: pointer;
  padding: 0.4rem 0;
  overflow: hidden;
}

.chapter-image-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 0;
}

.chapter-image-gradient {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
}

/* Gradient mask overlay */
.chapter-image-gradient::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to right, rgba(0, 0, 0, 0) 0%, rgba(13, 25, 35, 0.9) 100%);
}

/* Fallback gradient when no image is available */
.chapter-image-gradient:not([style*="background-image"]) {
  background: linear-gradient(to right,
    rgba(0, 196, 255, 0.2),
    rgba(0, 255, 127, 0.1),
    rgba(138, 43, 226, 0.05),
    transparent
  );
}

.chapter-container::before {
  content: '';
  position: absolute;
  height: 0.05rem;
  background: linear-gradient(90deg,
  transparent,
  rgba(0, 196, 255, 0.15),
  rgba(0, 255, 127, 0.1),
  rgba(0, 196, 255, 0.15),
  transparent
  );
  width: 100%;
  top: 50%;
  left: 0;
  z-index: 1; /* Above the image but below the text */
  box-shadow: 0 0 0.1rem rgba(0, 196, 255, 0.1);
  transition: all 0.3s ease;
}

.chapter-number-frame {
  position: relative;
  width: 3.2rem;
  height: 4rem;
  background: linear-gradient(145deg, #1a2a3a, #0d1825);
  border: 0.15rem solid #00c4ff;
  border-radius: 0.4rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow:
      0 0.3rem 0.8rem rgba(0, 0, 0, 0.6),
      inset 0 0.1rem 0.3rem rgba(0, 0, 0, 0.4),
      0 0 0.4rem rgba(0, 196, 255, 0.3);
  flex-shrink: 0;
  overflow: hidden;
  z-index: 2; /* Ensure it appears above the image */
}

.chapter-number-frame::before {
  content: '';
  position: absolute;
  top: 0.6rem;
  left: 0.5rem;
  right: 0.5rem;
  height: 0.1rem;
  background: linear-gradient(90deg,
  transparent,
  rgba(0, 255, 127, 0.8),
  rgba(0, 196, 255, 0.6),
  transparent
  );
  opacity: 0.8;
  box-shadow: 0 0 0.2rem rgba(0, 255, 127, 0.5);
}

.chapter-number-frame::after {
  content: '';
  position: absolute;
  top: 1rem;
  left: 0.6rem;
  right: 0.6rem;
  height: 0.05rem;
  background: linear-gradient(90deg,
  transparent,
  rgba(138, 43, 226, 0.6),
  transparent
  );
  opacity: 0.6;
}

.chapter-number {
  font-size: 1.4rem;
  font-weight: 700;
  color: #00f0ff;
  text-shadow:
      0 0 0.5rem rgba(0, 240, 255, 0.9),
      0 0 1rem rgba(0, 240, 255, 0.5),
      0.05rem 0.05rem 0.2rem rgba(0, 0, 0, 0.8);
  z-index: 2;
  font-family: var(--font-header);
  position: relative;
  filter: contrast(1.2) brightness(1.1);
}

.chapter-title {
  font-family: var(--font-header);
  font-size: 0.9rem;
  font-weight: 500;
  color: #b8e0ff;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  text-shadow:
      0.1rem 0.1rem 0.3rem rgba(0, 0, 0, 0.8),
      0 0 0.2rem rgba(184, 224, 255, 0.3);
  line-height: 1.1;
  position: relative;
  z-index: 2; /* Ensure it appears above the image */
}

.active .chapter-title {
  color: #00e6ff;
  text-shadow:
      0.1rem 0.1rem 0.3rem rgba(0, 0, 0, 0.8),
      0 0 0.4rem rgba(0, 230, 255, 0.6),
      0 0 0.8rem rgba(0, 230, 255, 0.3);
}

.chapter-container:hover .chapter-title {
  color: #20ffcc;
  text-shadow:
      0.1rem 0.1rem 0.3rem rgba(0, 0, 0, 0.8),
      0 0 0.3rem rgba(32, 255, 204, 0.5),
      0 0 0.6rem rgba(32, 255, 204, 0.3);
}

.chapter-container:hover::before {
  height: 0.08rem;
  background: linear-gradient(90deg,
  transparent,
  rgba(0, 196, 255, 0.35),
  rgba(0, 255, 127, 0.25),
  rgba(0, 196, 255, 0.35),
  transparent
  );
  box-shadow: 0 0 0.15rem rgba(0, 196, 255, 0.25);
}

.chapter-item.active .chapter-container::before {
  height: 0.1rem;
  background: linear-gradient(90deg,
  transparent,
  rgba(0, 230, 255, 0.6),
  rgba(0, 255, 127, 0.4),
  rgba(0, 230, 255, 0.6),
  transparent
  );
  box-shadow: 0 0 0.3rem rgba(0, 230, 255, 0.4);
}

.chapter-container:hover .chapter-number-frame {
  border-color: #00ff7f;
  box-shadow:
      0 0.3rem 0.8rem rgba(0, 0, 0, 0.6),
      inset 0 0.1rem 0.3rem rgba(0, 0, 0, 0.4),
      0 0 0.6rem rgba(0, 255, 127, 0.5);
}

.chapter-container:hover .chapter-number {
  color: #00ff7f;
  text-shadow:
      0 0 0.5rem rgba(0, 255, 127, 0.9),
      0 0 1rem rgba(0, 255, 127, 0.5),
      0.05rem 0.05rem 0.2rem rgba(0, 0, 0, 0.8);
  filter: contrast(1.3) brightness(1.2);
}

.chapter-quests {
  margin-top: 0.5rem;
  padding-left: 0.8rem;
  border-left: 0.1rem solid rgba(0, 196, 255, 0.4);
  box-shadow: -0.1rem 0 0.2rem rgba(0, 196, 255, 0.1);
  position: relative;
}

.chapter-quests::before {
  content: '';
  position: absolute;
  left: -0.05rem;
  top: 0;
  bottom: 0;
  width: 0.05rem;
  background: linear-gradient(180deg,
  rgba(0, 255, 127, 0.6),
  rgba(0, 196, 255, 0.6),
  rgba(138, 43, 226, 0.4)
  );
}

/* Responsive design */
@media (max-width: 768px) {
  .chapter-container {
    flex-direction: column;
    text-align: center;
    gap: 0.6rem;
    padding: 0.6rem 0;
  }

  .chapter-title {
    font-size: 0.8rem;
    letter-spacing: 0.08em;
  }

  .chapter-number-frame {
    width: 2.8rem;
    height: 3.5rem;
  }

  .chapter-number {
    font-size: 1.2rem;
  }

  .chapter-quests {
    padding-left: 0.5rem;
  }
}

/* Additional responsive design for smaller containers (30% width) */
@media (max-width: 480px), (max-width: 30vw) {
  .chapter-item {
    margin-bottom: 0.5rem;
    padding: 0.4rem;
    border-width: 0.05rem;
  }

  .chapter-container {
    gap: 0.5rem;
    padding: 0.3rem 0;
  }

  .chapter-number-frame {
    width: 2rem;
    height: 2.5rem;
    border-width: 0.1rem;
  }

  .chapter-number {
    font-size: 1rem;
  }

  .chapter-title {
    font-size: 0.7rem;
    letter-spacing: 0.05em;
  }

  .chapter-quests {
    margin-top: 0.3rem;
    padding-left: 0.4rem;
    border-left-width: 0.05rem;
  }
}

/* Additional animation for Flow energy effect */
@keyframes flowPulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

.chapter-item.active .chapter-number-frame::before {
  animation: flowPulse 2s ease-in-out infinite;
}
</style>