<template>
  <div class="template-stats-radar-chart">
    <canvas ref="chartCanvas" :width="width" :height="height"></canvas>
  </div>
</template>

<script>
export default {
  name: 'TemplateStatsRadarChart',
  props: {
    stats: {
      type: Array,
      required: true
    },
    width: {
      type: Number,
      default: 80
    },
    height: {
      type: Number,
      default: 80
    }
  },
  data() {
    return {
      drawTimeout: null
    };
  },
  mounted() {
    this.drawChart();
  },
  beforeUnmount() {
    // Clear any pending draw operations
    if (this.drawTimeout) {
      clearTimeout(this.drawTimeout);
      this.drawTimeout = null;
    }
  },
  watch: {
    stats: {
      handler() {
        this.debouncedDrawChart();
      },
      deep: true
    }
  },
  methods: {
    debouncedDrawChart() {
      // Clear existing timeout
      if (this.drawTimeout) {
        clearTimeout(this.drawTimeout);
      }
      
      // Set new timeout for drawing
      this.drawTimeout = setTimeout(() => {
        this.drawChart();
        this.drawTimeout = null;
      }, 50); // Small delay to prevent excessive redraws
    },
    
    drawChart() {
      // Safety check: ensure component is still mounted
      if (!this.$refs.chartCanvas) return;
      
      const canvas = this.$refs.chartCanvas;
      if (!canvas || !canvas.parentNode) return;

      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      
      const centerX = this.width / 2;
      const centerY = this.height / 2;
      const radius = Math.min(this.width, this.height) * 0.35;

      // Clear canvas
      ctx.clearRect(0, 0, this.width, this.height);

      if (!this.stats || this.stats.length === 0) return;

      // Get max stat value for normalization
      const maxValue = Math.max(...this.stats.map(stat => stat.value), 10);
      const angleStep = (2 * Math.PI) / this.stats.length;

      // Draw background circle
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
      ctx.stroke();

      // Draw radar lines
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
      ctx.lineWidth = 0.5;
      for (let i = 0; i < this.stats.length; i++) {
        const angle = i * angleStep - Math.PI / 2;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(
          centerX + Math.cos(angle) * radius,
          centerY + Math.sin(angle) * radius
        );
        ctx.stroke();
      }

      // Draw stat polygon
      ctx.fillStyle = 'rgba(30, 144, 255, 0.3)';
      ctx.strokeStyle = 'rgba(30, 144, 255, 0.8)';
      ctx.lineWidth = 2;
      ctx.beginPath();

      for (let i = 0; i < this.stats.length; i++) {
        const angle = i * angleStep - Math.PI / 2;
        const normalizedValue = (this.stats[i].value / maxValue) * radius;
        const x = centerX + Math.cos(angle) * normalizedValue;
        const y = centerY + Math.sin(angle) * normalizedValue;

        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }

      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      // Draw stat points
      ctx.fillStyle = '#1E90FF';
      for (let i = 0; i < this.stats.length; i++) {
        const angle = i * angleStep - Math.PI / 2;
        const normalizedValue = (this.stats[i].value / maxValue) * radius;
        const x = centerX + Math.cos(angle) * normalizedValue;
        const y = centerY + Math.sin(angle) * normalizedValue;

        ctx.beginPath();
        ctx.arc(x, y, 2, 0, 2 * Math.PI);
        ctx.fill();
      }
    }
  }
};
</script>

<style scoped>
.template-stats-radar-chart {
  display: flex;
  align-items: center;
  justify-content: center;
}

canvas {
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.2);
}
</style>