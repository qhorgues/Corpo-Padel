<script>
    import { authStore } from "$lib/store/auth.js";
    import match from "$lib/data/match_test.json";
    import ranking from "$lib/data/ranking_test.json";
    import Page from "../+page.svelte";
    import { goto } from '$app/navigation';
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
            <div class="bg-white rounded-2xl shadow-xl p-8">    
                <div class="flex flex-col items-center gap-6 p-7 rounded-2xl">
                    <span class="flex gap-2 font-medium text-gray-600 dark:text-gray-400">
                        <h1>Matchs les plus récents</h1>
                    </span>
                </div>    

                <div class="flex flex-col items-center gap-6 p-7 rounded-2xl">
                    {#each match.results as resultat}
                        <div class="w-full max-w-2xl bg-white border border-gray-200 rounded-lg shadow-md p-6">
                            <div class="mb-4">
                                <h2 class="text-2xl font-semibold mb-2">Match du {resultat.date}</h2>
                                <p class="text-gray-600">
                                    Adversaire: {resultat.adversaire.prenom} {resultat.adversaire.nom} ({resultat.adversaire.entreprise})
                                </p>
                            </div>
                            <div class="mb-4">
                                <p class="text-gray-800 font-semibold" 
                                   class:text-green-600={resultat.resultat === 'victoire'}
                                   class:text-red-600={resultat.resultat === 'defaite'}>
                                    Score: {resultat.score}
                                </p>
                                <p class="text-gray-800">Piste: {resultat.piste}</p>
                                <p class="text-gray-600 text-sm mt-2">
                                    {resultat.resultat === 'victoire' ? '✓ Victoire' : '✗ Défaite'}
                                </p>
                            </div>
                        </div>
                    {/each}
                </div>
            </div>
        {/if}
    </div>
</div>