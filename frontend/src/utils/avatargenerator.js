import { createAvatar } from '@dicebear/core';
import * as collection from '@dicebear/collection';

/**
 * Generates an avatar SVG based on the provided seed and style.
 *
 * @param {string} seed - Unique seed to generate a consistent avatar.
 * @param {string} style - Style name from @dicebear/collection (e.g., 'micah', 'bottts').
 * @returns {Promise<string>} - SVG string of the avatar.
 */
async function generateAvatarSvg(seed = 'default-seed', style = 'micah') {
  const selectedStyle = collection[style];

  if (!selectedStyle) {
    throw new Error(`Avatar style "${style}" not found in @dicebear/collection.`);
  }

  const avatar = createAvatar(selectedStyle, {
    seed,
    backgroundColor: ['b6e3f4', 'c0aede', 'd1d4f9'],
    size: 128,
  });

  const svg = await avatar.toString();
  return svg;
}


export default generateAvatarSvg