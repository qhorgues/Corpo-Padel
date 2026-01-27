import api from './api'

/**
 * This is the enumeration about the role.
 */
enum Role {
  JOUEUR = "JOUEUR",
  ADMINISTRATEUR = "ADMINISTRATEUR"
}



/**
 * This interface represents the response player.
 */
export interface PlayerOutput {
  /**
   * This is the player's id.
   */
  id: number;

  /**
   * This is the player's first name.
   */
  first_name: string;

  /**
   * This is the player's last name.
   */
  last_name: string;

  /**
   * This is the player's company name.
   */
  company: string;

  /**
   * This is the player's license.
   */
  license_number: string;

  /**
   * This is the player's birth date.
   */
  birth_date?: string;

  /**
   * This is the player's account.
   */
  photo_url?: string | null;
}



/**
 * This interface represents a request player.
 */
export interface PlayerInput {
  /**
   * This is the player's first name.
   */
  first_name: string;

  /**
   * This is the player's last name.
   */
  last_name: string;

  /**
   * This is the player's company name.
   */
  company: string;

  /**
   * This is the player's license.
   */
  license_number: string;

  /**
   * This is the player's email.
   */
  email: string;

  /**
   * This is the player's password.
   */
  password: string;

  /**
   * This is the player's role.
   */
  role: Role;

  /**
   * This is the player's birth date.
   */
  birth_date?: string;

  /**
   * This is the player's account.
   */
  photo_url?: string | null;
}



export const playersService = {

  /**
   * This function gets all the players.
   * 
   * @return Return all the players.
   */
  getAllPlayers() {
    return api.get<{ players: PlayerOutput[]; total: number }>("/players");
  },



  /**
   * This function gets a specific player.
   * 
   * @param playerId The player's id.
   * @return Return the player.
   */
  getPlayer(playerId: number) {
    return api.get<PlayerOutput>(`/players/${playerId}`);
  },



  /**
   * This function creates a player.
   * 
   * @param input The player's informations.
   * @return Return the created player.
   */
  createPlayer(input: PlayerInput) {
    return api.post<PlayerOutput>("/players", input);
  },



  /**
   * This function updates a player.
   * 
   * @param playerId The player's id.
   * @param input The player's informations.
   * @return Return the updated player.
   */
  updatePlayer(playerId: number, input: PlayerInput) {
    return api.put<PlayerOutput>(`/players/${playerId}`, input);
  },



  /**
   * This function deletes a player.
   * 
   * @param playerId The player's id.
   * @return Return no content. Or 404 if the player doesn't exist.
   */
  deletePlayer(playerId: number) {
    return api.delete(`/players/${playerId}`);
  }
};
