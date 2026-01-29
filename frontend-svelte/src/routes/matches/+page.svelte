<!-- ============================================
FICHIER : src/routes/matches/+page.svelte
============================================ -->

<script lang="ts">
    import { authStore } from "$lib/store/auth.js";
    import { matchesService, type MatchOutput, Status } from "$lib/services/match";
    import { teamsService, type TeamOutput } from "$lib/services/team";
    import { poolsService, type PoolOutput } from "$lib/services/pool";
    import { onMount } from "svelte";

    // Types
    type Player = {
        player_id: number;
        first_name: string;
        last_name: string;
    };

    type Team = {
        team_id: number;
        company: string;
        players: Player[];
    };

    type Match = {
        match_id: number;
        date: string;
        time: string;
        court_number: number;
        status: string;
        team1: Team;
        team2: Team;
        pool: string;
    };

    type TeamOption = {
        id: number;
        company: string;
    };

    type FormData = {
        date: string;
        time: string;
        court_number: number;
        team1_id: number | string;
        team2_id: number | string;
        status: string;
    };

    // Données des matchs
    let matches: Match[] = [];
    let userTeams: number[] = []; // IDs des équipes de l'utilisateur
    let allCompanies: string[] = [];
    let allPools: string[] = [];
    let loading = true;

    // Filtres
    let showAllMatches: boolean = false; // Pour les joueurs
    let filterCompany: string = ""; // Pour les admins
    let filterPool: string = ""; // Pour les admins
    let filterStatus: string = ""; // Pour les admins

    // Modale pour ajouter/modifier un match
    let showModal: boolean = false;
    let editMode: boolean = false;
    let currentMatch: Match | null = null;

    // Obtenir la date et l'heure actuelles
    const today = new Date().toISOString().split('T')[0];
    const now = new Date();
    const currentTime = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;

    // Formulaire
    let formData: FormData = {
        date: today,
        time: currentTime,
        court_number: 1,
        team1_id: "",
        team2_id: "",
        status: "A_VENIR",
    };

    // Liste des équipes pour les selects
    let teams: TeamOption[] = [];

    // Modale de confirmation de suppression
    let showDeleteModal: boolean = false;
    let matchToDelete: Match | null = null;

    // Charger les données depuis le backend
    onMount(async () => {
        await loadData();
    });

    async function loadData() {
        loading = true;
        try {
            // Récupérer les matchs à venir (30 prochains jours)
            const matchesResponse = await matchesService.getAllMatches({ upcoming: true });
            const backendMatches: MatchOutput[] = matchesResponse.data.matches;

            // Récupérer toutes les équipes
            const teamsResponse = await teamsService.getAllTeams();
            const backendTeams: TeamOutput[] = teamsResponse.data.teams;

            // Récupérer toutes les poules
            const poolsResponse = await poolsService.getAllPools();
            const backendPools: PoolOutput[] = poolsResponse.data.pools;

            // Construire la liste des équipes pour les selects
            teams = backendTeams.map(t => ({
                id: t.id,
                company: t.company
            }));

            // Transformer les matchs du backend au format de l'UI
            matches = backendMatches.map(match => ({
                match_id: match.id,
                date: match.event.event_date,
                time: match.event.event_time,
                court_number: match.court_number,
                status: match.status,
                team1: {
                    team_id: match.team1.id,
                    company: match.team1.company,
                    players: [
                        {
                            player_id: match.team1.player1.id,
                            first_name: match.team1.player1.first_name,
                            last_name: match.team1.player1.last_name
                        },
                        {
                            player_id: match.team1.player2.id,
                            first_name: match.team1.player2.first_name,
                            last_name: match.team1.player2.last_name
                        }
                    ]
                },
                team2: {
                    team_id: match.team2.id,
                    company: match.team2.company,
                    players: [
                        {
                            player_id: match.team2.player1.id,
                            first_name: match.team2.player1.first_name,
                            last_name: match.team2.player1.last_name
                        },
                        {
                            player_id: match.team2.player2.id,
                            first_name: match.team2.player2.first_name,
                            last_name: match.team2.player2.last_name
                        }
                    ]
                },
                pool: match.team1.pool.name // Les deux équipes ont la même poule
            }));

            // Extraire les entreprises et poules uniques
            allCompanies = [
                ...new Set(
                    matches.flatMap((m) => [
                        m.team1.company,
                        m.team2.company,
                    ]),
                ),
            ].sort();
            allPools = backendPools.map(p => p.name).sort();

            // TODO: Récupérer les équipes de l'utilisateur connecté
            userTeams = [];

        } catch (error) {
            console.error("Erreur lors du chargement des données:", error);
            alert("Erreur lors du chargement des données");
        } finally {
            loading = false;
        }
    }

    // Créer la liste des équipes (fonction plus utilisée avec nouveau code)
    const teamMap = new Map<number, TeamOption>();
    $: {
        teamMap.clear();
        matches.forEach((m) => {
        if (!teamMap.has(m.team1.team_id)) {
            teamMap.set(m.team1.team_id, {
                id: m.team1.team_id,
                company: m.team1.company,
            });
        }
        if (!teamMap.has(m.team2.team_id)) {
            teamMap.set(m.team2.team_id, {
                id: m.team2.team_id,
                company: m.team2.company,
            });
        }
    });
    }

    // Filtrer les matchs selon le rôle et les filtres actifs
    $: filteredMatches = matches.filter((match: Match) => {
        // Filtre joueur : ses équipes uniquement (sauf si "voir tous" activé)
        if (!$authStore.isAdmin && !showAllMatches) {
            const isUserMatch =
                userTeams.includes(match.team1.team_id) ||
                userTeams.includes(match.team2.team_id);
            if (!isUserMatch) return false;
        }

        // Filtres admin
        if ($authStore.isAdmin) {
            if (
                filterCompany &&
                match.team1.company !== filterCompany &&
                match.team2.company !== filterCompany
            ) {
                return false;
            }
            if (filterPool && match.pool !== filterPool) {
                return false;
            }
            if (filterStatus && match.status !== filterStatus) {
                return false;
            }
        }

        return true;
    });

    // Formater la date et l'heure en français
    function formatDateTime(date: string, time: string): string {
        const days: string[] = [
            "Dimanche",
            "Lundi",
            "Mardi",
            "Mercredi",
            "Jeudi",
            "Vendredi",
            "Samedi",
        ];
        const months: string[] = [
            "janvier",
            "février",
            "mars",
            "avril",
            "mai",
            "juin",
            "juillet",
            "août",
            "septembre",
            "octobre",
            "novembre",
            "décembre",
        ];

        const d = new Date(date);
        const dayName = days[d.getDay()];
        const day = d.getDate();
        const month = months[d.getMonth()];
        const year = d.getFullYear();

        return `${dayName} ${day} ${month} ${year} à ${time}`;
    }

    // Badge de statut
    function getStatusBadge(status: string): string {
        if (status === "A_VENIR") {
            return "bg-blue-100 text-blue-800";
        } else if (status === "ANNULE") {
            return "bg-red-100 text-red-800";
        }
        return "bg-gray-100 text-gray-800";
    }

    function getStatusLabel(status: string): string {
        if (status === "A_VENIR") return "À venir";
        if (status === "ANNULE") return "Annulé";
        return status;
    }

    // Ouvrir la modale pour ajouter un match
    function openAddModal(): void {
        editMode = false;
        currentMatch = null;
        const today = new Date().toISOString().split('T')[0];
        const now = new Date();
        const currentTime = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
        formData = {
            date: today,
            time: currentTime,
            court_number: 1,
            team1_id: "",
            team2_id: "",
            status: "A_VENIR",
        };
        showModal = true;
    }

    // Ouvrir la modale pour modifier un match
    function openEditModal(match: Match): void {
        editMode = true;
        currentMatch = match;
        formData = {
            date: match.date,
            time: match.time,
            court_number: match.court_number,
            team1_id: match.team1.team_id,
            team2_id: match.team2.team_id,
            status: match.status,
        };
        showModal = true;
    }

    // Valider qu'aucun autre match n'utilise la même piste au même créneau
    function validateCourtAvailability(): boolean {
        const dateTime = `${formData.date} ${formData.time}`;

        for (let match of matches) {
            // Ignorer le match en cours d'édition
            if (editMode && currentMatch && match.match_id === currentMatch.match_id) {
                continue;
            }

            const matchDateTime = `${match.date} ${match.time}`;
            if (
                matchDateTime === dateTime &&
                match.court_number === formData.court_number
            ) {
                return false;
            }
        }
        return true;
    }

    // Sauvegarder un match
    async function saveMatch() {
        // Validation de la date (>= aujourd'hui)
        const today = new Date().toISOString().split("T")[0];
        if (formData.date < today) {
            alert("La date doit être aujourd'hui ou dans le futur.");
            return;
        }

        // Validation des équipes différentes
        if (formData.team1_id === formData.team2_id) {
            alert("Les deux équipes doivent être différentes.");
            return;
        }

        // Validation de la disponibilité de la piste
        if (!validateCourtAvailability()) {
            alert(
                "Un autre match est déjà programmé sur cette piste à cette date et heure.",
            );
            return;
        }

        try {
            const matchInput = {
                court_number: formData.court_number,
                status: formData.status,
                team1_id: Number(formData.team1_id),
                team2_id: Number(formData.team2_id)
            };

            if (editMode && currentMatch) {
                // Modifier le match existant
                await matchesService.updateMatch(currentMatch.match_id, matchInput);
            } else {
                // Ajouter un nouveau match
                await matchesService.createMatch(matchInput);
            }

            // Recharger les données
            await loadData();
            showModal = false;
        } catch (error) {
            console.error("Erreur lors de la sauvegarde:", error);
            alert("Erreur lors de la sauvegarde du match");
        }
    }

    // Supprimer un match
    function confirmDelete(match: Match): void {
        if (match.status !== "A_VENIR") {
            alert("Seuls les matchs à venir peuvent être supprimés.");
            return;
        }
        matchToDelete = match;
        showDeleteModal = true;
    }

    function deleteMatch(): void {
        if (matchToDelete) {
            matchesService.deleteMatch(matchToDelete.match_id)
                .then(() => loadData())
                .catch((error) => {
                    console.error("Erreur lors de la suppression:", error);
                    alert("Erreur lors de la suppression du match");
                });
            showDeleteModal = false;
            matchToDelete = null;
        }
    }
