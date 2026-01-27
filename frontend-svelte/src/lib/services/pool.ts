import api from './api';

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

  /**
   * Number of teams.
   */
  teams_count: number;

  /**
   * Name of teams.
   */
  teams: string[]
}



/**
 * This interface represents a pool request.
 */
export interface PoolInput {
  /**
   * Pool name.
   */
  name: string;

  /**
   * Teams identifiers.
   */
  team_ids: number[];
}



export const poolsService = {

  /**
   * This function gets all pools.
   * 
   * @return Return all pools.
   */
  getAllPools() {
    return api.get<{ pools: PoolOutput[] }>('/pools');
  },



  /**
   * This function gets a specific pool.
   * 
   * @param poolId The pool's id.
   * @return Return the pool.
   */
  getPlayer(poolId: number) {
    return api.get<PoolOutput>(`/pools/${poolId}`);
  },



  /**
   * This function creates a pool.
   * 
   * @param input Pool informations.
   * @return Return the created pool.
   */
  createPool(input: PoolInput) {
    return api.post<PoolOutput>('/pools', input);
  },



  /**
   * This function updates a pool.
   * 
   * @param poolId Pool identifier.
   * @param input Pool informations.
   * @return Return the updated pool.
   */
  updatePool(poolId: number, input: PoolInput) {
    return api.put<PoolOutput>(`/pools/${poolId}`, input);
  },



  /**
   * This function deletes a pool.
   * 
   * @param poolId Pool identifier.
   * @return Return no content.
   */
  deletePool(poolId: number) {
    return api.delete(`/pools/${poolId}`);
  }
};
