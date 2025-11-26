/**
 * PNG Metadata Utilities
 * Handles embedding and extracting map data in PNG files
 * Based on PNG specification for tEXt and zTXt chunks
 */

/**
 * Embeds map data as metadata in a PNG image
 * @param {HTMLCanvasElement} canvas - The canvas containing the map visualization
 * @param {Object} mapData - The map data to embed
 * @returns {Promise<Blob>} - PNG blob with embedded metadata
 */
export async function embedMetadataInPNG(canvas, mapData) {
  return new Promise((resolve, reject) => {
    try {
      // Convert map data to JSON string
      const metadataJSON = JSON.stringify(mapData);

      // Get the PNG data from canvas
      canvas.toBlob(async (blob) => {
        if (!blob) {
          reject(new Error('Failed to create PNG blob'));
          return;
        }

        // Read the PNG blob as ArrayBuffer
        const arrayBuffer = await blob.arrayBuffer();
        const uint8Array = new Uint8Array(arrayBuffer);

        // Create a new PNG with embedded metadata
        const pngWithMetadata = addTextChunkToPNG(uint8Array, 'TabletopMapData', metadataJSON);

        // Create a new blob from the modified PNG
        const newBlob = new Blob([pngWithMetadata], { type: 'image/png' });
        resolve(newBlob);
      }, 'image/png', 1.0);
    } catch (error) {
      reject(error);
    }
  });
}

/**
 * Extracts map data from a PNG file
 * @param {File} file - The PNG file to extract metadata from
 * @returns {Promise<{mapData: Object|null, imageDataURL: string, hasMetadata: boolean, imageWidth: number, imageHeight: number}>} - Extracted map data, image, and metadata status
 */
export async function extractMetadataFromPNG(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = async (e) => {
      try {
        const arrayBuffer = e.target.result;
        const uint8Array = new Uint8Array(arrayBuffer);

        // Extract metadata from PNG
        const metadata = extractTextChunkFromPNG(uint8Array, 'TabletopMapData');

        // Convert the PNG to data URL for display
        const blob = new Blob([uint8Array], { type: 'image/png' });
        const imageDataURL = await blobToDataURL(blob);

        // Load image to get dimensions
        const { width, height } = await getImageDimensions(imageDataURL);

        if (!metadata) {
          // No metadata found - return image data without map data
          resolve({
            mapData: null,
            imageDataURL,
            hasMetadata: false,
            imageWidth: width,
            imageHeight: height
          });
          return;
        }

        // Parse the JSON metadata
        const mapData = JSON.parse(metadata);

        resolve({
          mapData,
          imageDataURL,
          hasMetadata: true,
          imageWidth: width,
          imageHeight: height
        });
      } catch (error) {
        reject(new Error('Failed to extract map data: ' + error.message));
      }
    };

    reader.onerror = () => reject(new Error('Failed to read file'));
    reader.readAsArrayBuffer(file);
  });
}

/**
 * Adds a tEXt chunk to a PNG file
 * @param {Uint8Array} pngData - Original PNG data
 * @param {string} keyword - Metadata keyword
 * @param {string} text - Metadata text
 * @returns {Uint8Array} - Modified PNG data
 */
function addTextChunkToPNG(pngData, keyword, text) {
  // Verify PNG signature
  if (!isPNG(pngData)) {
    throw new Error('Invalid PNG file');
  }

  // PNG signature is 8 bytes
  const signature = pngData.slice(0, 8);

  // Find the IEND chunk (last chunk in PNG)
  let iendPosition = findChunk(pngData, 'IEND');

  if (iendPosition === -1) {
    throw new Error('Invalid PNG: IEND chunk not found');
  }

  // Create tEXt chunk
  const textChunk = createTextChunk(keyword, text);

  // Combine: signature + original chunks (before IEND) + tEXt chunk + IEND chunk
  const beforeIEND = pngData.slice(0, iendPosition);
  const iendChunk = pngData.slice(iendPosition);

  const result = new Uint8Array(beforeIEND.length + textChunk.length + iendChunk.length);
  result.set(beforeIEND, 0);
  result.set(textChunk, beforeIEND.length);
  result.set(iendChunk, beforeIEND.length + textChunk.length);

  return result;
}

/**
 * Extracts a tEXt chunk from a PNG file
 * @param {Uint8Array} pngData - PNG data
 * @param {string} keyword - Metadata keyword to search for
 * @returns {string|null} - Extracted text or null if not found
 */
function extractTextChunkFromPNG(pngData, keyword) {
  if (!isPNG(pngData)) {
    throw new Error('Invalid PNG file');
  }

  let offset = 8; // Skip PNG signature

  while (offset < pngData.length) {
    // Read chunk length (4 bytes, big-endian)
    const length = readUint32BE(pngData, offset);
    offset += 4;

    // Read chunk type (4 bytes)
    const type = String.fromCharCode(...pngData.slice(offset, offset + 4));
    offset += 4;

    // Read chunk data
    const data = pngData.slice(offset, offset + length);
    offset += length;

    // Skip CRC (4 bytes)
    offset += 4;

    // Check if this is a tEXt chunk with our keyword
    if (type === 'tEXt') {
      const nullIndex = data.indexOf(0);
      if (nullIndex !== -1) {
        const chunkKeyword = String.fromCharCode(...data.slice(0, nullIndex));
        if (chunkKeyword === keyword) {
          const text = String.fromCharCode(...data.slice(nullIndex + 1));
          return text;
        }
      }
    }

    // Stop at IEND chunk
    if (type === 'IEND') {
      break;
    }
  }

  return null;
}

