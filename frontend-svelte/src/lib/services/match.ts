import api from './api';
import type { TeamOutput } from './team';

/**
 * This is the status of a match.
 */
export enum Status {
    A_VENIR = "A_VENIR",
    ANNULE = "ANNULE",
    TERMINE = "TERMINE"
}



/**
 * This interface represents a match.
 */
export interface MatchOutput {
  /**
   * Match identifier.
   */
  id: number;

  /**
   * Event information.
   */
  event: {
    event_date: string;
    event_time: string;
  };

  /**
   * Court number.
   */
  court_number: number;

  /**
   * First team.
   */
  team1: TeamOutput;

  /**
   * Second team.
   */
  team2: TeamOutput;

  /**
   * Match status.
   */
  status: Status;

  /**
   * Score for team 1.
   */
  score_team1?: string | null;

  /**
   * Score for team 2.
   */
  score_team2?: string | null;
}



/**
 * This interface represents a match update request.
 */
export interface MatchInput {
  /**
   * Court number.
   */
  court_number: number;
  
  /**
   * Match status.
   */
  status: string;

  /**
   * The first team id.
   */
  team1_id: number;

  /**
   * The second team id.
   */
  team2_id: number;

  /**
   * Score for team 1.
   */
  score_team1?: string;

  /**
   * Score for team 2.
   */
  score_team2?: string;
}



export const matchesService = {

  /**
   * This function gets all matches.
   * 
   * @param params Optional filters.
   * @return Return all matches.
   */
  getAllMatches(params?: {
    upcoming?: boolean;
    team_id?: number;
    status?: string;
    my_matches?: boolean;
  }) {
    return api.get<{ matches: MatchOutput[]; total: number }>('/matches', {
      params
    });
  },



  /**
   * This function updates a match.
   * 
   * @param matchId Match identifier.
   * @param input Match informations.
   * @return Return the updated match.
   */
  updateMatch(matchId: number, input: MatchInput) {
    return api.put<MatchOutput>(`/matches/${matchId}`, input);
  },



  /**
   * This function deletes a match.
   * 
   * @param matchId Match identifier.
   * @return Return no content.
   */
  deleteMatch(matchId: number) {
    return api.delete(`/matches/${matchId}`);
  }
};
