<template>
  <div class="bio-tab">
    <h3>Character Biography</h3>

    <!-- Character Avatar Section -->
    <div class="avatar-section">
      <h4>Character Avatar</h4>
      <div class="avatar-container">
        <div class="avatar-preview">
          <img
            v-if="currentAvatar"
            :src="currentAvatar"
            alt="Character Avatar"
            class="avatar-image"
            @error="onImageError"
          />
          <div v-else class="avatar-placeholder">
            <span class="placeholder-icon">📷</span>
            <span class="placeholder-text">No Avatar</span>
          </div>
        </div>
        
        <div class="avatar-controls">
          <div class="upload-section">
            <label class="upload-button" for="avatar-upload">
              <span class="upload-icon">📁</span>
              Upload Image
            </label>
            <input
              id="avatar-upload"
              type="file"
              accept="image/*"
              @change="handleFileUpload"
              class="file-input"
            />
          </div>
          
          <div class="url-section">
            <label>Or enter image URL:</label>
            <div class="url-input-group">
              <input
                type="url"
                :value="avatarUrl"
                @input="updateAvatarUrl"
                placeholder="https://example.com/image.jpg"
                class="url-input"
              />
              <button 
                @click="setAvatarFromUrl" 
                :disabled="!avatarUrl"
                class="set-url-button"
                title="Set avatar from URL"
              >
                Set
              </button>
            </div>
          </div>
          
          <button 
            v-if="currentAvatar" 
            @click="removeAvatar" 
            class="remove-button"
            title="Remove current avatar"
          >
            🗑️ Remove Avatar
          </button>
        </div>
      </div>
    </div>

    <!-- Character Details Section -->
    <div class="details-section">
      <div class="bio-section">
        <div class="bio-field">
          <label>Age</label>
          <input
            type="number"
            :value="template.data.bio.age"
            @input="updateAge"
            min="1"
            placeholder="25"
          />
        </div>
        <div class="bio-field">
          <label>Gender</label>
          <input
            type="text"
            :value="template.data.bio.gender"
            @input="updateGender"
            placeholder="Male/Female/Other"
          />
        </div>
      </div>

      <div class="bio-field full-width">
        <label>Appearance</label>
        <textarea
          :value="template.data.bio.appearance"
          @input="updateAppearance"
          placeholder="Describe the character's physical appearance, clothing, notable features..."
          rows="4"
        ></textarea>
      </div>

      <div class="bio-field full-width">
        <label>Background</label>
        <textarea
          :value="template.data.bio.background"
          @input="updateBackground"
          placeholder="Character's history, personality, motivations, goals..."
          rows="6"
        ></textarea>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BioTab',
  props: {
    template: {
      type: Object,
      required: true
    },
    service: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      avatarUrl: '',
      uploadingImage: false,
      imageError: false
    };
  },
  computed: {
    currentAvatar() {
      return this.template.data.bio.avatar || null;
    }
  },
  methods: {
    updateAge(event) {
      this.service.setBio({
        ...this.template.data.bio,
        age: parseInt(event.target.value, 10)
      });
      this.$emit('update');
    },
    updateGender(event) {
      this.service.setBio({
        ...this.template.data.bio,
        gender: event.target.value
      });
      this.$emit('update');
    },
    updateAppearance(event) {
      this.service.setBio({
        ...this.template.data.bio,
        appearance: event.target.value
      });
      this.$emit('update');
    },
    updateBackground(event) {
      this.service.setBio({
        ...this.template.data.bio,
        background: event.target.value
      });
      this.$emit('update');
    },
    
    // Avatar management methods
    updateAvatarUrl(event) {
      this.avatarUrl = event.target.value;
    },
    
    setAvatarFromUrl() {
      if (this.avatarUrl.trim()) {
        this.updateAvatar(this.avatarUrl.trim());
        this.avatarUrl = '';
      }
    },
    
    updateAvatar(avatarUrl) {
      this.service.setBio({
        ...this.template.data.bio,
        avatar: avatarUrl
      });
      this.$emit('update');
      this.imageError = false;
    },
    
    removeAvatar() {
      if (confirm('Are you sure you want to remove the current avatar?')) {
        this.service.setBio({
          ...this.template.data.bio,
          avatar: null
        });
        this.$emit('update');
        this.avatarUrl = '';
        this.imageError = false;
      }
    },
    
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      // Validate file type
      if (!file.type.startsWith('image/')) {
        alert('Please select a valid image file.');
        return;
      }
      
      // Validate file size (max 5MB)
      const maxSize = 5 * 1024 * 1024; // 5MB
      if (file.size > maxSize) {
        alert('Image file is too large. Please select an image smaller than 5MB.');
        return;
      }
      
      this.uploadingImage = true;
      
      // Create a FileReader to convert the file to a data URL
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const dataUrl = e.target.result;
          this.updateAvatar(dataUrl);
          console.log('Image uploaded successfully as data URL');
        } catch (error) {
          console.error('Error processing image:', error);
          alert('Error processing the image. Please try again.');
        } finally {
          this.uploadingImage = false;
          // Clear the file input
          event.target.value = '';
        }
      };
      
      reader.onerror = () => {
        console.error('Error reading file');
        alert('Error reading the file. Please try again.');
        this.uploadingImage = false;
        event.target.value = '';
      };
      
      reader.readAsDataURL(file);
    },
    
    onImageError() {
      console.warn('Failed to load avatar image:', this.currentAvatar);
      this.imageError = true;
    }
  }
};
</script>

