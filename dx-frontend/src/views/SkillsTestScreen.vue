<script setup lang="ts">
import HeroBackground from "@/components/WhatIsIt/HeroBackground.vue";
import GMRPGSkills from "@/components/GameMaster/RPGSkills/GMRPGSkills.vue";
import CustomAction from "@/components/GameMaster/CustomAction/CustomAction.vue";
import GmCharSelector from "@/components/GameMaster/Character/GMCharSelector.vue";
import {OpenaiCharacter} from "@/api/dx-backend";
import {ref} from "vue";
import RPGButton from "@/components/RPGButton/RPGButton.vue";
import { ButtonType } from "@/types/ButtonType";

// Reactive state for component integration
const showCharSelector = ref(false);
const currentSelectionType = ref<'initiator' | 'target' | null>(null);
const selectedInitiator = ref<any>(undefined);
const selectedTarget = ref<any>(undefined);
const selectedAction = ref<any>(undefined);
const showSkillSelector = ref(false);

// Event handlers for CustomAction
const handleSelectInitiator = () => {
  currentSelectionType.value = 'initiator';
  showCharSelector.value = true;
};

const handleSelectTarget = () => {
  currentSelectionType.value = 'target';
  showCharSelector.value = true;
};

const handleSelectAction = () => {
  showSkillSelector.value = true;
};

// Event handlers for GmCharSelector
const handleCharacterSelected = (characterId: string) => {
  const character = characters.find(c => c.id === characterId);
  if (character) {
    const participant = {
      id: character.id,
      name: character.name,
      imageUrl: character.biography?.avatar
    };

    if (currentSelectionType.value === 'initiator') {
      selectedInitiator.value = participant;
    } else if (currentSelectionType.value === 'target') {
      selectedTarget.value = participant;
    }
  }

  showCharSelector.value = false;
  currentSelectionType.value = null;
};

// Event handlers for GMRPGSkills
const handleSkillSelected = (skill: any) => {
  // Transform skill to action format
  const action = {
    skillId: skill.id || skill.name, // Use skill ID or name as identifier
    name: skill.name,
    description: skill.description,
    school: skill.school,
    grade: skill.grade,
    type: skill.type
  };

  selectedAction.value = action;
  showSkillSelector.value = false;
};

// Close event handlers for selectors
const handleCharSelectorClose = () => {
  showCharSelector.value = false;
  currentSelectionType.value = null;
};

const handleSkillSelectorClose = () => {
  showSkillSelector.value = false;
};


