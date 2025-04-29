export enum UserRole {
  ADMIN = "admin",
  USER = "user",
}

export interface UserCreate {
  email: string;
  password: string;
  name: string;
  username: string;
  profile_picture?: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface User {
  id: number;
  name: string;
  username: string;
  email: string;
  profile_image_url: string;
  is_superuser: boolean;
  role: UserRole;
}

export interface UserUpdate {
  name?: string;
  role?: UserRole;
}

export interface Token {
  access_token: string;
  refresh_token: string;
}