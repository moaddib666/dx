/**
 * PNG Metadata Utilities
 * Handles embedding and extracting map data in PNG files
 * Based on PNG specification for tEXt and zTXt chunks
 */

/**
 * Embeds map data as metadata in a PNG image
 * @param {string|HTMLCanvasElement} imageSource - Data URL of the original PNG or canvas (for backward compatibility)
 * @param {Object} mapData - The map data to embed
 * @returns {Promise<Blob>} - PNG blob with embedded metadata
 */
export async function embedMetadataInPNG(imageSource, mapData) {
  return new Promise(async (resolve, reject) => {
    try {
      // Convert map data to JSON string
      const metadataJSON = JSON.stringify(mapData);
      console.log('[PNG Export] Starting PNG metadata embedding...');
      console.log('[PNG Export] Map data object:', {
        hasMetadata: !!mapData.metadata,
        metadataName: mapData.metadata?.name,
        hasGrid: !!mapData.grid,
        gridConfig: mapData.grid,
        hasLayers: !!mapData.layers,
        layersCount: mapData.layers?.length,
        hasCells: !!mapData.cells,
        cellsCount: mapData.cells?.length
      });
      console.log('[PNG Export] Metadata JSON length:', metadataJSON.length, 'characters');
      console.log('[PNG Export] First 200 chars of JSON:', metadataJSON.substring(0, 200));

      let pngBlob;

      // Check if imageSource is a data URL (string) or canvas
      if (typeof imageSource === 'string') {
        // It's a data URL - convert to blob
        pngBlob = await dataURLToBlob(imageSource);
      } else if (imageSource instanceof HTMLCanvasElement) {
        // It's a canvas - convert to blob (backward compatibility)
        pngBlob = await new Promise((res, rej) => {
          imageSource.toBlob((blob) => {
            if (!blob) {
              rej(new Error('Failed to create PNG blob from canvas'));
              return;
            }
            res(blob);
          }, 'image/png', 1.0);
        });
      } else {
        reject(new Error('Invalid image source: must be a data URL string or HTMLCanvasElement'));
        return;
      }

      // Read the PNG blob as ArrayBuffer
      const arrayBuffer = await pngBlob.arrayBuffer();
      const uint8Array = new Uint8Array(arrayBuffer);

      // Create a new PNG with embedded metadata
      const pngWithMetadata = addTextChunkToPNG(uint8Array, 'TabletopMapData', metadataJSON);

      // Create a new blob from the modified PNG
      const newBlob = new Blob([pngWithMetadata], { type: 'image/png' });
      resolve(newBlob);
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
  console.log('[PNG Import] Starting extraction from file:', file.name, 'Size:', file.size, 'bytes');

  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = async (e) => {
      try {
        const arrayBuffer = e.target.result;
        const uint8Array = new Uint8Array(arrayBuffer);

        // Extract metadata from PNG
        console.log('[PNG Import] Searching for TabletopMapData chunk in PNG...');
        const metadata = extractTextChunkFromPNG(uint8Array, 'TabletopMapData');

        // Convert the PNG to data URL for display
        const blob = new Blob([uint8Array], { type: 'image/png' });
        const imageDataURL = await blobToDataURL(blob);

        // Load image to get dimensions
        const { width, height } = await getImageDimensions(imageDataURL);
        console.log('[PNG Import] Image dimensions:', width, 'x', height, 'pixels');

        if (!metadata) {
          // No metadata found - return image data without map data
          console.log('[PNG Import] ❌ No metadata found in PNG. Will create default map.');
          resolve({
            mapData: null,
            imageDataURL,
            hasMetadata: false,
            imageWidth: width,
            imageHeight: height
          });
          return;
        }

        console.log('[PNG Import] ✅ Metadata found! Length:', metadata.length, 'characters');

        // Parse the JSON metadata
        const mapData = JSON.parse(metadata);
        console.log('[PNG Import] ✅ Metadata parsed successfully!');
        console.log('[PNG Import] Map name:', mapData.metadata?.name);
        console.log('[PNG Import] Grid config:', mapData.grid);
        console.log('[PNG Import] Layers:', mapData.layers?.length);
        console.log('[PNG Import] Cells:', mapData.cells?.length);

        resolve({
          mapData,
          imageDataURL,
          hasMetadata: true,
          imageWidth: width,
          imageHeight: height
        });
      } catch (error) {
        console.error('[PNG Import] ❌ Error during extraction:', error);
        reject(new Error('Failed to extract map data: ' + error.message));
      }
    };

    reader.onerror = () => {
      console.error('[PNG Import] ❌ Failed to read file');
      reject(new Error('Failed to read file'));
    };
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
  console.log('[PNG Export] addTextChunkToPNG called');
  console.log('[PNG Export] Keyword:', keyword);
  console.log('[PNG Export] Text length:', text.length, 'characters');
  console.log('[PNG Export] Text first 200 chars:', text.substring(0, 200));

  // Verify PNG signature
  if (!isPNG(pngData)) {
    throw new Error('Invalid PNG file');
  }

  // PNG signature is 8 bytes
  const signature = pngData.slice(0, 8);

  // FIRST: Remove any existing chunks with the same keyword
  console.log('[PNG Export] Removing existing chunks with keyword:', keyword);
  const pngWithoutOldChunks = removeTextChunks(pngData, keyword);
  console.log('[PNG Export] Old chunks removed, new size:', pngWithoutOldChunks.length, 'bytes');

  // Find the IEND chunk (last chunk in PNG)
  let iendPosition = findChunk(pngWithoutOldChunks, 'IEND');

  if (iendPosition === -1) {
    throw new Error('Invalid PNG: IEND chunk not found');
  }

  console.log('[PNG Export] IEND chunk found at position:', iendPosition);

  // Create tEXt chunk
  const textChunk = createTextChunk(keyword, text);
  console.log('[PNG Export] Text chunk created, size:', textChunk.length, 'bytes');

  // Combine: signature + original chunks (before IEND) + tEXt chunk + IEND chunk
  const beforeIEND = pngWithoutOldChunks.slice(0, iendPosition);
  const iendChunk = pngWithoutOldChunks.slice(iendPosition);

  const result = new Uint8Array(beforeIEND.length + textChunk.length + iendChunk.length);
  result.set(beforeIEND, 0);
  result.set(textChunk, beforeIEND.length);
  result.set(iendChunk, beforeIEND.length + textChunk.length);

  console.log('[PNG Export] Final PNG size:', result.length, 'bytes');
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

  console.log('[PNG Extract] Starting extraction, looking for keyword:', keyword);
  const textDecoder = new TextDecoder('utf-8');
  let offset = 8; // Skip PNG signature
  let chunkCount = 0;

  while (offset < pngData.length) {
    // Read chunk length (4 bytes, big-endian)
    const length = readUint32BE(pngData, offset);
    offset += 4;

    // Read chunk type (4 bytes)
    const type = String.fromCharCode(...pngData.slice(offset, offset + 4));
    offset += 4;

    chunkCount++;
    console.log(`[PNG Extract] Chunk ${chunkCount}: type="${type}", length=${length}`);

    // Read chunk data
    const data = pngData.slice(offset, offset + length);
    offset += length;

    // Skip CRC (4 bytes)
    offset += 4;

    // Check if this is a tEXt chunk with our keyword
    if (type === 'tEXt') {
      console.log('[PNG Extract] Found tEXt chunk, data length:', data.length);
      const nullIndex = data.indexOf(0);
      console.log('[PNG Extract] Null separator at index:', nullIndex);
      if (nullIndex !== -1) {
        const chunkKeyword = textDecoder.decode(data.slice(0, nullIndex));
        console.log('[PNG Extract] Chunk keyword:', chunkKeyword);
        if (chunkKeyword === keyword) {
          const textData = data.slice(nullIndex + 1);
          console.log('[PNG Extract] ✅ Found matching keyword! Text data length:', textData.length, 'bytes');
          const text = textDecoder.decode(textData);
          console.log('[PNG Extract] Decoded text length:', text.length, 'characters');
          console.log('[PNG Extract] First 200 chars:', text.substring(0, 200));
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
  console.log('[PNG Export] createTextChunk called');
  console.log('[PNG Export] Input text length:', text.length);

  const textEncoder = new TextEncoder();

  // Keyword + null separator + text
  const keywordBytes = textEncoder.encode(keyword);
  const textBytes = textEncoder.encode(text);
  const dataLength = keywordBytes.length + 1 + textBytes.length;

  console.log('[PNG Export] Keyword bytes length:', keywordBytes.length);
  console.log('[PNG Export] Text bytes length:', textBytes.length);
  console.log('[PNG Export] Total data length:', dataLength);

  // Create chunk data: keyword + 0x00 + text
  const chunkData = new Uint8Array(dataLength);
  chunkData.set(keywordBytes, 0);
  chunkData[keywordBytes.length] = 0; // Null separator
  chunkData.set(textBytes, keywordBytes.length + 1);

  // Create chunk type
  const chunkType = textEncoder.encode('tEXt');

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
 * Removes all tEXt chunks with a specific keyword from PNG data
 * @param {Uint8Array} pngData - Original PNG data
 * @param {string} keyword - Keyword to match for removal
 * @returns {Uint8Array} - PNG data without matching tEXt chunks
 */
function removeTextChunks(pngData, keyword) {
  if (!isPNG(pngData)) {
    throw new Error('Invalid PNG file');
  }

  const textDecoder = new TextDecoder('utf-8');
  const chunks = [];

  // Keep the PNG signature
  chunks.push(pngData.slice(0, 8));

  let offset = 8; // Skip PNG signature
  let removedCount = 0;

  while (offset < pngData.length) {
    // Read chunk length (4 bytes, big-endian)
    const length = readUint32BE(pngData, offset);

    // Read chunk type (4 bytes)
    const type = String.fromCharCode(...pngData.slice(offset + 4, offset + 8));

    // Calculate full chunk size: length(4) + type(4) + data(length) + crc(4)
    const chunkSize = 4 + 4 + length + 4;
    const chunkData = pngData.slice(offset, offset + chunkSize);

    // Check if this is a tEXt chunk with our keyword
    let shouldRemove = false;
    if (type === 'tEXt') {
      const data = pngData.slice(offset + 8, offset + 8 + length);
      const nullIndex = data.indexOf(0);
      if (nullIndex !== -1) {
        const chunkKeyword = textDecoder.decode(data.slice(0, nullIndex));
        if (chunkKeyword === keyword) {
          shouldRemove = true;
          removedCount++;
          console.log('[PNG Export] Removing old tEXt chunk with keyword:', keyword);
        }
      }
    }

    // Keep the chunk if it's not a matching tEXt chunk
    if (!shouldRemove) {
      chunks.push(chunkData);
    }

    offset += chunkSize;

    // Stop at IEND chunk
    if (type === 'IEND') {
      break;
    }
  }

  console.log('[PNG Export] Removed', removedCount, 'old chunk(s) with keyword:', keyword);

  // Combine all chunks
  const totalLength = chunks.reduce((sum, chunk) => sum + chunk.length, 0);
  const result = new Uint8Array(totalLength);
  let position = 0;
  for (const chunk of chunks) {
    result.set(chunk, position);
    position += chunk.length;
  }

  return result;
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
 * Converts data URL to blob
 * @param {string} dataURL - Data URL to convert
 * @returns {Promise<Blob>} - Blob
 */
function dataURLToBlob(dataURL) {
  return new Promise((resolve, reject) => {
    try {
      // Split the data URL
      const parts = dataURL.split(',');
      if (parts.length !== 2) {
        reject(new Error('Invalid data URL format'));
        return;
      }

      // Get the mime type
      const mimeMatch = parts[0].match(/:(.*?);/);
      const mime = mimeMatch ? mimeMatch[1] : 'image/png';

      // Decode base64
      const bstr = atob(parts[1]);
      const n = bstr.length;
      const u8arr = new Uint8Array(n);

      for (let i = 0; i < n; i++) {
        u8arr[i] = bstr.charCodeAt(i);
      }

      resolve(new Blob([u8arr], { type: mime }));
    } catch (error) {
      reject(new Error('Failed to convert data URL to blob: ' + error.message));
    }
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
