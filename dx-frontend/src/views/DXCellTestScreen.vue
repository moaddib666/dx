<script setup lang="ts">
import DXCell from "@/components/DXCell.vue";
import HeroBackground from "@/components/WhatIsIt/HeroBackground.vue";
</script>

<template>
  <HeroBackground id="dxcell-test-background"></HeroBackground>

  <div class="dxcell-test-screen">
    <!-- DXCell Test Section -->
    <div class="dxcell-test-section">
      <h2>DXCell Component Test</h2>
      <p>Testing DXCell component with different container sizes</p>

      <div class="dxcell-containers">
        <!-- 3rem x 3rem container (extra small) -->
        <div class="dxcell-container extra-small">
          <h3>3rem × 3rem</h3>
          <div class="dxcell-wrapper">
            <DXCell
              image="https://i.pinimg.com/564x/a6/f7/96/a6f796412fc85d6280054c26413a72ec.jpg"
              title="Tiny Card"
              subtitle="3REM CONTAINER"
            />
          </div>
        </div>

        <!-- 5rem x 5rem container (mid-small) -->
        <div class="dxcell-container mid-small">
          <h3>5rem × 5rem</h3>
          <div class="dxcell-wrapper">
            <DXCell
                image="https://i.pinimg.com/564x/a6/f7/96/a6f796412fc85d6280054c26413a72ec.jpg"
                title="Mid Small Card"
                subtitle="5REM CONTAINER"
            />
          </div>
        </div>

        <!-- 10rem x 10rem container -->
        <div class="dxcell-container small">
          <h3>10rem × 10rem</h3>
          <div class="dxcell-wrapper">
            <DXCell
              image="https://i.pinimg.com/564x/a6/f7/96/a6f796412fc85d6280054c26413a72ec.jpg"
              title="Small Card"
              subtitle="10REM CONTAINER"
            />
          </div>
        </div>

        <!-- 15rem x 15rem container -->
        <div class="dxcell-container medium">
          <h3>15rem × 15rem</h3>
          <div class="dxcell-wrapper">
            <DXCell
              image="https://i.pinimg.com/564x/a6/f7/96/a6f796412fc85d6280054c26413a72ec.jpg"
              title="Medium Card"
              subtitle="15REM CONTAINER"
            />
          </div>
        </div>

        <!-- 20rem x 20rem container -->
        <div class="dxcell-container large">
          <h3>20rem × 20rem</h3>
          <div class="dxcell-wrapper">
            <DXCell
              image="https://i.pinimg.com/564x/a6/f7/96/a6f796412fc85d6280054c26413a72ec.jpg"
              title="Large Card"
              subtitle="20REM CONTAINER"
            />
          </div>
        </div>

        <!-- Test with non-existent image -->
        <div class="dxcell-container medium">
          <h3>Error Placeholder Test</h3>
          <div class="dxcell-wrapper">
            <DXCell
              image="@/assets/images/non-existent-image.png"
              title="Missing Image"
              subtitle="ERROR PLACEHOLDER"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dxcell-test-screen {
  padding: 2em;
  display: flex;
  flex-direction: column;
  width: 100%;
  min-height: calc(100vh - 4em);
  align-items: center;
  justify-content: center;
}

#dxcell-test-background {
  background-image: url('@/assets/images/backgrounds/generic-background.png');
}

/* DXCell Test Section Styles */
.dxcell-test-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  border: 1px solid rgba(216, 187, 124, 0.3);
  max-width: 1200px;
  width: 100%;
}

.dxcell-test-section h2 {
  font-family: 'Cinzel', serif;
  font-size: 1.8rem;
  font-weight: 700;
  color: #fada95;
  margin-bottom: 0.5rem;
  text-align: center;
}

.dxcell-test-section p {
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  color: #ffffff;
  margin-bottom: 1.5rem;
  text-align: center;
}

.dxcell-containers {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  justify-content: center;
}

.dxcell-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.dxcell-container h3 {
  font-family: 'Cinzel', serif;
  font-size: 1.2rem;
  color: #d6b97b;
  margin-bottom: 0.5rem;
}

.dxcell-wrapper {

}

/* Container sizes */
.dxcell-container.extra-small .dxcell-wrapper {
  width: 3rem;
  height: 3rem;
}

.dxcell-container.small .dxcell-wrapper {
  width: 10rem;
  height: 10rem;
}

.dxcell-container.medium .dxcell-wrapper {
  width: 15rem;
  height: 15rem;
}

.dxcell-container.large .dxcell-wrapper {
  width: 20rem;
  height: 20rem;
}
.dxcell-container.mid-small .dxcell-wrapper {
  width: 5rem;
  height: 5rem;
}
</style>