</script>

<div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- En-tête -->
        <div class="mb-8">
            <h1 class="text-4xl font-bold text-gray-900 mb-2">
                Matchs à venir
            </h1>
            <p class="text-gray-600">
                Prochains matchs dans les 30 jours
            </p>
        </div>

        <!-- Filtres et actions -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <div class="flex flex-wrap items-center gap-4">
                {#if !$authStore.isAdmin}
                    <!-- Filtre joueur -->
                    <label class="flex items-center space-x-2 cursor-pointer">
                        <input
                            type="checkbox"
                            bind:checked={showAllMatches}
                            class="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                        />
                        <span class="text-gray-700"
                            >Voir tous les matchs</span
                        >
                    </label>
                {:else}
                    <!-- Filtres admin -->
                    <div class="flex-1 min-w-[200px]">
                        <label class="block text-sm font-medium text-gray-700 mb-1"
                            >Entreprise</label
                        >
                        <select
                            bind:value={filterCompany}
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="">Toutes</option>
                            {#each allCompanies as company}
                                <option value={company}>{company}</option>
                            {/each}
                        </select>
                    </div>

                    <div class="flex-1 min-w-[200px]">
                        <label class="block text-sm font-medium text-gray-700 mb-1"
                            >Poule</label
                        >
                        <select
                            bind:value={filterPool}
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="">Toutes</option>
                            {#each allPools as pool}
                                <option value={pool}>{pool}</option>
                            {/each}
                        </select>
                    </div>

                    <div class="flex-1 min-w-[200px]">
                        <label class="block text-sm font-medium text-gray-700 mb-1"
                            >Statut</label
                        >
                        <select
                            bind:value={filterStatus}
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="">Tous</option>
                            <option value="A_VENIR">À venir</option>
                            <option value="ANNULE">Annulé</option>
                        </select>
                    </div>

                    <div class="flex-1 min-w-[200px] flex items-end">
                        <button
                            on:click={openAddModal}
                            class="w-full px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                        >
                            ➕ Ajouter un match
                        </button>
                    </div>
                {/if}
            </div>
        </div>

        <!-- Liste des matchs -->
        {#if filteredMatches.length === 0}
            <div class="bg-white rounded-lg shadow-md p-12 text-center">
                <div class="text-6xl mb-4">🎾</div>
                <h3 class="text-xl font-semibold text-gray-700 mb-2">
                    Aucun match à afficher
                </h3>
                <p class="text-gray-500">
                    {#if !$authStore.isAdmin && !showAllMatches}
                        Vous n'avez pas de match prévu dans les 30 prochains
                        jours.
                    {:else}
                        Aucun match ne correspond aux filtres sélectionnés.
                    {/if}
                </p>
            </div>
        {:else}
            <div class="space-y-4">
                {#each filteredMatches as match}
                    <div
                        class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
                    >
                        <div class="flex items-start justify-between">
                            <div class="flex-1">
                                <!-- Date et heure -->
                                <div
                                    class="flex items-center text-gray-700 mb-3"
                                >
                                    <span class="text-2xl mr-2">📅</span>
                                    <span class="font-semibold text-lg">
                                        {formatDateTime(
                                            match.date,
                                            match.time,
                                        )}
                                    </span>
                                </div>

                                <!-- Piste -->
                                <div class="flex items-center text-gray-600 mb-4">
                                    <span class="text-xl mr-2">🏟️</span>
                                    <span>Piste {match.court_number}</span>
                                </div>

                                <!-- Équipes -->
                                <div class="flex items-center justify-between mb-4">
                                    <div class="flex-1">
                                        <div
                                            class="font-semibold text-blue-600 text-lg mb-2"
                                        >
                                            {match.team1.company}
                                        </div>
                                        <div class="text-sm text-gray-600">
                                            {#each match.team1.players as player}
                                                <div>
                                                    {player.first_name}
                                                    {player.last_name}
                                                </div>
                                            {/each}
                                        </div>
                                    </div>

                                    <div class="px-4 text-2xl font-bold text-gray-400">
                                        VS
                                    </div>

                                    <div class="flex-1 text-right">
                                        <div
                                            class="font-semibold text-blue-600 text-lg mb-2"
                                        >
                                            {match.team2.company}
                                        </div>
                                        <div class="text-sm text-gray-600">
                                            {#each match.team2.players as player}
                                                <div>
                                                    {player.first_name}
                                                    {player.last_name}
                                                </div>
                                            {/each}
                                        </div>
                                    </div>
                                </div>

                                <!-- Statut -->
                                <div>
                                    <span
                                        class="inline-block px-3 py-1 rounded-full text-sm font-semibold {getStatusBadge(
                                            match.status,
                                        )}"
                                    >
                                        {getStatusLabel(match.status)}
                                    </span>
                                    <span class="ml-3 text-sm text-gray-500">
                                        {match.pool}
                                    </span>
                                </div>
                            </div>

                            <!-- Actions admin -->
                            {#if $authStore.isAdmin}
                                <div class="ml-4 flex flex-col space-y-2">
                                    <button
                                        on:click={() => openEditModal(match)}
                                        class="px-4 py-2 bg-yellow-500 text-white rounded-lg text-sm font-semibold hover:bg-yellow-600 transition-colors"
                                    >
                                        ✏️ Modifier
                                    </button>
                                    <button
                                        on:click={() => confirmDelete(match)}
                                        class="px-4 py-2 bg-red-500 text-white rounded-lg text-sm font-semibold hover:bg-red-600 transition-colors"
                                    >
                                        🗑️ Supprimer
                                    </button>
                                </div>
                            {/if}
                        </div>
                    </div>
                {/each}
            </div>
        {/if}
    </div>
</div>

<!-- Modale Ajouter/Modifier -->
{#if showModal}
    <div
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
        on:click={() => (showModal = false)}
        role="button"
        tabindex="0"
        on:keydown={(e) => e.key === 'Escape' && (showModal = false)}
    >
        <div
            class="bg-white rounded-lg shadow-xl max-w-md w-full p-6"
            on:click|stopPropagation
            role="dialog"
            tabindex="-1"
        >
            <h2 class="text-2xl font-bold text-gray-900 mb-6">
                {editMode ? "Modifier le match" : "Ajouter un match"}
            </h2>

            <form on:submit|preventDefault={saveMatch} class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1"
                        >Date</label
                    >
                    <input
                        type="date"
                        bind:value={formData.date}
                        required
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1"
                        >Heure</label
                    >
                    <input
                        type="time"
                        bind:value={formData.time}
                        required
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1"
                        >Piste (1-10)</label
                    >
                    <input
                        type="number"
                        bind:value={formData.court_number}
                        min="1"
                        max="10"
                        required
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1"
                        >Équipe 1</label
                    >
                    <select
                        bind:value={formData.team1_id}
                        required
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                        <option value="">Sélectionner</option>
                        {#each teams as team}
                            <option value={team.id}>{team.company}</option>
                        {/each}
                    </select>
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1"
                        >Équipe 2</label
                    >
                    <select
                        bind:value={formData.team2_id}
                        required
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                        <option value="">Sélectionner</option>
                        {#each teams as team}
                            <option value={team.id}>{team.company}</option>
                        {/each}
                    </select>
                </div>

                {#if editMode}
                    <div>
                        <label
                            class="block text-sm font-medium text-gray-700 mb-1"
                            >Statut</label
                        >
                        <select
                            bind:value={formData.status}
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="A_VENIR">À venir</option>
                            <option value="ANNULE">Annulé</option>
                        </select>
                    </div>
                {/if}

                <div class="flex space-x-3 pt-4">
                    <button
                        type="button"
                        on:click={() => (showModal = false)}
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

<!-- Modale de confirmation de suppression -->
{#if showDeleteModal}
    <div
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
        on:click={() => (showDeleteModal = false)}
        role="button"
        tabindex="0"
        on:keydown={(e) => e.key === 'Escape' && (showDeleteModal = false)}
    >
        <div
            class="bg-white rounded-lg shadow-xl max-w-md w-full p-6"
            on:click|stopPropagation
            role="dialog"
            tabindex="-1"
        >
            <h2 class="text-2xl font-bold text-gray-900 mb-4">
                Confirmer la suppression
            </h2>
            <p class="text-gray-700 mb-6">
                Êtes-vous sûr de vouloir supprimer ce match ?
            </p>

            <div class="flex space-x-3">
                <button
                    on:click={() => (showDeleteModal = false)}
                    class="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
                >
                    Annuler
                </button>
                <button
                    on:click={deleteMatch}
                    class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg font-semibold hover:bg-red-700 transition-colors"
                >
                    Supprimer
                </button>
            </div>
        </div>
    </div>
{/if}