/**
 * Creates a tEXt chunk
 * @param {string} keyword - Metadata keyword
 * @param {string} text - Metadata text
 * @returns {Uint8Array} - Complete tEXt chunk with length and CRC
 */
function createTextChunk(keyword, text) {
  // Keyword + null separator + text
  const keywordBytes = stringToBytes(keyword);
  const textBytes = stringToBytes(text);
  const dataLength = keywordBytes.length + 1 + textBytes.length;

  // Create chunk data: keyword + 0x00 + text
  const chunkData = new Uint8Array(dataLength);
  chunkData.set(keywordBytes, 0);
  chunkData[keywordBytes.length] = 0; // Null separator
  chunkData.set(textBytes, keywordBytes.length + 1);

  // Create chunk type
  const chunkType = stringToBytes('tEXt');

  // Calculate CRC
  const crcData = new Uint8Array(4 + dataLength);
  crcData.set(chunkType, 0);
  crcData.set(chunkData, 4);
  const crc = calculateCRC(crcData);

  // Assemble complete chunk: length + type + data + CRC
  const chunk = new Uint8Array(4 + 4 + dataLength + 4);
  writeUint32BE(chunk, 0, dataLength);
  chunk.set(chunkType, 4);
  chunk.set(chunkData, 8);
  writeUint32BE(chunk, 8 + dataLength, crc);

  return chunk;
}

/**
 * Checks if data is a valid PNG
 * @param {Uint8Array} data - Data to check
 * @returns {boolean} - True if valid PNG
 */
function isPNG(data) {
  if (data.length < 8) return false;

  // PNG signature: 137 80 78 71 13 10 26 10
  return data[0] === 137 &&
         data[1] === 80 &&
         data[2] === 78 &&
         data[3] === 71 &&
         data[4] === 13 &&
         data[5] === 10 &&
         data[6] === 26 &&
         data[7] === 10;
}

/**
 * Finds a chunk in PNG data
 * @param {Uint8Array} pngData - PNG data
 * @param {string} chunkType - Chunk type to find (e.g., 'IEND')
 * @returns {number} - Position of chunk or -1 if not found
 */
function findChunk(pngData, chunkType) {
  let offset = 8; // Skip PNG signature

  while (offset < pngData.length) {
    const length = readUint32BE(pngData, offset);
    const type = String.fromCharCode(...pngData.slice(offset + 4, offset + 8));

    if (type === chunkType) {
      return offset;
    }

    // Move to next chunk: length(4) + type(4) + data(length) + crc(4)
    offset += 4 + 4 + length + 4;
  }

  return -1;
}

/**
 * Reads a 32-bit unsigned integer (big-endian)
 * @param {Uint8Array} data - Data array
 * @param {number} offset - Offset to read from
 * @returns {number} - The integer value
 */
function readUint32BE(data, offset) {
  return (data[offset] << 24) |
         (data[offset + 1] << 16) |
         (data[offset + 2] << 8) |
         data[offset + 3];
}

/**
 * Writes a 32-bit unsigned integer (big-endian)
 * @param {Uint8Array} data - Data array
 * @param {number} offset - Offset to write to
 * @param {number} value - Value to write
 */
function writeUint32BE(data, offset, value) {
  data[offset] = (value >>> 24) & 0xFF;
  data[offset + 1] = (value >>> 16) & 0xFF;
  data[offset + 2] = (value >>> 8) & 0xFF;
  data[offset + 3] = value & 0xFF;
}

/**
 * Converts string to byte array
 * @param {string} str - String to convert
 * @returns {Uint8Array} - Byte array
 */
function stringToBytes(str) {
  const bytes = new Uint8Array(str.length);
  for (let i = 0; i < str.length; i++) {
    bytes[i] = str.charCodeAt(i);
  }
  return bytes;
}

/**
 * Calculates CRC32 for PNG chunk
 * @param {Uint8Array} data - Data to calculate CRC for
 * @returns {number} - CRC32 value
 */
function calculateCRC(data) {
  let crc = 0xFFFFFFFF;

  for (let i = 0; i < data.length; i++) {
    crc = crc ^ data[i];
    for (let j = 0; j < 8; j++) {
      if (crc & 1) {
        crc = (crc >>> 1) ^ 0xEDB88320;
      } else {
        crc = crc >>> 1;
      }
    }
  }

  return (crc ^ 0xFFFFFFFF) >>> 0;
}

/**
 * Converts blob to data URL
 * @param {Blob} blob - Blob to convert
 * @returns {Promise<string>} - Data URL
 */
function blobToDataURL(blob) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
}

/**
 * Gets image dimensions from data URL
 * @param {string} dataURL - Image data URL
 * @returns {Promise<{width: number, height: number}>} - Image dimensions
 */
function getImageDimensions(dataURL) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => {
      resolve({ width: img.width, height: img.height });
    };
    img.onerror = () => reject(new Error('Failed to load image'));
    img.src = dataURL;
  });
}
