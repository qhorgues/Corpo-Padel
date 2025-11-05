// src/hooks.server.js
import { getAuth } from "$lib/store/auth";
import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
  const auth = await getAuth(event);

  // Redirection si non connecté
  if (event.url.pathname.startsWith('/admin') && !auth?.isAdmin) {
    return Response.redirect(new URL('/login', event.url), 303);
  }

  if (event.url.pathname.startsWith('/profile') && !auth?.isAuthenticated) {
    return Response.redirect(new URL('/login', event.url), 303);
  }

  return resolve(event);
};
