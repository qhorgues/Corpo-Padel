import api from './api';

/**
 * This interface represents account creation response.
 */
export interface AdminAccountOutput {
  /**
   * Success message.
   */
  message: string;

  /**
   * Temporary password.
   */
  temporary_password: string;

  /**
   * Warning message.
   */
  warning: string;
}



export const adminService = {

  /**
   * This function resets a user's password.
   * 
   * @param userId User identifier.
   * @return Return new temporary password.
   */
  resetUserPassword(userId: number) {
    return api.post<{
      message: string;
      temporary_password: string;
      warning: string;
    }>(`/admin/accounts/${userId}/reset-password`);
  }
};
