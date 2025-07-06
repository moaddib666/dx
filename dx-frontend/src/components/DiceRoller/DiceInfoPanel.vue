<template>
  <div class="dice-info-panel">
    <h3 class="panel-title">🎲 Realistic D20 Roll</h3>
    
    <div class="info-content">
      <div class="info-item">
        <span class="bullet">•</span>
        <span>Choose target number (1‑20)</span>
      </div>
      
      <div class="info-item">
        <span class="bullet">•</span>
        <span>Load a texture to skin the dice</span>
      </div>
      
      <div class="info-item">
        <span class="bullet">•</span>
        <span>Click «Roll Dice» for realistic roll</span>
      </div>
      
      <div class="info-item">
        <span class="bullet">•</span>
        <span>Minimum 3.5s roll with natural settling</span>
      </div>
      
      <div class="info-item">
        <span class="bullet">•</span>
        <span>Guaranteed to land on your choice!</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DiceInfoPanel'
}
</script>

<style scoped>
.dice-info-panel {
  position: absolute;
  top: 10px;
  left: 10px;
  max-width: 300px;
  z-index: 100;
  background: rgba(0, 0, 0, 0.8);
  padding: 15px;
  border-radius: 5px;
  color: #fff;
  font-family: Arial, sans-serif;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.panel-title {
  margin: 0 0 15px 0;
  font-size: 18px;
  color: #00ffff;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.info-content {
  line-height: 1.6;
}

.info-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 8px;
  font-size: 14px;
}

.bullet {
  color: #00ffff;
  margin-right: 8px;
  margin-top: 2px;
  font-weight: bold;
}

.info-item span:last-child {
  flex: 1;
}

/* Responsive design */
@media (max-width: 768px) {
  .dice-info-panel {
    max-width: 250px;
    padding: 12px;
  }

  .panel-title {
    font-size: 16px;
  }

  .info-item {
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .dice-info-panel {
    position: relative;
    max-width: none;
    margin-bottom: 10px;
  }
}
</style>