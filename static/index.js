import { getKey } from './get.js';
if (process !== undefined) {
  process.env = (key) => getKey(key);
}