<template>
  <div class="item-icon-container">
    <img :src="itemData.item.icon" :alt="itemData.item.name" class="item-icon"
          :title="itemTitle"
    />
  </div>
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
  computed: {
    itemTitle() {
      return `${this.itemData.item.name} - ${this.itemData.item.type}`;
    },
  },
};
</script>

<style scoped>
/* Container for the icon and details */
.item-icon-container {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  width: 6em; /* Adjust icon container width */
  gap: 0.5em;
  text-align: center;
}

/* Icon Styling */
.item-icon {
  width: 2.5em;
  height: 2.5em;
  object-fit: contain;
  border: 0.1em solid rgba(255, 255, 255, 0.5); /* Border around the icon */
  border-radius: 0.3em; /* Rounded corners */
  transition: transform 0.2s ease, border-color 0.2s ease;
}


.item-type span {
  font-weight: bold;
  color: #fbc02d; /* Highlight for the type */
}

</style>
