import api from './api';

/**
 * This interface represents a team player.
 */
export interface TeamPlayerOutput {
  /**
   * Player identifier.
   */
  id: number;

  /**
   * Player first name.
   */
  first_name: string;

  /**
   * Player last name.
   */
  last_name: string;
}



/**
 * This interface represents a pool.
 */
export interface PoolOutput {
  /**
   * Pool identifier.
   */
  id: number;

  /**
   * Pool name.
   */
  name: string;
}



/**
 * This interface represents a team.
 */
export interface TeamOutput {
  /**
   * Team identifier.
   */
  id: number;

  /**
   * Company name.
   */
  company: string;

  /**
   * The first player.
   */
  player1: TeamPlayerOutput;

  /**
   * The second player.
   */
  player2: TeamPlayerOutput;

  /**
   * Team pool.
   */
  pool: PoolOutput;
}



/**
 * This interface represents a team creation request.
 */
export interface TeamInput {
  /**
   * Company name.
   */
  company: string;

  /**
   * First player identifier.
   */
  player1_id: number;

  /**
   * Second player identifier.
   */
  player2_id: number;

  /**
   * Pool identifier.
   */
  pool_id: number;
}



export const teamsService = {

  /**
   * This function gets all teams.
   * 
   * @param poolId Optional pool filter.
   * @param company Optional company filter.
   * @return Return all teams.
   */
  getAllTeams(poolId?: number, company?: string) {
    return api.get<{ teams: TeamOutput[]; total: number }>('/teams', {
      params: {
        pool_id: poolId,
        company: company
      }
    });
  },



  /**
   * This function gets a specific team.
   * 
   * @param teamId The team's id.
   * @return Return the team.
   */
  getTeam(teamId: number) {
    return api.get<TeamOutput>(`/teams/${teamId}`);
  },



  /**
   * This function creates a team.
   * 
   * @param input Team informations.
   * @return Return the created team.
   */
  createTeam(input: TeamInput) {
    return api.post<TeamOutput>('/teams', input);
  },



  /**
   * This function updates a team.
   * 
   * @param teamId Team identifier.
   * @param input Team informations.
   * @return Return the updated team.
   */
  updateTeam(teamId: number, input: TeamInput) {
    return api.put<TeamOutput>(`/teams/${teamId}`, input);
  },



  /**
   * This function deletes a team.
   * 
   * @param teamId Team identifier.
   * @return Return no content.
   */
  deleteTeam(teamId: number) {
    return api.delete(`/teams/${teamId}`);
  }
};
