export enum RequestType {
  BOOK = "book",
  ARTICLE = "article",
}

export enum RequestStatus {
  PENDING = "pending",
  APPROVED = "approved",
  REJECTED = "rejected",
}

export interface UploadRequestBase {
  title: string;
  author: string;
  type: RequestType;
  genre?: string;
  rating?: number;
  cover_image?: string;
  abstract?: string;
}

export interface UploadRequestCreate extends UploadRequestBase {}

export interface UploadRequestUpdate {
  title?: string;
  author?: string;
  genre?: string;
  rating?: number;
  cover_image?: string;
  abstract?: string;
  status?: RequestStatus;
}

export interface UploadRequestResponse extends UploadRequestBase {
  id: number;
  requested_by?: number;
  status: RequestStatus;
  created_at: string;
  updated_at: string;
}