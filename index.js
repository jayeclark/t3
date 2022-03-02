import { getKey } from 'get.js';

export const process = {
  env: (key) => getKey(key)
}