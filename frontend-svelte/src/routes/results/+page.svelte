<script lang="ts">
    import { authStore } from "$lib/store/auth.js";
    import { resultsService, type ResultOutput, type ResultStatisticsOutput, type Ranking } from "$lib/services/result";
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';

    let results: ResultOutput[] = [];
    let statistics: ResultStatisticsOutput | null = null;
    let rankings: Ranking[] = [];
    let loading = true;

    onMount(async () => {
        await loadData();
    });

    async function loadData() {
        loading = true;
        try {
            // Récupérer les résultats de l'utilisateur
            const resultsResponse = await resultsService.getMyResults();
            results = resultsResponse.data.results;
            statistics = resultsResponse.data.statistics;

            // Récupérer le classement
            const rankingsResponse = await resultsService.getRankings();
            rankings = rankingsResponse.data.rankings;
        } catch (error) {
            console.error("Erreur lors du chargement des données:", error);
            alert("Erreur lors du chargement des données");
        } finally {
            loading = false;
        }
    }
</script>

<div class="min-h-screen flex items-center justify-center bg-linear-to-br from-blue-50 to-indigo-100">
    <div class="max-w-8xl w-8xl mx-auto p-8 text-center flex gap-8 justify-center">

        {#if !$authStore.isAuthenticated}

            <div class="space-y-4">
                <p class="text-gray-700">
                    Connectez-vous pour accéder à votre planning, vos matchs et vos résultats
                </p>
                <a href="/login" class="inline-block px-8 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors shadow-lg">
                    Se connecter
                </a>
            </div>

        {:else}

            {#if loading}
                <div class="bg-white rounded-2xl shadow-xl p-8">
                    <p class="text-center text-gray-600">Chargement...</p>
                </div>
            {:else}
            <div class="bg-white rounded-2xl shadow-xl p-8">
                <div class="flex flex-col items-center gap-6 p-7 rounded-2xl">
                    <h1 class="font-medium text-gray-600 dark:text-gray-400">Matchs les plus récents</h1>
                </div>

                <div class="flex flex-col items-center gap-6 p-7 rounded-2xl">
                    {#if results.length === 0}
                        <p class="text-gray-500">Aucun résultat disponible</p>
                    {:else}
                        {#each results as resultat}
                        <div class="w-full max-w-2xl bg-white border border-gray-200 rounded-lg shadow-md p-6">
                            <div class="mb-4">
                                <h2 class="text-2xl font-semibold mb-2">Match du {new Date(resultat.date).toLocaleDateString('fr-FR')}</h2>

                                <p class="text-gray-600">
                                    Adversaire: {resultat.opponents.players.join(', ')} ({resultat.opponents.company})
                                </p>

                                <p class="text-gray-800 font-semibold">
                                    Score: {resultat.score}
                                </p>

                                {#if resultat.result === 'VICTOIRE'}
                                    <p class="font-semibold">
                                        <span class="text-black">Résultat :</span>
                                        <span class="text-green-600"> Victoire !</span>
                                    </p>
                                {:else}
                                    <p class="font-semibold">
                                        <span class="text-gray-600">Résultat :</span>
                                        <span class="text-red-600">Défaite..</span>
                                    </p>
                                {/if}
                            </div>

                        </div>
                    {/each}
                    {/if}
                </div>
            </div>

            <div class="bg-white rounded-2xl shadow-xl p-8">
                <div class="flex flex-col items-center gap-6 p-7 rounded-2xl">
                    <h1 class="font-medium text-gray-600 dark:text-gray-400">Classement des équipes du tournois</h1>
                </div>

                <div class="flex flex-col items-center gap-6 p-7 rounded-2xl">
                    {#if rankings.length === 0}
                        <p class="text-gray-500">Aucun classement disponible</p>
                    {:else}
                        {#each rankings as classement}
                        <div class="w-full max-w-2xl bg-white border border-gray-200 rounded-lg shadow-md p-6">
                            <div class="mb-4">
                                {#if classement.position === 1}
                                    <h2 class="text-2xl font-semibold mb-2 text-yellow-500">🥇 Position : {classement.position}</h2>
                                {:else if classement.position === 2}
                                    <h2 class="text-2xl font-semibold mb-2 text-gray-400">🥈 Position : {classement.position}</h2>
                                {:else if classement.position === 3}
                                    <h2 class="text-2xl font-semibold mb-2 text-yellow-800">🥉 Position : {classement.position}</h2>
                                {:else}
                                    <h2 class="text-2xl font-semibold mb-2">Position : {classement.position}</h2>
                                {/if}

                                <p class="text-gray-600">
                                    <span class="font-semibold">Nombre de matchs joués: {classement.matches_played} (</span>
                                    <span class="font-semibold text-green-500">{classement.wins}</span>
                                    <span class="font-semibold"> ; </span>
                                    <span class="font-semibold text-red-500">{classement.losses}</span>
                                    <span class="font-semibold">)</span>
                                </p>

                                <p class="text-gray-800 font-semibold">Points: {classement.points}</p>
                                <p class="text-gray-800 font-semibold">Set gagnés: {classement.sets_won}</p>
                                <p class="text-gray-800 font-semibold">Set perdus: {classement.sets_lost}</p>
                            </div>
                        </div>
                    {/each}
                    {/if}
                </div>
            </div>
            {/if}
            
        {/if}
    </div> 
</div> 