const characters = [
  {
    "id": "000fb433-232c-4d22-88ea-e7055132f821",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "a71eada8-45f0-4fb7-aadd-c92442dad26e",
      "created_at": "2024-12-25T12:24:20.506000Z",
      "updated_at": "2024-12-25T12:24:20.506000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "000fb433-232c-4d22-88ea-e7055132f821"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caef9bef"
  },
  {
    "id": "0034cfa3-20d1-48f0-91fc-4d46f80937b2",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "93af04cf-753b-48b9-ad1b-d69a44b17ce8",
      "created_at": "2024-12-25T12:24:22.491000Z",
      "updated_at": "2024-12-25T12:24:22.492000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "0034cfa3-20d1-48f0-91fc-4d46f80937b2"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf8eca9"
  },
  {
    "id": "01ea7738-01cb-4d02-a110-f71b5f697dd1",
    "name": "Mercenary Hex 2",
    "biography": {
      "id": "613f71a7-7092-4517-bfec-a46b1d346316",
      "created_at": "2024-12-25T10:42:18.715000Z",
      "updated_at": "2024-12-25T10:44:32.318000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_2H4TrEw.PNG",
      "character": "01ea7738-01cb-4d02-a110-f71b5f697dd1"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae74146"
  },
  {
    "id": "029f8216-8489-40e6-9d4b-e6532262c031",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "648a31c8-491d-412c-ab96-a6cbb2b0ea77",
      "created_at": "2024-12-25T12:24:23.734000Z",
      "updated_at": "2024-12-25T12:24:23.734000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "029f8216-8489-40e6-9d4b-e6532262c031"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafe2ee9"
  },
  {
    "id": "02ace204-e28f-4f04-ae30-c496c0a9c79c",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "ff55ffb0-e5fa-48a6-bf5d-a85d1a6921da",
      "created_at": "2024-12-25T12:24:20.914000Z",
      "updated_at": "2024-12-25T12:24:20.915000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "02ace204-e28f-4f04-ae30-c496c0a9c79c"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf4fcb2"
  },
  {
    "id": "03048984-528c-449c-9d07-55775cd5feab",
    "name": "Zeus Prime 00 9",
    "biography": {
      "id": "91646732-aa9e-40df-af74-e1a3bb3e254a",
      "created_at": "2024-12-25T12:24:20.777000Z",
      "updated_at": "2024-12-25T12:24:20.777000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "03048984-528c-449c-9d07-55775cd5feab"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf10277"
  },
  {
    "id": "0434f6a0-f6d3-4132-93df-4ca3dd32c878",
    "name": "Zeus Prime 00 6",
    "biography": {
      "id": "4d917978-5384-4c5b-826f-063a931e8326",
      "created_at": "2024-12-25T12:24:22.237000Z",
      "updated_at": "2024-12-25T12:24:22.237000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "0434f6a0-f6d3-4132-93df-4ca3dd32c878"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf73fee"
  },
  {
    "id": "043fb782-d646-45a2-a977-fb0d84bc3477",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "a77a3e86-57d7-4adf-a975-79f29a1a0558",
      "created_at": "2024-12-25T12:24:20.394000Z",
      "updated_at": "2024-12-25T12:24:20.394000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "043fb782-d646-45a2-a977-fb0d84bc3477"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caed92aa"
  },
  {
    "id": "04de0ba0-3dc1-4e51-b76b-29372b8d2cfb",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "4c8999f9-9000-41fe-bc7b-cf4cc69bb7f3",
      "created_at": "2024-12-25T10:42:19.508000Z",
      "updated_at": "2024-12-25T10:44:32.329000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_B6zZ4NE.PNG",
      "character": "04de0ba0-3dc1-4e51-b76b-29372b8d2cfb"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeaa236"
  },
  {
    "id": "0552f559-417e-470c-b39d-33e22b396849",
    "name": "Mercenary Hex",
    "biography": {
      "id": "fdb03365-309d-41bf-aa7a-864120787596",
      "created_at": "2024-12-24T12:28:31.225000Z",
      "updated_at": "2024-12-25T10:44:32.342000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_4XcYbiz.PNG",
      "character": "0552f559-417e-470c-b39d-33e22b396849"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "0637a8a1-3449-46dd-839d-39ca66241281",
    "name": "Mercenary Hex 2",
    "biography": {
      "id": "b1b661e6-4caf-43d8-b1d7-0584ac410d7c",
      "created_at": "2024-12-25T10:42:19.830000Z",
      "updated_at": "2024-12-25T10:44:32.352000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_eEuNnjR.PNG",
      "character": "0637a8a1-3449-46dd-839d-39ca66241281"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb27a9"
  },
  {
    "id": "06db8b1f-77d7-4cbd-a9e9-ed7f81f2ea77",
    "name": "Zeus Prime 00 5",
    "biography": {
      "id": "a8010a0d-82f4-4a4a-be25-c218001cc892",
      "created_at": "2024-12-25T12:24:20.760000Z",
      "updated_at": "2024-12-25T12:24:20.761000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "06db8b1f-77d7-4cbd-a9e9-ed7f81f2ea77"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf10277"
  },
  {
    "id": "0702b75b-436d-4d7f-9c60-bb19e9f48381",
    "name": "Mercenary Hex 4",
    "biography": {
      "id": "933c5f14-fffb-456a-898e-7eac1363414f",
      "created_at": "2024-12-25T10:42:19.895000Z",
      "updated_at": "2024-12-25T10:44:32.361000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_KNPnPZh.PNG",
      "character": "0702b75b-436d-4d7f-9c60-bb19e9f48381"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "07a35be9-01fb-4a62-85b3-60d24e48f4c1",
    "name": "Selena Veilforge",
    "biography": {
      "id": "a1fa70d2-aa01-4fcf-a6a1-6004ce180806",
      "created_at": "2024-12-24T13:21:01.623000Z",
      "updated_at": "2024-12-24T13:24:27.417000Z",
      "age": 34,
      "gender": "Female",
      "background": "Selena Veilforge is a master of Flow manipulation, specializing in constructing intricate defensive barriers. Known for her calm demeanor and tactical mind, she has been a cornerstone in countless battles, shielding allies from devastating attacks. Her knowledge of protective magic has earned her the nickname 'The Unyielding Shield' among her peers.",
      "appearance": "A composed woman with silver-streaked black hair tied in a tight braid. Her glowing azure eyes reflect her deep connection to the Flow. She wears flowing robes laced with symbols of protection and strength.",
      "avatar": "http://localhost:8000/media/avatars/3723F324-8BE6-4FAB-AC22-E8D4C0B84C4E.PNG",
      "character": "07a35be9-01fb-4a62-85b3-60d24e48f4c1"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Flow Bender",
      "Defensive Mage",
      "Barrier Specialist"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "9fd27c2f-246d-4f37-86e7-645689cc9d39",
      "name": "Three of magitians (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeee519"
  },
  {
    "id": "07d9cf83-5ea5-4d65-a065-3c1fc2884ec6",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "9d6c1a15-b8c2-41a8-8eee-a14719c659cf",
      "created_at": "2024-12-25T12:24:20.518000Z",
      "updated_at": "2024-12-25T12:24:20.519000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "07d9cf83-5ea5-4d65-a065-3c1fc2884ec6"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caef9bef"
  },
  {
    "id": "08a7fff3-727a-4486-b5a5-8e3cfcc44514",
    "name": "Mercenary Hex 2",
    "biography": {
      "id": "aa093c8a-b983-47d6-b709-eb604141f065",
      "created_at": "2024-12-25T10:42:19.990000Z",
      "updated_at": "2024-12-25T10:44:32.370000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_tKSX8UO.PNG",
      "character": "08a7fff3-727a-4486-b5a5-8e3cfcc44514"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9e60"
  },
  {
    "id": "08ca0e0f-2a67-4276-895f-82f9f3111978",
    "name": "Dax Ironstride",
    "biography": {
      "id": "0d730df4-e356-420b-8375-2a7045c8ee1e",
      "created_at": "2024-12-24T12:21:08.683000Z",
      "updated_at": "2024-12-24T12:21:33.598000Z",
      "age": 28,
      "gender": "Other",
      "background": "Dax is a seasoned mercenary who takes on contracts for the highest bidder. Skilled in both ranged and close-quarters combat, he relies on his sharp instincts and combat prowess to survive. While not one to question his employers, he holds a firm code of loyalty to his squadmates.",
      "appearance": "A rugged, muscular figure with short black hair and a weathered face. He wears a durable combat vest and cargo pants, with a Flow-enhanced rifle slung across his back.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB.PNG",
      "character": "08ca0e0f-2a67-4276-895f-82f9f3111978"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Combat Specialist",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae9ac9b"
  },
  {
    "id": "08ee290b-3c26-4fc4-9fd1-7f98e05e9d41",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "89d21716-8195-4ff4-87e1-b71812757130",
      "created_at": "2024-12-25T12:24:21.504000Z",
      "updated_at": "2024-12-25T12:24:21.505000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "08ee290b-3c26-4fc4-9fd1-7f98e05e9d41"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf5b7c4"
  },
  {
    "id": "09518f61-4675-457e-bf4d-387daa1dcdbe",
    "name": "Mercenary Hex 3",
    "biography": {
      "id": "12bbaf72-0971-4d04-a981-a1967e546241",
      "created_at": "2024-12-25T10:42:19Z",
      "updated_at": "2024-12-25T10:44:32.378000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_yy3cE28.PNG",
      "character": "09518f61-4675-457e-bf4d-387daa1dcdbe"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae85d7a"
  },
  {
    "id": "09f7d96d-c5d5-478f-ae7f-add50cba1b7b",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "828efa73-30f3-4e9d-b6cf-0bf3928aec3e",
      "created_at": "2024-12-25T10:42:17.041000Z",
      "updated_at": "2024-12-25T10:44:32.385000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_93kkmbX.PNG",
      "character": "09f7d96d-c5d5-478f-ae7f-add50cba1b7b"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cada0c14"
  },
  {
    "id": "0a834f79-819c-4f8d-ab40-6745cbe9d2da",
    "name": "Zeus Prime 00 4",
    "biography": {
      "id": "5b7860a2-22fd-4be4-8d6f-82e2e971068f",
      "created_at": "2024-12-25T12:24:23.019000Z",
      "updated_at": "2024-12-25T12:24:23.019000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "0a834f79-819c-4f8d-ab40-6745cbe9d2da"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafdd31e"
  },
  {
    "id": "0b169d41-fa57-4b6e-a391-1da800f62f38",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "65396f69-8da5-440e-8e68-b4cd61d301ba",
      "created_at": "2024-12-25T12:24:22.918000Z",
      "updated_at": "2024-12-25T12:24:22.919000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "0b169d41-fa57-4b6e-a391-1da800f62f38"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafdd31e"
  },
  {
    "id": "0ba2f991-f726-4292-afd8-6157f7f55269",
    "name": "Zeus Prime 00 5",
    "biography": {
      "id": "2478b899-74bd-407b-b1a5-d7a8423ed87a",
      "created_at": "2024-12-25T12:24:23.871000Z",
      "updated_at": "2024-12-25T12:24:23.871000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "0ba2f991-f726-4292-afd8-6157f7f55269"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb0478be"
  },
  {
    "id": "0c1e1d9d-c74c-43d4-b32d-e948cd345ff2",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "93b14d48-22bd-46b2-a768-dbfcb932173d",
      "created_at": "2024-12-25T12:24:20.463000Z",
      "updated_at": "2024-12-25T12:24:20.463000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "0c1e1d9d-c74c-43d4-b32d-e948cd345ff2"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caee7c1a"
  },
  {
    "id": "0ca25ce8-7807-4de1-b964-d29c7b855cba",
    "name": "Mercenary Hex 2",
    "biography": {
      "id": "ad5259ee-94ff-470f-98b0-b575bd60f466",
      "created_at": "2024-12-25T10:42:19.047000Z",
      "updated_at": "2024-12-25T10:44:32.392000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_LJpVQH9.PNG",
      "character": "0ca25ce8-7807-4de1-b964-d29c7b855cba"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae8b665"
  },
  {
    "id": "0cbb4727-4a35-4776-9634-50bb46fd84be",
    "name": "Vito Ashenvale",
    "biography": {
      "id": "05f45219-75e5-40e5-b60d-e701218ee96d",
      "created_at": "2024-12-24T12:47:10.140000Z",
      "updated_at": "2024-12-24T12:47:44.062000Z",
      "age": 39,
      "gender": "Other",
      "background": "Victor Ashenvale is a top-tier adventurer, born into a family of wealth and prestige. Known for his tactical brilliance and mastery of Flow-enhanced combat, he combines skill, wit, and luxury in every mission. Despite his high-society upbringing, Victor has earned his reputation through relentless pursuit of perfection, often taking on missions deemed impossible.",
      "appearance": "A sophisticated figure with sharp, angular features and an air of confidence. He wears custom-tailored combat gear enhanced with cutting-edge Flow technology. An electric Flow cigarette often dangles from his lips, emitting faint, glowing vapor.",
      "avatar": "http://localhost:8000/media/avatars/EF720330-85DE-4412-8DF5-235575AC0AA8.PNG",
      "character": "0cbb4727-4a35-4776-9634-50bb46fd84be"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Elite Adventurer",
      "Flow Enhanced",
      "High Society"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": null,
    "position_id": "00000000-0000-0000-0000-0193cb04838e"
  },
  {
    "id": "0da1e8f9-a2b7-4a6b-9655-29644521ac8b",
    "name": "Mercenary Hex 2",
    "biography": {
      "id": "f950c6ce-06d4-4f56-91bf-64acdb02cada",
      "created_at": "2024-12-25T10:42:18.817000Z",
      "updated_at": "2024-12-25T10:44:32.401000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_7sLVHzf.PNG",
      "character": "0da1e8f9-a2b7-4a6b-9655-29644521ac8b"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae79d20"
  },
  {
    "id": "12d14243-dd91-448d-9903-0f852ac9adea",
    "name": "Finn Barrelstride",
    "biography": {
      "id": "20fcbb1f-7336-47f0-a63f-f4e7cf64cbf8",
      "created_at": "2024-12-24T11:32:24.423000Z",
      "updated_at": "2024-12-24T11:33:08.421000Z",
      "age": 33,
      "gender": "Other",
      "background": "Finn Barrelstride is a renowned adventurer who has traveled across dimensions and amassed both fame and treasures, including the legendary Amber of the Eternal. Known for his laid-back and jovial personality, Finn takes life as it comes, always ready for the next adventure. However, after a long night at the Misfits Pub, he’s content to rest, savor his beer, and tell exaggerated tales of his exploits to anyone willing to listen.",
      "appearance": "A slightly disheveled man with a carefree grin and a glint of mischief in his hazel eyes. His adventurer's gear is sleek and powered by glowing amber Flow energy, though it's worn casually and with little care. A tankard is always within reach, and his relaxed demeanor suggests he’s ready for anything—just not today.",
      "avatar": "http://localhost:8000/media/avatars/830FD57E-11E2-4369-BCF8-52A64577B3BC.PNG",
      "character": "12d14243-dd91-448d-9903-0f852ac9adea"
    },
    "npc": true,
    "rank": {
      "name": "Elite Mercenary",
      "grade": 5,
      "experience_needed": 14760
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 14761,
    "tags": [
      "Adventurer",
      "Drunken",
      "Power Gear"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": null,
    "position_id": "00000000-0000-0000-0000-0193cb15bc66"
  },
  {
    "id": "1b7aea79-b62a-44d1-b809-59ac36239c45",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "977df7af-300f-47e0-a8a1-2ed74481ac57",
      "created_at": "2024-12-25T12:24:23.667000Z",
      "updated_at": "2024-12-25T12:24:23.667000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "1b7aea79-b62a-44d1-b809-59ac36239c45"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafdff09"
  },
  {
    "id": "1c6dbbef-0d12-4264-b0f3-b7ab1ec76f1e",
    "name": "Zeus Prime 00 5",
    "biography": {
      "id": "9e010285-6629-44ce-9f5b-f4c4dce8b7a0",
      "created_at": "2024-12-25T12:24:23.752000Z",
      "updated_at": "2024-12-25T12:24:23.752000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "1c6dbbef-0d12-4264-b0f3-b7ab1ec76f1e"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafe2ee9"
  },
  {
    "id": "1d3dcd9c-e87a-4254-90b4-5695c4884c98",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "f15f529b-be0f-4c4c-beab-410727178d8d",
      "created_at": "2024-12-25T12:24:23.581000Z",
      "updated_at": "2024-12-25T12:24:23.582000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "1d3dcd9c-e87a-4254-90b4-5695c4884c98"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafdf1c3"
  },
  {
    "id": "1e67a9b6-684c-448d-926b-bbd3407e54eb",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "6767ed32-6ad8-4352-86a5-4914e31f8712",
      "created_at": "2024-12-25T12:24:22.930000Z",
      "updated_at": "2024-12-25T12:24:22.930000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "1e67a9b6-684c-448d-926b-bbd3407e54eb"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafdd31e"
  },
  {
    "id": "1ec54727-aa09-4ea7-83b8-8cf1f620c56a",
    "name": "Zane Crossblade",
    "biography": {
      "id": "88d0852e-0756-49b6-846e-b78eb99c6fe1",
      "created_at": "2024-12-24T12:34:21.175000Z",
      "updated_at": "2024-12-24T12:43:47.351000Z",
      "age": 34,
      "gender": "Other",
      "background": "Zane is a master swordsman known for his precision and deadly efficiency. While he prefers fighting solo, he values teamwork when missions require it.",
      "appearance": "A lean man with a focused gaze and a scar running down his cheek. His sword is always polished and ready for combat, gleaming with Flow energy.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_9X9DFVh.PNG",
      "character": "1ec54727-aa09-4ea7-83b8-8cf1f620c56a"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Swordsman",
      "Combat Specialist"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "20b302fd-f9ac-4263-9931-f3f20fab9586",
    "name": "Mercenary Hex 4",
    "biography": {
      "id": "c2521e06-1685-4386-81b9-089c29fe1867",
      "created_at": "2024-12-25T10:42:18.478000Z",
      "updated_at": "2024-12-25T10:44:32.437000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_jo4Qe8q.PNG",
      "character": "20b302fd-f9ac-4263-9931-f3f20fab9586"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cadbcb55"
  },
  {
    "id": "20c25242-650f-4bc1-aa6d-abe53a8f0036",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "04e1a153-2528-48d7-aea3-1b1e42ec41b3",
      "created_at": "2024-12-25T12:24:20.918000Z",
      "updated_at": "2024-12-25T12:24:20.918000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "20c25242-650f-4bc1-aa6d-abe53a8f0036"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf4fcb2"
  },
  {
    "id": "21c509e3-4fec-45b6-8139-b22a3f6f3556",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "18bc8195-b5ff-461f-be23-0f79b437bb42",
      "created_at": "2024-12-25T10:42:18.467000Z",
      "updated_at": "2024-12-25T10:44:32.445000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_hDi4iig.PNG",
      "character": "21c509e3-4fec-45b6-8139-b22a3f6f3556"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cadbcb55"
  },
  {
    "id": "2472ca09-de7f-43e5-be22-2ddfc8a18a46",
    "name": "Mercenary Hex 3",
    "biography": {
      "id": "9413503b-6897-4571-898e-f241db115a07",
      "created_at": "2024-12-25T10:42:19.050000Z",
      "updated_at": "2024-12-25T10:44:32.521000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_xpb8GUa.PNG",
      "character": "2472ca09-de7f-43e5-be22-2ddfc8a18a46"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae8b665"
  },
  {
    "id": "24ec4e20-6b84-47b9-9769-ef501cf7450d",
    "name": "Zeus Prime 00 8",
    "biography": {
      "id": "74c18c70-a2e9-414b-a1d8-95858682eff0",
      "created_at": "2024-12-25T12:24:21.627000Z",
      "updated_at": "2024-12-25T12:24:21.627000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "24ec4e20-6b84-47b9-9769-ef501cf7450d"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf5e8d7"
  },
  {
    "id": "254bee40-e0a1-4845-9843-95199914f112",
    "name": "Mercenary Hex 6",
    "biography": {
      "id": "84aa46f2-55ac-4f1d-9053-ba9f71532287",
      "created_at": "2024-12-25T10:42:18.904000Z",
      "updated_at": "2024-12-25T10:44:32.631000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_5k4xp9x.PNG",
      "character": "254bee40-e0a1-4845-9843-95199914f112"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae7d299"
  },
  {
    "id": "25974078-ebbe-484a-90ad-cc5ddad011cc",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "18c4ac8c-a7c2-4d90-8574-b94e773fce38",
      "created_at": "2024-12-25T12:24:23.700000Z",
      "updated_at": "2024-12-25T12:24:23.700000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "25974078-ebbe-484a-90ad-cc5ddad011cc"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafe22b9"
  },
  {
    "id": "26e9ad31-406f-4b83-ba1f-05d04bea6c52",
    "name": "Zeus Prime 00 7",
    "biography": {
      "id": "bc3f7029-bb40-4757-8e68-0ae8465d438c",
      "created_at": "2024-12-25T12:24:22.652000Z",
      "updated_at": "2024-12-25T12:24:22.653000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "26e9ad31-406f-4b83-ba1f-05d04bea6c52"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf924e2"
  },
  {
    "id": "27c4a738-3940-4cfd-9050-aaa41403b8a6",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "06f765b9-3bb2-485e-80f8-973c4f32526e",
      "created_at": "2024-12-25T10:42:18.580000Z",
      "updated_at": "2024-12-25T10:44:32.741000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_KwaaquI.PNG",
      "character": "27c4a738-3940-4cfd-9050-aaa41403b8a6"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cade1f26"
  },
  {
    "id": "27de3fb5-4458-4a90-b99a-960c553bb5dc",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "573ab0f2-72f8-4fc0-90a1-1744b39a4ae9",
      "created_at": "2024-12-25T10:42:19.987000Z",
      "updated_at": "2024-12-25T10:44:32.863000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_dYlUhqH.PNG",
      "character": "27de3fb5-4458-4a90-b99a-960c553bb5dc"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9e60"
  },
  {
    "id": "27ed4c60-18da-4b09-b26f-c99f0903f9e2",
    "name": "Mercenary Hex 2",
    "biography": {
      "id": "531eef8f-6aa2-4b69-a99c-6bcf4024611a",
      "created_at": "2024-12-25T10:42:20.460000Z",
      "updated_at": "2024-12-25T10:44:33.070000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_7XYlVg4.PNG",
      "character": "27ed4c60-18da-4b09-b26f-c99f0903f9e2"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caebb774"
  },
  {
    "id": "28f32279-105d-4dea-a898-fa911d989bcd",
    "name": "Mercenary Hex 8",
    "biography": {
      "id": "74b127b8-a663-41a7-9e08-81d474d07302",
      "created_at": "2024-12-25T10:42:18.911000Z",
      "updated_at": "2024-12-25T10:44:33.139000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_oZyAdsc.PNG",
      "character": "28f32279-105d-4dea-a898-fa911d989bcd"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae7d299"
  },
  {
    "id": "29163dbc-e3db-4971-889e-3a62ca09e007",
    "name": "Lysara Windsoul",
    "biography": {
      "id": "b65cb1b8-b254-417f-bf73-7e62191088bd",
      "created_at": "2024-12-24T10:32:58.269000Z",
      "updated_at": "2024-12-24T12:43:47.358000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born in the heart of the City of Memories, Lysara is a devoted follower of the Way of JSon. She is a master of the Heal School, using her Flow manipulation to mend wounds and inspire hope. Known for her compassion and wisdom, Lysara often guides novices on their first journeys.",
      "appearance": "A graceful figure with flowing silver hair and vibrant green eyes that seem to glow with an ethereal energy. She wears a robe adorned with shimmering Flow-infused symbols.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_GCZ5SYl.PNG",
      "character": "29163dbc-e3db-4971-889e-3a62ca09e007"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Way of JSon",
      "Flow Manipulator",
      "Healer"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "2932c242-c1c9-4b2c-b422-79a287bb23be",
    "name": "Zeus Prime 00 9",
    "biography": {
      "id": "d24c9152-ef3d-4645-af63-a3c05aa93b3f",
      "created_at": "2024-12-25T12:24:23.796000Z",
      "updated_at": "2024-12-25T12:24:23.796000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "2932c242-c1c9-4b2c-b422-79a287bb23be"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafe2ee9"
  },
  {
    "id": "2985b2ea-e826-4331-8e46-68154d7b3587",
    "name": "Mercenary Hex 7",
    "biography": {
      "id": "ddf9822f-0261-45b8-adae-1e7c00dcb9da",
      "created_at": "2024-12-25T10:42:18.172000Z",
      "updated_at": "2024-12-25T10:44:33.218000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_NrnodMu.PNG",
      "character": "2985b2ea-e826-4331-8e46-68154d7b3587"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cadbb206"
  },
  {
    "id": "2a1f0081-c4cc-4ed7-9970-95fa3be229c3",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "de01c2da-aa05-41ac-a6bc-4031151fc401",
      "created_at": "2024-12-25T12:24:20.896000Z",
      "updated_at": "2024-12-25T12:24:20.896000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "2a1f0081-c4cc-4ed7-9970-95fa3be229c3"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf4439d"
  },
  {
    "id": "2d881ab4-4ac4-48aa-874f-e68603f40d8f",
    "name": "Dr. Elias Thorne",
    "biography": {
      "id": "11d9f6d0-1ab2-4665-a066-b57ffaed7f48",
      "created_at": "2024-12-24T11:54:22.784000Z",
      "updated_at": "2024-12-27T21:47:25.497000Z",
      "age": 90,
      "gender": "Other",
      "background": "Dr. Elias Thorne is a renowned Flow scientist who has dedicated his life to uncovering the secrets of the Maze. As the leader of the Lost Researchers, he is driven to locate the archives containing knowledge about a powerful MacGuffin. His calculated and authoritative demeanor keeps the group focused despite the challenges of the Maze.",
      "appearance": "A tall, wiry man with sharp features and piercing green eyes. His tattered cloak and sturdy boots suggest a lifetime of expeditions, while the numerous Flow-infused gadgets hanging from his belt display his expertise.",
      "avatar": "http://localhost:8000/media/avatars/02218D37-0E7A-4E7B-8B55-15EB4109D00E.PNG",
      "character": "2d881ab4-4ac4-48aa-874f-e68603f40d8f"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Lost Researchers",
      "Leader",
      "Flow Expert"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f5bc6dd1-f08d-49eb-88a0-f4099a7db09a",
      "name": "Free Archive Seekers (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cad941a0"
  },
  {
    "id": "2e37b079-6705-4863-b8ea-bfdbff04ba6b",
    "name": "Mercenary Hex 5",
    "biography": {
      "id": "e4583301-62f1-4a58-af0d-092f84ef68b8",
      "created_at": "2024-12-25T10:42:19.999000Z",
      "updated_at": "2024-12-25T10:44:33.327000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_M0KAROV.PNG",
      "character": "2e37b079-6705-4863-b8ea-bfdbff04ba6b"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9e60"
  },
  {
    "id": "2e74e754-ccf5-41e0-8a0e-e9615b454247",
    "name": "Zeus Prime 00 6",
    "biography": {
      "id": "008bc657-9beb-4d24-bf6e-1db675dc61f4",
      "created_at": "2024-12-25T12:24:22.625000Z",
      "updated_at": "2024-12-25T12:24:22.625000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "2e74e754-ccf5-41e0-8a0e-e9615b454247"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf924e2"
  },
  {
    "id": "2f47d11a-65ae-40af-9782-5164a4ecfdde",
    "name": "Zeus Prime 00 4",
    "biography": {
      "id": "78905d09-160e-4681-bf0f-f72ab89c27df",
      "created_at": "2024-12-25T12:24:22.495000Z",
      "updated_at": "2024-12-25T12:24:22.495000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "2f47d11a-65ae-40af-9782-5164a4ecfdde"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf8eca9"
  },
  {
    "id": "2f57d21a-1541-4942-a167-a14a6d63f38e",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "2df460fc-e91c-4f3d-9598-7d7c415dbf4c",
      "created_at": "2024-12-25T12:24:20.810000Z",
      "updated_at": "2024-12-25T12:24:20.810000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "2f57d21a-1541-4942-a167-a14a6d63f38e"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf1a4de"
  },
  {
    "id": "2f8baa58-54f8-4145-af3a-c046d74fbe4d",
    "name": "Mercenary Hex 3",
    "biography": {
      "id": "c8120ab4-7915-49de-b267-d43faddad793",
      "created_at": "2024-12-25T10:42:18.892000Z",
      "updated_at": "2024-12-25T10:44:33.477000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_p0lXFq3.PNG",
      "character": "2f8baa58-54f8-4145-af3a-c046d74fbe4d"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae7d299"
  },
  {
    "id": "2fbb6939-bbf3-4f05-99af-30f9e0d010ac",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "aa850067-68b1-490c-a49c-0eab02a7ab1a",
      "created_at": "2024-12-25T12:24:20.481000Z",
      "updated_at": "2024-12-25T12:24:20.482000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "2fbb6939-bbf3-4f05-99af-30f9e0d010ac"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caef4ba0"
  },
  {
    "id": "30aef0c0-0d39-48c8-89ca-aaf1fe47b479",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "fba52632-573c-4c5f-95f0-5300c6ed1afe",
      "created_at": "2024-12-25T12:24:23.654000Z",
      "updated_at": "2024-12-25T12:24:23.655000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "30aef0c0-0d39-48c8-89ca-aaf1fe47b479"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafdff09"
  },
  {
    "id": "3122a995-d6c8-4075-b1d3-cdc30ae9aa58",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "94d5b241-6698-473f-a548-0d4290a1da0f",
      "created_at": "2024-12-25T12:24:20.417000Z",
      "updated_at": "2024-12-25T12:24:20.417000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "3122a995-d6c8-4075-b1d3-cdc30ae9aa58"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caee229f"
  },
  {
    "id": "33379066-ad67-48cd-af09-e5cb98bf1048",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "b0f11b9d-af11-45a4-b49c-183c1bf16493",
      "created_at": "2024-12-25T12:24:20.441000Z",
      "updated_at": "2024-12-25T12:24:20.441000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "33379066-ad67-48cd-af09-e5cb98bf1048"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caee42a7"
  },
  {
    "id": "33f1f59c-69f3-4493-b360-fa781ee4c1be",
    "name": "Mercenary Hex 5",
    "biography": {
      "id": "1cb49e00-41cd-4488-b9d8-5c088481ca2a",
      "created_at": "2024-12-25T10:42:18.483000Z",
      "updated_at": "2024-12-25T10:44:34.036000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_WnS9zub.PNG",
      "character": "33f1f59c-69f3-4493-b360-fa781ee4c1be"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cadbcb55"
  },
  {
    "id": "34d73dd3-98fb-4368-83d5-b9d0eae1d672",
    "name": "Zeus Prime 00 9",
    "biography": {
      "id": "232ba743-3af6-4524-8750-1501a2b27187",
      "created_at": "2024-12-25T12:24:23.330000Z",
      "updated_at": "2024-12-25T12:24:23.330000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "34d73dd3-98fb-4368-83d5-b9d0eae1d672"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafdd31e"
  },
  {
    "id": "34e951c7-c48e-4d7b-b55f-4a5d5e7731d2",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "d5b7f5ff-a010-4e01-848a-530941e83a4a",
      "created_at": "2024-12-25T12:24:22.925000Z",
      "updated_at": "2024-12-25T12:24:22.925000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "34e951c7-c48e-4d7b-b55f-4a5d5e7731d2"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafdd31e"
  },
  {
    "id": "35c4e57b-1d1a-4858-a56c-cd0d874d3f94",
    "name": "Zeus Prime 00 4",
    "biography": {
      "id": "9c35723e-cb8d-40fc-b209-cdbc5cfe9500",
      "created_at": "2024-12-25T12:24:21.479000Z",
      "updated_at": "2024-12-25T12:24:21.479000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "35c4e57b-1d1a-4858-a56c-cd0d874d3f94"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf51a85"
  },
  {
    "id": "35da0f23-2ecc-4425-9fe2-ed11e832e4d6",
    "name": "Zeus Prime 00 5",
    "biography": {
      "id": "e8fc4436-8637-4d52-b48f-c111459dd829",
      "created_at": "2024-12-25T12:24:21.483000Z",
      "updated_at": "2024-12-25T12:24:21.484000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "35da0f23-2ecc-4425-9fe2-ed11e832e4d6"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf51a85"
  },
  {
    "id": "36603634-fca3-4741-afda-72022fd5df2e",
    "name": "Mercenary Hex 7",
    "biography": {
      "id": "448b1a20-d34e-495b-a8c8-eaf3dd380bd4",
      "created_at": "2024-12-25T10:42:19.953000Z",
      "updated_at": "2024-12-25T10:44:34.218000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_XQLvOZ0.PNG",
      "character": "36603634-fca3-4741-afda-72022fd5df2e"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "37698269-ba4e-4922-89da-5a6f6dc83f3d",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "bae220e6-1141-4c9e-ba0d-66518edb6892",
      "created_at": "2024-12-25T12:24:22.934000Z",
      "updated_at": "2024-12-25T12:24:22.935000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "37698269-ba4e-4922-89da-5a6f6dc83f3d"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafdd31e"
  },
  {
    "id": "379f0ab4-4e1b-46bd-bae8-8e097d3160d0",
    "name": "Mercenary Hex 6",
    "biography": {
      "id": "ed3a8582-fd9f-44cb-96e5-a45437d0228d",
      "created_at": "2024-12-25T10:42:19.843000Z",
      "updated_at": "2024-12-25T10:44:34.331000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_9Gya1sD.PNG",
      "character": "379f0ab4-4e1b-46bd-bae8-8e097d3160d0"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb27a9"
  },
  {
    "id": "3ba03dcc-67ec-4b8d-b19e-2cf1e4f5c3db",
    "name": "Zeus Prime 00 4",
    "biography": {
      "id": "69d2a89b-e07c-4214-b54a-8f74359dc080",
      "created_at": "2024-12-25T12:24:20.595000Z",
      "updated_at": "2024-12-25T12:24:20.596000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "3ba03dcc-67ec-4b8d-b19e-2cf1e4f5c3db"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf00f84"
  },
  {
    "id": "3c2a318b-c4f2-496b-a1de-deb44e51a239",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "89ed561e-67bd-4d23-a8cb-b1b80dec090a",
      "created_at": "2024-12-25T12:24:22.782000Z",
      "updated_at": "2024-12-25T12:24:22.782000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "3c2a318b-c4f2-496b-a1de-deb44e51a239"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafaa0ee"
  },
  {
    "id": "3cfb80c8-13a4-47a9-8a12-d9548ad6c073",
    "name": "Zeus Prime 00 7",
    "biography": {
      "id": "4d08d30f-3ba3-4e39-bf6a-c72d7c5ed3e2",
      "created_at": "2024-12-25T12:24:20.939000Z",
      "updated_at": "2024-12-25T12:24:20.939000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "3cfb80c8-13a4-47a9-8a12-d9548ad6c073"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf4fcb2"
  },
  {
    "id": "3d0764af-828e-454f-9761-2c2b4a4ad335",
    "name": "Jarek Bloodfang",
    "biography": {
      "id": "4ad529fa-16ff-46b4-abc3-d4c47f2fb409",
      "created_at": "2024-12-24T12:30:15.616000Z",
      "updated_at": "2024-12-24T12:43:47.363000Z",
      "age": 31,
      "gender": "Other",
      "background": "Jarek thrives in the heat of battle, using his raw strength and fury to overwhelm opponents. While he lacks tactical finesse, his ability to charge into danger and survive makes him invaluable in chaotic skirmishes.",
      "appearance": "A towering figure with tribal tattoos across his arms and a wild mane of black hair. His armor is battered but functional, and his twin axes gleam with recent use.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_KJVlMxC.PNG",
      "character": "3d0764af-828e-454f-9761-2c2b4a4ad335"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Berserker",
      "Close Combat Specialist"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "3df5e7d2-3f06-40e2-b37c-a04be84a5502",
    "name": "Zeus Prime 00 8",
    "biography": {
      "id": "6c47980a-d510-452b-8dc1-b81bbf5fff4d",
      "created_at": "2024-12-25T12:24:20.611000Z",
      "updated_at": "2024-12-25T12:24:20.611000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "3df5e7d2-3f06-40e2-b37c-a04be84a5502"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf00f84"
  },
  {
    "id": "3dff6759-c8e0-4308-9b72-27a88409cfd5",
    "name": "Rynak",
    "biography": {
      "id": "7ffd0495-654b-4b5c-b305-51914813d175",
      "created_at": "2024-12-25T09:45:18.186000Z",
      "updated_at": "2024-12-25T09:48:42.531000Z",
      "age": 18,
      "gender": "Other",
      "background": "Rynak was once an ordinary creature in the underbelly of the City of Memories, until an accidental exposure to a concentrated Flow nexus transformed it. Now imbued with intelligence and mystical abilities, Rynak roams the city, seeking out secrets and whispering cryptic warnings to those who cross its path.",
      "appearance": "A sleek rat-like creature with glowing blue veins of Flow energy running across its fur. Its eyes shimmer with a faint luminescent glow, and its tail emits a subtle hum of power. It moves with an unnaturally fluid grace, blending seamlessly into shadows.",
      "avatar": "http://localhost:8000/media/avatars/36DC1C4C-F827-4B75-85D8-7399434A86E7.webp",
      "character": "3dff6759-c8e0-4308-9b72-27a88409cfd5"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Flow-Touched",
      "Rat",
      "Mystical"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": null,
    "position_id": "00000000-0000-0000-0000-0193cada027a"
  },
  {
    "id": "3f287e0a-4612-4cc5-9498-004d9c2eef2d",
    "name": "Mercenary Hex 3",
    "biography": {
      "id": "58042af3-43e4-4b17-b6db-432d3667df78",
      "created_at": "2024-12-25T10:42:18.718000Z",
      "updated_at": "2024-12-25T10:44:34.580000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_24zdArT.PNG",
      "character": "3f287e0a-4612-4cc5-9498-004d9c2eef2d"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae74146"
  },
  {
    "id": "3f32c73d-480b-48f7-b24d-d004ee7c43a4",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "ff7f2e40-9583-4f72-a3f4-e7cf8fc9cfb5",
      "created_at": "2024-12-25T12:24:21.587000Z",
      "updated_at": "2024-12-25T12:24:21.587000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "3f32c73d-480b-48f7-b24d-d004ee7c43a4"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf5e8d7"
  },
  {
    "id": "3f3d0281-5a03-461f-a85e-b091c2a0d1de",
    "name": "Mercenary Hex 3",
    "biography": {
      "id": "747d71ec-4d7a-4e70-b5c0-47139db398d1",
      "created_at": "2024-12-25T10:42:19.993000Z",
      "updated_at": "2024-12-25T10:44:34.630000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_V6g1xZI.PNG",
      "character": "3f3d0281-5a03-461f-a85e-b091c2a0d1de"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9e60"
  },
  {
    "id": "3f9c91ef-75f6-4b2b-b303-0a9aeaf24f85",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "3a7d87b1-18a8-46c2-b34c-d17d3ffbbe32",
      "created_at": "2024-12-25T12:24:23.846000Z",
      "updated_at": "2024-12-25T12:24:23.846000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "3f9c91ef-75f6-4b2b-b303-0a9aeaf24f85"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb03a283"
  },
  {
    "id": "40c0bbcc-d5fc-4ca0-8d5e-3c3334986c22",
    "name": "Kael Vortex",
    "biography": {
      "id": "5a864055-8519-460a-b599-97ae6f947795",
      "created_at": "2024-12-24T11:49:24.956000Z",
      "updated_at": "2024-12-24T11:49:55.397000Z",
      "age": 50,
      "gender": "Other",
      "background": "Once a respected Flow Guardian, Kael Vortex was tasked with protecting the Maze—a labyrinth said to hold secrets of the Flow. During his duty, he encountered a creature of unimaginable power and was cursed, leaving him disoriented and unstable. While his mind is fractured, his magical prowess remains intact, making him a near-unstoppable force within the Maze. Few dare approach him, as even elite forces have failed to subdue him.",
      "appearance": "A gaunt, disheveled figure with wild, unkempt hair and eyes that glow unnaturally with the colors of the Flow. His tattered robes are adorned with shifting runes and symbols that pulse with chaotic energy. His body is scarred, and the air around him crackles with an unsettling power.",
      "avatar": "http://localhost:8000/media/avatars/F3FECD59-722D-4F78-A623-E1F9464C61F8.PNG",
      "character": "40c0bbcc-d5fc-4ca0-8d5e-3c3334986c22"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Maze Flow Guardian",
      "Cursed Mage",
      "Insane"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "0168061a-8a88-4e79-b73c-6f46c3a6c5c7",
      "name": "Flow Guardians (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf04268"
  },
  {
    "id": "4162aa61-9428-4a06-8a70-3a8c07247cdb",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "579bc22c-5cc4-4b1e-b2d8-e46d018d5c4a",
      "created_at": "2024-12-25T12:24:21.593000Z",
      "updated_at": "2024-12-25T12:24:21.593000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "4162aa61-9428-4a06-8a70-3a8c07247cdb"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf5e8d7"
  },
  {
    "id": "41db1a1c-290b-4458-ae94-313b776b8abc",
    "name": "Mercenary Hex 3",
    "biography": {
      "id": "1eb16df9-0817-4fe0-ac5d-2e745e0a98fd",
      "created_at": "2024-12-25T10:42:19.833000Z",
      "updated_at": "2024-12-25T10:44:34.751000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_FXWEbNJ.PNG",
      "character": "41db1a1c-290b-4458-ae94-313b776b8abc"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb27a9"
  },
  {
    "id": "42700939-fe94-4c66-abf5-bcea86671db4",
    "name": "Zeus Prime 00 4",
    "biography": {
      "id": "2f6926a5-1fa5-45b2-99ef-f80e9dd6f083",
      "created_at": "2024-12-25T12:24:20.930000Z",
      "updated_at": "2024-12-25T12:24:20.930000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "42700939-fe94-4c66-abf5-bcea86671db4"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf4fcb2"
  },
  {
    "id": "42a7e10e-893b-4c86-afac-4950e0cf3fad",
    "name": "Mercenary Hex 2",
    "biography": {
      "id": "de5a3207-8301-46e5-8240-ec974ff01edb",
      "created_at": "2024-12-25T10:42:17.725000Z",
      "updated_at": "2024-12-25T10:44:34.830000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_Akn4nCe.PNG",
      "character": "42a7e10e-893b-4c86-afac-4950e0cf3fad"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cadbb206"
  },
  {
    "id": "4495304c-7b7c-4bee-824f-e9a3a2da706f",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "c368856a-325e-4325-b49d-307fb01eb9a1",
      "created_at": "2024-12-25T10:42:20.817000Z",
      "updated_at": "2024-12-25T10:44:34.945000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_TGEt3Gn.PNG",
      "character": "4495304c-7b7c-4bee-824f-e9a3a2da706f"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf67c98"
  },
  {
    "id": "4567c7d4-dbbe-400e-ac86-5f18581ea7b6",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "41e8325c-48fb-4826-abaf-ad2d8b7f69d4",
      "created_at": "2024-12-25T10:42:16.974000Z",
      "updated_at": "2024-12-25T10:44:35.102000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_9wEfj3m.PNG",
      "character": "4567c7d4-dbbe-400e-ac86-5f18581ea7b6"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cad9bfe5"
  },
  {
    "id": "46a4afc4-21d8-4cdd-ae47-a959f1db24a1",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "9fa8efb6-4a93-4e00-8d0b-d394bb4c6ea4",
      "created_at": "2024-12-25T10:42:20.813000Z",
      "updated_at": "2024-12-25T10:44:35.307000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_r7yXrcE.PNG",
      "character": "46a4afc4-21d8-4cdd-ae47-a959f1db24a1"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf67c98"
  },
  {
    "id": "470a5f89-ca3c-44f3-8d5f-1ce83b1398a8",
    "name": "Zeus Prime 00 5",
    "biography": {
      "id": "0a1f4ac4-0260-4d17-895b-8d85479c2dcb",
      "created_at": "2024-12-25T12:24:20.933000Z",
      "updated_at": "2024-12-25T12:24:20.933000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "470a5f89-ca3c-44f3-8d5f-1ce83b1398a8"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf4fcb2"
  },
  {
    "id": "47795629-7bf8-4586-92c5-fcbf17c53cb9",
    "name": "Zeus Prime 00 7",
    "biography": {
      "id": "0a0d0a23-3c38-4cbf-91cb-2890a6c636c6",
      "created_at": "2024-12-25T12:24:20.831000Z",
      "updated_at": "2024-12-25T12:24:20.831000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "47795629-7bf8-4586-92c5-fcbf17c53cb9"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf1a4de"
  },
  {
    "id": "47bc25a8-130a-4d8d-8be2-6e0d42ba15af",
    "name": "Zeus Prime 00 8",
    "biography": {
      "id": "54eaa46c-015f-45d3-80e5-0d3e742eccff",
      "created_at": "2024-12-25T12:24:20.989000Z",
      "updated_at": "2024-12-25T12:24:20.989000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "47bc25a8-130a-4d8d-8be2-6e0d42ba15af"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf4fcb2"
  },
  {
    "id": "4caea1b3-641e-435d-a269-9b1ce2b22abc",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "1954dfb4-bdc5-4ec3-83ee-8be69a27436f",
      "created_at": "2024-12-25T10:42:17.580000Z",
      "updated_at": "2024-12-25T10:44:35.593000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_Qfjhs34.PNG",
      "character": "4caea1b3-641e-435d-a269-9b1ce2b22abc"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cadbb206"
  },
  {
    "id": "4e19003a-54a7-4bf8-bcff-c0f212cc71eb",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "8de2510a-156c-490e-9f0f-daa6982b98bc",
      "created_at": "2024-12-25T12:24:20.551000Z",
      "updated_at": "2024-12-25T12:24:20.552000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "4e19003a-54a7-4bf8-bcff-c0f212cc71eb"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf00f84"
  },
  {
    "id": "4e6f4eb2-f35d-431d-b8be-ecf577f3e8fe",
    "name": "Zeus Prime 00 5",
    "biography": {
      "id": "ed75429d-6871-4e22-bfdf-aff2b60f88dd",
      "created_at": "2024-12-25T12:24:22.499000Z",
      "updated_at": "2024-12-25T12:24:22.499000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "4e6f4eb2-f35d-431d-b8be-ecf577f3e8fe"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf8eca9"
  },
  {
    "id": "4ea8a4d9-fe95-4bef-8762-646ef5f8c14a",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "52b6e968-795f-42cd-a6df-80bb6ae20c68",
      "created_at": "2024-12-25T12:24:21.877000Z",
      "updated_at": "2024-12-25T12:24:21.878000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "4ea8a4d9-fe95-4bef-8762-646ef5f8c14a"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf73fee"
  },
  {
    "id": "4ecc6fa5-acee-4ebf-9f0c-f383b67f03c6",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "f93f0c57-81fb-43f4-96bc-9362556b5f5c",
      "created_at": "2024-12-25T10:42:18.577000Z",
      "updated_at": "2024-12-25T10:44:35.781000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_2VTI1me.PNG",
      "character": "4ecc6fa5-acee-4ebf-9f0c-f383b67f03c6"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cade1f26"
  },
  {
    "id": "4f024ea4-0025-4d6b-9003-e002641c190c",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "27b392e2-2325-461b-ab14-77292bf3ea45",
      "created_at": "2024-12-25T10:42:17.535000Z",
      "updated_at": "2024-12-25T10:44:35.793000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_SoO8OdD.PNG",
      "character": "4f024ea4-0025-4d6b-9003-e002641c190c"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cadbb206"
  },
  {
    "id": "4fa59aa6-988e-439d-b06a-49477308696d",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "66e1e338-11c2-49f8-b0f6-cde3a5514af7",
      "created_at": "2024-12-25T12:24:20.460000Z",
      "updated_at": "2024-12-25T12:24:20.460000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "4fa59aa6-988e-439d-b06a-49477308696d"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caee7c1a"
  },
  {
    "id": "4fe52248-bc05-4daa-967d-d0148c82a93f",
    "name": "Thane Ironmaw",
    "biography": {
      "id": "12def6c2-b6c7-4304-afa9-41e5c1d0c556",
      "created_at": "2024-12-24T12:31:08.244000Z",
      "updated_at": "2024-12-24T12:43:47.366000Z",
      "age": 35,
      "gender": "Other",
      "background": "Thane is the squad’s heavy gunner, specializing in suppressive fire and crowd control. His imposing presence and firepower make him a key asset in larger battles.",
      "appearance": "A massive, broad-shouldered man with a thick beard and a gravelly voice. He carries a heavy Flow-powered machine gun and wears reinforced armor covered in scorch marks.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_RxZ91Io.PNG",
      "character": "4fe52248-bc05-4daa-967d-d0148c82a93f"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Heavy Gunner",
      "Hired Muscle"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "50151525-1038-41ff-aaac-0e8d314464e4",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "7dde1219-02fe-4690-8885-4d9318f3410b",
      "created_at": "2024-12-25T12:24:20.514000Z",
      "updated_at": "2024-12-25T12:24:20.515000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "50151525-1038-41ff-aaac-0e8d314464e4"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caef9bef"
  },
  {
    "id": "50573440-1d3a-4e2d-8ee6-4e9aed3d9894",
    "name": "Zeus Prime 00 7",
    "biography": {
      "id": "97bb3a42-1f09-453f-ab5b-c6bb22345e92",
      "created_at": "2024-12-25T12:24:20.767000Z",
      "updated_at": "2024-12-25T12:24:20.768000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "50573440-1d3a-4e2d-8ee6-4e9aed3d9894"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf10277"
  },
  {
    "id": "50a522e7-2711-4829-97c8-23290deb82af",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "ae5a5a4f-1323-4d86-aa2b-3ec3b5906fd0",
      "created_at": "2024-12-25T10:42:19.828000Z",
      "updated_at": "2024-12-25T10:44:35.936000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_qW9TOIk.PNG",
      "character": "50a522e7-2711-4829-97c8-23290deb82af"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb27a9"
  },
  {
    "id": "50a99542-28bb-4867-9d8d-b2eec7a47020",
    "name": "Ember Flareheart",
    "biography": {
      "id": "d9c13755-bbcd-45c7-9bcb-00b2520a04c8",
      "created_at": "2024-12-24T12:52:00.556000Z",
      "updated_at": "2024-12-24T12:53:54.635000Z",
      "age": 25,
      "gender": "Other",
      "background": "Ember Flareheart discovered her affinity for fire magic at an early age when she accidentally summoned a blaze that engulfed her village. Determined to master her powers and prevent further harm, she studied under some of the greatest Fire Mages in the realms. Her fierce determination and innate talent have made her a formidable mage, known for her raw power and passionate spirit.",
      "appearance": "A slender woman with fiery red hair that seems to shimmer like flames in the light. Her amber eyes burn with intensity, and she wears a flowing robe adorned with intricate patterns of embers and flames.",
      "avatar": "http://localhost:8000/media/avatars/F2437B11-E520-402F-AD68-98970D29117D.PNG",
      "character": "50a99542-28bb-4867-9d8d-b2eec7a47020"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Fire Mage",
      "Flow Manipulator",
      "Prodigy"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": null,
    "position_id": "00000000-0000-0000-0000-0193cb0478be"
  },
  {
    "id": "50e3b3b6-e230-47c8-972a-08a9551a083d",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "30d29f75-d579-4336-bbbd-f4c59cd23eae",
      "created_at": "2024-12-25T10:42:19.452000Z",
      "updated_at": "2024-12-25T10:44:36.026000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_9XsETDf.PNG",
      "character": "50e3b3b6-e230-47c8-972a-08a9551a083d"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caea9038"
  },
  {
    "id": "526d89ac-5251-45e4-917f-514e508e4397",
    "name": "Mercenary Hex 3",
    "biography": {
      "id": "db726956-92c3-4d52-b445-550d5e3bfc1d",
      "created_at": "2024-12-25T10:42:18.475000Z",
      "updated_at": "2024-12-25T10:44:36.191000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_X6jhAkb.PNG",
      "character": "526d89ac-5251-45e4-917f-514e508e4397"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cadbcb55"
  },
  {
    "id": "52c87952-7c9b-4738-aa69-5f744fe681fb",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "7c112fb8-faa6-4b07-9ef3-04a38baf3956",
      "created_at": "2024-12-25T10:42:19.812000Z",
      "updated_at": "2024-12-25T10:44:36.340000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_1WWLNEB.PNG",
      "character": "52c87952-7c9b-4738-aa69-5f744fe681fb"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb17aa"
  },
  {
    "id": "53f25ae0-a479-4c25-b38c-87398b311d3b",
    "name": "Mercenary Hex 5",
    "biography": {
      "id": "8fd58a87-2a6f-4521-abd0-de4d7437f219",
      "created_at": "2024-12-25T10:42:19.060000Z",
      "updated_at": "2024-12-25T10:44:36.406000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_JdkMzxh.PNG",
      "character": "53f25ae0-a479-4c25-b38c-87398b311d3b"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae8b665"
  },
  {
    "id": "547e20f5-c003-405b-a96f-072f9fc462cb",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "12fa141f-d886-4140-9152-e2516037a84e",
      "created_at": "2024-12-25T10:42:19.042000Z",
      "updated_at": "2024-12-25T10:44:36.471000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_vyHCXXo.PNG",
      "character": "547e20f5-c003-405b-a96f-072f9fc462cb"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae8b665"
  },
  {
    "id": "550c8c74-2968-48e7-a7ff-23803ddfba3c",
    "name": "Mercenary Hex 6",
    "biography": {
      "id": "a83efb70-ced3-4aff-b2f3-4524d7fc349e",
      "created_at": "2024-12-25T10:42:18.730000Z",
      "updated_at": "2024-12-25T10:44:36.555000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_gWGOLwt.PNG",
      "character": "550c8c74-2968-48e7-a7ff-23803ddfba3c"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae74146"
  },
  {
    "id": "564dd031-be47-44b6-98fc-9824f536b0d5",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "b6c21d26-9b53-4033-afbf-49e2bb5737b2",
      "created_at": "2024-12-25T12:24:20.888000Z",
      "updated_at": "2024-12-25T12:24:20.888000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "564dd031-be47-44b6-98fc-9824f536b0d5"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf4439d"
  },
  {
    "id": "5672dcc1-b796-4182-8c6f-bfbd204fdc64",
    "name": "Mercenary Hex 2",
    "biography": {
      "id": "fdac5828-59ac-493d-a7c5-b79ae3f9888c",
      "created_at": "2024-12-25T10:42:19.785000Z",
      "updated_at": "2024-12-25T10:44:36.675000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_7XCYRc0.PNG",
      "character": "5672dcc1-b796-4182-8c6f-bfbd204fdc64"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeaa236"
  },
  {
    "id": "56fb18c3-efd8-4530-ab9d-22e74491499e",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "72d90c99-dd82-4f51-9be0-ea2a935c3086",
      "created_at": "2024-12-25T12:24:20.398000Z",
      "updated_at": "2024-12-25T12:24:20.398000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "56fb18c3-efd8-4530-ab9d-22e74491499e"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caed92aa"
  },
  {
    "id": "5740bb37-c35f-4d00-9e13-cb968022127d",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "a1391798-603e-4e7c-b9ba-3b52ed44b893",
      "created_at": "2024-12-25T12:24:22.467000Z",
      "updated_at": "2024-12-25T12:24:22.467000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "5740bb37-c35f-4d00-9e13-cb968022127d"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf84dcd"
  },
  {
    "id": "5777c888-a001-47ed-a620-32d696902a98",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "dc63259c-a67b-4af1-b118-76861d51e795",
      "created_at": "2024-12-25T10:42:18.793000Z",
      "updated_at": "2024-12-25T10:44:36.767000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_sapt9Nh.PNG",
      "character": "5777c888-a001-47ed-a620-32d696902a98"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae765b7"
  },
  {
    "id": "5929a5f9-a880-4ad2-a5d2-f6ecf02618b1",
    "name": "Captain Aria Steelborne",
    "biography": {
      "id": "af802b83-66ba-49f8-9786-a88a3661f7f8",
      "created_at": "2024-12-24T12:16:22.585000Z",
      "updated_at": "2024-12-24T12:16:51.569000Z",
      "age": 37,
      "gender": "Other",
      "background": "Captain Aria Steelborne is the leader of the 'Iron Tempest' mercenary squad, known for their precision and effectiveness. She built her reputation during the Dimensional Rift Wars, where her strategic acumen and leadership skills saved countless lives. Now, she leads her team on high-stakes missions, balancing honor and survival in a world full of chaos.",
      "appearance": "A tall, muscular woman with piercing gray eyes and a scar running across her cheek. She wears a reinforced tactical suit with Flow-enhanced plating, a badge of command on her chest.",
      "avatar": "http://localhost:8000/media/avatars/21942B78-619B-4DEC-824E-64103BB58FFD.PNG",
      "character": "5929a5f9-a880-4ad2-a5d2-f6ecf02618b1"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Commander",
      "Strategist"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "59b1d3ca-780e-4f1f-ba3f-58d6ac725861",
    "name": "Copipasta",
    "biography": {
      "id": "000a4c90-294f-45d3-a971-50d468c755dd",
      "created_at": "2024-12-26T09:16:32.431000Z",
      "updated_at": "2024-12-26T09:18:01.567000Z",
      "age": 35,
      "gender": "Other",
      "background": "Raised by an enigmatic hermit rumored to be an exiled alchemist. From a young age, he was taught the secrets of the natural world—how to extract poison from plants, transmute base metals, and harness the elements. Their mentor's teachings were harsh and unrelenting, shaping character into a cunning and resourceful individual.",
      "appearance": "Sharp-featured alchemist with piercing blue eyes and an athletic build, exuding an aura of cold intellect and cruelty, driven by an unrelenting pursuit of forbidden knowledge and power, wielding deadly concoctions and transmutations with ruthless precision.",
      "avatar": "http://localhost:8000/media/avatars/copypasta.webp",
      "character": "59b1d3ca-780e-4f1f-ba3f-58d6ac725861"
    },
    "npc": false,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "dark",
      "alchemist"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "fe887164-987d-449e-96eb-4f3762b76358",
      "name": "House of Gryphon (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cad964e5"
  },
  {
    "id": "5aeb15bc-5c36-4583-aced-0861aafb3da6",
    "name": "Zeus Prime 00 7",
    "biography": {
      "id": "0f63ea22-1656-4bca-a306-acc51e35ac04",
      "created_at": "2024-12-25T12:24:23.268000Z",
      "updated_at": "2024-12-25T12:24:23.268000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "5aeb15bc-5c36-4583-aced-0861aafb3da6"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafdd31e"
  },
  {
    "id": "5aed5f35-d4f5-412a-95ac-148325a11365",
    "name": "Mercenary Hex 2",
    "biography": {
      "id": "9562e484-3034-4e94-bd38-6f302c241493",
      "created_at": "2024-12-25T10:42:18.470000Z",
      "updated_at": "2024-12-25T10:44:36.928000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_NcBu4BC.PNG",
      "character": "5aed5f35-d4f5-412a-95ac-148325a11365"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cadbcb55"
  },
  {
    "id": "5af3eb04-06e4-4c63-84be-083d473e427b",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "700a90ee-bf31-4a0e-8acd-65c97316253a",
      "created_at": "2024-12-25T12:24:21.680000Z",
      "updated_at": "2024-12-25T12:24:21.680000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "5af3eb04-06e4-4c63-84be-083d473e427b"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf616e3"
  },
  {
    "id": "5cd46c13-bf57-42d3-9f07-89aff148c7da",
    "name": "Lyra Ashvale",
    "biography": {
      "id": "a32c1230-a7d8-4b5d-a6ad-a079e80ad434",
      "created_at": "2024-12-24T12:34:32.931000Z",
      "updated_at": "2024-12-24T12:43:47.370000Z",
      "age": 27,
      "gender": "Other",
      "background": "Lyra is a patient sniper who values precision and preparation above all else. Her ability to assess the battlefield makes her a strategic asset to her team.",
      "appearance": "A sharp-eyed woman with tied-back hair and a calm demeanor. Her sniper rifle is sleek and meticulously maintained, capable of precise, long-range shots.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_3L4qujl.PNG",
      "character": "5cd46c13-bf57-42d3-9f07-89aff148c7da"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Sniper",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "5e54963a-0669-4a27-8c11-d3a20bdd5718",
    "name": "Zeus Prime 00 7",
    "biography": {
      "id": "5bc4a842-93c2-4c7c-89af-3319f4de5dd0",
      "created_at": "2024-12-25T12:24:23.762000Z",
      "updated_at": "2024-12-25T12:24:23.763000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "5e54963a-0669-4a27-8c11-d3a20bdd5718"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafe2ee9"
  },
  {
    "id": "5f334457-3816-48f8-8596-c666031d5f7d",
    "name": "Zeus Prime 00 5",
    "biography": {
      "id": "a7db5f58-0ca1-45ad-a984-62e90b468833",
      "created_at": "2024-12-25T12:24:22.099000Z",
      "updated_at": "2024-12-25T12:24:22.100000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "5f334457-3816-48f8-8596-c666031d5f7d"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf73fee"
  },
  {
    "id": "608faaef-3a25-41a4-96f8-d101410bb6f5",
    "name": "Zeus Prime 00 4",
    "biography": {
      "id": "9bab367f-001b-44ff-9212-7284baa01a9f",
      "created_at": "2024-12-25T12:24:20.526000Z",
      "updated_at": "2024-12-25T12:24:20.527000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "608faaef-3a25-41a4-96f8-d101410bb6f5"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caef9bef"
  },
  {
    "id": "60f14bae-a019-4cac-bf5a-6f1744de4096",
    "name": "Zeus Prime 00 6",
    "biography": {
      "id": "3aae0aba-3714-4011-bb38-fcaaa2547521",
      "created_at": "2024-12-25T12:24:20.764000Z",
      "updated_at": "2024-12-25T12:24:20.764000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "60f14bae-a019-4cac-bf5a-6f1744de4096"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf10277"
  },
  {
    "id": "621c4e95-143b-46d8-9e4c-d913e0a0b51e",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "e8f8c8cf-431a-48cf-beb0-34d5e157bb87",
      "created_at": "2024-12-25T12:24:20.860000Z",
      "updated_at": "2024-12-25T12:24:20.860000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "621c4e95-143b-46d8-9e4c-d913e0a0b51e"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf2e872"
  },
  {
    "id": "629be84f-7462-4668-ad52-f9f8e1e8f069",
    "name": "Malrick Crimsonthorn",
    "biography": {
      "id": "1c623441-2878-47c4-a22e-e743b0bf6f66",
      "created_at": "2024-12-24T12:56:43.349000Z",
      "updated_at": "2024-12-24T12:59:49.269000Z",
      "age": 45,
      "gender": "Other",
      "background": "Malrick Crimsonthorn is a master of blood magic, having delved into the forbidden arts to gain immense power. Known for his calculating mind and ruthless demeanor, he leads his apprentices with an iron will, seeking ancient blood rituals to unlock even greater abilities.",
      "appearance": "A tall, gaunt figure with deep-set crimson eyes and pale skin. He wears dark robes adorned with blood-red runes that pulsate faintly, emanating a sinister aura.",
      "avatar": "http://localhost:8000/media/avatars/47B6C1F9-D168-4880-933B-B173532E6BEE.PNG",
      "character": "629be84f-7462-4668-ad52-f9f8e1e8f069"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Blood Mage",
      "Leader",
      "Dark Sorcerer"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "27c7c780-cd43-44c9-800f-13f4a131488e",
      "name": "Blood Hunters (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caefcdf2"
  },
  {
    "id": "634c0471-0260-4d5f-a357-1158ff60fe93",
    "name": "Mercenary Hex 3",
    "biography": {
      "id": "1f105d4e-6408-4c65-ae6e-a578007d55b9",
      "created_at": "2024-12-25T10:42:19.791000Z",
      "updated_at": "2024-12-25T10:44:37.029000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_hGWUvP3.PNG",
      "character": "634c0471-0260-4d5f-a357-1158ff60fe93"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeaa236"
  },
  {
    "id": "66b5a91e-1e94-41b6-8386-876c7de88fea",
    "name": "Mercenary Hex 2",
    "biography": {
      "id": "0ca5ead0-6d39-4bd2-82fb-00e8b4c94631",
      "created_at": "2024-12-25T10:42:18.679000Z",
      "updated_at": "2024-12-25T10:44:37.193000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_PWyhAAn.PNG",
      "character": "66b5a91e-1e94-41b6-8386-876c7de88fea"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae599d5"
  },
  {
    "id": "67266842-c60d-4e87-af6f-84a6d558822f",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "633b7bf8-8f8c-412e-b94d-3d58a2e9265d",
      "created_at": "2024-12-25T10:42:18.712000Z",
      "updated_at": "2024-12-25T10:44:37.299000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_7Av5aEe.PNG",
      "character": "67266842-c60d-4e87-af6f-84a6d558822f"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae74146"
  },
  {
    "id": "67313c97-898b-4c24-a587-b7a5f68ff532",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "997ac58e-54d0-43e7-b781-8972268a5444",
      "created_at": "2024-12-25T10:42:16.778000Z",
      "updated_at": "2024-12-25T10:44:37.504000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_W1f0KS9.PNG",
      "character": "67313c97-898b-4c24-a587-b7a5f68ff532"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cad9bfe5"
  },
  {
    "id": "6832fdff-7b5b-424f-9017-ae7e4777af5d",
    "name": "Lyric Dawnshade",
    "biography": {
      "id": "ae8db26a-6d00-4262-9070-afaa93c71d52",
      "created_at": "2024-12-24T12:11:55.612000Z",
      "updated_at": "2024-12-24T12:12:21.891000Z",
      "age": 32,
      "gender": "Other",
      "background": "Lyric was a healer who wandered the dimensions, using her Flow manipulation skills to restore balance and harmony. Known for her compassion, she joined countless adventures, always leaving a trail of hope in her wake.",
      "appearance": "A graceful figure with long, silver hair and ethereal blue eyes, wearing robes that shimmer faintly with Flow energy.",
      "avatar": "http://localhost:8000/media/avatars/7C88A960-EC20-42BD-8F14-F931338ABBCF.PNG",
      "character": "6832fdff-7b5b-424f-9017-ae7e4777af5d"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Adventurer",
      "Flow Manipulator",
      "Healer"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": null,
    "position_id": "00000000-0000-0000-0000-0193caf863ce"
  },
  {
    "id": "68641d74-ff0b-4810-9dc6-6e483ec563bc",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "356a8c16-e43c-410b-9695-d1becac42d34",
      "created_at": "2024-12-25T12:24:23.703000Z",
      "updated_at": "2024-12-25T12:24:23.703000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "68641d74-ff0b-4810-9dc6-6e483ec563bc"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafe22b9"
  },
  {
    "id": "69de6ddf-ad93-43c7-840a-a3af9dcb680f",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "af093c30-3465-48a9-b3e4-919f9d74b9cc",
      "created_at": "2024-12-25T10:42:18.809000Z",
      "updated_at": "2024-12-25T10:44:37.736000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_YKSr1OG.PNG",
      "character": "69de6ddf-ad93-43c7-840a-a3af9dcb680f"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae79d20"
  },
  {
    "id": "6a15a85e-e31d-4929-b757-84b708b3cc9b",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "a6c02770-33d4-4e8d-bb85-b0b24a39a5ab",
      "created_at": "2024-12-25T12:24:20.561000Z",
      "updated_at": "2024-12-25T12:24:20.561000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "6a15a85e-e31d-4929-b757-84b708b3cc9b"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf00f84"
  },
  {
    "id": "6b98703b-e526-40cc-9d4a-60dc096e7bc4",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "db9f3337-6d02-44c0-a197-ba8379fee961",
      "created_at": "2024-12-25T12:24:23.628000Z",
      "updated_at": "2024-12-25T12:24:23.628000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "6b98703b-e526-40cc-9d4a-60dc096e7bc4"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafdff09"
  },
  {
    "id": "6c1b89ef-1f1c-4c6e-afa6-771d87816b11",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "5f680eb9-c6a8-4cae-95f9-1e035d10aa9c",
      "created_at": "2024-12-25T12:24:23.737000Z",
      "updated_at": "2024-12-25T12:24:23.738000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "6c1b89ef-1f1c-4c6e-afa6-771d87816b11"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafe2ee9"
  },
  {
    "id": "6c7ce649-6b58-4570-8be2-05081b953b6d",
    "name": "Orlin Shardwright",
    "biography": {
      "id": "13a1c7a7-924b-4869-98bc-454b0b32f087",
      "created_at": "2024-12-24T13:19:30.704000Z",
      "updated_at": "2024-12-24T13:24:51.228000Z",
      "age": 52,
      "gender": "Male",
      "background": "Orlin Shardwright is a master of artifact creation, known throughout the realms for his unparalleled skill in imbuing objects with Flow energy. He apprenticed under ancient sages and developed unique techniques to blend raw magic and physical enhancements. Though he can be gruff and focused on his craft, Orlin takes pride in teaching the next generation of creators, ensuring that his legacy lives on.",
      "appearance": "A wiry man with streaks of silver in his shoulder-length hair and sharp, discerning eyes. His hands are adorned with intricate Flow-infused rings, and his long coat is embroidered with symbols of power and precision.",
      "avatar": "http://localhost:8000/media/avatars/5149D034-7E5F-4333-AD8C-ACDD677156F1.PNG",
      "character": "6c7ce649-6b58-4570-8be2-05081b953b6d"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Artifact Creator",
      "Flow Master",
      "Enhancement Specialist"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "9fd27c2f-246d-4f37-86e7-645689cc9d39",
      "name": "Three of magitians (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeee519"
  },
  {
    "id": "6d9f2f89-d9bd-4457-a355-2369c1a19dbb",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "50e6ef8d-8992-4b89-b11b-0f7d7117fcc5",
      "created_at": "2024-12-25T12:24:21.455000Z",
      "updated_at": "2024-12-25T12:24:21.455000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "6d9f2f89-d9bd-4457-a355-2369c1a19dbb"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf51a85"
  },
  {
    "id": "6dc4d64a-f290-4376-b220-73028d640186",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "4e7ef073-c639-4ac0-a87c-3aff141fa4b8",
      "created_at": "2024-12-25T12:24:22.486000Z",
      "updated_at": "2024-12-25T12:24:22.487000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "6dc4d64a-f290-4376-b220-73028d640186"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf8eca9"
  },
  {
    "id": "704d1dea-1a69-4454-89b8-2119a57170c4",
    "name": "Mira Emberforge",
    "biography": {
      "id": "10213f3a-ed0a-41eb-b5ce-061ec2cd6876",
      "created_at": "2024-12-24T12:35:39.410000Z",
      "updated_at": "2024-12-24T12:43:47.375000Z",
      "age": 30,
      "gender": "Other",
      "background": "Mira is the squad’s engineer, skilled in crafting and repairing equipment. Her quick thinking and technical expertise often turn the tide in high-pressure situations.",
      "appearance": "A sharp-eyed woman with fiery red hair and a confident smirk. She wears a utility vest loaded with tools and gadgets.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_pYFjwUB.PNG",
      "character": "704d1dea-1a69-4454-89b8-2119a57170c4"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Engineer",
      "Tactician"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "70825eb6-5641-4ff6-8dbd-c1f8bb6f8da2",
    "name": "Zeus Prime 00 4",
    "biography": {
      "id": "351cbea4-8604-48aa-ae3e-725f85d3a134",
      "created_at": "2024-12-25T12:24:23.671000Z",
      "updated_at": "2024-12-25T12:24:23.672000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "70825eb6-5641-4ff6-8dbd-c1f8bb6f8da2"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafdff09"
  },
  {
    "id": "70a7eb69-3cc8-4bf8-b324-ef100a304606",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "38773e48-0214-45d6-aee8-460e6372473e",
      "created_at": "2024-12-25T12:24:20.548000Z",
      "updated_at": "2024-12-25T12:24:20.548000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "70a7eb69-3cc8-4bf8-b324-ef100a304606"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf00f84"
  },
  {
    "id": "714ce91b-aaae-48ea-8d05-b907d26eeeb9",
    "name": "Zeus Prime 00 5",
    "biography": {
      "id": "6b5cf577-6966-41f9-bf67-766ed6c74a00",
      "created_at": "2024-12-25T12:24:22.618000Z",
      "updated_at": "2024-12-25T12:24:22.618000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "714ce91b-aaae-48ea-8d05-b907d26eeeb9"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf924e2"
  },
  {
    "id": "7165c25f-fb75-4f80-a828-66b2038d40e9",
    "name": "Mercenary Hex 8",
    "biography": {
      "id": "aa4ee108-847c-4a48-8fea-467681de0078",
      "created_at": "2024-12-25T10:42:18.298000Z",
      "updated_at": "2024-12-25T10:44:38.018000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_h7l4COv.PNG",
      "character": "7165c25f-fb75-4f80-a828-66b2038d40e9"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cadbb206"
  },
  {
    "id": "71b8e28c-04d1-431c-9ccf-dd2a6044050b",
    "name": "Mercenary Hex 5",
    "biography": {
      "id": "f83a94a5-fdb6-488f-ac87-1fde1a1e647a",
      "created_at": "2024-12-25T10:42:18.727000Z",
      "updated_at": "2024-12-25T10:44:38.305000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_R0mZ5gJ.PNG",
      "character": "71b8e28c-04d1-431c-9ccf-dd2a6044050b"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae74146"
  },
  {
    "id": "71eb9c18-74ca-4e75-a06e-338f832c5969",
    "name": "Zeus Prime 00 5",
    "biography": {
      "id": "90328331-bbcc-4111-88ae-2d76b654c681",
      "created_at": "2024-12-25T12:24:20.530000Z",
      "updated_at": "2024-12-25T12:24:20.531000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "71eb9c18-74ca-4e75-a06e-338f832c5969"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caef9bef"
  },
  {
    "id": "71fa94f1-bb63-460c-84cb-6e1331059075",
    "name": "Elyra Duskveil",
    "biography": {
      "id": "57f29631-e4fa-4481-97f3-cdd36aa04df0",
      "created_at": "2024-12-24T12:57:36.154000Z",
      "updated_at": "2024-12-24T12:59:26.825000Z",
      "age": 28,
      "gender": "Other",
      "background": "Elyra is a devoted apprentice under Malrick Crimsonthorn. She is ambitious and unrelenting, seeking to master the forbidden arts of blood magic under her master's tutelage. Her loyalty is unwavering, though she often questions Malrick’s methods in private.",
      "appearance": "A slender woman with long black hair and piercing crimson eyes. Her hands are stained red from countless rituals, and her robes are marked with intricate blood magic symbols.",
      "avatar": "http://localhost:8000/media/avatars/6F973806-8FCF-4236-B576-D4A14A5090E3.PNG",
      "character": "71fa94f1-bb63-460c-84cb-6e1331059075"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Blood Mage",
      "Apprentice",
      "Dark Sorceress"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "27c7c780-cd43-44c9-800f-13f4a131488e",
      "name": "Blood Hunters (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caefcdf2"
  },
  {
    "id": "73bda446-4b25-44ed-a056-8f33df11721f",
    "name": "Zeus Prime 00 9",
    "biography": {
      "id": "d2b81606-7f60-473e-883e-8dad22a3ed42",
      "created_at": "2024-12-25T12:24:22.668000Z",
      "updated_at": "2024-12-25T12:24:22.668000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "73bda446-4b25-44ed-a056-8f33df11721f"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf924e2"
  },
  {
    "id": "73c633da-273f-4e32-9fa2-80639169d37f",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "4d44ee84-524d-4ed6-b7b8-7238d22685bc",
      "created_at": "2024-12-25T12:24:20.728000Z",
      "updated_at": "2024-12-25T12:24:20.728000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "73c633da-273f-4e32-9fa2-80639169d37f"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf10277"
  },
  {
    "id": "74f84004-2227-4a00-ab96-df22cb34526f",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "572afb87-71af-476b-aa14-dbc61b0a3106",
      "created_at": "2024-12-25T12:24:20.724000Z",
      "updated_at": "2024-12-25T12:24:20.725000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "74f84004-2227-4a00-ab96-df22cb34526f"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf10277"
  },
  {
    "id": "752bd812-1bbd-4001-a6d6-44d06d7a19c0",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "14d9c9f0-83a2-4956-aa26-9bb05164d7e2",
      "created_at": "2024-12-25T12:24:22.786000Z",
      "updated_at": "2024-12-25T12:24:22.787000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "752bd812-1bbd-4001-a6d6-44d06d7a19c0"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafaa0ee"
  },
  {
    "id": "764edcf1-0d27-4181-a170-d8c1bcb9d4c1",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "6a715f1f-8a4c-4ea6-89d6-2dda06c4b2a3",
      "created_at": "2024-12-25T10:42:18.881000Z",
      "updated_at": "2024-12-25T10:44:38.425000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_PPfUYWE.PNG",
      "character": "764edcf1-0d27-4181-a170-d8c1bcb9d4c1"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae7d299"
  },
  {
    "id": "76a2e981-79d8-4fb4-82d5-03d2352ea102",
    "name": "Zeus Prime 00 8",
    "biography": {
      "id": "b1e61d1f-1c5a-43bb-b9f4-3484caf7e406",
      "created_at": "2024-12-25T12:24:23.326000Z",
      "updated_at": "2024-12-25T12:24:23.327000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "76a2e981-79d8-4fb4-82d5-03d2352ea102"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafdd31e"
  },
  {
    "id": "76cfc99d-2354-4c8f-84d4-d5beb7ed39b1",
    "name": "Zeus Prime 00 5",
    "biography": {
      "id": "a58e828a-d0ac-4e43-a691-28c01ebb1d50",
      "created_at": "2024-12-25T12:24:23.104000Z",
      "updated_at": "2024-12-25T12:24:23.105000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "76cfc99d-2354-4c8f-84d4-d5beb7ed39b1"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafdd31e"
  },
  {
    "id": "77d7dc7e-ddcb-403c-939e-5bd7296a2e06",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "8e7580f9-e7c8-4384-8838-fa2395090fa9",
      "created_at": "2024-12-25T12:24:23.742000Z",
      "updated_at": "2024-12-25T12:24:23.742000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "77d7dc7e-ddcb-403c-939e-5bd7296a2e06"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafe2ee9"
  },
  {
    "id": "77f6cfd2-9dcd-4d35-87e5-4a73c8d0f40b",
    "name": "Mercenary Hex 2",
    "biography": {
      "id": "7b615b17-90e8-447f-8e8f-02020dc293b8",
      "created_at": "2024-12-25T10:42:19.816000Z",
      "updated_at": "2024-12-25T10:44:38.533000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_Be8fjrG.PNG",
      "character": "77f6cfd2-9dcd-4d35-87e5-4a73c8d0f40b"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb17aa"
  },
  {
    "id": "77fefc2f-64a3-4bf3-913e-05a486fd3a01",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "125b39e4-9882-4f5f-9332-e8be2f11d204",
      "created_at": "2024-12-25T12:24:23.857000Z",
      "updated_at": "2024-12-25T12:24:23.857000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "77fefc2f-64a3-4bf3-913e-05a486fd3a01"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb0478be"
  },
  {
    "id": "798b8415-635d-46f5-9a5c-a00ad77fc304",
    "name": "Mercenary Hex 9",
    "biography": {
      "id": "c499ce60-616e-46bf-9149-837f83deb37b",
      "created_at": "2024-12-25T10:42:19.960000Z",
      "updated_at": "2024-12-25T10:44:38.582000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_cGPs37B.PNG",
      "character": "798b8415-635d-46f5-9a5c-a00ad77fc304"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "79d66657-b983-4623-b497-ef670b3a0a7c",
    "name": "Mercenary Hex 5",
    "biography": {
      "id": "4b213948-9d1c-4654-9143-657a60768c4e",
      "created_at": "2024-12-25T10:42:19.009000Z",
      "updated_at": "2024-12-25T10:44:38.688000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_NyH61Ic.PNG",
      "character": "79d66657-b983-4623-b497-ef670b3a0a7c"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae85d7a"
  },
  {
    "id": "7a3afe97-a14f-4d31-88b8-5424488747f8",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "bee87f2b-a274-421e-8b82-253c3add096d",
      "created_at": "2024-12-25T12:24:20.813000Z",
      "updated_at": "2024-12-25T12:24:20.813000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "7a3afe97-a14f-4d31-88b8-5424488747f8"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf1a4de"
  },
  {
    "id": "7c72fd85-23af-432e-8e26-30b6daf8303e",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "ae39f5b9-cdbf-4571-8ac0-6a1a07e20ae3",
      "created_at": "2024-12-25T12:24:22.796000Z",
      "updated_at": "2024-12-25T12:24:22.796000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "7c72fd85-23af-432e-8e26-30b6daf8303e"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafaa0ee"
  },
  {
    "id": "7cf2cccc-4457-4e27-aaaa-c571fbec9710",
    "name": "Zeus Prime 00 8",
    "biography": {
      "id": "6457f5a0-51fc-491e-a9af-84f607d5cf89",
      "created_at": "2024-12-25T12:24:23.767000Z",
      "updated_at": "2024-12-25T12:24:23.767000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "7cf2cccc-4457-4e27-aaaa-c571fbec9710"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafe2ee9"
  },
  {
    "id": "7cfc2d21-1b46-4ba9-9f0b-0bfb7cf2dc1a",
    "name": "Zeus Prime 00 6",
    "biography": {
      "id": "ae8be598-e3e4-476e-8ab8-27fcf9617278",
      "created_at": "2024-12-25T12:24:20.603000Z",
      "updated_at": "2024-12-25T12:24:20.603000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "7cfc2d21-1b46-4ba9-9f0b-0bfb7cf2dc1a"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf00f84"
  },
  {
    "id": "7d5bbd50-7751-4424-abf9-7136dfe0b4b8",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "ca57e1ea-2a18-48b8-9757-cca533611a1e",
      "created_at": "2024-12-25T12:24:20.477000Z",
      "updated_at": "2024-12-25T12:24:20.478000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "7d5bbd50-7751-4424-abf9-7136dfe0b4b8"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caef4ba0"
  },
  {
    "id": "7ddc5e58-d79a-49b4-a300-176fcb4fb9f7",
    "name": "Max Ironstride",
    "biography": {
      "id": "ed7085d6-e679-4943-bf5f-44f249096fbd",
      "created_at": "2024-12-24T12:25:52.657000Z",
      "updated_at": "2024-12-24T12:25:52.657000Z",
      "age": 28,
      "gender": "Other",
      "background": "Dax is a seasoned mercenary who takes on contracts for the highest bidder. Skilled in both ranged and close-quarters combat, he relies on his sharp instincts and combat prowess to survive. While not one to question his employers, he holds a firm code of loyalty to his squadmates.",
      "appearance": "A rugged, muscular figure with short black hair and a weathered face. He wears a durable combat vest and cargo pants, with a Flow-enhanced rifle slung across his back.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB.PNG",
      "character": "7ddc5e58-d79a-49b4-a300-176fcb4fb9f7"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Combat Specialist",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "7e7af740-b2f9-4bdb-baf9-de622fea7e6d",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "e364d252-f425-41e7-a4da-d8900c2370a1",
      "created_at": "2024-12-25T12:24:20.865000Z",
      "updated_at": "2024-12-25T12:24:20.865000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "7e7af740-b2f9-4bdb-baf9-de622fea7e6d"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf2e872"
  },
  {
    "id": "7f9ef830-e577-4dcc-9470-318ebb3eea32",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "4ca9e1f1-14fa-4511-9b4d-806c53df7db5",
      "created_at": "2024-12-25T12:24:22.596000Z",
      "updated_at": "2024-12-25T12:24:22.596000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "7f9ef830-e577-4dcc-9470-318ebb3eea32"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf924e2"
  },
  {
    "id": "80e7457b-61a3-4046-8c3e-a41517e6f20f",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "49a68909-942f-47aa-b896-9840fab99dfa",
      "created_at": "2024-12-25T12:24:23.662000Z",
      "updated_at": "2024-12-25T12:24:23.662000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "80e7457b-61a3-4046-8c3e-a41517e6f20f"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafdff09"
  },
  {
    "id": "81950ebc-0e5a-489e-a8da-5a99c5ac6f2b",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "c889d2f6-e5a7-4bcc-a39f-97245ecfc653",
      "created_at": "2024-12-25T12:24:21.684000Z",
      "updated_at": "2024-12-25T12:24:21.684000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "81950ebc-0e5a-489e-a8da-5a99c5ac6f2b"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf616e3"
  },
  {
    "id": "81dd5b53-b5ea-4e18-b453-fe7e7861d018",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "038ff746-b2a1-4e6b-a9ab-a809dbc61527",
      "created_at": "2024-12-25T10:42:18.676000Z",
      "updated_at": "2024-12-25T10:44:38.714000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_mwKyVFK.PNG",
      "character": "81dd5b53-b5ea-4e18-b453-fe7e7861d018"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae599d5"
  },
  {
    "id": "81e8391c-2d06-4359-9d5c-5dc5ef9ba8e9",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "b4c32bad-1faf-4d83-9838-430908de987c",
      "created_at": "2024-12-25T10:42:19.882000Z",
      "updated_at": "2024-12-25T10:44:38.823000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_yhotpMY.PNG",
      "character": "81e8391c-2d06-4359-9d5c-5dc5ef9ba8e9"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "826cef04-624d-42bc-b088-fa2744a2ea10",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "9df2ac5b-6685-4cb2-9656-71a95c365785",
      "created_at": "2024-12-25T12:24:20.485000Z",
      "updated_at": "2024-12-25T12:24:20.485000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "826cef04-624d-42bc-b088-fa2744a2ea10"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caef4ba0"
  },
  {
    "id": "8299af31-186f-4c42-8349-90cf29272a3e",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "a4c0a3fc-09ee-475d-a45e-6b67b700a90f",
      "created_at": "2024-12-25T12:24:21.582000Z",
      "updated_at": "2024-12-25T12:24:21.582000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "8299af31-186f-4c42-8349-90cf29272a3e"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf5e8d7"
  },
  {
    "id": "83eeba52-6e89-49cb-8010-b33738c4d4d8",
    "name": "Zeus Prime 00 5",
    "biography": {
      "id": "8c376f37-ec16-4310-8775-8f3bdce3fc45",
      "created_at": "2024-12-25T12:24:20.659000Z",
      "updated_at": "2024-12-25T12:24:20.659000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "83eeba52-6e89-49cb-8010-b33738c4d4d8"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf08060"
  },
  {
    "id": "85aa825d-ef0d-407d-ba44-cc8afcd9709e",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "0bcb12b8-5f69-4275-aefa-2c4d2d2b92f6",
      "created_at": "2024-12-25T10:42:19.809000Z",
      "updated_at": "2024-12-25T10:44:38.968000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_65rZsRH.PNG",
      "character": "85aa825d-ef0d-407d-ba44-cc8afcd9709e"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb17aa"
  },
  {
    "id": "85ed96b9-3f46-4a5f-9b08-bf62dd91b51b",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "2d13e259-e40d-4690-b92f-7a74637b6f94",
      "created_at": "2024-12-25T12:24:22.478000Z",
      "updated_at": "2024-12-25T12:24:22.478000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "85ed96b9-3f46-4a5f-9b08-bf62dd91b51b"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf8eca9"
  },
  {
    "id": "86380099-fd33-49db-8111-dff9a9591667",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "df64ce9f-cdce-4418-b86e-50809eb87dbf",
      "created_at": "2024-12-25T10:42:20.863000Z",
      "updated_at": "2024-12-25T10:44:39.056000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_xJitKzB.PNG",
      "character": "86380099-fd33-49db-8111-dff9a9591667"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb0ad298"
  },
  {
    "id": "879d76e7-36a9-4487-a6d6-3bef23589d3a",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "307ff0f2-a98b-4731-add8-3adf037dbdc0",
      "created_at": "2024-12-25T10:42:18.690000Z",
      "updated_at": "2024-12-25T10:44:39.111000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_8Z9I7Zh.PNG",
      "character": "879d76e7-36a9-4487-a6d6-3bef23589d3a"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae63a37"
  },
  {
    "id": "88910239-df8d-4c57-9d53-bb50f62cff1e",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "d70df524-d5f5-40f9-a434-11a24d0c5ca2",
      "created_at": "2024-12-25T12:24:21.704000Z",
      "updated_at": "2024-12-25T12:24:21.705000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "88910239-df8d-4c57-9d53-bb50f62cff1e"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf73fee"
  },
  {
    "id": "8a2a93d1-e3aa-43ea-8991-b8a2f351ba85",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "7cfd2236-c8ed-4762-a59f-8b35dec00238",
      "created_at": "2024-12-25T12:24:20.450000Z",
      "updated_at": "2024-12-25T12:24:20.450000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "8a2a93d1-e3aa-43ea-8991-b8a2f351ba85"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caee7c1a"
  },
  {
    "id": "8a421f6e-c8e0-468e-b333-6a05e2c6c8ee",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "21d19198-55ac-4b67-99c7-bb87ce20fd2d",
      "created_at": "2024-12-25T12:24:20.644000Z",
      "updated_at": "2024-12-25T12:24:20.644000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "8a421f6e-c8e0-468e-b333-6a05e2c6c8ee"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf08060"
  },
  {
    "id": "8a8a01b5-ce19-4be9-9d7f-4e632eca5b66",
    "name": "Mercenary Hex 3",
    "biography": {
      "id": "2a5d6741-b9f3-4eb0-9558-19d2d7d5420c",
      "created_at": "2024-12-25T10:42:19.890000Z",
      "updated_at": "2024-12-25T10:44:39.277000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_rsy8DgS.PNG",
      "character": "8a8a01b5-ce19-4be9-9d7f-4e632eca5b66"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "8ab03e5f-8573-415d-957a-8c04653519ae",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "1645ab95-c6c0-4448-858a-404d90354de6",
      "created_at": "2024-12-25T12:24:22.729000Z",
      "updated_at": "2024-12-25T12:24:22.729000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "8ab03e5f-8573-415d-957a-8c04653519ae"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafa744f"
  },
  {
    "id": "8acd83ff-dd27-408a-b4e8-f439ae6d4873",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "3ae6051f-da41-4840-813d-8132650d4d11",
      "created_at": "2024-12-25T12:24:20.892000Z",
      "updated_at": "2024-12-25T12:24:20.893000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "8acd83ff-dd27-408a-b4e8-f439ae6d4873"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf4439d"
  },
  {
    "id": "8b263aa8-bbc8-4536-b378-9e70212aef9a",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "a9bf9727-9580-4298-b1eb-bae661ea44d3",
      "created_at": "2024-12-25T12:24:20.806000Z",
      "updated_at": "2024-12-25T12:24:20.806000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "8b263aa8-bbc8-4536-b378-9e70212aef9a"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf1a4de"
  },
  {
    "id": "8dfa9d6d-7216-4350-a04f-dbec2a909af0",
    "name": "Mercenary Hex 2",
    "biography": {
      "id": "e2bbea63-4fe7-4967-837b-d690ca5585ea",
      "created_at": "2024-12-25T10:42:18.885000Z",
      "updated_at": "2024-12-25T10:44:39.345000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_lV5rwye.PNG",
      "character": "8dfa9d6d-7216-4350-a04f-dbec2a909af0"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae7d299"
  },
  {
    "id": "8e576474-d37a-4cfe-8bc0-7d1c3c533b4d",
    "name": "Mercenary Hex 2",
    "biography": {
      "id": "8b56559b-afc1-491f-8f3d-ab406cea6658",
      "created_at": "2024-12-25T10:42:18.584000Z",
      "updated_at": "2024-12-25T10:44:39.523000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_u8rPoEy.PNG",
      "character": "8e576474-d37a-4cfe-8bc0-7d1c3c533b4d"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cade1f26"
  },
  {
    "id": "8e79162b-89d0-4f43-bbe8-fcf4b209eb6e",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "4b9b17eb-4544-4d49-add4-8ecf3bc1c8ee",
      "created_at": "2024-12-25T12:24:22.735000Z",
      "updated_at": "2024-12-25T12:24:22.735000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "8e79162b-89d0-4f43-bbe8-fcf4b209eb6e"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafa744f"
  },
  {
    "id": "8f060bbe-64c8-416e-b1a6-1419537de365",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "6a8bf522-9b4e-4410-b6e4-7f2a2bb3bfdb",
      "created_at": "2024-12-25T12:24:23.551000Z",
      "updated_at": "2024-12-25T12:24:23.552000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "8f060bbe-64c8-416e-b1a6-1419537de365"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafdf1c3"
  },
  {
    "id": "91501d25-cef3-4977-abad-522f0a79039e",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "88b30331-1985-450c-be24-6c3cbc13386a",
      "created_at": "2024-12-25T12:24:21.670000Z",
      "updated_at": "2024-12-25T12:24:21.670000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "91501d25-cef3-4977-abad-522f0a79039e"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf616e3"
  },
  {
    "id": "91d7cbe5-56ba-409a-94d4-f29b13ecc55a",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "90a58c2d-fc1d-4f7a-b233-fcd900d2040f",
      "created_at": "2024-12-25T12:24:23.864000Z",
      "updated_at": "2024-12-25T12:24:23.864000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "91d7cbe5-56ba-409a-94d4-f29b13ecc55a"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb0478be"
  },
  {
    "id": "9380e9d3-81c8-4dd1-b0d3-f0a704951312",
    "name": "Mercenary Hex 2",
    "biography": {
      "id": "f0f7cc03-3a01-41cb-858b-b518fb3041ba",
      "created_at": "2024-12-25T10:42:18.975000Z",
      "updated_at": "2024-12-25T10:44:39.690000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_GVeei0c.PNG",
      "character": "9380e9d3-81c8-4dd1-b0d3-f0a704951312"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae85d7a"
  },
  {
    "id": "9571e2ee-db07-49e6-8082-f5d3bcfbcd75",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "9f4bd830-a58c-439d-a7ba-c6c71bec11f8",
      "created_at": "2024-12-25T10:42:18.943000Z",
      "updated_at": "2024-12-25T10:44:39.994000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_KUZP7Qp.PNG",
      "character": "9571e2ee-db07-49e6-8082-f5d3bcfbcd75"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae85d7a"
  },
  {
    "id": "962965ca-519f-40bb-9aef-8cdc89078816",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "53454bbb-948c-48a4-b1e2-5f60ad689ed9",
      "created_at": "2024-12-25T12:24:21.740000Z",
      "updated_at": "2024-12-25T12:24:21.740000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "962965ca-519f-40bb-9aef-8cdc89078816"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf73fee"
  },
  {
    "id": "964091d6-d415-4a30-acc3-95670465101e",
    "name": "Calvin Drift",
    "biography": {
      "id": "9026e3f7-0d1b-48b3-8644-31cf54919d56",
      "created_at": "2024-12-24T11:14:43.309000Z",
      "updated_at": "2024-12-24T11:17:00.547000Z",
      "age": 45,
      "gender": "Other",
      "background": "Calvin Drift was once a proud member of the Flow Guard, tasked with maintaining law and order across dimensions. However, a mysterious scandal led to his disgrace and dismissal, leaving him to wander the streets of the City of Memories. His name is whispered with suspicion, as no one knows exactly what he did to earn such shame. Banned from the Misfits Pub, Calvin now spends his days asking for beer and recounting fragmented tales of his past glory to anyone who will listen.",
      "appearance": "A scruffy, unkempt man with tangled brown hair and a patchy beard. His clothes are tattered remnants of what once may have been a uniform, now barely recognizable. His eyes are weary, yet they seem to hide a hint of the strength he once possessed.",
      "avatar": "http://localhost:8000/media/avatars/599564A9-0D7F-4648-B524-D99E71AB464B.PNG",
      "character": "964091d6-d415-4a30-acc3-95670465101e"
    },
    "npc": true,
    "rank": {
      "name": "Elite Mercenary",
      "grade": 5,
      "experience_needed": 14760
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 14761,
    "tags": [
      "Homeless",
      "Former Flow Guard",
      "Outcast"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": null,
    "position_id": "00000000-0000-0000-0000-0193cb14e174"
  },
  {
    "id": "979a5806-4660-4cf9-9993-b096ec405cc7",
    "name": "Mercenary Hex 2",
    "biography": {
      "id": "df7abef6-5886-4fee-b694-a1c939692e01",
      "created_at": "2024-12-25T10:42:19.885000Z",
      "updated_at": "2024-12-25T10:44:40.141000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_LCYmGwN.PNG",
      "character": "979a5806-4660-4cf9-9993-b096ec405cc7"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "97ab1162-fd03-4345-9f36-7eb62192ae0f",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "e1fc418e-a546-4de5-8ff5-c6725e625ef1",
      "created_at": "2024-12-25T12:24:21.712000Z",
      "updated_at": "2024-12-25T12:24:21.712000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "97ab1162-fd03-4345-9f36-7eb62192ae0f"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf73fee"
  },
  {
    "id": "98519ca4-c6f7-46a4-a72f-169ee2536e34",
    "name": "Cassian Vey",
    "biography": {
      "id": "14b86e0e-9d7e-49fe-b071-5d7b1b67abdb",
      "created_at": "2024-12-24T12:32:30.161000Z",
      "updated_at": "2024-12-24T12:43:47.380000Z",
      "age": 26,
      "gender": "Other",
      "background": "Cassian is the squad’s scout and tracker, using his speed and sharp senses to navigate terrain and locate targets. His keen instincts often help the squad avoid ambushes and traps.",
      "appearance": "A wiry man with a confident smirk and sharp, angular features. He wears lightweight tactical gear and carries a pair of binoculars strapped to his chest.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_GmSRdUk.PNG",
      "character": "98519ca4-c6f7-46a4-a72f-169ee2536e34"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Scout",
      "Tracker"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "98e043db-4a26-468d-a078-3d91c602eec0",
    "name": "Derrik Auger",
    "biography": {
      "id": "fbf1f636-b683-4f88-93eb-42951c2d9df7",
      "created_at": "2024-12-24T11:06:27.456000Z",
      "updated_at": "2024-12-24T11:07:00.906000Z",
      "age": 30,
      "gender": "Other",
      "background": "Derrik Auger is a former soldier who served in numerous dimensional conflicts, earning a reputation for his precision and resilience. However, after years of battles and countless scars—both physical and emotional—Derrik chose to leave his life of conflict. Settling in the City of Memories, he now dedicates his life to mentoring others, teaching them the principles of augmentation, discipline, and the Way of John.",
      "appearance": "A rugged man with short-cropped hair and a stern expression. His brown coat partially conceals the left side of his body, which is augmented with intricate machinery that glows faintly with orange Flow energy. His mechanical neck and shoulder add a sense of otherworldly strength, but his calm demeanor reflects his transition from a warrior to a guide.",
      "avatar": "http://localhost:8000/media/avatars/05A7DB4E-4B43-41CD-85CA-516774B956D3.PNG",
      "character": "98e043db-4a26-468d-a078-3d91c602eec0"
    },
    "npc": true,
    "rank": {
      "name": "Veteran Champion",
      "grade": 4,
      "experience_needed": 40520
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 40521,
    "tags": [
      "Path of John",
      "Augmented Soldier",
      "Mentor"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "73db031a-55cd-47c6-9e44-4b70cb09f27b",
      "name": "Mentors (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb8c86ad"
  },
  {
    "id": "992266c5-859e-4db0-b33a-8bf988bd9310",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "2a41f162-575f-4a51-98d1-fb222f77540e",
      "created_at": "2024-12-25T12:24:20.556000Z",
      "updated_at": "2024-12-25T12:24:20.556000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "992266c5-859e-4db0-b33a-8bf988bd9310"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf00f84"
  },
  {
    "id": "993ccef9-4f39-4d38-a9d2-bd68b50816fa",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "4ec8f68f-b481-447d-bb59-50e660d735eb",
      "created_at": "2024-12-25T12:24:20.421000Z",
      "updated_at": "2024-12-25T12:24:20.421000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "993ccef9-4f39-4d38-a9d2-bd68b50816fa"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caee229f"
  },
  {
    "id": "99994f0f-f538-4414-b0eb-f8277a916820",
    "name": "Zeus Prime 00 6",
    "biography": {
      "id": "3c4fa6a6-1ea0-4512-84dc-004636439805",
      "created_at": "2024-12-25T12:24:20.663000Z",
      "updated_at": "2024-12-25T12:24:20.664000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "99994f0f-f538-4414-b0eb-f8277a916820"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf08060"
  },
  {
    "id": "9a269649-135a-44f8-8e9d-2957b871982e",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "130c1b6c-945d-4a7f-bbf4-112cbb61e63a",
      "created_at": "2024-12-25T12:24:21.577000Z",
      "updated_at": "2024-12-25T12:24:21.577000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "9a269649-135a-44f8-8e9d-2957b871982e"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf5e8d7"
  },
  {
    "id": "9a9a8ad4-d704-407d-ae28-57a39b4dbedb",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "81a20205-e914-4c3c-8b21-16c3807c2151",
      "created_at": "2024-12-25T12:24:20.803000Z",
      "updated_at": "2024-12-25T12:24:20.803000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "9a9a8ad4-d704-407d-ae28-57a39b4dbedb"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf1a4de"
  },
  {
    "id": "9aa1a60b-c32d-4b82-8e61-ba2cdbebe8c4",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "7e80ec26-afff-4d04-ba6b-b7ce7794b8e1",
      "created_at": "2024-12-25T12:24:23.851000Z",
      "updated_at": "2024-12-25T12:24:23.852000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "9aa1a60b-c32d-4b82-8e61-ba2cdbebe8c4"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb0478be"
  },
  {
    "id": "9b66a56f-2c5d-4db3-86d9-4b75aed0406d",
    "name": "Max",
    "biography": {
      "id": "975a1a31-650a-4897-ba6e-f6ceca872d47",
      "created_at": "2024-12-26T20:26:35.138000Z",
      "updated_at": "2025-01-10T16:40:59.041000Z",
      "age": 300,
      "gender": "Other",
      "background": "Placeholder for background. Suggestions: 'Born in a small village and trained in combat by a retired warrior. Now seeking adventure to uncover the mysteries of the Flow.'",
      "appearance": "Placeholder for appearance. Suggestions: 'Tall with an athletic build, sharp features, piercing blue eyes.'",
      "avatar": "http://localhost:8000/media/avatars/max.webp",
      "character": "9b66a56f-2c5d-4db3-86d9-4b75aed0406d"
    },
    "npc": false,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "test"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d9df3d52-eec2-4e45-995e-b04d25679d69",
      "name": "Karmic Shield (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb1463dc"
  },
  {
    "id": "9c7bab23-e0ac-42fe-8704-4ae3495cf5ed",
    "name": "Victor Raines",
    "biography": {
      "id": "19c2af85-0f32-42de-8088-c8cf83ea99df",
      "created_at": "2024-12-24T11:59:17.376000Z",
      "updated_at": "2024-12-24T12:06:40.401000Z",
      "age": 48,
      "gender": "Other",
      "background": "Victor is the financier of the expedition, driven by a desire to uncover the MacGuffin’s secrets for both personal gain and intellectual curiosity. His connections and resources have enabled the team to take on this perilous journey, but his resolve is tested as the dangers of the Maze unfold.",
      "appearance": "A well-dressed man with graying hair and an air of authority. His tailored suit and Flow-infused wristwatch hint at his wealth and importance to the group’s mission.",
      "avatar": "http://localhost:8000/media/avatars/B538C266-1C68-4C10-9FCE-EAC6F1CAF6AE_P3QAzOs.PNG",
      "character": "9c7bab23-e0ac-42fe-8704-4ae3495cf5ed"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Lost Researchers",
      "Financier",
      "Patron"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f5bc6dd1-f08d-49eb-88a0-f4099a7db09a",
      "name": "Free Archive Seekers (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cade1cd3"
  },
  {
    "id": "9cf66665-ab61-46fb-a08c-2e4d3576698e",
    "name": "Zeus Prime 00 8",
    "biography": {
      "id": "f05a28a6-1ae5-4ceb-9ec5-5eafa91a2d6f",
      "created_at": "2024-12-25T12:24:22.662000Z",
      "updated_at": "2024-12-25T12:24:22.662000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "9cf66665-ab61-46fb-a08c-2e4d3576698e"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf924e2"
  },
  {
    "id": "9d720ef5-3b17-4909-bb3b-7b2f5ffabf70",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "298e45fd-226b-438d-a84b-c53ea0f7a481",
      "created_at": "2024-12-25T10:42:18.878000Z",
      "updated_at": "2024-12-25T10:44:40.187000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_uWuaQCd.PNG",
      "character": "9d720ef5-3b17-4909-bb3b-7b2f5ffabf70"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae7d299"
  },
  {
    "id": "9e588635-ff10-477c-9fec-817edddd00c7",
    "name": "Zeus Prime 00 4",
    "biography": {
      "id": "30a681e1-4026-4f6a-982f-a4d8af9a8056",
      "created_at": "2024-12-25T12:24:22.033000Z",
      "updated_at": "2024-12-25T12:24:22.033000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "9e588635-ff10-477c-9fec-817edddd00c7"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf73fee"
  },
  {
    "id": "9e907cbd-c0c2-40ab-95da-acf046a6d8b3",
    "name": "Drake Ironshade",
    "biography": {
      "id": "0a7b0dc3-483f-416e-ae11-d39968f3e90e",
      "created_at": "2024-12-24T11:43:39.184000Z",
      "updated_at": "2024-12-24T11:44:36.498000Z",
      "age": 45,
      "gender": "Male",
      "background": "Drake Ironshade was once a daring contrabandist who led a crew into the 4th dimension on a high-stakes mission. The expedition ended in disaster, leaving him with severe injuries, including the loss of his eye. Retreating from the adventuring life, he established an underground hub where illegal deals and trades flourish. Despite his gruff exterior, Drake commands respect and loyalty from those who frequent his domain, enforcing a strict code among his associates.",
      "appearance": "A burly man with a commanding presence, his rugged face marked by scars and a black patch covering his left eye. His remaining eye glows faintly with orange Flow energy. He carries a massive power axe slung over his shoulder, a weapon he wields with deadly precision. His attire is a mix of functional and intimidating, with a reinforced coat and utility gear.",
      "avatar": "http://localhost:8000/media/avatars/143FB8A1-0AE3-456C-BF52-37EE90A360F7.PNG",
      "character": "9e907cbd-c0c2-40ab-95da-acf046a6d8b3"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Contrabandist Leader",
      "Underground Hub Owner",
      "Power Axe Wielder"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caebbd9c"
  },
  {
    "id": "9ed6fd73-5386-4433-a180-12d00b2cb922",
    "name": "Lena Ironclad",
    "biography": {
      "id": "1fb22814-165c-4c73-9397-c0c741b3d58b",
      "created_at": "2024-12-24T12:36:01.987000Z",
      "updated_at": "2024-12-24T12:43:47.384000Z",
      "age": 35,
      "gender": "Other",
      "background": "Lena is a steadfast defender who specializes in protecting her teammates during battle. Her resilience and unyielding spirit make her a pillar of strength in any fight.",
      "appearance": "A tall, muscular woman with a shield slung over her back and a determined expression. Her armor gleams with reinforced plating.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_U37vFHU.PNG",
      "character": "9ed6fd73-5386-4433-a180-12d00b2cb922"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Tank",
      "Defender"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "9efa8a2a-083f-4baa-a48a-15dd5f6fea4b",
    "name": "Zeus Prime 00 6",
    "biography": {
      "id": "d5f223fc-d2c5-42c8-a9ad-b3aa51dc68bc",
      "created_at": "2024-12-25T12:24:23.714000Z",
      "updated_at": "2024-12-25T12:24:23.714000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "9efa8a2a-083f-4baa-a48a-15dd5f6fea4b"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafe22b9"
  },
  {
    "id": "a00647d7-28c7-42f2-b193-744fa5cd862f",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "f140e24c-b665-49d7-9a3e-dcfe9ead3ee0",
      "created_at": "2024-12-25T12:24:22.792000Z",
      "updated_at": "2024-12-25T12:24:22.792000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "a00647d7-28c7-42f2-b193-744fa5cd862f"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafaa0ee"
  },
  {
    "id": "a014ac05-bb49-4317-925a-945f617aff0a",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "a28b8aff-1d0a-477b-9cc9-5f23d9f72c38",
      "created_at": "2024-12-25T12:24:20.497000Z",
      "updated_at": "2024-12-25T12:24:20.497000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "a014ac05-bb49-4317-925a-945f617aff0a"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caef902f"
  },
  {
    "id": "a0be40d1-7d72-424f-8c66-6931ee808d78",
    "name": "Eira Frostvale",
    "biography": {
      "id": "06966ab8-b8b1-4714-8c74-c7d1fa81b375",
      "created_at": "2024-12-24T10:48:19.164000Z",
      "updated_at": "2024-12-24T10:54:24.083000Z",
      "age": 42,
      "gender": "Other",
      "background": "Born and raised in the City of Memories, Eira Frostvale is a devout follower of the Way of JSon. Her mastery of ice magic and dedication to preserving the natural harmony of Dimension-X have made her a revered figure. She spends her days mentoring new adventurers, guiding them with patience and wisdom, and instilling in them a deep respect for the Flow and the balance it represents.",
      "appearance": "A regal figure with flowing silver hair cascading over her shoulders, her skin as pale as freshly fallen snow. Her blue robes are adorned with intricate frost-like patterns that shimmer faintly in the light.",
      "avatar": "http://localhost:8000/media/avatars/F8FCA9BB-0048-43A6-B488-9710F95700DE.PNG",
      "character": "a0be40d1-7d72-424f-8c66-6931ee808d78"
    },
    "npc": true,
    "rank": {
      "name": "Veteran Champion",
      "grade": 4,
      "experience_needed": 40520
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 40521,
    "tags": [
      "Way of JSon",
      "Ice Mage",
      "Mentor"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "73db031a-55cd-47c6-9e44-4b70cb09f27b",
      "name": "Mentors (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb8c845f"
  },
  {
    "id": "a10e5997-ae1d-4ce1-9de9-2822a0481fa7",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "90292782-61dc-492a-be31-4491feaf0029",
      "created_at": "2024-12-25T12:24:20.437000Z",
      "updated_at": "2024-12-25T12:24:20.437000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "a10e5997-ae1d-4ce1-9de9-2822a0481fa7"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caee42a7"
  },
  {
    "id": "a1f9ce6a-58fe-4971-975b-bdb98e23b535",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "8cf4c4aa-393a-4494-ba67-51b593cde6ed",
      "created_at": "2024-12-25T10:42:18.671000Z",
      "updated_at": "2024-12-25T10:44:40.198000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_vOzgZS9.PNG",
      "character": "a1f9ce6a-58fe-4971-975b-bdb98e23b535"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae599d5"
  },
  {
    "id": "a1fa3121-c1a7-44d2-a278-e90096b9a6c5",
    "name": "Zeus Prime 00 4",
    "biography": {
      "id": "ddb225c4-82a1-40c6-9935-5b972d5f8501",
      "created_at": "2024-12-25T12:24:23.610000Z",
      "updated_at": "2024-12-25T12:24:23.611000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "a1fa3121-c1a7-44d2-a278-e90096b9a6c5"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafdf1c3"
  },
  {
    "id": "a204ed6d-c969-4ebe-a2a9-d49ed3d24705",
    "name": "Mercenary Hex 6",
    "biography": {
      "id": "80ffd3cc-7f5a-4837-bd7d-18f7aa3af567",
      "created_at": "2024-12-25T10:42:19.012000Z",
      "updated_at": "2024-12-25T10:44:40.215000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_kChVRb9.PNG",
      "character": "a204ed6d-c969-4ebe-a2a9-d49ed3d24705"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae85d7a"
  },
  {
    "id": "a2cc997d-0c09-4412-a568-f13f7377f091",
    "name": "The Veiled Keeper",
    "biography": {
      "id": "ffe8d52f-697e-4658-a1f0-3e03fc0c5d6b",
      "created_at": "2024-12-24T11:38:29.373000Z",
      "updated_at": "2024-12-24T12:13:29.868000Z",
      "age": 500,
      "gender": "Other",
      "background": "Little is known about the Veiled Keeper, the mysterious proprietor of the Mystical Staging Shop in the City of Memories. Their shop is renowned as a trove of rare and enchanted items, frequented by adventurers, magicians, and even the occasional rogue Flow manipulator. Whispers suggest they were once a powerful mage who chose a life of solitude, using their vast knowledge to assist others discreetly. The Veiled Keeper speaks in riddles and cryptic phrases, leaving those who meet them with more questions than answers.",
      "appearance": "A figure shrouded in a long, flowing cloak that obscures all but their glowing eyes, which emit a soft, otherworldly light. The faint clinking of enchanted amulets and gear around their neck hints at their magical prowess, while their deliberate, almost ethereal movements suggest a being beyond ordinary comprehension.",
      "avatar": "http://localhost:8000/media/avatars/72C14675-863A-45E4-966C-56E762D64BE9.PNG",
      "character": "a2cc997d-0c09-4412-a568-f13f7377f091"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Mystical Shop Owner",
      "Magician",
      "Enigmatic"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "614fee91-593a-4296-88da-f5446b5a8c37",
      "name": "Dark Merchant Guild (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf1dfbb"
  },
  {
    "id": "a36cedbe-10ff-44d4-b58d-1e36b4b90af3",
    "name": "Zeus Prime 00 4",
    "biography": {
      "id": "85bbb76e-911f-4b55-8050-7fd2a1a2fe89",
      "created_at": "2024-12-25T12:24:20.654000Z",
      "updated_at": "2024-12-25T12:24:20.654000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "a36cedbe-10ff-44d4-b58d-1e36b4b90af3"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf08060"
  },
  {
    "id": "a43a6d85-41c1-4d0c-80a3-0148caf213aa",
    "name": "Mercenary Hex 7",
    "biography": {
      "id": "c3b9495c-56a2-4c54-9b56-7c352b4b9d78",
      "created_at": "2024-12-25T10:42:18.733000Z",
      "updated_at": "2024-12-25T10:44:40.428000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_7Ydknxc.PNG",
      "character": "a43a6d85-41c1-4d0c-80a3-0148caf213aa"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae74146"
  },
  {
    "id": "a495eb3c-d07d-47a8-84fe-3908afe0c4be",
    "name": "Zeus Prime 00 4",
    "biography": {
      "id": "d0b7e11f-5063-4679-99d6-f85784f204fe",
      "created_at": "2024-12-25T12:24:23.748000Z",
      "updated_at": "2024-12-25T12:24:23.748000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "a495eb3c-d07d-47a8-84fe-3908afe0c4be"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafe2ee9"
  },
  {
    "id": "a514743f-46ec-4b69-a66f-d92a197e4683",
    "name": "Mercenary Hex 5",
    "biography": {
      "id": "3be3fc20-1cf3-410f-9409-d2e53c9f88c8",
      "created_at": "2024-12-25T10:42:19.924000Z",
      "updated_at": "2024-12-25T10:44:40.571000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_nb1oRz3.PNG",
      "character": "a514743f-46ec-4b69-a66f-d92a197e4683"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "a585aba0-3cf0-4f2d-9454-807b693cebff",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "55998104-89c2-40d9-9ade-77f02ad5763d",
      "created_at": "2024-12-25T12:24:21.561000Z",
      "updated_at": "2024-12-25T12:24:21.561000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "a585aba0-3cf0-4f2d-9454-807b693cebff"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf5b7c4"
  },
  {
    "id": "a6b83e7e-d4b1-4378-a58c-37eb5245ab96",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "6f8e3da8-990a-4b7e-92f5-d2b2617dc294",
      "created_at": "2024-12-25T12:24:20.927000Z",
      "updated_at": "2024-12-25T12:24:20.927000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "a6b83e7e-d4b1-4378-a58c-37eb5245ab96"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf4fcb2"
  },
  {
    "id": "a6bff64f-f79b-4f33-8a4f-d8067446f247",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "106cc886-29d7-47c5-8f51-0582c14c7f79",
      "created_at": "2024-12-25T12:24:23.841000Z",
      "updated_at": "2024-12-25T12:24:23.841000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "a6bff64f-f79b-4f33-8a4f-d8067446f247"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb01c07f"
  },
  {
    "id": "a80d023c-5708-45a6-9c57-223e54e0a11b",
    "name": "Draven Steelwind",
    "biography": {
      "id": "a38b53ec-a9b1-4d63-bad4-c99c05b4ca61",
      "created_at": "2024-12-24T12:36:55.986000Z",
      "updated_at": "2024-12-24T12:43:47.388000Z",
      "age": 33,
      "gender": "Other",
      "background": "Draven is a sharpshooter renowned for his precision and calm demeanor under pressure. Whether with a bow or rifle, he delivers lethal accuracy and unmatched focus on the battlefield.",
      "appearance": "A lean, athletic man with a confident smirk and piercing blue eyes. His bow, reinforced with Flow energy, is always within arm’s reach.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_RH47HNw.PNG",
      "character": "a80d023c-5708-45a6-9c57-223e54e0a11b"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Ranged Specialist",
      "Sharpshooter"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "a857d5f5-3bec-41f8-bad4-5078075a9a59",
    "name": "Zeus Prime 00 5",
    "biography": {
      "id": "478d4b0c-2cba-4164-bca5-53a08b2c0a4c",
      "created_at": "2024-12-25T12:24:21.605000Z",
      "updated_at": "2024-12-25T12:24:21.606000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "a857d5f5-3bec-41f8-bad4-5078075a9a59"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf5e8d7"
  },
  {
    "id": "a8accb89-0eb4-494b-82a4-5d63f4597fbd",
    "name": "Lucian Vale",
    "biography": {
      "id": "49d5f635-4135-4da3-a809-3bf110c95668",
      "created_at": "2024-12-24T11:58:28.185000Z",
      "updated_at": "2024-12-24T12:05:39.438000Z",
      "age": 31,
      "gender": "Other",
      "background": "Lucian is the field researcher and a key member of the Lost Researchers. His charm and resourcefulness make him an asset in navigating the Maze’s dangers. He is deeply invested in uncovering its secrets, both for personal fulfillment and to support his friends.",
      "appearance": "A rugged man with a charming smile and a confident stride. His practical attire is fitted with protective gear, and his Flow-imbued gloves reveal his hands-on approach to exploration.",
      "avatar": "http://localhost:8000/media/avatars/42D37C03-1EFA-43FE-AB62-DEA2EB92953F.PNG",
      "character": "a8accb89-0eb4-494b-82a4-5d63f4597fbd"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Lost Researchers",
      "Field Researcher",
      "Adventurer"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f5bc6dd1-f08d-49eb-88a0-f4099a7db09a",
      "name": "Free Archive Seekers (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae7f21d"
  },
  {
    "id": "a8c0da33-70a8-4fca-9b51-6b48cee40e31",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "997e02cc-cca3-4872-bc77-115934ba436a",
      "created_at": "2024-12-25T10:42:19.162000Z",
      "updated_at": "2024-12-25T10:44:40.784000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_D0KPngA.PNG",
      "character": "a8c0da33-70a8-4fca-9b51-6b48cee40e31"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae9b356"
  },
  {
    "id": "a99673be-f54f-4b6c-b50a-ea478bff11a5",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "c28e0a0d-efe7-4337-a8a9-a60300132d9b",
      "created_at": "2024-12-25T10:42:19.862000Z",
      "updated_at": "2024-12-25T10:44:40.892000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_e0PSW0u.PNG",
      "character": "a99673be-f54f-4b6c-b50a-ea478bff11a5"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb8fc4"
  },
  {
    "id": "a9ef1f71-35b2-44d2-beb6-e007ceb71d79",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "ca6509bc-495f-41ae-9aba-de71d41c9e57",
      "created_at": "2024-12-25T10:42:19.878000Z",
      "updated_at": "2024-12-25T10:44:41.011000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_eZP2UEw.PNG",
      "character": "a9ef1f71-35b2-44d2-beb6-e007ceb71d79"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "a9f6cd3f-65fc-4323-bec0-9db96df14e1f",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "b167d1ba-a539-4146-a276-bd3296178279",
      "created_at": "2024-12-25T12:24:21.463000Z",
      "updated_at": "2024-12-25T12:24:21.464000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "a9f6cd3f-65fc-4323-bec0-9db96df14e1f"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf51a85"
  },
  {
    "id": "aa860bae-ad61-4cfd-8b0a-69ad02c3deed",
    "name": "Mercenary Hex 4",
    "biography": {
      "id": "b99aa2ed-ef74-4c49-9761-ac5d8a11b5c0",
      "created_at": "2024-12-25T10:42:18.722000Z",
      "updated_at": "2024-12-25T10:44:41.137000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_cWzAIHD.PNG",
      "character": "aa860bae-ad61-4cfd-8b0a-69ad02c3deed"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae74146"
  },
  {
    "id": "ab049e13-ccef-4b32-8b04-7c64972b494c",
    "name": "Selene Darkmoor",
    "biography": {
      "id": "09e04771-abc8-47f6-82f3-533b698dfc31",
      "created_at": "2024-12-24T12:37:10.939000Z",
      "updated_at": "2024-12-24T12:43:47.396000Z",
      "age": 30,
      "gender": "Other",
      "background": "Selene is a shadowy infiltrator who excels at reconnaissance and assassination. Her ability to move unseen and strike silently makes her invaluable for covert missions.",
      "appearance": "A lithe figure with dark eyes and a hooded cloak that blends into the shadows. Her dual daggers glint ominously, a sign of her expertise in stealth combat.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_qMjaacc.PNG",
      "character": "ab049e13-ccef-4b32-8b04-7c64972b494c"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Infiltrator",
      "Recon Specialist"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "ab0d1fba-2e56-4511-bcc9-22836500d0f8",
    "name": "Mercenary Hex 4",
    "biography": {
      "id": "eccf5da4-5b9e-43cc-b995-5e031e7a4847",
      "created_at": "2024-12-25T10:42:18.591000Z",
      "updated_at": "2024-12-25T10:44:41.300000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_caVRbLE.PNG",
      "character": "ab0d1fba-2e56-4511-bcc9-22836500d0f8"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cade1f26"
  },
  {
    "id": "ad8ab491-c6c2-4fd3-aad4-d68a50d65570",
    "name": "Zeus Prime 00 6",
    "biography": {
      "id": "5d807ee9-8da1-4989-8639-6f2825895513",
      "created_at": "2024-12-25T12:24:20.935000Z",
      "updated_at": "2024-12-25T12:24:20.936000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "ad8ab491-c6c2-4fd3-aad4-d68a50d65570"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf4fcb2"
  },
  {
    "id": "ae4d6cc2-2784-4495-8208-fdfed8a32512",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "37361337-097e-4a6c-bd33-71d63399e999",
      "created_at": "2024-12-25T12:24:22.482000Z",
      "updated_at": "2024-12-25T12:24:22.482000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "ae4d6cc2-2784-4495-8208-fdfed8a32512"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf8eca9"
  },
  {
    "id": "aeaaef11-2723-4497-ab8c-3501cfd9af8a",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "67559016-f430-487b-8888-0d0fd0680718",
      "created_at": "2024-12-25T12:24:20.455000Z",
      "updated_at": "2024-12-25T12:24:20.455000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "aeaaef11-2723-4497-ab8c-3501cfd9af8a"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caee7c1a"
  },
  {
    "id": "afa543cb-0a37-4f01-9811-38653d06ec66",
    "name": "Zeus Prime 00 6",
    "biography": {
      "id": "2a2c81ef-1ad2-445e-a0ca-6ac77d9a250b",
      "created_at": "2024-12-25T12:24:23.758000Z",
      "updated_at": "2024-12-25T12:24:23.758000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "afa543cb-0a37-4f01-9811-38653d06ec66"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafe2ee9"
  },
  {
    "id": "b08c4814-30e1-4ee4-bc30-6353560dfeee",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "fd1bb64c-f960-4c6e-bd28-5371c50233b3",
      "created_at": "2024-12-25T12:24:23.745000Z",
      "updated_at": "2024-12-25T12:24:23.745000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "b08c4814-30e1-4ee4-bc30-6353560dfeee"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafe2ee9"
  },
  {
    "id": "b1057b6b-dca8-41db-9ca6-86977e5502e6",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "5364eba8-7dc7-486c-be9f-768da9bbb942",
      "created_at": "2024-12-25T10:42:20.859000Z",
      "updated_at": "2024-12-25T10:44:41.515000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_O2MGdz1.PNG",
      "character": "b1057b6b-dca8-41db-9ca6-86977e5502e6"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb0ad298"
  },
  {
    "id": "b10d99c1-1b7d-453d-92ee-d57c1998aa39",
    "name": "Zeus Prime 00 4",
    "biography": {
      "id": "9cc033da-bbec-4270-a293-ae5d96fb9e61",
      "created_at": "2024-12-25T12:24:23.867000Z",
      "updated_at": "2024-12-25T12:24:23.867000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "b10d99c1-1b7d-453d-92ee-d57c1998aa39"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb0478be"
  },
  {
    "id": "b19ff482-b633-4c92-acd8-2d84f8f6cf9c",
    "name": "Isabelle Orwin",
    "biography": {
      "id": "a9c44b3f-5e4c-43e3-8e70-27eda11ee99d",
      "created_at": "2024-12-24T11:57:47.852000Z",
      "updated_at": "2024-12-24T12:00:04.483000Z",
      "age": 35,
      "gender": "Other",
      "background": "Isabelle is the historian of the group, dedicated to uncovering the Maze’s hidden lore and its connection to the MacGuffin. She meticulously records every discovery, piecing together fragments of the past to guide the team.",
      "appearance": "A composed woman with long auburn hair tied into a practical braid. Her leather-bound journal and quill-like pen suggest a traditional yet thorough approach to documenting the history of the Maze.",
      "avatar": "http://localhost:8000/media/avatars/FDA0988D-6440-43FB-941C-A15DB5A75E13.PNG",
      "character": "b19ff482-b633-4c92-acd8-2d84f8f6cf9c"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Lost Researchers",
      "Historian",
      "Archivist"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f5bc6dd1-f08d-49eb-88a0-f4099a7db09a",
      "name": "Free Archive Seekers (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb40ae"
  },
  {
    "id": "b228e4bb-41f1-4d8a-a6c6-ceda0a78dee5",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "4713d96d-c549-4b22-bcce-63e1a69b597a",
      "created_at": "2024-12-25T10:42:18.788000Z",
      "updated_at": "2024-12-25T10:44:41.723000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_QO39RSj.PNG",
      "character": "b228e4bb-41f1-4d8a-a6c6-ceda0a78dee5"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae765b7"
  },
  {
    "id": "b23c22ca-ecf1-4e7c-931b-678ba97c831b",
    "name": "Zeus Prime 00 4",
    "biography": {
      "id": "44f196d5-4e49-4c33-8444-ada8fcb86175",
      "created_at": "2024-12-25T12:24:20.818000Z",
      "updated_at": "2024-12-25T12:24:20.818000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "b23c22ca-ecf1-4e7c-931b-678ba97c831b"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf1a4de"
  },
  {
    "id": "b2748b04-3e9a-47b0-b629-b043b4b7320a",
    "name": "Zeus Prime 00 6",
    "biography": {
      "id": "6b12cb8b-fce1-41a6-b542-b2fa1727d36f",
      "created_at": "2024-12-25T12:24:20.828000Z",
      "updated_at": "2024-12-25T12:24:20.828000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "b2748b04-3e9a-47b0-b629-b043b4b7320a"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf1a4de"
  },
  {
    "id": "b2f61145-2216-4f1b-b675-cd76b6f6d248",
    "name": "Mercenary Hex 6",
    "biography": {
      "id": "89f9d685-4e25-49b5-b74d-4cfa1cb00c6c",
      "created_at": "2024-12-25T10:42:18.487000Z",
      "updated_at": "2024-12-25T10:44:41.842000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_ZnrR0xq.PNG",
      "character": "b2f61145-2216-4f1b-b675-cd76b6f6d248"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cadbcb55"
  },
  {
    "id": "b47d6afa-e2ea-4c1d-95e0-467c72b072fc",
    "name": "Mercenary Hex 2",
    "biography": {
      "id": "57e93213-1d6f-4517-8e16-4af2aa0c4405",
      "created_at": "2024-12-25T10:42:17.287000Z",
      "updated_at": "2024-12-25T10:44:41.890000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_1DW7dTv.PNG",
      "character": "b47d6afa-e2ea-4c1d-95e0-467c72b072fc"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cada0c14"
  },
  {
    "id": "b4ffcd3d-b4ba-429b-bb48-e19083c740c3",
    "name": "Zeus Prime 00 4",
    "biography": {
      "id": "e564c3e9-79cd-4ff1-be2d-01298b996548",
      "created_at": "2024-12-25T12:24:23.707000Z",
      "updated_at": "2024-12-25T12:24:23.707000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "b4ffcd3d-b4ba-429b-bb48-e19083c740c3"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafe22b9"
  },
  {
    "id": "b5bf0705-1679-4588-a7d6-df8b7b5c38fb",
    "name": "Mercenary Hex 3",
    "biography": {
      "id": "7313465a-60cb-418e-bd42-c001ee00669a",
      "created_at": "2024-12-25T10:42:17.894000Z",
      "updated_at": "2024-12-25T10:44:42.150000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_kGhR3v4.PNG",
      "character": "b5bf0705-1679-4588-a7d6-df8b7b5c38fb"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cadbb206"
  },
  {
    "id": "b70a252b-769f-427b-b7b1-4a6ff824bd19",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "099a81e0-99b1-4ce3-9a84-f7637ba40730",
      "created_at": "2024-12-25T10:42:17.310000Z",
      "updated_at": "2024-12-25T10:44:42.547000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_yYZ9lPG.PNG",
      "character": "b70a252b-769f-427b-b7b1-4a6ff824bd19"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cada9c52"
  },
  {
    "id": "b75c1d9c-26a9-4819-b0d6-0aebc0c6917f",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "bba78749-8eda-4def-b638-f485c533ee5e",
      "created_at": "2024-12-25T12:24:20.650000Z",
      "updated_at": "2024-12-25T12:24:20.650000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "b75c1d9c-26a9-4819-b0d6-0aebc0c6917f"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf08060"
  },
  {
    "id": "b805cb2f-c9e0-4175-8781-60b2e7956745",
    "name": "Mercenary Hex 2",
    "biography": {
      "id": "ccf88b2c-9cd3-428a-86d3-cb462f79f0b6",
      "created_at": "2024-12-25T10:42:18.697000Z",
      "updated_at": "2024-12-25T10:44:42.658000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_PvAVDUN.PNG",
      "character": "b805cb2f-c9e0-4175-8781-60b2e7956745"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae63a37"
  },
  {
    "id": "b8a03ba9-d6fd-4a53-89e6-2b76706eaf96",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "3eb27e47-33c9-4b2f-b5b3-e3e7602f3b74",
      "created_at": "2024-12-25T12:24:20.922000Z",
      "updated_at": "2024-12-25T12:24:20.922000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "b8a03ba9-d6fd-4a53-89e6-2b76706eaf96"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf4fcb2"
  },
  {
    "id": "b8ab21ca-391b-4c9e-badf-a0d033c57938",
    "name": "Mercenary Hex 6",
    "biography": {
      "id": "7eee9629-9308-45de-81d3-04deeedbfa21",
      "created_at": "2024-12-25T10:42:20.885000Z",
      "updated_at": "2024-12-25T10:44:42.828000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_nvWiBB1.PNG",
      "character": "b8ab21ca-391b-4c9e-badf-a0d033c57938"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb0ad298"
  },
  {
    "id": "b967642c-230b-4953-bc65-1906c9292e50",
    "name": "Zeus Prime 00 6",
    "biography": {
      "id": "94ba9458-3892-4867-9837-d3eb0ab16394",
      "created_at": "2024-12-25T12:24:21.614000Z",
      "updated_at": "2024-12-25T12:24:21.614000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "b967642c-230b-4953-bc65-1906c9292e50"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf5e8d7"
  },
  {
    "id": "b99e19f8-f1e0-4b44-8a90-15fdf64678bd",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "909c9150-094d-4461-bfb0-3b24c534fc46",
      "created_at": "2024-12-25T12:24:23.691000Z",
      "updated_at": "2024-12-25T12:24:23.691000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "b99e19f8-f1e0-4b44-8a90-15fdf64678bd"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafe22b9"
  },
  {
    "id": "b9f42c9c-f23d-4229-acc1-e770a42ea005",
    "name": "Zeus Prime 00 6",
    "biography": {
      "id": "46dddabe-fef2-45e1-ae24-b2a883907be9",
      "created_at": "2024-12-25T12:24:22.504000Z",
      "updated_at": "2024-12-25T12:24:22.504000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "b9f42c9c-f23d-4229-acc1-e770a42ea005"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf8eca9"
  },
  {
    "id": "bbe9bcfc-1a6e-425b-97dd-80d795cbc6af",
    "name": "Damon Shade",
    "biography": {
      "id": "5ea37ef0-216d-4010-bead-52757dccf3e8",
      "created_at": "2024-12-24T12:35:51.430000Z",
      "updated_at": "2024-12-24T12:43:47.400000Z",
      "age": 32,
      "gender": "Other",
      "background": "Damon is the squad’s infiltrator, excelling at stealth and reconnaissance. His ability to slip past enemy lines undetected has earned him a reputation as a ghost on the battlefield.",
      "appearance": "A wiry man clad in dark tactical gear, with sharp features and a calculating gaze. His movements are quiet and deliberate.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_qxbXQmw.PNG",
      "character": "bbe9bcfc-1a6e-425b-97dd-80d795cbc6af"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Infiltrator",
      "Stealth Specialist"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "bc907e6a-5e82-4664-a8d6-9e64c5f73312",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "c9455e1b-a1bf-4b02-83d2-87965306bd8f",
      "created_at": "2024-12-25T12:24:20.899000Z",
      "updated_at": "2024-12-25T12:24:20.899000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "bc907e6a-5e82-4664-a8d6-9e64c5f73312"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf4439d"
  },
  {
    "id": "be6542ea-0017-4f27-8c30-38f42613aebc",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "439dc52c-ee5b-4c2b-a97d-f8c3cab656c3",
      "created_at": "2024-12-25T12:24:22.720000Z",
      "updated_at": "2024-12-25T12:24:22.720000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "be6542ea-0017-4f27-8c30-38f42613aebc"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafa744f"
  },
  {
    "id": "be918e7f-87f9-4cc0-92c3-0828ee00fdcd",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "1176dbb1-1e49-4eb5-ba79-beb9005dd6f4",
      "created_at": "2024-12-25T12:24:22.712000Z",
      "updated_at": "2024-12-25T12:24:22.712000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "be918e7f-87f9-4cc0-92c3-0828ee00fdcd"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafa744f"
  },
  {
    "id": "beb2db53-3c21-4527-8522-dcf5159242e7",
    "name": "Mercenary Hex 3",
    "biography": {
      "id": "f0007f9b-1997-4a52-a853-81ad9af10e4a",
      "created_at": "2024-12-25T10:42:18.587000Z",
      "updated_at": "2024-12-25T10:44:43.011000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_Cbgr2aw.PNG",
      "character": "beb2db53-3c21-4527-8522-dcf5159242e7"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cade1f26"
  },
  {
    "id": "bf3b1e49-4729-41e8-a7ec-c8db703df4e6",
    "name": "Zeus Prime 00 4",
    "biography": {
      "id": "f6eac067-4925-4fd3-980f-c520155ebd97",
      "created_at": "2024-12-25T12:24:21.599000Z",
      "updated_at": "2024-12-25T12:24:21.599000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "bf3b1e49-4729-41e8-a7ec-c8db703df4e6"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf5e8d7"
  },
  {
    "id": "c0424fa3-87a9-47d2-ae5b-13e11d9ccc2e",
    "name": "Nancy Flair",
    "biography": {
      "id": "08e9887e-7bc6-455a-af31-759aded2d05a",
      "created_at": "2024-12-24T11:21:50.328000Z",
      "updated_at": "2024-12-24T11:22:13.512000Z",
      "age": 24,
      "gender": "Other",
      "background": "Nancy Flair is a lively and sharp-tongued waitress at the Misfits Pub. Having grown up in the City of Memories, she’s no stranger to the chaos that often erupts around the pub. Known for her quick wit and charm, Nancy is skilled at defusing tense situations and entertaining patrons with her banter. While she keeps her past private, her deep knowledge of the city and its lore hints at a more adventurous past.",
      "appearance": "A petite, energetic young woman with a playful smile and vibrant red hair tied up in a messy bun. She wears a simple yet stylish apron adorned with patches and magical trinkets, hinting at her quirky personality.",
      "avatar": "http://localhost:8000/media/avatars/53C76BE8-3581-4DA1-9565-B80CB3C17FA7.PNG",
      "character": "c0424fa3-87a9-47d2-ae5b-13e11d9ccc2e"
    },
    "npc": true,
    "rank": {
      "name": "Elite Champion",
      "grade": 4,
      "experience_needed": 34080
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 34081,
    "tags": [
      "Misfits Pub Staff",
      "Waiter",
      "Charismatic"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "a25ca87a-f59d-4497-9b16-fb97ec8ef4e2",
      "name": "Misfits Pub (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb143b50"
  },
  {
    "id": "c0a70680-a416-468b-a2e4-241fe041c10d",
    "name": "Kaelion Stormspire",
    "biography": {
      "id": "1480b649-0ea8-4d30-8b6b-ec7eee1b76dc",
      "created_at": "2024-12-24T13:22:26.297000Z",
      "updated_at": "2024-12-24T13:25:06.562000Z",
      "age": 29,
      "gender": "Male",
      "background": "Kaelion Stormspire is a prodigy of the Pure Energy School, channeling raw, unfiltered Flow into devastating attacks and efficient utilities. Born in a high-energy dimensional rift, he learned to harness and control the volatile forces that shaped his environment. Known for his precision and intensity, Kaelion is both a scholar and a formidable combatant.",
      "appearance": "A tall figure with strikingly bright white hair that crackles with faint energy. His piercing silver eyes seem to glow with unrestrained power, and he wears a sleek, form-fitting outfit infused with Flow conduits.",
      "avatar": "http://localhost:8000/media/avatars/E135DB4F-25EC-424F-BB68-B717AC9CF9D9.PNG",
      "character": "c0a70680-a416-468b-a2e4-241fe041c10d"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Energy Mage",
      "Flow Manipulator",
      "Pure Energy Specialist"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "9fd27c2f-246d-4f37-86e7-645689cc9d39",
      "name": "Three of magitians (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeee519"
  },
  {
    "id": "c1fa8331-8210-4a36-9bd1-12ccb1254d41",
    "name": "Mercenary Hex 5",
    "biography": {
      "id": "906556b6-1910-48e3-8d28-2eb043f320af",
      "created_at": "2024-12-25T10:42:18.067000Z",
      "updated_at": "2024-12-25T10:44:43.170000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_tTAwFSZ.PNG",
      "character": "c1fa8331-8210-4a36-9bd1-12ccb1254d41"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cadbb206"
  },
  {
    "id": "c2cd0205-4d4d-4f45-94c0-5d8019d6ad5b",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "d4e9111a-7e89-4b49-bfcd-3dd87effa432",
      "created_at": "2024-12-25T10:42:19.701000Z",
      "updated_at": "2024-12-25T10:44:43.310000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_AvisatA.PNG",
      "character": "c2cd0205-4d4d-4f45-94c0-5d8019d6ad5b"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeaa236"
  },
  {
    "id": "c34797a8-bb3d-4950-bb16-3b40e1539bab",
    "name": "Cursed Rat",
    "biography": {
      "id": "40a658f4-21da-4b87-aa7f-65d37e81e05f",
      "created_at": "2024-12-25T10:13:44.691000Z",
      "updated_at": "2024-12-25T10:14:57.655000Z",
      "age": 18,
      "gender": "Other",
      "background": "Once an ordinary denizen of the undercity, this rat was cursed by a surge of corrupted Flow energy. Now a shadow of its former self, the Cursed Rat prowls dark alleys and ruins, spreading fear and decay wherever it goes. It is said that its very touch corrupts, making it a dangerous foe to encounter.",
      "appearance": "A dark, ragged rat-like creature with glowing red cracks running along its fur. Its eyes emit a sinister red glow, and its jagged tail radiates dark energy pulses. The creature’s presence feels ominous and unnatural, blending stealth and menace in its movements.",
      "avatar": "http://localhost:8000/media/avatars/BF090231-4674-493F-9818-428AA54CE9D6.webp",
      "character": "c34797a8-bb3d-4950-bb16-3b40e1539bab"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Cursed",
      "Rat",
      "Flow-Touched",
      "Dark Entity"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "3135c8b9-3220-4a1c-ad59-69cc12f41ce8",
      "name": "Miracle Creatures (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae659ce"
  },
  {
    "id": "c49b83dc-caad-4ba3-be79-49fd4d36ee00",
    "name": "Mercenary Hex 4",
    "biography": {
      "id": "65383be8-1ccd-420b-8ee7-4ba8c59ed065",
      "created_at": "2024-12-25T10:42:19.996000Z",
      "updated_at": "2024-12-25T10:44:43.439000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_Wb1Joai.PNG",
      "character": "c49b83dc-caad-4ba3-be79-49fd4d36ee00"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9e60"
  },
  {
    "id": "c537a8c7-2004-4afe-8480-cbdfd0eb374b",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "ca634b66-6890-4037-8faa-3f25364f4c22",
      "created_at": "2024-12-25T12:24:23.607000Z",
      "updated_at": "2024-12-25T12:24:23.607000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "c537a8c7-2004-4afe-8480-cbdfd0eb374b"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafdf1c3"
  },
  {
    "id": "c59c5a47-84be-4b34-b095-989a015ba612",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "fde5f2f4-6a74-408b-96fa-8dff167d5c1e",
      "created_at": "2024-12-25T12:24:20.647000Z",
      "updated_at": "2024-12-25T12:24:20.647000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "c59c5a47-84be-4b34-b095-989a015ba612"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf08060"
  },
  {
    "id": "c6f606a2-a999-41d6-af67-e55e8c5ad990",
    "name": "Alyssa Gearwright",
    "biography": {
      "id": "861afede-1590-4017-af9a-20754f91071b",
      "created_at": "2024-12-24T12:49:07.816000Z",
      "updated_at": "2024-12-24T12:49:30.391000Z",
      "age": 23,
      "gender": "Other",
      "background": "Alyssa Gearwright is a prodigy in Flow-integrated technology, inventing devices that seem to defy the laws of physics. Born into a modest family, her talent was recognized at an early age, earning her a reputation as a technological miracle worker. Despite her brilliance, Alyssa remains humble and quirky, often lost in her own world of gadgets and ideas.",
      "appearance": "A petite girl with vibrant pink hair tied in twin tails, her goggles perched on her forehead and her fingers constantly tinkering with gadgets. She wears a jumpsuit covered in smudges of oil and Flow energy residue.",
      "avatar": "http://localhost:8000/media/avatars/546A44BD-F72C-40AC-9C89-2B86691028A5.PNG",
      "character": "c6f606a2-a999-41d6-af67-e55e8c5ad990"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Tech Genius",
      "Inventor",
      "Flow Engineer"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": null,
    "position_id": "00000000-0000-0000-0000-0193caf73da5"
  },
  {
    "id": "c7382484-2d45-472d-b480-bca4fe1aef93",
    "name": "Zeus Prime 00 4",
    "biography": {
      "id": "c041b491-16b6-4189-bb42-89f42c5e18fe",
      "created_at": "2024-12-25T12:24:20.873000Z",
      "updated_at": "2024-12-25T12:24:20.873000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "c7382484-2d45-472d-b480-bca4fe1aef93"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf2e872"
  },
  {
    "id": "c7dce18e-d38d-4c7d-82b9-0754cc04b521",
    "name": "Talon Ironspire",
    "biography": {
      "id": "acf5341a-1f09-471f-bdc7-0444c6b49e11",
      "created_at": "2024-12-24T12:37:22.240000Z",
      "updated_at": "2024-12-24T12:43:47.410000Z",
      "age": 28,
      "gender": "Other",
      "background": "Talon is the squad’s demolitions expert, specializing in breaching fortifications and setting traps. His destructive tendencies are matched only by his reliability in the field.",
      "appearance": "A muscular figure with soot-streaked armor and a mischievous grin. Explosives hang from his belt, ready to detonate at a moment’s notice.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_Bl6nsf3.PNG",
      "character": "c7dce18e-d38d-4c7d-82b9-0754cc04b521"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Muscle"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "c9f1fe2c-e995-4538-92cb-c452d1d7c630",
    "name": "Kaelen Vrynn",
    "biography": {
      "id": "e1486920-df2d-4c94-82ea-341c3cc3eba9",
      "created_at": "2024-12-24T12:58:37.867000Z",
      "updated_at": "2024-12-24T12:58:58.524000Z",
      "age": 26,
      "gender": "Other",
      "background": "Kaelen is the second apprentice to Malrick, often acting as Elyra’s rival in their master’s lessons. While he is reckless and impulsive, his raw talent in blood magic makes him a rising force within their trio.",
      "appearance": "A lean young man with pale skin and jet-black hair that falls over his glowing crimson eyes. His robes are tattered, yet the blood runes etched on them radiate power.",
      "avatar": "http://localhost:8000/media/avatars/5972A363-4612-4E57-971B-A4E7BEDF5471.PNG",
      "character": "c9f1fe2c-e995-4538-92cb-c452d1d7c630"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Blood Mage",
      "Apprentice",
      "Dark Sorcerer"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "27c7c780-cd43-44c9-800f-13f4a131488e",
      "name": "Blood Hunters (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caefcdf2"
  },
  {
    "id": "ca484b6a-0480-4c9c-b894-5e644f56f43e",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "b06d5d91-1e3c-4733-93fa-3c37f9e1e2f7",
      "created_at": "2024-12-25T12:24:20.408000Z",
      "updated_at": "2024-12-25T12:24:20.409000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "ca484b6a-0480-4c9c-b894-5e644f56f43e"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caee229f"
  },
  {
    "id": "caa74be3-f068-4b56-b811-6f3a9ba59c5e",
    "name": "Zeus Prime 00 4",
    "biography": {
      "id": "0fd37b7f-a8a3-4a9d-b681-3d6dfd00156c",
      "created_at": "2024-12-25T12:24:22.614000Z",
      "updated_at": "2024-12-25T12:24:22.614000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "caa74be3-f068-4b56-b811-6f3a9ba59c5e"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf924e2"
  },
  {
    "id": "cb89ccc9-ff71-420e-b4bd-6cecc50da13c",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "679b4c71-82ef-4c6d-b6ab-30ca8c7425d2",
      "created_at": "2024-12-25T12:24:20.640000Z",
      "updated_at": "2024-12-25T12:24:20.640000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "cb89ccc9-ff71-420e-b4bd-6cecc50da13c"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf08060"
  },
  {
    "id": "cc25ca40-ba23-4f81-a93f-e6f7e14e2a3d",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "c9318964-d4c4-4acb-9418-ddcad918631c",
      "created_at": "2024-12-25T12:24:20.413000Z",
      "updated_at": "2024-12-25T12:24:20.414000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "cc25ca40-ba23-4f81-a93f-e6f7e14e2a3d"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caee229f"
  },
  {
    "id": "cc5cc916-9145-4275-8d3f-54f4249bf287",
    "name": "Mercenary Hex 4",
    "biography": {
      "id": "f0ace5bc-12a2-42b5-94db-4ee875f6650c",
      "created_at": "2024-12-25T10:42:18.897000Z",
      "updated_at": "2024-12-25T10:44:43.582000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_LZswhPK.PNG",
      "character": "cc5cc916-9145-4275-8d3f-54f4249bf287"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae7d299"
  },
  {
    "id": "ccccace3-07c7-41d5-8512-68782b5364ca",
    "name": "Zeus Prime 00 5",
    "biography": {
      "id": "b049542e-c767-42ce-a5ba-e80442ee83cf",
      "created_at": "2024-12-25T12:24:23.676000Z",
      "updated_at": "2024-12-25T12:24:23.676000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "ccccace3-07c7-41d5-8512-68782b5364ca"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafdff09"
  },
  {
    "id": "ccf6ee99-5d6c-4d17-b669-f4a96501f1ea",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "8d9f0675-4ce9-445f-9bb3-39e4d647da18",
      "created_at": "2024-12-25T12:24:21.469000Z",
      "updated_at": "2024-12-25T12:24:21.469000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "ccf6ee99-5d6c-4d17-b669-f4a96501f1ea"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf51a85"
  },
  {
    "id": "cd1c9be2-6133-4178-91d3-234d5816a1ce",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "eaf74991-878c-40ec-ba1c-129e95ea6dca",
      "created_at": "2024-12-25T12:24:20.717000Z",
      "updated_at": "2024-12-25T12:24:20.717000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "cd1c9be2-6133-4178-91d3-234d5816a1ce"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf10277"
  },
  {
    "id": "cd30f7ac-66a5-4225-a4ec-06e982a76f3a",
    "name": "Mercenary Hex 5",
    "biography": {
      "id": "45e53db8-09b8-495c-abc5-880e50432b51",
      "created_at": "2024-12-25T10:42:20.882000Z",
      "updated_at": "2024-12-25T10:44:43.682000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_8MYViE1.PNG",
      "character": "cd30f7ac-66a5-4225-a4ec-06e982a76f3a"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb0ad298"
  },
  {
    "id": "cd78fbaf-ccdc-40c9-a909-65fee5d7defb",
    "name": "Mercenary Hex 2",
    "biography": {
      "id": "39157dc8-2141-437c-ac3d-1ca977585c05",
      "created_at": "2024-12-25T10:42:19.868000Z",
      "updated_at": "2024-12-25T10:44:43.769000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_HXD6sfg.PNG",
      "character": "cd78fbaf-ccdc-40c9-a909-65fee5d7defb"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb8fc4"
  },
  {
    "id": "ce1fef40-aca4-48b6-9996-bea2db123d62",
    "name": "Alex Forge",
    "biography": {
      "id": "3d39dee6-72c1-4ee5-9af3-9cec27d64477",
      "created_at": "2024-12-24T11:24:17.775000Z",
      "updated_at": "2024-12-24T11:24:56.994000Z",
      "age": 38,
      "gender": "Other",
      "background": "Alex Forge, the bartender of the Misfits Pub, is a former mercenary who left his adventurous life behind after a disastrous mission in the 4th dimension. With years of experience navigating the chaos of battles and negotiations, Alex is a natural at managing the diverse and often unruly patrons of the pub. While he rarely talks about his past, he’s a well of knowledge for those who earn his trust.",
      "appearance": "A tall, broad-shouldered man with a rugged face and a thick black beard. His piercing blue eyes and scarred arms hint at a dangerous past. Alex wears a practical black apron over a faded leather jacket, adding to his imposing yet approachable demeanor.",
      "avatar": "http://localhost:8000/media/avatars/7AD52CF6-CB1D-4A76-B6D9-A125A067B7B2.PNG",
      "character": "ce1fef40-aca4-48b6-9996-bea2db123d62"
    },
    "npc": true,
    "rank": {
      "name": "Hero",
      "grade": 3,
      "experience_needed": 66260
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 66261,
    "tags": [
      "Misfits Pub Staff",
      "Bartender",
      "Ex-Mercenary"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "a25ca87a-f59d-4497-9b16-fb97ec8ef4e2",
      "name": "Misfits Pub (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb13c612"
  },
  {
    "id": "ce490809-feac-4d98-b742-424b2ae4ce13",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "48cb87f5-17a6-4f1e-9196-30bf9fe349cf",
      "created_at": "2024-12-25T10:42:18.709000Z",
      "updated_at": "2024-12-25T10:44:43.859000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_DYvpBTX.PNG",
      "character": "ce490809-feac-4d98-b742-424b2ae4ce13"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae74146"
  },
  {
    "id": "d06d58df-6eb7-4d5c-91cf-6380e33fed71",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "852deada-54c8-49a2-bd61-6f5f2f8eb873",
      "created_at": "2024-12-25T12:24:20.753000Z",
      "updated_at": "2024-12-25T12:24:20.753000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "d06d58df-6eb7-4d5c-91cf-6380e33fed71"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf10277"
  },
  {
    "id": "d0bb37bb-004a-4d47-9645-35624ae42236",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "82464076-5d42-416d-93e7-48a68c5094ba",
      "created_at": "2024-12-25T12:24:22.593000Z",
      "updated_at": "2024-12-25T12:24:22.593000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "d0bb37bb-004a-4d47-9645-35624ae42236"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf924e2"
  },
  {
    "id": "d0c86523-6960-4766-bd6d-77551ae9502a",
    "name": "Zeus Prime 00 7",
    "biography": {
      "id": "de22666f-9921-4a0a-a51e-18583f1ba8d4",
      "created_at": "2024-12-25T12:24:22.510000Z",
      "updated_at": "2024-12-25T12:24:22.511000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "d0c86523-6960-4766-bd6d-77551ae9502a"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf8eca9"
  },
  {
    "id": "d130a657-8381-4194-9a82-b01229f48b1e",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "69b2f482-69ca-4676-b1af-dc830dfbfa98",
      "created_at": "2024-12-25T12:24:21.512000Z",
      "updated_at": "2024-12-25T12:24:21.512000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "d130a657-8381-4194-9a82-b01229f48b1e"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf5b7c4"
  },
  {
    "id": "d1317c03-36fc-4de7-9cb9-f3f0495e0b4d",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "bb4cfc67-5c34-451c-b42e-8283fb7e481b",
      "created_at": "2024-12-25T10:42:17.223000Z",
      "updated_at": "2024-12-25T10:44:43.923000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_kAg6Dch.PNG",
      "character": "d1317c03-36fc-4de7-9cb9-f3f0495e0b4d"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cada0c14"
  },
  {
    "id": "d19ec216-8f21-499b-b62f-c5ebc3f535b9",
    "name": "Zeus Prime 00 5",
    "biography": {
      "id": "45008351-e9fb-4361-8073-11fe5dde8b90",
      "created_at": "2024-12-25T12:24:20.823000Z",
      "updated_at": "2024-12-25T12:24:20.823000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "d19ec216-8f21-499b-b62f-c5ebc3f535b9"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf1a4de"
  },
  {
    "id": "d1a84aa9-a237-4acb-a5a0-d108971227cc",
    "name": "Mercenary Hex 3",
    "biography": {
      "id": "7e183ccb-309c-4b48-a0b5-2e15b444acbc",
      "created_at": "2024-12-25T10:42:20.874000Z",
      "updated_at": "2024-12-25T10:44:43.968000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_mfhRcgv.PNG",
      "character": "d1a84aa9-a237-4acb-a5a0-d108971227cc"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb0ad298"
  },
  {
    "id": "d29b7544-3751-41f2-84bd-bf51f63253ef",
    "name": "Mercenary Hex 7",
    "biography": {
      "id": "970e5c10-1c28-4f24-bbc8-6a641b7f7ea7",
      "created_at": "2024-12-25T10:42:18.908000Z",
      "updated_at": "2024-12-25T10:44:44.168000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_16hLbfN.PNG",
      "character": "d29b7544-3751-41f2-84bd-bf51f63253ef"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae7d299"
  },
  {
    "id": "d2e03181-8a0a-41cd-885b-ad23ab2e341c",
    "name": "Zeus Prime 00 5",
    "biography": {
      "id": "da74ebbe-9af1-4b5e-b8fb-2111582ad21f",
      "created_at": "2024-12-25T12:24:23.711000Z",
      "updated_at": "2024-12-25T12:24:23.711000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "d2e03181-8a0a-41cd-885b-ad23ab2e341c"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafe22b9"
  },
  {
    "id": "d3b107ac-e524-479a-80b1-77af04d8f45b",
    "name": "Zeus Prime 00 7",
    "biography": {
      "id": "d3745f3a-647a-4cab-99ce-f38aff348483",
      "created_at": "2024-12-25T12:24:21.621000Z",
      "updated_at": "2024-12-25T12:24:21.621000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "d3b107ac-e524-479a-80b1-77af04d8f45b"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf5e8d7"
  },
  {
    "id": "d3c9c36e-8100-4e0a-b25d-70998f4de0b4",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "ce5badcd-c34a-41e3-9c23-9e3813afd93e",
      "created_at": "2024-12-25T12:24:21.676000Z",
      "updated_at": "2024-12-25T12:24:21.676000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "d3c9c36e-8100-4e0a-b25d-70998f4de0b4"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf616e3"
  },
  {
    "id": "d405edf0-80f9-41a7-9e48-db5d5bc18312",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "9034a1e4-06ce-4a6e-a337-eaf63d7178d1",
      "created_at": "2024-12-25T12:24:23.697000Z",
      "updated_at": "2024-12-25T12:24:23.697000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "d405edf0-80f9-41a7-9e48-db5d5bc18312"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafe22b9"
  },
  {
    "id": "d43df975-fc76-447e-87cd-e9e100e5eae1",
    "name": "Zeus Prime 00 9",
    "biography": {
      "id": "0f3c5602-97b6-4f8a-88f0-656f28d7f60e",
      "created_at": "2024-12-25T12:24:20.614000Z",
      "updated_at": "2024-12-25T12:24:20.614000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "d43df975-fc76-447e-87cd-e9e100e5eae1"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf00f84"
  },
  {
    "id": "d514ab37-9961-4e1c-8a74-2024b04a0aa5",
    "name": "Zeus Prime 00 9",
    "biography": {
      "id": "077af5c7-4129-4ae0-9875-8c3a3ec02f00",
      "created_at": "2024-12-25T12:24:21.632000Z",
      "updated_at": "2024-12-25T12:24:21.632000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "d514ab37-9961-4e1c-8a74-2024b04a0aa5"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf5e8d7"
  },
  {
    "id": "d5562c44-0692-44d5-ae51-acb00b0f9821",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "ab3d5f53-34ce-4d9c-be77-81e7892a5b47",
      "created_at": "2024-12-25T12:24:20.868000Z",
      "updated_at": "2024-12-25T12:24:20.869000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "d5562c44-0692-44d5-ae51-acb00b0f9821"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf2e872"
  },
  {
    "id": "d5bff4ed-431a-4d2e-97a6-0f3706372b37",
    "name": "Kara Stonefist",
    "biography": {
      "id": "c0ddd08d-6c70-4252-ba63-3ed3b6f9448f",
      "created_at": "2024-12-24T12:34:10.263000Z",
      "updated_at": "2024-12-24T12:43:47.415000Z",
      "age": 29,
      "gender": "Other",
      "background": "Kara thrives in close combat, often charging headfirst into fights to protect her team. Her blunt attitude and fierce loyalty make her an indispensable ally in battle.",
      "appearance": "A muscular woman with short-cropped hair and a confident stride. Her knuckles are wrapped in worn bandages, and her armor is dented from countless brawls.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_BjjNZ3Z.PNG",
      "character": "d5bff4ed-431a-4d2e-97a6-0f3706372b37"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Brawler",
      "Close Combat Specialist"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "d61b8255-6d94-4515-aada-0c9d9037823e",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "67e18ed5-efa0-4a70-a8d8-369fe1fd9183",
      "created_at": "2024-12-25T12:24:20.854000Z",
      "updated_at": "2024-12-25T12:24:20.854000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "d61b8255-6d94-4515-aada-0c9d9037823e"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf2e872"
  },
  {
    "id": "d8663faa-724b-4069-a6b8-8cf000c9977d",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "cd6c3609-567e-4d28-a28c-a8f97056f4f3",
      "created_at": "2024-12-25T10:42:19.825000Z",
      "updated_at": "2024-12-25T10:44:44.397000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_0V7jN0A.PNG",
      "character": "d8663faa-724b-4069-a6b8-8cf000c9977d"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb27a9"
  },
  {
    "id": "d8fce35b-1755-4986-9adc-a983fd82c4a7",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "8d6e9e92-3f30-47ef-8b1b-4e6af9d824cb",
      "created_at": "2024-12-25T12:24:22.607000Z",
      "updated_at": "2024-12-25T12:24:22.608000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "d8fce35b-1755-4986-9adc-a983fd82c4a7"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf924e2"
  },
  {
    "id": "d96f9140-a15c-4413-a510-585c5b5653bf",
    "name": "Mercenary Hex 4",
    "biography": {
      "id": "5f5903a0-e611-47f4-a4d0-9e9d6f39063b",
      "created_at": "2024-12-25T10:42:20.878000Z",
      "updated_at": "2024-12-25T10:44:44.794000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_F488VZn.PNG",
      "character": "d96f9140-a15c-4413-a510-585c5b5653bf"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb0ad298"
  },
  {
    "id": "d99c7171-40eb-4681-999e-f8fe8a5133c1",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "36e1fdb9-493c-481d-ba58-5a7f32b65ee7",
      "created_at": "2024-12-25T10:42:19.270000Z",
      "updated_at": "2024-12-25T10:44:44.903000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_MYC2xft.PNG",
      "character": "d99c7171-40eb-4681-999e-f8fe8a5133c1"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae9b356"
  },
  {
    "id": "d9f57a25-d020-49cb-b222-e971793ead81",
    "name": "Mercenary Hex 2",
    "biography": {
      "id": "168a9781-e10f-4f03-b850-792b931244d8",
      "created_at": "2024-12-25T10:42:18.796000Z",
      "updated_at": "2024-12-25T10:44:44.994000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_TurNIRR.PNG",
      "character": "d9f57a25-d020-49cb-b222-e971793ead81"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae765b7"
  },
  {
    "id": "da321dfd-1464-412e-9647-97b52ca1f9ef",
    "name": "Zeus Prime 00 6",
    "biography": {
      "id": "519b7e80-24d6-4ba5-b328-2e45959cf3bf",
      "created_at": "2024-12-25T12:24:23.147000Z",
      "updated_at": "2024-12-25T12:24:23.148000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "da321dfd-1464-412e-9647-97b52ca1f9ef"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafdd31e"
  },
  {
    "id": "dbcd033d-db44-41c4-99ff-a24ea334bb66",
    "name": "Zeus Prime 00 4",
    "biography": {
      "id": "6f87c7cc-4151-43c4-8580-78206c848360",
      "created_at": "2024-12-25T12:24:22.800000Z",
      "updated_at": "2024-12-25T12:24:22.800000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "dbcd033d-db44-41c4-99ff-a24ea334bb66"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafaa0ee"
  },
  {
    "id": "dc7fcaff-8f6b-4091-8024-9be7f2c8fc69",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "0525b222-ec0f-4669-9335-f0b4d002fdbd",
      "created_at": "2024-12-25T12:24:22.600000Z",
      "updated_at": "2024-12-25T12:24:22.600000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "dc7fcaff-8f6b-4091-8024-9be7f2c8fc69"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf924e2"
  },
  {
    "id": "dcc5a419-fd23-4d2e-9787-4cc22294cd4b",
    "name": "Zeus Prime 00 1",
    "biography": {
      "id": "11c0744d-68e6-4ed6-bbb7-652dc0ca1f50",
      "created_at": "2024-12-25T12:24:20.510000Z",
      "updated_at": "2024-12-25T12:24:20.510000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "dcc5a419-fd23-4d2e-9787-4cc22294cd4b"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caef9bef"
  },
  {
    "id": "dd5b00df-34b1-46c7-a81a-0dfa551375ac",
    "name": "Zeus Prime 00 7",
    "biography": {
      "id": "dd09aa71-6dad-41ea-a12e-c052e91d7932",
      "created_at": "2024-12-25T12:24:20.607000Z",
      "updated_at": "2024-12-25T12:24:20.607000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "dd5b00df-34b1-46c7-a81a-0dfa551375ac"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf00f84"
  },
  {
    "id": "ddc79c49-14b6-4234-865d-da936d539590",
    "name": "Mercenary Hex 4",
    "biography": {
      "id": "75ce60b1-e230-41d5-bca4-6527a3bd9e1d",
      "created_at": "2024-12-25T10:42:18.003000Z",
      "updated_at": "2024-12-25T10:44:45.164000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_vvdvFsC.PNG",
      "character": "ddc79c49-14b6-4234-865d-da936d539590"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cadbb206"
  },
  {
    "id": "dde4f231-fb90-4ceb-a059-3a7671953496",
    "name": "Zeus Prime 00 4",
    "biography": {
      "id": "3cc2de70-1756-44da-9ec2-d615ea3c4030",
      "created_at": "2024-12-25T12:24:20.757000Z",
      "updated_at": "2024-12-25T12:24:20.757000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "dde4f231-fb90-4ceb-a059-3a7671953496"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf10277"
  },
  {
    "id": "df94ee01-816f-4685-9d81-2288a1c623dd",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "b347b4f2-2e30-4a3e-a5bd-31375f656db5",
      "created_at": "2024-12-25T10:42:19.983000Z",
      "updated_at": "2024-12-25T10:44:45.273000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_ZArOvmX.PNG",
      "character": "df94ee01-816f-4685-9d81-2288a1c623dd"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9e60"
  },
  {
    "id": "e10a5d04-8860-4d13-8c46-8e0dd85063bb",
    "name": "Zeus Prime 00 3",
    "biography": {
      "id": "03752140-33d2-4b77-9890-d90e14c0696d",
      "created_at": "2024-12-25T12:24:21.475000Z",
      "updated_at": "2024-12-25T12:24:21.475000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "e10a5d04-8860-4d13-8c46-8e0dd85063bb"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf51a85"
  },
  {
    "id": "e32f630a-0636-4657-893b-5864277a6cd3",
    "name": "Axel Steelguard",
    "biography": {
      "id": "71629797-50e1-47a4-b7c8-6feeeb0876c6",
      "created_at": "2024-12-24T11:19:26.739000Z",
      "updated_at": "2024-12-24T11:19:47.026000Z",
      "age": 28,
      "gender": "Other",
      "background": "Axel Steelguard serves as the head of security at the Misfits Pub, ensuring order in a place where adventurers, mercenaries, and rogues often converge. His past as a street fighter in the City of Memories honed his combat skills and discipline, eventually earning him recognition and his role at the pub. Known for his accuracy, strength, and no-nonsense demeanor, Axel commands respect and fear in equal measure.",
      "appearance": "A tall and imposing young man with short black hair and piercing gray eyes. His heavily augmented arms glow faintly with orange Flow energy, their mechanical precision a testament to cutting-edge technology. He wears a fitted security uniform, emphasizing his solid build and readiness to act.",
      "avatar": "http://localhost:8000/media/avatars/C7099B84-633E-4AE0-A1F6-DD65C4D48781.PNG",
      "character": "e32f630a-0636-4657-893b-5864277a6cd3"
    },
    "npc": true,
    "rank": {
      "name": "Veteran Champion",
      "grade": 4,
      "experience_needed": 40520
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 40521,
    "tags": [
      "Misfits Pub Security",
      "Augmented Enforcer",
      "Path of John"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "a25ca87a-f59d-4497-9b16-fb97ec8ef4e2",
      "name": "Misfits Pub (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb13c612"
  },
  {
    "id": "e37f65db-148b-4d54-a41e-0eb1507881ec",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "e7e1ef09-019a-4725-ad55-c33e6a1c437d",
      "created_at": "2024-12-25T10:42:19.458000Z",
      "updated_at": "2024-12-25T10:44:45.391000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_OGJztjY.PNG",
      "character": "e37f65db-148b-4d54-a41e-0eb1507881ec"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caea9038"
  },
  {
    "id": "e46b55e9-1143-483d-b252-278f03bd9244",
    "name": "Rhea Stonebreaker",
    "biography": {
      "id": "ccb4d220-3b68-4007-ae5f-b4f9f15eba46",
      "created_at": "2024-12-24T12:28:09.564000Z",
      "updated_at": "2024-12-24T12:43:47.419000Z",
      "age": 30,
      "gender": "Other",
      "background": "Rhea is a no-nonsense brawler who thrives in chaotic combat situations. Known for her raw strength and unwavering resolve, she often takes point in dangerous missions, clearing the way for her squadmates.",
      "appearance": "A stocky woman with a buzzed haircut and a grim expression. She wears reinforced body armor and wields a massive Flow-enhanced hammer.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_YzrxGKq.PNG",
      "character": "e46b55e9-1143-483d-b252-278f03bd9244"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Close Combat Specialist",
      "Hired Muscle"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "e4913747-9bce-44dc-a357-557dbe2efd3d",
    "name": "Mercenary Hex 4",
    "biography": {
      "id": "9b427958-3b30-4dfa-a1fd-b6c990426f2c",
      "created_at": "2024-12-25T10:42:19.056000Z",
      "updated_at": "2024-12-25T10:44:45.442000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_tfvpi5E.PNG",
      "character": "e4913747-9bce-44dc-a357-557dbe2efd3d"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae8b665"
  },
  {
    "id": "e4978d15-6944-4741-948f-1ff64434e575",
    "name": "Zeus Prime 00 8",
    "biography": {
      "id": "7906a9a8-ed1b-4ff4-961e-f1a269701c9d",
      "created_at": "2024-12-25T12:24:20.771000Z",
      "updated_at": "2024-12-25T12:24:20.771000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "e4978d15-6944-4741-948f-1ff64434e575"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf10277"
  },
  {
    "id": "e5c38d28-3da7-4b97-9e04-776b17351f58",
    "name": "Ronan Blackthorn",
    "biography": {
      "id": "c50e258b-e84f-49a6-8943-7efca636a87a",
      "created_at": "2024-12-24T12:35:27.994000Z",
      "updated_at": "2024-12-24T12:43:47.424000Z",
      "age": 36,
      "gender": "Other",
      "background": "Ronan is the squad’s heavy gunner, known for his ability to suppress enemies with overwhelming firepower. His stoic demeanor hides a fiercely loyal nature.",
      "appearance": "A burly man with a thick beard and a grizzled face. He wears heavy tactical armor and wields a massive Flow-powered machine gun.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_wfBTnxo.PNG",
      "character": "e5c38d28-3da7-4b97-9e04-776b17351f58"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Heavy Gunner",
      "Hired Muscle"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "e64cba7a-4ac3-469d-b5dd-d43511da7879",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "24723c75-93a1-47ba-ad50-0577f7a4f7b9",
      "created_at": "2024-12-25T10:42:19.037000Z",
      "updated_at": "2024-12-25T10:44:45.607000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_4Bd0lAK.PNG",
      "character": "e64cba7a-4ac3-469d-b5dd-d43511da7879"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae8b665"
  },
  {
    "id": "e944aecf-1e54-4b22-8807-cca1b9cae46a",
    "name": "Aegis Prime 00",
    "biography": {
      "id": "2a27589d-0ef4-4776-8f0f-6c36c0fc0507",
      "created_at": "2024-12-24T13:37:52.590000Z",
      "updated_at": "2024-12-24T13:43:18.662000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/047AF0FC-CF07-4499-B852-2FB729326D1C.webp",
      "character": "e944aecf-1e54-4b22-8807-cca1b9cae46a"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf08293"
  },
  {
    "id": "e9eb1abf-bfb7-4642-bc54-76747016f302",
    "name": "Sienna Flint",
    "biography": {
      "id": "46d3b278-a37f-406a-a98d-b8dcc1bf5e25",
      "created_at": "2024-12-24T12:30:40.031000Z",
      "updated_at": "2024-12-24T12:43:47.428000Z",
      "age": 29,
      "gender": "Other",
      "background": "Sienna is the squad’s combat medic and tactician, combining quick thinking with field medical expertise. Her ability to keep teammates alive under fire has earned her respect in countless battles.",
      "appearance": "A lean woman with short auburn hair and sharp features. She wears light armor designed for mobility, and her belt is lined with medical supplies and Flow-infused syringes.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_6F6phHf.PNG",
      "character": "e9eb1abf-bfb7-4642-bc54-76747016f302"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Tactician",
      "Combat Medic"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "ec366139-853c-4432-bb0a-7ab183aa74b8",
    "name": "Zeus Prime 00 5",
    "biography": {
      "id": "b20ee296-53f1-46c6-a9ee-3af7829e2233",
      "created_at": "2024-12-25T12:24:20.599000Z",
      "updated_at": "2024-12-25T12:24:20.600000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "ec366139-853c-4432-bb0a-7ab183aa74b8"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf00f84"
  },
  {
    "id": "ed38054b-f753-47c5-9acb-56aeab0affd0",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "d261f191-08d2-40d7-8cc4-2748145e5015",
      "created_at": "2024-12-25T10:42:20.435000Z",
      "updated_at": "2024-12-25T10:44:45.743000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_GFtjyY1.PNG",
      "character": "ed38054b-f753-47c5-9acb-56aeab0affd0"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caebb774"
  },
  {
    "id": "ed949185-bbfc-4f6c-8fcf-c5f97cb362d4",
    "name": "Mercenary Hex 8",
    "biography": {
      "id": "1f99593a-25b6-4222-baf6-463611c4c867",
      "created_at": "2024-12-25T10:42:19.957000Z",
      "updated_at": "2024-12-25T10:44:45.852000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_JeLhwIt.PNG",
      "character": "ed949185-bbfc-4f6c-8fcf-c5f97cb362d4"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "f150bf14-0a3d-42ed-936a-714169f74fe6",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "3e1f61b8-520b-42f4-9162-c1575239eea9",
      "created_at": "2024-12-25T10:42:18.694000Z",
      "updated_at": "2024-12-25T10:44:46.168000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_rhkpf7V.PNG",
      "character": "f150bf14-0a3d-42ed-936a-714169f74fe6"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae63a37"
  },
  {
    "id": "f1f6fd03-f4c8-421c-9427-d78d152a65ce",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "66053034-90ff-4e13-891c-5885ec12f9c5",
      "created_at": "2024-12-25T10:42:19.865000Z",
      "updated_at": "2024-12-25T10:44:46.301000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_I8z7uvm.PNG",
      "character": "f1f6fd03-f4c8-421c-9427-d78d152a65ce"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb8fc4"
  },
  {
    "id": "f261bd61-8b82-4bc4-96f1-f815c62707de",
    "name": "Mercenary Hex 4",
    "biography": {
      "id": "739732c4-e194-4300-b89c-e1a675d57ff2",
      "created_at": "2024-12-25T10:42:19.004000Z",
      "updated_at": "2024-12-25T10:44:46.391000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_Jdno3IE.PNG",
      "character": "f261bd61-8b82-4bc4-96f1-f815c62707de"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae85d7a"
  },
  {
    "id": "f3c4216f-cbaa-4792-b6e6-1cedd502defe",
    "name": "The Veiled Arbiter",
    "biography": {
      "id": "012e5d6e-bad2-459c-a7a6-62329ecd7508",
      "created_at": "2024-12-24T14:18:04.753000Z",
      "updated_at": "2024-12-24T14:19:28.959000Z",
      "age": 900,
      "gender": "Other",
      "background": "The Veiled Arbiter exists beyond the bounds of mortal realms, serving as the omniscient overseer of the game world. It appears to inspect, guide, or intervene when the balance of Flow or the integrity of the realm is threatened. With mastery over teleportation, invisibility, and Flow manipulation, its presence is both awe-inspiring and unsettling.",
      "appearance": "A translucent figure cloaked in flowing, dark robes inscribed with glowing blue and silver symbols. Its hood obscures its face, revealing only glowing white eyes. Tendrils of spectral mist swirl around its form, giving it an ethereal and ever-shifting presence.",
      "avatar": "http://localhost:8000/media/avatars/83A73E18-2066-4263-B8F3-F299660160F4.PNG",
      "character": "f3c4216f-cbaa-4792-b6e6-1cedd502defe"
    },
    "npc": false,
    "rank": {
      "name": "Mythical Paragon",
      "grade": 2,
      "experience_needed": 284460
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Game Master",
      "Phantom",
      "Flow Manipulator"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "73db031a-55cd-47c6-9e44-4b70cb09f27b",
      "name": "Mentors (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb1463dc"
  },
  {
    "id": "f4731134-c5e1-454b-921e-d5bef1bfea03",
    "name": "Mercenary Hex 7",
    "biography": {
      "id": "b8ac511e-46fb-43fd-a781-8c5bead80093",
      "created_at": "2024-12-25T10:42:19.016000Z",
      "updated_at": "2024-12-25T10:44:46.513000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_rGJYyQV.PNG",
      "character": "f4731134-c5e1-454b-921e-d5bef1bfea03"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae85d7a"
  },
  {
    "id": "f489297d-3f4a-4b65-aacc-67b7d2bd6862",
    "name": "Victor Ashforge",
    "biography": {
      "id": "3f42b92e-9203-4d62-b52e-e1f625826c4b",
      "created_at": "2024-12-24T12:29:00.037000Z",
      "updated_at": "2024-12-24T12:43:47.433000Z",
      "age": 33,
      "gender": "Other",
      "background": "Victor is the squad’s sniper, specializing in long-range precision kills. His patience and focus make him a vital asset during covert operations or ambush scenarios.",
      "appearance": "A tall, wiry man with a calm demeanor and sharp eyes. His dark tactical gear is built for stealth, and his Flow-enhanced sniper rifle gleams in the light.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_M8QN7A5.PNG",
      "character": "f489297d-3f4a-4b65-aacc-67b7d2bd6862"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Sniper",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "f48c5a7f-fd16-4721-baa8-549d6305d62a",
    "name": "Mercenary Hex 6",
    "biography": {
      "id": "0fb1cf82-3ac7-45e4-9b4f-2e0701fe0453",
      "created_at": "2024-12-25T10:42:19.949000Z",
      "updated_at": "2024-12-25T10:44:46.817000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_5sAo1ke.PNG",
      "character": "f48c5a7f-fd16-4721-baa8-549d6305d62a"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb9903"
  },
  {
    "id": "f63d9f0d-ed40-4d2d-83f7-c31b2b920fbb",
    "name": "Zeus Prime 00 2",
    "biography": {
      "id": "e048f4d5-7d27-470c-8033-e2eebe45fe12",
      "created_at": "2024-12-25T12:24:23.861000Z",
      "updated_at": "2024-12-25T12:24:23.861000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "f63d9f0d-ed40-4d2d-83f7-c31b2b920fbb"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb0478be"
  },
  {
    "id": "f712d65b-80b1-4995-8ff5-910981208154",
    "name": "Zeus Prime 00 8",
    "biography": {
      "id": "f1d938c5-528b-445d-acbe-2b7380376cdd",
      "created_at": "2024-12-25T12:24:22.516000Z",
      "updated_at": "2024-12-25T12:24:22.516000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "f712d65b-80b1-4995-8ff5-910981208154"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf8eca9"
  },
  {
    "id": "f728dc41-a643-44a3-8a8b-3b3e6d5d2dc6",
    "name": "Mercenary Hex 5",
    "biography": {
      "id": "9e84fb4e-9573-41f1-91d2-d5babedec2d1",
      "created_at": "2024-12-25T10:42:18.900000Z",
      "updated_at": "2024-12-25T10:44:47.063000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_dpWaWZB.PNG",
      "character": "f728dc41-a643-44a3-8a8b-3b3e6d5d2dc6"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae7d299"
  },
  {
    "id": "f76c01de-9f7e-4fd2-bb8e-648ba40c0bea",
    "name": "Mercenary Hex 2",
    "biography": {
      "id": "a831d7d2-3e02-4161-b07a-e49f34e7480e",
      "created_at": "2024-12-25T10:42:20.821000Z",
      "updated_at": "2024-12-25T10:44:47.088000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_9VgLOMu.PNG",
      "character": "f76c01de-9f7e-4fd2-bb8e-648ba40c0bea"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caf67c98"
  },
  {
    "id": "f8165587-5e97-4fef-99f3-6273adbbada5",
    "name": "Mercenary Hex 4",
    "biography": {
      "id": "e04607ab-6c06-44a5-818e-3c8d82d13aa7",
      "created_at": "2024-12-25T10:42:19.836000Z",
      "updated_at": "2024-12-25T10:44:47.224000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_x8xEUSS.PNG",
      "character": "f8165587-5e97-4fef-99f3-6273adbbada5"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb27a9"
  },
  {
    "id": "f8622142-562f-43cd-9c99-0f184d52f38a",
    "name": "Mercenary Hex 0",
    "biography": {
      "id": "c3273687-0951-4c5c-b07b-8f00227194f0",
      "created_at": "2024-12-25T10:42:20.431000Z",
      "updated_at": "2024-12-25T10:44:47.318000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_fGl7WJr.PNG",
      "character": "f8622142-562f-43cd-9c99-0f184d52f38a"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caebb774"
  },
  {
    "id": "f91b73cf-b4e6-4d2c-a2ca-f456517d32ac",
    "name": "Mercenary Hex 6",
    "biography": {
      "id": "0a686d3f-df60-4baa-8c48-91ae63aa2a09",
      "created_at": "2024-12-25T10:42:18.127000Z",
      "updated_at": "2024-12-25T10:44:47.453000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_wWSG3pK.PNG",
      "character": "f91b73cf-b4e6-4d2c-a2ca-f456517d32ac"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cadbb206"
  },
  {
    "id": "f96384d2-9b89-4fef-a648-c17f10c3bacb",
    "name": "Zeus Prime 00 0",
    "biography": {
      "id": "997f9b57-e042-4539-9e24-5285c24fa83d",
      "created_at": "2024-12-25T12:24:23.547000Z",
      "updated_at": "2024-12-25T12:24:23.547000Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "f96384d2-9b89-4fef-a648-c17f10c3bacb"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cafdf1c3"
  },
  {
    "id": "f9e208de-9add-45a0-81b9-5c75388e2153",
    "name": "Mercenary Hex 5",
    "biography": {
      "id": "c7c4d740-4422-470d-b8b1-7652857bef0f",
      "created_at": "2024-12-25T10:42:19.840000Z",
      "updated_at": "2024-12-25T10:44:47.555000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_dIawkgQ.PNG",
      "character": "f9e208de-9add-45a0-81b9-5c75388e2153"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb27a9"
  },
  {
    "id": "fa65b675-28fb-48b7-81dc-fb75b9e6b081",
    "name": "Cablo",
    "biography": {
      "id": "6bac20d8-686f-4ff5-b731-350cfb83d442",
      "created_at": "2024-12-24T13:27:25.118000Z",
      "updated_at": "2024-12-24T13:33:15.860000Z",
      "age": 900,
      "gender": "Other",
      "background": "Cablo is one of the oldest entities in existence, said to have been born from the primordial Flow itself. Legends speak of Cablo as the 'Architect of Balance,' capable of shaping realities and commanding Flow energy with effortless grace. While its motives are enigmatic, its power is unquestionable, and many consider it the ultimate guardian of Flow’s equilibrium.",
      "appearance": "A towering, ethereal being of shifting forms. Its body glows with vibrant, swirling Flow energy, constantly changing between humanoid, beast, and abstract shapes. Its presence alone distorts the surrounding space, creating an aura of immense power.",
      "avatar": "http://localhost:8000/media/avatars/79A66F4B-6434-4E6E-B4EF-44304A74CEA1.PNG",
      "character": "fa65b675-28fb-48b7-81dc-fb75b9e6b081"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Ancient Creature",
      "Flow Master",
      "Omnipotent Being"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "3135c8b9-3220-4a1c-ad59-69cc12f41ce8",
      "name": "Miracle Creatures (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb0a00e8"
  },
  {
    "id": "fbac46aa-1b56-4e82-a3cb-f6c3460b5bda",
    "name": "Mercenary Hex 9",
    "biography": {
      "id": "d453899f-82fd-4319-8329-6ba3a1a2b6bb",
      "created_at": "2024-12-25T10:42:18.914000Z",
      "updated_at": "2024-12-25T10:44:47.581000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_GF0oD2Y.PNG",
      "character": "fbac46aa-1b56-4e82-a3cb-f6c3460b5bda"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae7d299"
  },
  {
    "id": "fc90f6de-3292-4824-a228-ca36977c4bb4",
    "name": "Mercenary Hex 2",
    "biography": {
      "id": "5554a7e4-4944-4198-b940-b9e91d2cdbfe",
      "created_at": "2024-12-25T10:42:20.867000Z",
      "updated_at": "2024-12-25T10:44:47.726000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_nRJZ2D6.PNG",
      "character": "fc90f6de-3292-4824-a228-ca36977c4bb4"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb0ad298"
  },
  {
    "id": "fd39c9e4-c46f-438b-9078-c73b57b86d20",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "88e740d9-b739-4d36-80a3-d904d40d326a",
      "created_at": "2024-12-25T10:42:18.949000Z",
      "updated_at": "2024-12-25T10:44:47.854000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_Xyirma4.PNG",
      "character": "fd39c9e4-c46f-438b-9078-c73b57b86d20"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae85d7a"
  },
  {
    "id": "fe77177b-2a6b-47d6-8de3-4b6900bff044",
    "name": "Mercenary Hex 1",
    "biography": {
      "id": "f8d19dda-69f6-41ce-94a6-b1f3d08593b5",
      "created_at": "2024-12-25T10:42:18.813000Z",
      "updated_at": "2024-12-25T10:44:47.996000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_rd5DSXF.PNG",
      "character": "fe77177b-2a6b-47d6-8de3-4b6900bff044"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae79d20"
  },
  {
    "id": "ff82108a-d49d-40b8-8286-7192fc0875e2",
    "name": "Mercenary Hex 3",
    "biography": {
      "id": "c2c43b8c-7a62-4ae5-9ca0-0ad07916e64f",
      "created_at": "2024-12-25T10:42:18.844000Z",
      "updated_at": "2024-12-25T10:44:48.148000Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/BF9CA0EB-DE2B-4DDA-9A3C-B03A9AD98CDB_sz9HXom.PNG",
      "character": "ff82108a-d49d-40b8-8286-7192fc0875e2"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae79d20"
  },
  {
    "id": "3f7d8e07-cf63-45fd-a9b0-19568b64234f",
    "name": "Ororon",
    "biography": {
      "id": "2d9d6bf3-777e-4482-b499-069436ded838",
      "created_at": "2025-01-22T19:45:26.023000Z",
      "updated_at": "2025-01-23T07:21:51.630000Z",
      "age": 21,
      "gender": "Other",
      "background": "He was born in a rural family with a \"damaged\" soul. The family was thrilled by the child and decided to abandon him.\r\n\r\nFortunately, a group of shrouded disciples from the veiled conclave passing by heard Ororon's cries. \r\nOne of the followers decided to adopt the child, as she just suffered the loss.\r\n\r\nShe turned out to be a respected member of the faction, being a proficient mind shaper.\r\n\r\nOroron discovered a natural feeling of the flow and connection with it, possibly because of his \"damaged\" soul.\r\n\r\nThe boy was raised and taught the secrets of mind manipulation. He was a good student, he respected his \"mother\" and owed her his life.\r\n\r\nThroughout his life he often questioned his life’s purpose and nature of his \"damaged\" soul. He decided to take a journey to find more about the world he lives in and himself.",
      "appearance": "He is a tall character with pale skin and navy hair. He has heterochromatic eyes—his right eye is magenta, and his left eye is cyan. Distinctive features include a dark blue marking beneath his left eye. He wears dark blue clothes with a heavy cloak and a hood.",
      "avatar": "http://localhost:8000/media/avatars/Ororon.webp",
      "character": "3f7d8e07-cf63-45fd-a9b0-19568b64234f"
    },
    "npc": false,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Mind Shaper",
      "Adopted",
      "Veiled Conclave",
      "Heterochromatic Eyes",
      "Mysterious"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "fe887164-987d-449e-96eb-4f3762b76358",
      "name": "House of Gryphon (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb146bce"
  },
  {
    "id": "505678ac-2070-4a0a-a0ce-719251568b75",
    "name": "Аурум Хемкрафт",
    "biography": {
      "id": "7391ab58-5891-4869-b60a-2dbf149d963b",
      "created_at": "2025-01-22T14:17:21.782000Z",
      "updated_at": "2025-01-22T16:35:23.683000Z",
      "age": 27,
      "gender": "Other",
      "background": "Лазар Хемкрафт народився у відомій родині алхіміків, які славилися своїми відкриттями у трансмутації та створенні еліксирів. Його мати довго хворіла на невиліковну недугу, а батько присвятив весь вільний час пошуку ліків, однак його зусилля виявилися марними.\r\n\r\nОдного разу Лазар знайшов заборонений фоліант у сімейній бібліотеці — Гемокодекс, у якому описувалася магія крові. У відчаї він вирішив спробувати магію з книги, щоб вилікувати чи хоча б полегшити страждання матері. Це дало тимчасовий результат, але викликало серйозні побічні ефекти. Дізнавшись про це, батько заборонив Лазару користуватися цією магією, назвавши її \"скверною та ганьбою для роду Хемкрафтів\".\r\n\r\nПісля смерті матері Лазар усвідомив, що відмова від магії крові — це не раціональний вибір, а всього лише страх незвіданого. Він покинув батьківський дім, вирішивши для себе, що справжнє призначення роду Хемкрафтів — не просто створювати цікаві прилади або еліксири, а робити ВСЕ, щоб допомагати людям у найскладніші моменти, навіть якщо для цього потрібно переступити етичні межі.\r\n\r\nЙого мета — створити щось унікальне. Щось, що зможе врятувати інших від тих втрат, які він сам пережив. І в цьому йому допоможе магія крові.\r\nУсвідомлюючи всю небезпеку свого шляху і сподіваючись, що жага до пізнання магії крові не переросте у жагу самої крові, Лазар вирушив подорожувати світом",
      "appearance": "Буде аватарка. Худий, середнього росту, з невеличкою щетиною.\r\nРуки в шрамах, які він сам називає відмітинами досвіду.",
      "avatar": "http://localhost:8000/media/avatars/%D0%90%D1%83%D1%80%D1%83%D0%BC_%D0%A5%D0%B5%D0%BC%D0%BA%D1%80%D0%B0%D1%84%D1%82.webp",
      "character": "505678ac-2070-4a0a-a0ce-719251568b75"
    },
    "npc": false,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Blood Mage",
      "Alchemist",
      "Transmutation",
      "Moral Dilemma",
      "Wanderer"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "fe887164-987d-449e-96eb-4f3762b76358",
      "name": "House of Gryphon (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cad964e5"
  },
  {
    "id": "825c4bcd-a442-4b04-b8c8-b526537695e4",
    "name": "Kael “Frostfang” Venir",
    "biography": {
      "id": "1041c796-a6d6-437a-890f-736da67982f0",
      "created_at": "2025-01-15T17:45:58.849000Z",
      "updated_at": "2025-01-15T17:48:24.920000Z",
      "age": 30,
      "gender": "Other",
      "background": "Born in the frigid northern realms, Kael was molded by the harsh environment and his unyielding pursuit of perfection. His mastery of water magic is unparalleled, but his unique style incorporates the biting cold of frost, a reflection of his own hardened and detached personality. Once a protector of his homeland, a betrayal turned his heart to ice, and he now wanders the dimensions seeking purpose while maintaining an air of stoic elegance.",
      "appearance": "Tall and elegant, Kael has sharp features and icy blue eyes that seem to pierce through anyone he gazes at. His flowing silver hair is tied back in a sleek ponytail, and his attire consists of a pristine white robe accented with frost-like embroidery. He wields a sleek katana that shimmers with a frost-covered blade, exuding a chill mist as if the weapon itself breathes cold.",
      "avatar": "http://localhost:8000/media/avatars/45D30DA6-D64F-4EF4-94A5-9C44B2B93F01_2.PNG",
      "character": "825c4bcd-a442-4b04-b8c8-b526537695e4"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Mage",
      "Water Magic",
      "Frost Katana",
      "Cold Soul"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "85e3d4a0-5fc1-4097-9e31-ae0f8492d74a",
      "name": "Soul Ripper (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb0924a2"
  },
  {
    "id": "8678a4e2-cd73-4aac-bca4-2fd2efddbf52",
    "name": "Iron Spider",
    "biography": {
      "id": "016f70a4-87b0-4797-ac2b-95544d76806f",
      "created_at": "2025-01-14T19:34:56.923000Z",
      "updated_at": "2025-01-14T19:36:03.482000Z",
      "age": 200,
      "gender": "Other",
      "background": "Forged in the depths of an industrial cavern, the Iron Spider is a rogue creation born of a failed experiment to merge Flow energy with advanced robotics. The corrupted energy within its core drives its relentless aggression and cunning, making it a feared predator of the underworld. It guards the remains of its creators and the glowing red crystals that feed its power.",
      "appearance": "A mechanical arachnid infused with corrupted Flow energy. Its sleek metallic body is adorned with glowing red Flow circuits, and its eight razor-sharp legs are poised for action. Its central core pulsates with dark energy, while its multiple glowing sensor eyes add a menacing aura.",
      "avatar": "http://localhost:8000/media/avatars/6C74A670-8E94-4D8D-B274-CEC66A9CDABA_2.PNG",
      "character": "8678a4e2-cd73-4aac-bca4-2fd2efddbf52"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mechanical",
      "Corrupted Flow",
      "Arachnid"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "95627a88-dfbf-4e82-be5d-c1dd2503069d",
      "name": "Elder Creatures (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb01f651"
  },
  {
    "id": "9094e8f3-3df2-4205-aef7-375b8c2c9326",
    "name": "Maximus",
    "biography": {
      "id": "f9a34e29-fbdc-4aeb-9a88-d79452074569",
      "created_at": "2025-01-12T15:03:41.443000Z",
      "updated_at": "2025-01-12T15:06:34.099000Z",
      "age": 32,
      "gender": "Other",
      "background": "Born in the industrial outskirts of the City of Memories, augmented after a Flow accident.",
      "appearance": "Towering, muscular, bald with a thick stubbly beard, wearing scratched Flow-infused armor.",
      "avatar": "http://localhost:8000/media/avatars/Maximus_22Boulder22_Forge.webp",
      "character": "9094e8f3-3df2-4205-aef7-375b8c2c9326"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Tank",
      "Way of John",
      "Cybernetic Enhancements"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "ac184495-58fe-42f0-a7cd-c4dec5e787c9",
      "name": "Power Fist (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cadefd46"
  },
  {
    "id": "9818e6f5-2144-4605-a60c-cc937b7ad30e",
    "name": "Tyler Drake",
    "biography": {
      "id": "276043b0-b17d-4576-9079-cf80624d0082",
      "created_at": "2025-01-23T17:54:33.380000Z",
      "updated_at": "2025-01-23T18:00:54.791000Z",
      "age": 35,
      "gender": "Other",
      "background": "Grew up fascinated by ancient legends and long-lost treasures, spending his youth poring over dusty tomes and maps. With a knack for solving puzzles and an eye for detail, he became an adventurous treasure hunter, walking the line between scholar and rogue.",
      "appearance": "A rugged man in his 30s with messy dark brown hair, green eyes, and a sharp stubble. Wears a leather jacket and sturdy boots. Athletic and ready for action.",
      "avatar": "http://localhost:8000/media/avatars/Tyler_Drake.webp",
      "character": "9818e6f5-2144-4605-a60c-cc937b7ad30e"
    },
    "npc": false,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Treasure Hunter",
      "Adventurer",
      "Rogue Scholar",
      "Puzzle Solver",
      "Explorer"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "fe887164-987d-449e-96eb-4f3762b76358",
      "name": "House of Gryphon (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cad941a0"
  },
  {
    "id": "a5e59aec-7409-46ff-8428-3d0a5a2e483f",
    "name": "Cyberhound",
    "biography": {
      "id": "a82c200c-c1aa-4a1a-bf8a-c4e61267a9c6",
      "created_at": "2025-01-14T18:27:31.358000Z",
      "updated_at": "2025-01-14T18:28:51.982000Z",
      "age": 30,
      "gender": "Other",
      "background": "Originally created as a high-tech companion for military use, Bolt developed self-awareness after exposure to the Flow. Now it roams the streets as a loyal protector to punks and outcasts, its cybernetic enhancements making it a formidable ally and a fierce adversary.",
      "appearance": "A sleek, robotic canine with a metallic frame covered in black and silver plating. Bolt’s eyes glow a sharp blue, and its tail is a segmented whip-like appendage. Embedded on its side are glowing energy cores that hum softly.",
      "avatar": "http://localhost:8000/media/avatars/611CC12F-0745-4F9F-B3DE-54FF24117ECD_2.PNG",
      "character": "a5e59aec-7409-46ff-8428-3d0a5a2e483f"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "creature",
      "pet"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "ac184495-58fe-42f0-a7cd-c4dec5e787c9",
      "name": "Power Fist (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeb3a17"
  },
  {
    "id": "d0332870-40ba-42b3-a128-2bd168c12da6",
    "name": "Shadow Droid",
    "biography": {
      "id": "5a25b94f-01de-45af-a3c0-d3cfd334d64f",
      "created_at": "2025-01-12T20:08:23.171000Z",
      "updated_at": "2025-01-12T20:11:53.681000Z",
      "age": 240,
      "gender": "Other",
      "background": "Originally designed by a rogue faction as an advanced Flow protector, now corrupted and hunting humanity.",
      "appearance": "Sleek humanoid robotic figure made from matte black alloy, faint purple glowing circuits, reflective face with red glow when active.",
      "avatar": "http://localhost:8000/media/avatars/Shadow_Droid.webp",
      "character": "d0332870-40ba-42b3-a128-2bd168c12da6"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Assassin",
      "Artificial Intelligence",
      "Stealth",
      "Anti-Human"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": null,
    "position_id": "00000000-0000-0000-0000-0193cafa91ab"
  },
  {
    "id": "eed85cf7-0ce2-421e-90e4-1dbd4e4a3ddc",
    "name": "Titan “Steelhorn” Mazer",
    "biography": {
      "id": "7288dfae-1d0f-4b85-9a4d-c08d54ac1730",
      "created_at": "2025-01-14T18:59:13.454000Z",
      "updated_at": "2025-01-14T19:01:21.141000Z",
      "age": 40,
      "gender": "Other",
      "background": "Once a mythological guardian of ancient labyrinths, Titan was captured by a shadowy underworld syndicate and augmented with cybernetic enhancements to serve as an enforcer. Now broken free, he stalks the underworld’s depths, seeking vengeance against his creators while unleashing chaos in his wake. Known for his unparalleled strength and terrifying presence, Titan is both a hunter and a legend among the underworld's denizens.",
      "appearance": "A towering robotic minotaur standing over 9 feet tall, with glimmering steel-plated horns that pulse with red energy. His body is a mix of ancient, rusted machinery and high-tech augmentations, with visible wiring snaking across his limbs. His eyes burn like molten lava, and his left arm is a massive hydraulic claw.",
      "avatar": "http://localhost:8000/media/avatars/1FE5EA8E-4F62-4E78-AE99-F96D3246D6FE.PNG",
      "character": "eed85cf7-0ce2-421e-90e4-1dbd4e4a3ddc"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "elder",
      "chaos",
      "mad",
      "bloody"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "95627a88-dfbf-4e82-be5d-c1dd2503069d",
      "name": "Elder Creatures (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caeffd80"
  },
  {
    "id": "71f5131a-48e8-420f-9c06-b214a4a8ae5b",
    "name": "Test NPC for Fix",
    "biography": null,
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": null
  },
  {
    "id": "fbeeef42-3c0a-48ea-9f18-f1edcb33b238",
    "name": "Test NPC for Skills",
    "biography": null,
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cad941a0"
  },
  {
    "id": "32d7bf88-3f58-4fd8-92d5-5a2c569a23b7",
    "name": "Test NPC for Skills",
    "biography": null,
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cad941a0"
  },
  {
    "id": "209739e9-e55f-4656-94a6-c3a91eb383f2",
    "name": "Mercenary Hex 3 Template",
    "biography": {
      "id": "47dd2fd8-4c98-4d90-8da3-3582bd62f710",
      "created_at": "2025-06-21T14:00:53.944919Z",
      "updated_at": "2025-06-21T14:00:53.945109Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/deepseek-r1-v2.png",
      "character": "209739e9-e55f-4656-94a6-c3a91eb383f2"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cae6ce17"
  },
  {
    "id": "d391f6bc-5660-4453-a3c1-9b1561c287f4",
    "name": "Zeus Prime 00 2 Template",
    "biography": {
      "id": "40709f2b-15b4-43c9-9374-b62f1a3e5f89",
      "created_at": "2025-06-21T14:06:56.473646Z",
      "updated_at": "2025-06-21T14:06:56.473765Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "d391f6bc-5660-4453-a3c1-9b1561c287f4"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb0a7429"
  },
  {
    "id": "5a07a0e4-d0ea-468a-ac25-0b26d9b4df54",
    "name": "Zeus Prime 00 2 Template",
    "biography": {
      "id": "07a06d45-4084-4425-aed1-7598c756d203",
      "created_at": "2025-06-21T14:31:52.248610Z",
      "updated_at": "2025-06-21T14:31:52.248848Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "5a07a0e4-d0ea-468a-ac25-0b26d9b4df54"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb0a7429"
  },
  {
    "id": "237fbdc2-1f76-4f01-90d4-2cf21ce36ca3",
    "name": "Zeus Prime 00 2 Template",
    "biography": {
      "id": "3fab03cc-3783-465d-8b4e-6b33f0c2b69c",
      "created_at": "2025-06-21T14:32:00.793021Z",
      "updated_at": "2025-06-21T14:32:00.793182Z",
      "age": 100,
      "gender": "Other",
      "background": "Aegis-01 is a standard combat android designed for security and reconnaissance missions. It operates with precision and efficiency, following its programming to protect and execute commands. While its intelligence is artificial, it demonstrates adaptive behavior, learning from its experiences in the field.",
      "appearance": "A sleek humanoid frame made of reinforced alloy, with glowing blue energy lines running along its limbs. Its face is a smooth, featureless mask with a single glowing optical sensor.",
      "avatar": "http://localhost:8000/media/avatars/43288955-89E9-4F17-A3C8-A5473D90B63B.webp",
      "character": "237fbdc2-1f76-4f01-90d4-2cf21ce36ca3"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Android",
      "Combat Unit",
      "Artificial Intelligence"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "f24fa6a9-785b-4cfe-857f-b2bd87f411e4",
      "name": "Cyber Lab (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193cb0a7429"
  },
  {
    "id": "b23935bb-1167-4bd4-80cd-cbd40b271f28",
    "name": "Mercenary Hex 3 Template (First Campaign)",
    "biography": {
      "id": "043c8b6d-d30b-4f45-9580-a98a60b86c96",
      "created_at": "2025-07-14T11:35:48.401970Z",
      "updated_at": "2025-07-14T11:35:48.402203Z",
      "age": 35,
      "gender": "Other",
      "background": "Born into the chaotic slums of the lower districts of the City of Memories, Darin grew up learning to fend for himself. Life in the undercity was harsh, and survival often meant aligning with questionable figures. By the age of sixteen, he had joined a local gang, earning his nickname \"Ironshade\" for his uncanny ability to find safety even in dangerous skirmishes.\r\n\r\nHis natural talent for combat and strategic thinking caught the attention of a rogue Flow scholar who taught him how to incorporate Flow energy into his fighting style. Equipped with this knowledge and armed with a Flow-powered rifle he scavenged during a gang raid, Darin left the undercity to pursue life as a mercenary.\r\n\r\nFor the past decade, Darin has operated as a freelance mercenary, specializing in high-risk infiltration and sabotage missions. While his work has brought him fame and wealth, it has also left him jaded. He now views life through a pragmatic lens, focusing only on what will help him survive the next mission. Despite his tough exterior, he has a soft spot for outcasts and rookies trying to make their way, often taking them under his wing.",
      "appearance": "Darin is a rugged and battle-worn mercenary with short-cropped black hair streaked with silver, a scar running down his left cheek, and piercing gray eyes that seem to weigh every situation. He wears a modular combat suit reinforced with Flow-infused plates, marked with scrapes and burns that tell stories of countless battles. His demeanor is calm but guarded, with a slight smirk often hinting at his underlying confidence.",
      "avatar": "http://localhost:8000/media/avatars/deepseek-r1-v2.png",
      "character": "b23935bb-1167-4bd4-80cd-cbd40b271f28"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of John",
      "description": "A path focusing on technical enhancements.",
      "icon": "http://localhost:8000/media/icons/path/john.webp",
      "id": "c7b92d32-4c21-4a29-84c2-469e4f888d31"
    },
    "experience": 0,
    "tags": [
      "Mercenary",
      "Demolitions Expert",
      "Hired Gun"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": {
      "id": "d5c0cf04-5945-40b5-b89f-942efbb52899",
      "name": "Underground Mercenaries (First Campaign)"
    },
    "position_id": "00000000-0000-0000-0000-0193caea48d3"
  },
  {
    "id": "51bb8d1e-ffec-4994-ac53-1fe7329834c1",
    "name": "Vito Ashenvale",
    "biography": {
      "id": "e72f5bb1-2065-4abc-a8db-63436de0f732",
      "created_at": "2025-07-14T13:01:41.918743Z",
      "updated_at": "2025-07-14T13:01:41.919702Z",
      "age": 39,
      "gender": "Other",
      "background": "Victor Ashenvale is a top-tier adventurer, born into a family of wealth and prestige. Known for his tactical brilliance and mastery of Flow-enhanced combat, he combines skill, wit, and luxury in every mission. Despite his high-society upbringing, Victor has earned his reputation through relentless pursuit of perfection, often taking on missions deemed impossible.",
      "appearance": "A sophisticated figure with sharp, angular features and an air of confidence. He wears custom-tailored combat gear enhanced with cutting-edge Flow technology. An electric Flow cigarette often dangles from his lips, emitting faint, glowing vapor.",
      "avatar": "http://localhost:8000/media/avatars/EF720330-85DE-4412-8DF5-235575AC0AA8.PNG",
      "character": "51bb8d1e-ffec-4994-ac53-1fe7329834c1"
    },
    "npc": true,
    "rank": {
      "name": "Novice",
      "grade": 9,
      "experience_needed": 200
    },
    "path": {
      "name": "Path of JSon",
      "description": "A path focusing on magical abilities.",
      "icon": "http://localhost:8000/media/icons/path/json.webp",
      "id": "7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"
    },
    "experience": 0,
    "tags": [
      "Elite Adventurer",
      "Flow Enhanced",
      "High Society"
    ],
    "resetting_base_stats": false,
    "is_active": true,
    "campaign": {
      "id": "b6de2027-2372-434f-bff4-b799ef5d1cd2",
      "name": "First Campaign"
    },
    "fight": null,
    "organization": null,
    "position_id": "00000000-0000-0000-0000-0193cb04838e"
  }
] as OpenaiCharacter[];
</script>


<template>
  <HeroBackground></HeroBackground>
  <!--  START TEST VIEW -->
  <div class="test-screen">
    <h1>Test Screen</h1>
    <!-- Button Examples Row -->
    <div class="button-examples-row">
      <RPGButton :type="ButtonType.SUCCESS" @click="">Success</RPGButton>
      <RPGButton :type="ButtonType.CANCEL" @click="">Cancel</RPGButton>
      <RPGButton :type="ButtonType.SUBMIT" @click="">Submit</RPGButton>
      <RPGButton :type="ButtonType.DEFAULT" @click="">Default</RPGButton>
    </div>

    <!-- CustomAction with integrated event handlers -->
    <CustomAction
      :initiator="selectedInitiator"
      :target="selectedTarget"
      :action="selectedAction"
      @selectInitiator="handleSelectInitiator"
      @selectTarget="handleSelectTarget"
      @selectAction="handleSelectAction"
    />

    <!-- Character Selector Modal -->
    <div v-if="showCharSelector" class="modal-overlay" @click="handleCharSelectorClose">
      <div class="modal-container" @click.stop>
        <GmCharSelector
          :characters="characters"
          @select="handleCharacterSelected"
          @close="handleCharSelectorClose"
        />
      </div>
    </div>

    <!-- Skill Selector Modal -->
    <div v-if="showSkillSelector" class="modal-overlay" @click="handleSkillSelectorClose">
      <div class="modal-container" @click.stop>
        <GMRPGSkills
          :isDraggable="false"
          @skillSelected="handleSkillSelected"
          @close="handleSkillSelectorClose"
        />
      </div>
    </div>
  </div>
  <!--  END TEST VIEW-->
</template>

<style scoped>
.test-screen {
  padding: 2rem;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.button-examples-row {
  display: flex;
  flex-direction: row;
  gap: 1.5rem;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
}

/* Modal container styles - invisible positioning containers */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
}

.modal-container {
  max-width: 90vw;
  max-height: 90vh;
  overflow: auto;
  border-radius: 0.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
}

/* Custom scrollbar for modal container */
.modal-container::-webkit-scrollbar {
  width: 8px;
}

.modal-container::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.modal-container::-webkit-scrollbar-thumb {
  background: rgba(127, 255, 22, 0.6);
  border-radius: 4px;
}

.modal-container::-webkit-scrollbar-thumb:hover {
  background: rgba(127, 255, 22, 0.8);
}

</style>