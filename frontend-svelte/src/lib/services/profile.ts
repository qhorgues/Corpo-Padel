import api from './api';
import type { Role } from './player';

/**
 * This interface represents the authenticated user.
 */
export interface ProfileUserOutput {
  /**
   * User identifier.
   */
  id: number;

  /**
   * User email.
   */
  email: string;

  /**
   * User role.
   */
  role: Role;
}



/**
 * This interface represents the player profile.
 */
export interface ProfilePlayerOutput {
  /**
   * Player identifier.
   */
  id: number;

  /**
   * First name.
   */
  first_name: string;

  /**
   * Last name.
   */
  last_name: string;

  /**
   * Company name.
   */
  company: string;

  /**
   * License number.
   */
  license_number: string;

  /**
   * Birth date.
   */
  birth_date?: string;

  /**
   * Profile photo URL.
   */
  photo_url?: string | null;
}



/**
 * This interface represents the profile response.
 */
export interface ProfileOutput {
  /**
   * User informations.
   */
  user: ProfileUserOutput;

  /**
   * Player informations.
   */
  player: ProfilePlayerOutput;
}



/**
 * This interface represents profile update data.
 */
export interface ProfileInput {
  /**
   * First name.
   */
  first_name?: string;

  /**
   * Last name.
   */
  last_name?: string;

  /**
   * Company name.
   */
  company?: string;

  /**
   * The email.
   */
  email?: string

  /**
   * License number.
   */
  license_number?: string;

  /**
   * Birth date.
   */
  birth_date?: string;

  /**
   * Profile photo URL.
   */
  photo_url?: string | null;
}



/**
 * This interface represents the container for the photo URI.
 */
export interface ProfilePhoto {
    /**
     * The URI of the image (yes it's write URL instead of URI).
     */
    photo_url: string
}



export const profileService = {

  /**
   * This function gets the authenticated user profile.
   * 
   * @return Return profile informations.
   */
  getMyProfile() {
    return api.get<ProfileOutput>('/profile/me');
  },



  /**
   * This function updates the authenticated user profile.
   * 
   * @param input Profile informations.
   * @return Return updated profile.
   */
  updateMyProfile(input: ProfileInput) {
    return api.put<ProfileOutput>('/profile/me', input);
  },



  /**
   * This function uploads a profile photo.
   * 
   * @param input The image URI.
   * @return Return updated profile.
   */
  uploadProfilePhoto(input: ProfilePhoto) {
    return api.post<ProfileOutput>('/profile/me/photo', input);
  },



  /**
   * This function deletes the profile photo.
   * 
   * @return Return updated profile.
   */
  deleteProfilePhoto() {
    return api.delete<ProfileOutput>('/profile/me/photo');
  }
};
