<!-- ============================================
FICHIER : src/routes/admin/teams-pools/+page.svelte
============================================ -->

<script lang="ts">
    import { authStore } from "$lib/store/auth.js";
    import { teamsService, type TeamOutput, type TeamInput } from "$lib/services/team";
    import { poolsService, type PoolOutput, type PoolInput } from "$lib/services/pool";
    import { playersService, type PlayerOutput } from "$lib/services/player";
    import { onMount } from "svelte";

    // Types
    type Tab = "teams" | "pools";

    // État général
    let currentTab: Tab = "teams";
    let loading = true;

    // Données
    let teams: TeamOutput[] = [];
    let pools: PoolOutput[] = [];
    let players: PlayerOutput[] = [];

    // Modales
    let showTeamModal = false;
    let showPoolModal = false;
    let showDeleteTeamModal = false;
    let showDeletePoolModal = false;

    // Édition
    let editMode = false;
    let currentTeam: TeamOutput | null = null;
    let currentPool: PoolOutput | null = null;
    let teamToDelete: TeamOutput | null = null;
    let poolToDelete: PoolOutput | null = null;

    // Formulaire équipe
    let teamForm = {
        company: "",
        pool_id: "",
        player1_id: "",
        player2_id: ""
    };

    // Formulaire poule
    let poolForm = {
        name: "",
        description: ""
    };

    // Charger les données
    onMount(async () => {
        await loadData();
    });

    async function loadData() {
        loading = true;
        try {
            const [teamsResponse, poolsResponse, playersResponse] = await Promise.all([
                teamsService.getAllTeams(),
                poolsService.getAllPools(),
                playersService.getAllPlayers()
            ]);

            teams = teamsResponse.data.teams;
            pools = poolsResponse.data.pools;
            players = playersResponse.data.players;
        } catch (error) {
            console.error("Erreur lors du chargement des données:", error);
            alert("Erreur lors du chargement des données");
        } finally {
            loading = false;
        }
    }

    // ========== GESTION DES ÉQUIPES ==========

    function openCreateTeamModal() {
        editMode = false;
        currentTeam = null;
        teamForm = {
            company: "",
            pool_id: "",
            player1_id: "",
            player2_id: ""
        };
        showTeamModal = true;
    }

    function openEditTeamModal(team: TeamOutput) {
        editMode = true;
        currentTeam = team;
        teamForm = {
            company: team.company,
            pool_id: String(team.pool.id),
            player1_id: String(team.player1.id),
            player2_id: String(team.player2.id)
        };
        showTeamModal = true;
    }

    async function saveTeam() {
        // Validation
        if (!teamForm.company || !teamForm.pool_id || !teamForm.player1_id || !teamForm.player2_id) {
            alert("Veuillez remplir tous les champs");
            return;
        }

        if (teamForm.player1_id === teamForm.player2_id) {
            alert("Les deux joueurs doivent être différents");
            return;
        }

        // Vérifier que les joueurs ne sont pas déjà dans une autre équipe
        const player1InTeam = teams.find(t => 
            (editMode && t.id !== currentTeam?.id) && 
            (t.player1.id === Number(teamForm.player1_id) || t.player2.id === Number(teamForm.player1_id))
        );
        const player2InTeam = teams.find(t => 
            (editMode && t.id !== currentTeam?.id) && 
            (t.player1.id === Number(teamForm.player2_id) || t.player2.id === Number(teamForm.player2_id))
        );

        if (player1InTeam) {
            const player = players.find(p => p.id === Number(teamForm.player1_id));
            alert(`${player?.first_name} ${player?.last_name} est déjà dans l'équipe ${player1InTeam.company}`);
            return;
        }

        if (player2InTeam) {
            const player = players.find(p => p.id === Number(teamForm.player2_id));
            alert(`${player?.first_name} ${player?.last_name} est déjà dans l'équipe ${player2InTeam.company}`);
            return;
        }

        try {
            const teamInput: TeamInput = {
                company: teamForm.company,
                pool_id: Number(teamForm.pool_id),
                player1_id: Number(teamForm.player1_id),
                player2_id: Number(teamForm.player2_id)
            };

            if (editMode && currentTeam) {
                await teamsService.updateTeam(currentTeam.id, teamInput);
            } else {
                await teamsService.createTeam(teamInput);
            }

            await loadData();
            showTeamModal = false;
        } catch (error) {
            console.error("Erreur lors de la sauvegarde:", error);
            alert("Erreur lors de la sauvegarde de l'équipe");
        }
    }

    function confirmDeleteTeam(team: TeamOutput) {
        teamToDelete = team;
        showDeleteTeamModal = true;
    }

    async function deleteTeam() {
        if (!teamToDelete) return;

        try {
            await teamsService.deleteTeam(teamToDelete.id);
            await loadData();
            showDeleteTeamModal = false;
            teamToDelete = null;
        } catch (error) {
            console.error("Erreur lors de la suppression:", error);
            alert("Erreur lors de la suppression de l'équipe");
        }
    }

    // ========== GESTION DES POULES ==========

    function openCreatePoolModal() {
        editMode = false;
        currentPool = null;
        poolForm = {
            name: "",
            description: ""
        };
        showPoolModal = true;
    }

    function openEditPoolModal(pool: PoolOutput) {
        editMode = true;
        currentPool = pool;
        poolForm = {
            name: pool.name,
            description: (pool as any).description || ""
        };
        showPoolModal = true;
    }

    async function savePool() {
        if (!poolForm.name) {
            alert("Veuillez saisir un nom de poule");
            return;
        }

        try {
            const poolInput: any = {
                name: poolForm.name
            };
            
            // Ajouter la description uniquement si elle existe dans le type PoolInput
            if (poolForm.description) {
                poolInput.description = poolForm.description;
            }

            if (editMode && currentPool) {
                await poolsService.updatePool(currentPool.id, poolInput);
            } else {
                await poolsService.createPool(poolInput);
            }

            await loadData();
            showPoolModal = false;
        } catch (error) {
            console.error("Erreur lors de la sauvegarde:", error);
            alert("Erreur lors de la sauvegarde de la poule");
        }
    }

    function confirmDeletePool(pool: PoolOutput) {
        // Vérifier qu'aucune équipe n'utilise cette poule
        const teamsInPool = teams.filter(t => t.pool.id === pool.id);
        if (teamsInPool.length > 0) {
            alert(`Impossible de supprimer cette poule. ${teamsInPool.length} équipe(s) l'utilise(nt) encore.`);
            return;
        }

        poolToDelete = pool;
        showDeletePoolModal = true;
    }

    async function deletePool() {
        if (!poolToDelete) return;

        try {
            await poolsService.deletePool(poolToDelete.id);
            await loadData();
            showDeletePoolModal = false;
            poolToDelete = null;
        } catch (error) {
            console.error("Erreur lors de la suppression:", error);
            alert("Erreur lors de la suppression de la poule");
        }
    }

    // ========== HELPERS ==========

    function getPlayerName(playerId: number): string {
        const player = players.find(p => p.id === playerId);
        return player ? `${player.first_name} ${player.last_name}` : "Inconnu";
    }

    function getPoolName(poolId: number): string {
        const pool = pools.find(p => p.id === poolId);
        return pool?.name || "Inconnue";
    }

    // Filtrer les joueurs disponibles (pas déjà dans une équipe)
    $: availablePlayers = players.filter(player => {
        const inTeam = teams.find(t => 
            (editMode && t.id !== currentTeam?.id ? true : true) &&
            (t.player1.id === player.id || t.player2.id === player.id)
        );
        return !inTeam;
    });

    // Joueurs déjà sélectionnés dans le formulaire
    $: selectedPlayer1 = teamForm.player1_id ? players.find(p => p.id === Number(teamForm.player1_id)) : null;
    $: selectedPlayer2 = teamForm.player2_id ? players.find(p => p.id === Number(teamForm.player2_id)) : null;
