import api from './api';
import type { MatchInput } from './match';

/**
 * This interface represents a match inside an event.
 */
export interface EventMatchOutput {
  /**
   * Match identifier.
   */
  id: number;

  /**
   * Court number.
   */
  court_number: number;

  /**
   * Match status.
   */
  status: string;

  /**
   * This is the first team in the match.
   */ 
  team1_id: number

  /**
   * This is the second team in the match.
   */
  team2_id: number
}



/**
 * This interface represents an event.
 */
export interface EventOutput {
  /**
   * Event identifier.
   */
  id: number;

  /**
   * Event date.
   */
  event_date: string;

  /**
   * Event time.
   */
  event_time: string;

  /**
   * Event matches.
   */
  matches: EventMatchOutput[];
}



/**
 * This interface represents an event request.
 */
export interface EventInput {
  /**
   * Event date.
   */
  event_date: string;

  /**
   * Event time.
   */
  event_time: string;

  /**
   * Matches to create.
   */
  matches: MatchInput[];
}



export const eventsService = {

  /**
   * This function gets all events.
   * 
   * @param start_date The start date when to get the event (can be null).
   * @param end_date The end date when to get the event (can be null).
   * @param mine Filter to show only the event of the user.
   * @return Return all events.
   */
  getAllEvents(start_date?: Date, end_date?: Date, mine?: boolean) {
    return api.get<{ events: EventOutput[]; total: number }>('/events', {
      params: {
        start_date: start_date,
        end_date: end_date,
        mine: mine
      }
    });
  },



  /**
   * This function creates an event.
   * 
   * @param input Event informations.
   * @return Return the created event.
   */
  createEvent(input: EventInput) {
    return api.post<EventOutput>('/events', input);
  },



  /**
   * This function updates an event.
   * 
   * @param eventId Event identifier.
   * @param input Event informations.
   * @return Return the updated event.
   */
  updateEvent(eventId: number, input: EventInput) {
    return api.put<EventOutput>(`/events/${eventId}`, input);
  },



  /**
   * This function deletes an event.
   * 
   * @param eventId Event identifier.
   * @return Return no content.
   */
  deleteEvent(eventId: number) {
    return api.delete(`/events/${eventId}`);
  }
};
