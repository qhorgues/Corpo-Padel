<!-- ============================================
FICHIER : src/routes/HomePage.svelte
============================================ -->

<script>
    import { authStore } from "$lib/store/auth.js";
    import admin from "$lib/data/admin_test.json"; 
</script>

{#if !$authStore.isAuthenticated}
    <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <div class="max-w-4xl mx-auto p-8 text-center">
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
        </div>
    </div>
{:else}
    {#if $authStore.isAdmin}
    <div class="h-screen w-screen bg-gradient-to-br from-blue-50 to-indigo-100 overflow-hidden">
        <div class="h-full bg-white shadow-xl overflow-auto">
            <h2 class="text-2xl font-bold text-gray-800 p-6 bg-gray-50 border-b sticky top-0">Liste des joueurs</h2>
            
            <!-- En-têtes -->
            <div class="grid grid-cols-[1fr_1fr_1.5fr_1fr_2fr] gap-6 px-8 py-3 bg-gray-100 border-b font-semibold text-gray-700 text-sm sticky top-[73px]">
                <div>Nom</div>
                <div>Prénom</div>
                <div>Entreprise</div>
                <div>Licence</div>
                <div>Email</div>
            </div>
            
            <!-- Lignes de données -->
            {#each admin.joueurs as joueur, index}
                <div class="grid grid-cols-[1fr_1fr_1.5fr_1fr_2fr] gap-6 px-8 py-4 border-b hover:bg-blue-50 transition-colors {index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}">
                    <div class="text-gray-900">{joueur.nom}</div>
                    <div class="text-gray-900">{joueur.prenom}</div>
                    <div class="text-gray-600">{joueur.entreprise}</div>
                    <div class="text-gray-600">{joueur.numero_licence}</div>
                    <div class="text-blue-600 text-sm">{joueur.email}</div>
                </div>
            {/each}
        </div>
    </div>
    {:else}
    <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <div class="max-w-4xl mx-auto p-8 text-center">
            <div class="space-y-4">
                <h2 class="text-3xl font-bold text-red-600">VOUS N'ÊTES PAS ADMIN</h2>
                <p class="text-gray-700">
                    Vous n'avez pas les autorisations nécessaires pour accéder à cette page.
                </p>
                <a
                    href="/"
                    class="inline-block px-8 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors shadow-lg"
                >
                    Retour à l'accueil
                </a>
            </div>
        </div>
    </div>
    {/if}
    
{/if}
