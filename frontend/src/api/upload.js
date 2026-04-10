import { postFile } from './client';

export function uploadHtml(file) {
  return postFile('/api/upload-html', file);
}
