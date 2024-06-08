<template>
  <div>
    <main class="faq">
      <TitleComponent>FAQ.</TitleComponent>
      <p>Find answers to the most frequently asked questions about Dimension-X.</p>
      <f-a-q></f-a-q>
    </main>
  </div>
</template>

<script>
import TitleComponent from '@/components/TitleComponent.vue';
import FAQ from '@/components/FAQ.vue';
export default {

  components: {
    FAQ,
    TitleComponent
  }
};
</script>

<style scoped>
.faq {
  padding: 60px;
  color: white;
}
</style>
