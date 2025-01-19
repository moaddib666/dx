<template>
  <div class="inspection-result">
    <div
        class="character-card"
        v-for="(character, index) in characters"
        :key="character.id"
    >
      <!-- Character Info -->
      <div class="character-info">
        <div class="character-name">{{ character.name || "xx" }}</div>
        <div class="rank">
          Rank: <span class="rank-value">{{ character.rank_grade || "xx" }}</span>
        </div>
      </div>

      <!-- Attributes -->
      <div class="character-attributes">
        <div
            class="attribute"
            v-for="(attribute, index) in character.attributes || []"
            :key="index"
        >
          <span class="attribute-name">
            {{ attribute.name || "xx" }}:
          </span>
          <span class="attribute-value">
            {{ attribute.current !== undefined ? attribute.current : "xx" }}
            /
            {{ attribute.max !== undefined ? attribute.max : "xx" }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "InspectionResult",
  props: {
    characters: {
      type: Array,
      required: true, // Array of inspection results
    },
  },
};
</script>

<style scoped>
/* Container for the inspection results */
.inspection-result {
  display: flex;
  flex-wrap: wrap;
  gap: 1em; /* Space between cards */
  justify-content: flex-start;
}

/* Individual character card */
.character-card {
  display: flex;
  flex-direction: column;
  background-color: #2d2d2d; /* Dark gray background */
  border: 0.1em solid #4a4a4a; /* Subtle border */
  border-radius: 0.5em;
  padding: 1em;
  width: 14em; /* Fixed card width */
  box-sizing: border-box;
  text-align: left;
  color: #cfcfcf; /* Light gray text */
  font-size: 0.9em;
}

/* Character name */
.character-name {
  font-size: 1.1em;
  font-weight: bold;
  margin-bottom: 0.5em;
}

/* Rank */
.rank {
  font-size: 0.9em;
  color: #b0b0b0; /* Slightly lighter gray */
  margin-bottom: 0.5em;
}

.rank-value {
  font-weight: bold;
  color: #dcdcdc; /* Light gray for value */
}

/* Attributes container */
.character-attributes {
  display: flex;
  flex-direction: column;
  gap: 0.3em; /* Space between attributes */
}

/* Attribute row */
.attribute {
  display: flex;
  justify-content: space-between;
  font-size: 0.85em;
}

/* Attribute name */
.attribute-name {
  color: #b0b0b0; /* Slightly lighter gray for attribute name */
}

/* Attribute value */
.attribute-value {
  color: #cfcfcf; /* Light gray for values */
  font-weight: bold;
}
</style>
