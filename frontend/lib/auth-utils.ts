/**
 * Auth utility functions for getting Supabase tokens
 */

import { createClient } from '@/lib/supabase/client';

/**
 * Get the current Supabase auth token
 * @returns The access token or null if not authenticated
 */
export async function getAuthToken(): Promise<string | null> {
  try {
    const supabase = createClient();
    const { data: { session }, error } = await supabase.auth.getSession();

    if (error || !session) {
      console.error('No auth session found:', error);
      return null;
    }

    return session.access_token;
  } catch (err) {
    console.error('Error getting auth token:', err);
    return null;
  }
}
