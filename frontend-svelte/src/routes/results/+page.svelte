<script>
    import { authStore } from "$lib/store/auth.js";
    import match from "$lib/data/match_test.json";
    import ranking from "$lib/data/ranking_test.json";
    import { goto } from '$app/navigation';
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

            <div class="bg-white rounded-2xl shadow-xl p-8">
                <div class="flex flex-col items-center gap-6 p-7 rounded-2xl">
                    <h1 class="font-medium text-gray-600 dark:text-gray-400">Matchs les plus récents</h1>
                </div>

                <div class="flex flex-col items-center gap-6 p-7 rounded-2xl">
                    {#each match.results as resultat}
                        <div class="w-full max-w-2xl bg-white border border-gray-200 rounded-lg shadow-md p-6">
                            <div class="mb-4">
                                <h2 class="text-2xl font-semibold mb-2">Match du {resultat.date}</h2>

                                <p class="text-gray-600">
                                    Adversaire: {resultat.opponents.players} ({resultat.opponents.company})
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
                </div>
            </div>

            <div class="bg-white rounded-2xl shadow-xl p-8">
                <div class="flex flex-col items-center gap-6 p-7 rounded-2xl">
                    <h1 class="font-medium text-gray-600 dark:text-gray-400">Classement des équipes du tournois</h1>
                </div>

                <div class="flex flex-col items-center gap-6 p-7 rounded-2xl">
                    {#each ranking.rankings as classement}
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
                </div>
            </div>
            
        {/if}
    </div> 
</div> 
