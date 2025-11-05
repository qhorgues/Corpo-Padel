import { writable } from "svelte/store";
import { authAPI } from "$lib/services/api";
import { goto } from "$app/navigation";
import type { RequestEvent } from "@sveltejs/kit";

interface User {
  email: string;
  is_admin?: boolean;
  [key: string]: unknown;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isAdmin: boolean;
}

function createAuthStore() {
  const { subscribe, set, update } = writable<AuthState>({
    user: null,
    token: null,
    isAuthenticated: false,
    isAdmin: false,
  });

  return {
    subscribe,

    checkAuth: (): void => {
      const token = localStorage.getItem("token");
      const userJson = localStorage.getItem("user");
      const user = userJson ? (JSON.parse(userJson) as User) : null;

      if (token && user) {
        set({ user, token, isAuthenticated: true, isAdmin: !user.is_admin });
      }
    },

    login: async (email: string, password: string): Promise<void> => {
      const response = await authAPI.login(email, password);
      const { token, user } = response.data;

      localStorage.setItem("token", token);
      localStorage.setItem("user", JSON.stringify(user));

      set({
        user,
        token,
        isAuthenticated: true,
        isAdmin: !user.is_admin,
      });
      goto("/");
    },

    logout: async (): Promise<void> => {
      try {
        await authAPI.logout();
      } catch (error) {
        console.error(error);
      }

      localStorage.removeItem("token");
      localStorage.removeItem("user");
      set({ user: null, token: null, isAuthenticated: false, isAdmin: false });
      goto("/login");
    },
  };
}

export const authStore = createAuthStore();

export async function getAuth(event: RequestEvent) {
  // Exemple simple : récupère le token dans les cookies
  const token = event.cookies.get("token");
  const userStr = event.cookies.get("user");

  if (token && userStr) {
    const user: User = JSON.parse(userStr);
    return {
      user,
      isAuthenticated: true,
      isAdmin: user.isAdmin,
    };
  }

  return {
    user: null,
    isAuthenticated: false,
    isAdmin: false,
  };
}
