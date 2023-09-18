/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export interface NewUser {
  /**
   * The username of the user.
   */
  username: string;
  /**
   * The full name of the user.
   */
  full_name?: string;
  /**
   * The URL of the user's profile picture.
   */
  profile_picture_url?: string;
  /**
   * The email of the user.
   */
  email: string;
  /**
   * The password of the user.
   */
  password: string;
}
export interface PublicUser {
  /**
   * The username of the user.
   */
  username: string;
  /**
   * The full name of the user.
   */
  full_name?: string;
  /**
   * The URL of the user's profile picture.
   */
  profile_picture_url?: string;
}
export interface Token {
  /**
   * The access token.
   */
  access_token: string;
  /**
   * The type of token.
   */
  token_type: string;
}
export interface TokenData {
  /**
   * The username.
   */
  username: string;
}
export interface User {
  /**
   * The username of the user.
   */
  username: string;
  /**
   * The full name of the user.
   */
  full_name?: string;
  /**
   * The URL of the user's profile picture.
   */
  profile_picture_url?: string;
  /**
   * The email of the user.
   */
  email: string;
  /**
   * Whether the user is disabled.
   */
  disabled?: boolean;
  /**
   * Whether the user's email is verified.
   */
  email_verified?: boolean;
  /**
   * Whether the user is an admin.
   */
  is_admin?: boolean;
}
