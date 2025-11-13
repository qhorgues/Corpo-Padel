<!-- ============================================
FICHIER : src/routes/HomePage.svelte
============================================ -->

<script>
    import { authStore } from "$lib/store/auth.js";
    import Match from "$lib/components/profile.svelte"; 
    // authStore est supposé être un store Svelte (writable/derived)
    // Exemple : export const authStore = writable({ isAuthenticated: false, user: null, isAdmin: false });
</script>

<div
    class="min-h-screen flex items-center justify-center bg-linear-to-br from-blue-50 to-indigo-100"
>
    <div class="max-w-4xl mx-auto p-8 text-center">
  


        <!-- Contenu conditionnel -->
        {#if !$authStore.isAuthenticated}
            <div class="space-y-4">
                <p class="text-gray-700">
                    Connectez-vous pour accéder à votre planning, vos matchs et
                    vos résultats
                </p>
                <a
                    href="/login"
                    class="inline-block px-8 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors shadow-lg"
                >
                    Se connecter
                </a>
            </div>
        {:else}

        <div class="Profile">     
                <Profile />
        </div>



        {/if}
    </div>
</div>
