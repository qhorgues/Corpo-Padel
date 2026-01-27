import api from './api';

/**
 * This interface represents a match result.
 */
export interface ResultOutput {
  /**
   * Match identifier.
   */
  match_id: number;

  /**
   * Match date.
   */
  date: string;

  /**
   * Opponent informations.
   */
  opponents: {
    company: string;
    players: string[];
  };

  /**
   * Match score.
   */
  score: string;

  /**
   * Match result.
   */
  result: string;

  /**
   * Court number.
   */
  court_number: number;
}



/**
 * This interface represents result statistics.
 */
export interface ResultStatisticsOutput {
  /**
   * Total matches played.
   */
  total_matches: number;

  /**
   * Number of wins.
   */
  wins: number;

  /**
   * Number of losses.
   */
  losses: number;

  /**
   * Win rate percentage.
   */
  win_rate: number;
}



/**
 * This interface represents the ranking.
 */
export interface Ranking {
    /**
     * The positon of the company.
     */
    position: number;

    /**
     * The company's name.
     */
    company: string;

    /**
     * The number of match played.
     */
    matches_played: number;

    /**
     * The number of wins.
     */
    wins: number;

    /**
     * The number of losses.
     */
    losses: number;

    /**
     * The number of points.
     */
    points: number;

    /**
     * The number of sets won.
     */
    sets_won: number;

    /**
     * The number of sets lost.
     */
    sets_lost: number;
}



export const resultsService = {

  /**
   * This function gets results of the authenticated player.
   * 
   * @return Return player results and statistics.
   */
  getMyResults() {
    return api.get<{
      results: ResultOutput[];
      statistics: ResultStatisticsOutput;
    }>('/results/my-results');
  },



  /**
   * This function gets company rankings.
   * 
   * @return Return rankings.
   */
  getRankings() {
    return api.get<{
      rankings: Ranking[];
    }>('/results/rankings');
  }
};
