<!-- ============================================
FICHIER : src/routes/HomePage.svelte
============================================ -->

<script>
    import { authStore } from "$lib/store/auth.js";
    import profile from "$lib/data/profile_test.json"; 
    // authStore est supposé être un store Svelte (writable/derived)
    // Exemple : export const authStore = writable({ isAuthenticated: false, user: null, isAdmin: false });
</script>

<div
    class="min-h-screen flex items-center justify-center bg-linear-to-br from-blue-50 to-indigo-100"
>
    <div class="max-w-4xl mx-auto p-8 text-center">
  
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

      
<span class="flex gap-2 font-medium text-gray-600 dark:text-gray-400"><h1>Profil utilisateur</h1></span>
<div class="flex flex-col items-center gap-6 p-7 rounded-2xl">
  <div>
    <img class="size-48 shadow-xl rounded-md" alt="" src={`${profile.filename}`} />
  </div>
  <div class="flex items-center">
    <span class="text-2xl font-medium"><p><strong>Nom :</strong> {profile.nom}</p>
    <p><strong>Prénom :</strong> {profile.prenom}</p>
    <p><strong>Date de naissance :</strong> {profile.date_naissance}</p>
    <p><strong>Email :</strong> {profile.email}</p>
    <p><strong>Numéro de licence :</strong> {profile.numero_licence}</p></span>
    <span class="flex gap-2 font-medium text-gray-600 dark:text-gray-400">
    </span>
  </div>
</div>



        {/if}
    </div>
</div>
