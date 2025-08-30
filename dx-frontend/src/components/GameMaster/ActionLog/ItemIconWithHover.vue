<template>
    <img :src="itemData.item.icon" :alt="itemData.item.name" class="item-icon"
    />
</template>

<script>
export default {
  name: "ItemIcon",
  props: {
    itemData: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>

</style>
