export interface Book {
  id: number;
  title: string;
  author: string;
  genre?: string;
  rating?: number;
  cover_image?: string;
  uploaded_by?: string;
}

export class UploadRequest {
}