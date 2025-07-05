/**
 * Simple test script for CharacterTemplateEditorService
 *
 * This script tests the basic functionality of the CharacterTemplateEditorService
 * using the sample data from the CharacterTemplateFull model.
 */

import { characterTemplateEditorService } from '../services/CharacterTemplateEditorService.js';
import { createSampleCharacterTemplate } from '../models/CharacterTemplateFull.js';

/**
 * Run tests for the CharacterTemplateEditorService
 */
async function testCharacterTemplateEditorService() {
  console.log('=== Testing CharacterTemplateEditorService ===');

  // Initialize the service
  await characterTemplateEditorService.initialize();
  console.log('Service initialized');

  // Load sample template
  const sampleTemplate = createSampleCharacterTemplate();
  characterTemplateEditorService.template = sampleTemplate;
  console.log('Sample template loaded:', characterTemplateEditorService.getTemplate().data.name);

  // Test getters
  console.log('\n--- Testing Getters ---');
  console.log('Name:', characterTemplateEditorService.getName());
  console.log('Tags:', characterTemplateEditorService.getTags());
  console.log('Bio:', characterTemplateEditorService.getBio());
  console.log('Rank:', characterTemplateEditorService.getRank());
  console.log('Path:', characterTemplateEditorService.getPath());
  console.log('Stats:', characterTemplateEditorService.getStats().length);
  console.log('Items:', characterTemplateEditorService.getItems().length);
  console.log('Schools:', characterTemplateEditorService.getSchools().length);
  console.log('Spells:', characterTemplateEditorService.getSpells().length);

  // Test setters
  console.log('\n--- Testing Setters ---');
  characterTemplateEditorService.setName('Updated Template Name');
  console.log('Updated Name:', characterTemplateEditorService.getName());

  characterTemplateEditorService.addTag('New Tag');
  console.log('Added Tag:', characterTemplateEditorService.getTags());

  characterTemplateEditorService.removeTag('New Tag');
  console.log('Removed Tag:', characterTemplateEditorService.getTags());

  characterTemplateEditorService.updateStat('Physical Strength', 15);
  console.log('Updated Stat:', characterTemplateEditorService.getStats().find(s => s.name === 'Physical Strength').value);

  // Test validation
  console.log('\n--- Testing Validation ---');
  const validationResult = characterTemplateEditorService.validate();
  console.log('Validation Result:', validationResult.isValid ? 'Valid' : 'Invalid');
  if (!validationResult.isValid) {
    console.log('Validation Errors:', validationResult.errors);
  }

  // Test export
  console.log('\n--- Testing Export ---');
  const exportedTemplate = characterTemplateEditorService.export();
  console.log('Export successful:', exportedTemplate !== null);

  // Test reset
  console.log('\n--- Testing Reset ---');
  characterTemplateEditorService.reset();
  console.log('Template reset, name is now:', characterTemplateEditorService.getName());

  console.log('\n=== CharacterTemplateEditorService Tests Completed ===');
}

// Run the tests
testCharacterTemplateEditorService().catch(error => {
  console.error('Test failed:', error);
});

// Export the test function for potential reuse
export default testCharacterTemplateEditorService;