<style scoped>
.bio-tab {
  padding: 20px 0;
}

/* Avatar Section */
.avatar-section {
  background: #2d2d2d;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 30px;
  border: 1px solid #444;
}

.avatar-section h4 {
  color: #1E90FF;
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.1rem;
}

.avatar-container {
  display: flex;
  gap: 30px;
  align-items: flex-start;
}

.avatar-preview {
  flex-shrink: 0;
  width: 150px;
  height: 150px;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid #555;
  background: #333;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.avatar-image:hover {
  transform: scale(1.05);
}

.avatar-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #888;
  text-align: center;
}

.placeholder-icon {
  font-size: 2rem;
  margin-bottom: 8px;
  opacity: 0.7;
}

.placeholder-text {
  font-size: 14px;
  font-weight: bold;
}

.avatar-controls {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Upload Section */
.upload-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.upload-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #4CAF50;
  color: white;
  padding: 12px 20px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: bold;
  border: none;
  width: fit-content;
}

.upload-button:hover {
  background: #3d8b40;
  transform: translateY(-2px);
}

.upload-icon {
  font-size: 16px;
}

.file-input {
  display: none;
}

/* URL Section */
.url-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.url-section label {
  color: #ccc;
  font-weight: bold;
  font-size: 14px;
}

.url-input-group {
  display: flex;
  gap: 8px;
  align-items: center;
}

.url-input {
  flex: 1;
  padding: 10px;
  background: #333;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.url-input:focus {
  border-color: #1E90FF;
  outline: none;
}

.set-url-button {
  padding: 10px 16px;
  background: #1E90FF;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: bold;
}

.set-url-button:hover:not(:disabled) {
  background: #1565C0;
}

.set-url-button:disabled {
  background: #555;
  cursor: not-allowed;
  opacity: 0.5;
}

/* Remove Button */
.remove-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #f44336;
  color: white;
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: bold;
  width: fit-content;
}

.remove-button:hover {
  background: #d32f2f;
  transform: translateY(-2px);
}

/* Details Section */
.details-section {
  background: #2d2d2d;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #444;
}

.bio-section {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.bio-field {
  flex: 1;
  margin-bottom: 20px;
}

.bio-field.full-width {
  width: 100%;
}

.bio-field label {
  display: block;
  margin-bottom: 5px;
  color: #ccc;
  font-weight: bold;
}

.bio-field input,
.bio-field textarea {
  width: 100%;
  padding: 10px;
  background: #333;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  transition: all 0.3s ease;
  resize: vertical;
}

.bio-field input:focus,
.bio-field textarea:focus {
  border-color: #1E90FF;
  outline: none;
  background: #3a3a3a;
}

.bio-field textarea {
  font-family: inherit;
  line-height: 1.5;
}

.bio-field input::placeholder,
.bio-field textarea::placeholder {
  color: #888;
  font-style: italic;
}

/* Headers */
h3 {
  color: #1E90FF;
  margin-top: 0;
  margin-bottom: 25px;
  font-size: 1.3rem;
  text-align: center;
  padding-bottom: 10px;
  border-bottom: 2px solid #444;
}

h4 {
  color: #1E90FF;
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 1.1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .avatar-container {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .avatar-preview {
    width: 120px;
    height: 120px;
  }
  
  .avatar-controls {
    width: 100%;
  }
  
  .bio-section {
    flex-direction: column;
    gap: 0;
  }
  
  .url-input-group {
    flex-direction: column;
    align-items: stretch;
  }
  
  .set-url-button {
    margin-top: 8px;
  }
}

@media (max-width: 480px) {
  .avatar-section,
  .details-section {
    padding: 15px;
  }
  
  .avatar-preview {
    width: 100px;
    height: 100px;
  }
  
  .upload-button,
  .remove-button {
    padding: 10px 16px;
    font-size: 14px;
  }
}
</style>