</script>

{#if !$authStore.isAdmin}
    <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <div class="max-w-4xl mx-auto p-8 text-center">
            <h2 class="text-3xl font-bold text-red-600 mb-4">Accès refusé</h2>
            <p class="text-gray-700 mb-6">Vous devez être administrateur pour accéder à cette page.</p>
            <a href="/" class="inline-block px-8 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors">
                Retour à l'accueil
            </a>
        </div>
    </div>
{:else}
    <div class="min-h-screen bg-gray-50 py-8">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <!-- En-tête -->
            <div class="mb-8">
                <div class="flex items-center gap-4 mb-2">
                    <a
                        href="/admin"
                        class="px-4 py-2 bg-gray-600 text-white rounded-lg font-semibold hover:bg-gray-700 transition-colors flex items-center gap-2"
                    >
                        ← Retour aux joueurs
                    </a>
                    <h1 class="text-4xl font-bold text-gray-900">Gestion des équipes et poules</h1>
                </div>
                <p class="text-gray-600">Créez et gérez les équipes et les poules de la saison</p>
            </div>

            <!-- Onglets -->
            <div class="bg-white rounded-lg shadow-md mb-6">
                <div class="border-b border-gray-200">
                    <nav class="flex -mb-px">
                        <button
                            on:click={() => currentTab = "teams"}
                            class="px-6 py-4 text-sm font-medium border-b-2 transition-colors {currentTab === 'teams'
                                ? 'border-blue-500 text-blue-600'
                                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}"
                        >
                            Équipes ({teams.length})
                        </button>
                        <button
                            on:click={() => currentTab = "pools"}
                            class="px-6 py-4 text-sm font-medium border-b-2 transition-colors {currentTab === 'pools'
                                ? 'border-blue-500 text-blue-600'
                                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}"
                        >
                            Poules ({pools.length})
                        </button>
                    </nav>
                </div>

                <!-- Contenu des onglets -->
                <div class="p-6">
                    {#if currentTab === "teams"}
                        <!-- Gestion des équipes -->
                        <div class="mb-4 flex justify-between items-center">
                            <h2 class="text-xl font-semibold text-gray-900">Liste des équipes</h2>
                            <button
                                on:click={openCreateTeamModal}
                                class="px-6 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                            >
                                ➕ Ajouter une équipe
                            </button>
                        </div>

                        {#if loading}
                            <div class="text-center py-12">
                                <div class="text-gray-500">Chargement...</div>
                            </div>
                        {:else if teams.length === 0}
                            <div class="text-center py-12">
                                <div class="text-6xl mb-4">👥</div>
                                <h3 class="text-xl font-semibold text-gray-700 mb-2">Aucune équipe</h3>
                                <p class="text-gray-500">Commencez par créer votre première équipe</p>
                            </div>
                        {:else}
                            <div class="space-y-4">
                                {#each teams as team}
                                    <div class="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                                        <div class="flex items-start justify-between">
                                            <div class="flex-1">
                                                <h3 class="text-xl font-semibold text-blue-600 mb-2">{team.company}</h3>
                                                <div class="space-y-2 text-gray-700">
                                                    <div class="flex items-center">
                                                        <span class="text-sm font-medium w-24">Poule:</span>
                                                        <span class="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-semibold">
                                                            {team.pool.name}
                                                        </span>
                                                    </div>
                                                    <div class="flex items-center">
                                                        <span class="text-sm font-medium w-24">Joueur 1:</span>
                                                        <span class="text-sm">{team.player1.first_name} {team.player1.last_name}</span>
                                                    </div>
                                                    <div class="flex items-center">
                                                        <span class="text-sm font-medium w-24">Joueur 2:</span>
                                                        <span class="text-sm">{team.player2.first_name} {team.player2.last_name}</span>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="ml-4 flex flex-col space-y-2">
                                                <button
                                                    on:click={() => openEditTeamModal(team)}
                                                    class="px-4 py-2 bg-yellow-500 text-white rounded-lg text-sm font-semibold hover:bg-yellow-600 transition-colors"
                                                >
                                                    ✏️ Modifier
                                                </button>
                                                <button
                                                    on:click={() => confirmDeleteTeam(team)}
                                                    class="px-4 py-2 bg-red-500 text-white rounded-lg text-sm font-semibold hover:bg-red-600 transition-colors"
                                                >
                                                    🗑️ Supprimer
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                {/each}
                            </div>
                        {/if}
                    {:else}
                        <!-- Gestion des poules -->
                        <div class="mb-4 flex justify-between items-center">
                            <h2 class="text-xl font-semibold text-gray-900">Liste des poules</h2>
                            <button
                                on:click={openCreatePoolModal}
                                class="px-6 py-2 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700 transition-colors"
                            >
                                ➕ Ajouter une poule
                            </button>
                        </div>

                        {#if loading}
                            <div class="text-center py-12">
                                <div class="text-gray-500">Chargement...</div>
                            </div>
                        {:else if pools.length === 0}
                            <div class="text-center py-12">
                                <div class="text-6xl mb-4">📋</div>
                                <h3 class="text-xl font-semibold text-gray-700 mb-2">Aucune poule</h3>
                                <p class="text-gray-500">Commencez par créer votre première poule</p>
                            </div>
                        {:else}
                            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                                {#each pools as pool}
                                    {@const teamsInPool = teams.filter(t => t.pool.id === pool.id)}
                                    <div class="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                                        <div class="flex items-start justify-between mb-4">
                                            <div>
                                                <h3 class="text-xl font-semibold text-purple-600 mb-2">{pool.name}</h3>
                                                {#if (pool as any).description}
                                                    <p class="text-sm text-gray-600 mb-3">{(pool as any).description}</p>
                                                {/if}
                                                <div class="text-sm text-gray-500">
                                                    {teamsInPool.length} équipe{teamsInPool.length > 1 ? 's' : ''}
                                                </div>
                                            </div>
                                        </div>
                                        <div class="flex gap-2">
                                            <button
                                                on:click={() => openEditPoolModal(pool)}
                                                class="flex-1 px-3 py-2 bg-yellow-500 text-white rounded-lg text-sm font-semibold hover:bg-yellow-600 transition-colors"
                                            >
                                                ✏️ Modifier
                                            </button>
                                            <button
                                                on:click={() => confirmDeletePool(pool)}
                                                class="flex-1 px-3 py-2 bg-red-500 text-white rounded-lg text-sm font-semibold hover:bg-red-600 transition-colors"
                                            >
                                                🗑️ Supprimer
                                            </button>
                                        </div>
                                    </div>
                                {/each}
                            </div>
                        {/if}
                    {/if}
                </div>
            </div>
        </div>
    </div>

    <!-- Modal Équipe -->
    {#if showTeamModal}
        <div
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
            on:click={() => (showTeamModal = false)}
            role="button"
            tabindex="0"
            on:keydown={(e) => e.key === 'Escape' && (showTeamModal = false)}
        >
            <div
                class="bg-white rounded-lg shadow-xl max-w-2xl w-full p-6"
                on:click|stopPropagation
                role="dialog"
                tabindex="-1"
            >
                <h2 class="text-2xl font-bold text-gray-900 mb-6">
                    {editMode ? "Modifier l'équipe" : "Ajouter une équipe"}
                </h2>

                <form on:submit|preventDefault={saveTeam} class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Nom de l'entreprise</label>
                        <input
                            type="text"
                            bind:value={teamForm.company}
                            required
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            placeholder="Ex: TechCorp"
                        />
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Poule</label>
                        <select
                            bind:value={teamForm.pool_id}
                            required
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="">Sélectionner une poule</option>
                            {#each pools as pool}
                                <option value={pool.id}>{pool.name}</option>
                            {/each}
                        </select>
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Joueur 1</label>
                        <select
                            bind:value={teamForm.player1_id}
                            required
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="">Sélectionner un joueur</option>
                            {#if editMode && currentTeam}
                                <option value={currentTeam.player1.id}>
                                    {currentTeam.player1.first_name} {currentTeam.player1.last_name}
                                </option>
                            {/if}
                            {#each availablePlayers as player}
                                {#if !teamForm.player2_id || player.id !== Number(teamForm.player2_id)}
                                    <option value={player.id}>
                                        {player.first_name} {player.last_name} - {player.company}
                                    </option>
                                {/if}
                            {/each}
                        </select>
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Joueur 2</label>
                        <select
                            bind:value={teamForm.player2_id}
                            required
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="">Sélectionner un joueur</option>
                            {#if editMode && currentTeam}
                                <option value={currentTeam.player2.id}>
                                    {currentTeam.player2.first_name} {currentTeam.player2.last_name}
                                </option>
                            {/if}
                            {#each availablePlayers as player}
                                {#if !teamForm.player1_id || player.id !== Number(teamForm.player1_id)}
                                    <option value={player.id}>
                                        {player.first_name} {player.last_name} - {player.company}
                                    </option>
                                {/if}
                            {/each}
                        </select>
                    </div>

                    <div class="flex space-x-3 pt-4">
                        <button
                            type="button"
                            on:click={() => (showTeamModal = false)}
                            class="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
                        >
                            Annuler
                        </button>
                        <button
                            type="submit"
                            class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                        >
                            {editMode ? "Enregistrer" : "Ajouter"}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    {/if}

    <!-- Modal Poule -->
    {#if showPoolModal}
        <div
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
            on:click={() => (showPoolModal = false)}
            role="button"
            tabindex="0"
            on:keydown={(e) => e.key === 'Escape' && (showPoolModal = false)}
        >
            <div
                class="bg-white rounded-lg shadow-xl max-w-md w-full p-6"
                on:click|stopPropagation
                role="dialog"
                tabindex="-1"
            >
                <h2 class="text-2xl font-bold text-gray-900 mb-6">
                    {editMode ? "Modifier la poule" : "Ajouter une poule"}
                </h2>

                <form on:submit|preventDefault={savePool} class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Nom de la poule</label>
                        <input
                            type="text"
                            bind:value={poolForm.name}
                            required
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                            placeholder="Ex: Poule A"
                        />
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Description (optionnel)</label>
                        <textarea
                            bind:value={poolForm.description}
                            rows="3"
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                            placeholder="Description de la poule..."
                        ></textarea>
                    </div>

                    <div class="flex space-x-3 pt-4">
                        <button
                            type="button"
                            on:click={() => (showPoolModal = false)}
                            class="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
                        >
                            Annuler
                        </button>
                        <button
                            type="submit"
                            class="flex-1 px-4 py-2 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700 transition-colors"
                        >
                            {editMode ? "Enregistrer" : "Ajouter"}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    {/if}

    <!-- Modal de confirmation suppression équipe -->
    {#if showDeleteTeamModal}
        <div
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
            on:click={() => (showDeleteTeamModal = false)}
            role="button"
            tabindex="0"
            on:keydown={(e) => e.key === 'Escape' && (showDeleteTeamModal = false)}
        >
            <div
                class="bg-white rounded-lg shadow-xl max-w-md w-full p-6"
                on:click|stopPropagation
                role="dialog"
                tabindex="-1"
            >
                <h2 class="text-2xl font-bold text-gray-900 mb-4">Confirmer la suppression</h2>
                {#if teamToDelete}
                    <p class="text-gray-700 mb-6">
                        Êtes-vous sûr de vouloir supprimer l'équipe <strong>{teamToDelete.company}</strong> ?
                        <br /><br />
                        Cette action est irréversible.
                    </p>
                {/if}

                <div class="flex space-x-3">
                    <button
                        on:click={() => (showDeleteTeamModal = false)}
                        class="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
                    >
                        Annuler
                    </button>
                    <button
                        on:click={deleteTeam}
                        class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg font-semibold hover:bg-red-700 transition-colors"
                    >
                        Supprimer
                    </button>
                </div>
            </div>
        </div>
    {/if}

    <!-- Modal de confirmation suppression poule -->
    {#if showDeletePoolModal}
        <div
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
            on:click={() => (showDeletePoolModal = false)}
            role="button"
            tabindex="0"
            on:keydown={(e) => e.key === 'Escape' && (showDeletePoolModal = false)}
        >
            <div
                class="bg-white rounded-lg shadow-xl max-w-md w-full p-6"
                on:click|stopPropagation
                role="dialog"
                tabindex="-1"
            >
                <h2 class="text-2xl font-bold text-gray-900 mb-4">Confirmer la suppression</h2>
                {#if poolToDelete}
                    <p class="text-gray-700 mb-6">
                        Êtes-vous sûr de vouloir supprimer la poule <strong>{poolToDelete.name}</strong> ?
                        <br /><br />
                        Cette action est irréversible.
                    </p>
                {/if}

                <div class="flex space-x-3">
                    <button
                        on:click={() => (showDeletePoolModal = false)}
                        class="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
                    >
                        Annuler
                    </button>
                    <button
                        on:click={deletePool}
                        class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg font-semibold hover:bg-red-700 transition-colors"
                    >
                        Supprimer
                    </button>
                </div>
            </div>
        </div>
    {/if}
{/if}