<!-- ============================================
FICHIER : src/routes/planning/+page.svelte
============================================ -->

<script lang="ts">
    import { authStore } from "$lib/store/auth.js";
    import { eventsService, type EventOutput, type EventInput } from "$lib/services/event";
    import { teamsService, type TeamOutput } from "$lib/services/team";
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
        court_number: number;
        team1: Team;
        team2: Team;
        status: string;
        score_team1: string | null;
        score_team2: string | null;
    };

    type Event = {
        event_id: number;
        date: string;
        time: string;
        matches: Match[];
    };

    type TeamOption = {
        id: number;
        company: string;
    };

    type MatchForm = {
        court_number: number;
        team1_id: number | string;
        team2_id: number | string;
    };

    type EventForm = {
        date: string;
        time: string;
        match_count: number;
        matches: MatchForm[];
    };

    // Données
    let events: Event[] = [];
    let filteredEvents: Event[] = [];
    let userTeams: number[] = [];
    let teams: TeamOption[] = [];
    let loading = true;

    // État du calendrier
    let currentDate = new Date();
    let currentYear = currentDate.getFullYear();
    let currentMonth = currentDate.getMonth();
    let selectedDate: string | null = null;

    // Filtres
    let showOnlyUserEvents = true; // Activé par défaut

    // Modales
    let showEventModal = false;
    let showAddEditModal = false;
    let showDeleteModal = false;
    let editMode = false;
    let currentEvent: Event | null = null;
    let eventToDelete: Event | null = null;

    // Obtenir la date et l'heure actuelles en fuseau horaire français
    function getLocalDate(): string {
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    function getLocalTime(): string {
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        return `${hours}:${minutes}`;
    }

    const today = getLocalDate();
    const currentTime = getLocalTime();

    // Formulaire
    let eventForm: EventForm = {
        date: today,
        time: currentTime,
        match_count: 1,
        matches: [{ court_number: 1, team1_id: "", team2_id: "" }],
    };

    // Charger les données depuis le backend
    onMount(async () => {
        await loadData();
    });

    async function loadData() {
        loading = true;
        try {
            // Récupérer les événements
            const eventsResponse = await eventsService.getAllEvents();
            const backendEvents: EventOutput[] = eventsResponse.data.events;

            // Récupérer toutes les équipes
            const teamsResponse = await teamsService.getAllTeams();
            const backendTeams: TeamOutput[] = teamsResponse.data.teams;

            // Construire la liste des équipes pour les selects
            teams = backendTeams.map(t => ({
                id: t.id,
                company: t.company
            }));

            // Transformer les événements du backend au format de l'UI
            events = backendEvents.map(event => ({
                event_id: event.id,
                date: event.event_date,
                time: event.event_time,
                matches: event.matches.map(match => {
                    const team1 = backendTeams.find(t => t.id === match.team1_id);
                    const team2 = backendTeams.find(t => t.id === match.team2_id);
                    
                    return {
                        match_id: match.id,
                        court_number: match.court_number,
                        team1: {
                            team_id: match.team1_id,
                            company: team1?.company || "Unknown",
                            players: team1 ? [
                                {
                                    player_id: team1.player1.id,
                                    first_name: team1.player1.first_name,
                                    last_name: team1.player1.last_name
                                },
                                {
                                    player_id: team1.player2.id,
                                    first_name: team1.player2.first_name,
                                    last_name: team1.player2.last_name
                                }
                            ] : []
                        },
                        team2: {
                            team_id: match.team2_id,
                            company: team2?.company || "Unknown",
                            players: team2 ? [
                                {
                                    player_id: team2.player1.id,
                                    first_name: team2.player1.first_name,
                                    last_name: team2.player2.last_name
                                },
                                {
                                    player_id: team2.player2.id,
                                    first_name: team2.player2.first_name,
                                    last_name: team2.player2.last_name
                                }
                            ] : []
                        },
                        status: match.status,
                        score_team1: null,
                        score_team2: null
                    };
                })
            }));

            // TODO: Récupérer les équipes de l'utilisateur connecté
            // Pour l'instant, on laisse vide
            userTeams = [];

        } catch (error) {
            console.error("Erreur lors du chargement des données:", error);
            alert("Erreur lors du chargement des données");
        } finally {
            loading = false;
        }
    }

    // Filtrer les événements
    $: {
        console.log("=== DEBUG FILTRAGE ===");
        console.log("showOnlyUserEvents:", showOnlyUserEvents);
        console.log("userTeams:", userTeams);
        console.log("Total events:", events.length);
        
        filteredEvents = events.filter((event: Event) => {
            if (!showOnlyUserEvents) {
                console.log("Filtre désactivé, on affiche tout");
                return true;
            }

            // Vérifier si l'utilisateur participe à au moins un match de l'événement
            const isUserEvent = event.matches.some(
                (match) =>
                    userTeams.includes(match.team1.team_id) ||
                    userTeams.includes(match.team2.team_id),
            );
            console.log(`Event ${event.event_id}: isUserEvent = ${isUserEvent}`);
            return isUserEvent;
        });
        
        console.log("Filtered events:", filteredEvents.length);
        console.log("===================");
    }

    // Obtenir les événements d'une date spécifique
    function getEventsForDate(dateStr: string): Event[] {
        return filteredEvents.filter((event) => event.date === dateStr);
    }

    // Générer le calendrier du mois
    function generateCalendar(year: number, month: number): Date[] {
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const daysInMonth = lastDay.getDate();

        const startDay = firstDay.getDay(); // 0 = dimanche
        const days: Date[] = [];

        // Ajouter les jours vides du début
        for (let i = 0; i < startDay; i++) {
            days.push(new Date(0)); // Date invalide pour les cases vides
        }

        // Ajouter les jours du mois
        for (let i = 1; i <= daysInMonth; i++) {
            days.push(new Date(year, month, i));
        }

        return days;
    }

    $: calendarDays = generateCalendar(currentYear, currentMonth);
    
    // Forcer la réactivité du calendrier quand les événements filtrés changent
    $: calendarKey = `${currentYear}-${currentMonth}-${filteredEvents.length}-${showOnlyUserEvents}`;


    // Navigation du calendrier
    function previousMonth(): void {
        if (currentMonth === 0) {
            currentMonth = 11;
            currentYear--;
        } else {
            currentMonth--;
        }
    }

    function nextMonth(): void {
        if (currentMonth === 11) {
            currentMonth = 0;
            currentYear++;
        } else {
            currentMonth++;
        }
    }

    // Noms des mois
    const monthNames = [
        "Janvier",
        "Février",
        "Mars",
        "Avril",
        "Mai",
        "Juin",
        "Juillet",
        "Août",
        "Septembre",
        "Octobre",
        "Novembre",
        "Décembre",
    ];

    // Formater une date
    function formatDate(date: Date): string {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, "0");
        const day = String(date.getDate()).padStart(2, "0");
        return `${year}-${month}-${day}`;
    }

    function formatDateLong(dateStr: string): string {
        const date = new Date(dateStr);
        const days = [
            "Dimanche",
            "Lundi",
            "Mardi",
            "Mercredi",
            "Jeudi",
            "Vendredi",
            "Samedi",
        ];
        const dayName = days[date.getDay()];
        const day = date.getDate();
        const month = monthNames[date.getMonth()];
        const year = date.getFullYear();
        return `${dayName} ${day} ${month} ${year}`;
    }

    // Cliquer sur un jour
    function handleDayClick(date: Date): void {
        if (date.getTime() === 0) return; // Case vide
        const dateStr = formatDate(date);
        const dayEvents = getEventsForDate(dateStr);

        if (dayEvents.length > 0) {
            selectedDate = dateStr;
            showEventModal = true;
        }
    }

    // Vérifier si un jour a des événements
    function hasEvents(date: Date): boolean {
        if (date.getTime() === 0) return false;
        const dateStr = formatDate(date);
        return getEventsForDate(dateStr).length > 0;
    }

    // Ouvrir la modale d'ajout
    function openAddModal(): void {
        editMode = false;
        currentEvent = null;
        const today = getLocalDate();
        const currentTime = getLocalTime();
        eventForm = {
            date: today,
            time: currentTime,
            match_count: 1,
            matches: [{ court_number: 1, team1_id: "", team2_id: "" }],
        };
        showAddEditModal = true;
    }

    // Ouvrir la modale de modification
    function openEditModal(event: Event): void {
        editMode = true;
        currentEvent = event;
        eventForm = {
            date: event.date,
            time: event.time,
            match_count: event.matches.length,
            matches: event.matches.map((m) => ({
                court_number: m.court_number,
                team1_id: m.team1.team_id,
                team2_id: m.team2.team_id,
            })),
        };
        showEventModal = false;
        showAddEditModal = true;
    }

    // Mettre à jour le nombre de matchs
    function updateMatchCount(): void {
        const count = eventForm.match_count;
        const currentLength = eventForm.matches.length;

        if (count > currentLength) {
            // Ajouter des matchs
            for (let i = currentLength; i < count; i++) {
                eventForm.matches.push({
                    court_number: i + 1,
                    team1_id: "",
                    team2_id: "",
                });
            }
        } else if (count < currentLength) {
            // Supprimer des matchs
            eventForm.matches = eventForm.matches.slice(0, count);
        }
    }

    $: if (eventForm.match_count) {
        updateMatchCount();
    }

    // Valider le formulaire
    function validateEventForm(): string | null {
        // Date >= aujourd'hui
        const today = getLocalDate();
        if (eventForm.date < today) {
            return "La date doit être aujourd'hui ou dans le futur.";
        }

        // Format de l'heure
        const timeRegex = /^([0-1][0-9]|2[0-3]):[0-5][0-9]$/;
        if (!timeRegex.test(eventForm.time)) {
            return "L'heure doit être au format HH:MM (00:00 à 23:59).";
        }

        // Pistes uniques
        const courts = eventForm.matches.map((m) => m.court_number);
        const uniqueCourts = new Set(courts);
        if (courts.length !== uniqueCourts.size) {
            return "Deux matchs ne peuvent pas utiliser la même piste.";
        }

        // Équipes uniques
        const teamIds: (number | string)[] = [];
        for (const match of eventForm.matches) {
            if (!match.team1_id || !match.team2_id) {
                return "Veuillez sélectionner toutes les équipes.";
            }
            if (match.team1_id === match.team2_id) {
                return "Les deux équipes d'un match doivent être différentes.";
            }
            teamIds.push(match.team1_id, match.team2_id);
        }
        const uniqueTeams = new Set(teamIds);
        if (teamIds.length !== uniqueTeams.size) {
            return "Une équipe ne peut jouer qu'un seul match par événement.";
        }

        return null;
    }

    // Sauvegarder l'événement
    async function saveEvent() {
        const error = validateEventForm();
        if (error) {
            alert(error);
            return;
        }

        try {
            const eventInput: EventInput = {
                event_date: eventForm.date,
                event_time: eventForm.time,
                matches: eventForm.matches.map(m => ({
                    court_number: m.court_number,
                    status: "A_VENIR",
                    team1_id: Number(m.team1_id),
                    team2_id: Number(m.team2_id)
                }))
            };

            if (editMode && currentEvent) {
                // Modifier l'événement existant
                await eventsService.updateEvent(currentEvent.event_id, eventInput);
            } else {
                // Ajouter un nouvel événement
                await eventsService.createEvent(eventInput);
            }

            // Fermer la modale et recharger les données
            showAddEditModal = false;
            await loadData();
        } catch (error) {
            console.error("Erreur lors de la sauvegarde:", error);
            alert("Erreur lors de la sauvegarde de l'événement");
        }
    }

    // Confirmer la suppression
    function confirmDelete(event: Event): void {
        // Vérifier que tous les matchs sont à venir
        const allUpcoming = event.matches.every((m) => m.status === "A_VENIR");
        if (!allUpcoming) {
            alert(
                "Seuls les événements dont tous les matchs sont à venir peuvent être supprimés.",
            );
            return;
        }

        eventToDelete = event;
        showEventModal = false;
        showDeleteModal = true;
    }

    // Supprimer l'événement
    async function deleteEvent() {
        if (eventToDelete) {
            try {
                await eventsService.deleteEvent(eventToDelete.event_id);
                showDeleteModal = false;
                eventToDelete = null;
                await loadData();
            } catch (error) {
                console.error("Erreur lors de la suppression:", error);
                alert("Erreur lors de la suppression de l'événement");
            }
        }
    }

    // Badge de statut
    function getStatusBadge(status: string): string {
        if (status === "A_VENIR") return "bg-blue-100 text-blue-800";
        if (status === "TERMINE") return "bg-green-100 text-green-800";
        if (status === "ANNULE") return "bg-red-100 text-red-800";
        return "bg-gray-100 text-gray-800";
    }

    function getStatusLabel(status: string): string {
        if (status === "A_VENIR") return "À venir";
        if (status === "TERMINE") return "Terminé";
        if (status === "ANNULE") return "Annulé";
        return status;
    }
</script>

<div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- En-tête -->
        <div class="mb-8">
            <h1 class="text-4xl font-bold text-gray-900 mb-2">Planning</h1>
            <p class="text-gray-600">
                Calendrier de la saison - Cliquez sur un jour pour voir les
                événements
            </p>
        </div>

        <!-- Filtres et actions -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <div class="flex flex-wrap items-center justify-between gap-4">
                <label class="flex items-center space-x-2 cursor-pointer">
                    <input
                        type="checkbox"
                        bind:checked={showOnlyUserEvents}
                        class="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                    />
                    <span class="text-gray-700"
                        >Voir uniquement mes événements</span
                    >
                </label>

                {#if $authStore.isAdmin}
                    <button
                        on:click={openAddModal}
                        class="px-6 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                    >
                        ➕ Ajouter un événement
                    </button>
                {/if}
            </div>
        </div>

        <!-- Calendrier -->
        <div class="bg-white rounded-lg shadow-md p-6">
            <!-- Navigation du calendrier -->
            <div class="flex items-center justify-between mb-6">
                <button
                    on:click={previousMonth}
                    class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
                >
                    ← Précédent
                </button>

                <h2 class="text-2xl font-bold text-gray-900">
                    {monthNames[currentMonth]}
                    {currentYear}
                </h2>

                <button
                    on:click={nextMonth}
                    class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
                >
                    Suivant →
                </button>
            </div>

            <!-- Jours de la semaine -->
            <div class="grid grid-cols-7 gap-2 mb-2">
                {#each ["Dim", "Lun", "Mar", "Mer", "Jeu", "Ven", "Sam"] as day}
                    <div
                        class="text-center font-semibold text-gray-600 py-2"
                    >
                        {day}
                    </div>
                {/each}
            </div>

            <!-- Grille du calendrier -->
            {#key calendarKey}
                <div class="grid grid-cols-7 gap-2">
                    {#each calendarDays as day}
                        {#if day.getTime() === 0}
                            <!-- Case vide -->
                            <div class="aspect-square"></div>
                        {:else}
                            {@const dayHasEvents = hasEvents(day)}
                            {@const isToday = day.getDate() === new Date().getDate() &&
                                day.getMonth() === new Date().getMonth() &&
                                day.getFullYear() === new Date().getFullYear()}
                            
                            <button
                                on:click={() => handleDayClick(day)}
                                class="aspect-square border rounded-lg p-2 transition-all duration-200 
                                    {dayHasEvents
                                        ? 'bg-blue-50 border-blue-400 hover:bg-blue-100 hover:border-blue-500 cursor-pointer shadow-sm'
                                        : 'border-gray-200 hover:bg-gray-50 cursor-default'}
                                    {isToday ? 'ring-2 ring-blue-600 ring-offset-1' : ''}"
                            >
                                <div class="text-sm {dayHasEvents ? 'font-bold text-blue-700' : 'text-gray-700'}">
                                    {day.getDate()}
                                </div>
                                {#if dayHasEvents}
                                    <div class="mt-1 flex items-center justify-center">
                                        <div class="w-2 h-2 bg-blue-600 rounded-full"></div>
                                    </div>
                                    <div class="text-xs text-blue-600 mt-1 font-medium">
                                        {getEventsForDate(formatDate(day)).length}
                                        event{getEventsForDate(formatDate(day)).length > 1 ? "s" : ""}
                                    </div>
                                {/if}
                            </button>
                        {/if}
                    {/each}
                </div>
            {/key}
        </div>
    </div>
</div>

<!-- Modale des événements du jour -->
{#if showEventModal && selectedDate}
    <div
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
        on:click={() => (showEventModal = false)}
        role="button"
        tabindex="0"
        on:keydown={(e) => e.key === "Escape" && (showEventModal = false)}
    >
        <div
            class="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[80vh] overflow-y-auto p-6"
            on:click|stopPropagation
            role="dialog"
            tabindex="-1"
        >
            <h2 class="text-2xl font-bold text-gray-900 mb-6">
                Événements du {formatDateLong(selectedDate)}
            </h2>

            <div class="space-y-6">
                {#each getEventsForDate(selectedDate) as event}
                    <div class="border border-gray-200 rounded-lg p-6">
                        <div class="flex items-start justify-between mb-4">
                            <div>
                                <h3 class="text-xl font-semibold mb-2">
                                    Créneau : {event.time}
                                </h3>
                                <p class="text-gray-600">
                                    {event.matches.length} match{event.matches
                                        .length > 1
                                        ? "s"
                                        : ""}
                                </p>
                            </div>

                            {#if $authStore.isAdmin}
                                <div class="flex gap-2">
                                    <button
                                        on:click={() => openEditModal(event)}
                                        class="px-4 py-2 bg-yellow-500 text-white rounded-lg text-sm font-semibold hover:bg-yellow-600 transition-colors"
                                    >
                                        ✏️ Modifier
                                    </button>
                                    <button
                                        on:click={() => confirmDelete(event)}
                                        class="px-4 py-2 bg-red-500 text-white rounded-lg text-sm font-semibold hover:bg-red-600 transition-colors"
                                    >
                                        🗑️ Supprimer
                                    </button>
                                </div>
                            {/if}
                        </div>

                        <!-- Matchs -->
                        <div class="space-y-4">
                            {#each event.matches as match}
                                <div
                                    class="bg-gray-50 rounded-lg p-4 border border-gray-200"
                                >
                                    <div class="flex items-center justify-between mb-3">
                                        <span
                                            class="text-sm font-semibold text-gray-600"
                                            >Piste {match.court_number}</span
                                        >
                                        <span
                                            class="inline-block px-3 py-1 rounded-full text-xs font-semibold {getStatusBadge(
                                                match.status,
                                            )}"
                                        >
                                            {getStatusLabel(match.status)}
                                        </span>
                                    </div>

                                    <div class="flex items-center justify-between">
                                        <div class="flex-1">
                                            <div
                                                class="font-semibold text-blue-600 mb-1"
                                            >
                                                {match.team1.company}
                                            </div>
                                            {#if match.score_team1}
                                                <div
                                                    class="text-sm text-gray-700 font-mono"
                                                >
                                                    {match.score_team1}
                                                </div>
                                            {/if}
                                        </div>

                                        <div
                                            class="px-4 text-xl font-bold text-gray-400"
                                        >
                                            VS
                                        </div>

                                        <div class="flex-1 text-right">
                                            <div
                                                class="font-semibold text-blue-600 mb-1"
                                            >
                                                {match.team2.company}
                                            </div>
                                            {#if match.score_team2}
                                                <div
                                                    class="text-sm text-gray-700 font-mono"
                                                >
                                                    {match.score_team2}
                                                </div>
                                            {/if}
                                        </div>
                                    </div>
                                </div>
                            {/each}
                        </div>
                    </div>
                {/each}
            </div>

            <div class="mt-6">
                <button
                    on:click={() => (showEventModal = false)}
                    class="w-full px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
                >
                    Fermer
                </button>
            </div>
        </div>
    </div>
{/if}

<!-- Modale Ajouter/Modifier événement -->
{#if showAddEditModal}
    <div
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
        on:click={() => (showAddEditModal = false)}
        role="button"
        tabindex="0"
        on:keydown={(e) => e.key === "Escape" && (showAddEditModal = false)}
    >
        <div
            class="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[80vh] overflow-y-auto p-6"
            on:click|stopPropagation
            role="dialog"
            tabindex="-1"
        >
            <h2 class="text-2xl font-bold text-gray-900 mb-6">
                {editMode ? "Modifier l'événement" : "Ajouter un événement"}
            </h2>

            <form on:submit|preventDefault={saveEvent} class="space-y-6">
                <!-- Date et heure -->
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label
                            class="block text-sm font-medium text-gray-700 mb-1"
                            >Date</label
                        >
                        <input
                            type="date"
                            bind:value={eventForm.date}
                            required
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                    </div>

                    <div>
                        <label
                            class="block text-sm font-medium text-gray-700 mb-1"
                            >Heure</label
                        >
                        <input
                            type="time"
                            bind:value={eventForm.time}
                            required
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                    </div>
                </div>

                <!-- Nombre de matchs -->
                <div>
                    <label
                        class="block text-sm font-medium text-gray-700 mb-1"
                        >Nombre de matchs</label
                    >
                    <select
                        bind:value={eventForm.match_count}
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                        <option value={1}>1 match</option>
                        <option value={2}>2 matchs</option>
                        <option value={3}>3 matchs</option>
                    </select>
                </div>

                <!-- Matchs -->
                <div class="space-y-4">
                    {#each eventForm.matches as match, idx}
                        <div class="border border-gray-200 rounded-lg p-4">
                            <h3 class="font-semibold text-gray-900 mb-3">
                                Match {idx + 1}
                            </h3>

                            <div class="grid grid-cols-3 gap-4">
                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700 mb-1"
                                        >Piste</label
                                    >
                                    <input
                                        type="number"
                                        bind:value={match.court_number}
                                        min="1"
                                        max="10"
                                        required
                                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    />
                                </div>

                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700 mb-1"
                                        >Équipe 1</label
                                    >
                                    <select
                                        bind:value={match.team1_id}
                                        required
                                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    >
                                        <option value="">Sélectionner</option>
                                        {#each teams as team}
                                            <option value={team.id}
                                                >{team.company}</option
                                            >
                                        {/each}
                                    </select>
                                </div>

                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700 mb-1"
                                        >Équipe 2</label
                                    >
                                    <select
                                        bind:value={match.team2_id}
                                        required
                                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    >
                                        <option value="">Sélectionner</option>
                                        {#each teams as team}
                                            <option value={team.id}
                                                >{team.company}</option
                                            >
                                        {/each}
                                    </select>
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>

                <!-- Boutons -->
                <div class="flex space-x-3 pt-4">
                    <button
                        type="button"
                        on:click={() => (showAddEditModal = false)}
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
        on:keydown={(e) => e.key === "Escape" && (showDeleteModal = false)}
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
                Êtes-vous sûr de vouloir supprimer cet événement ?
            </p>

            <div class="flex space-x-3">
                <button
                    on:click={() => (showDeleteModal = false)}
                    class="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
                >
                    Annuler
                </button>
                <button
                    on:click={deleteEvent}
                    class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg font-semibold hover:bg-red-700 transition-colors"
                >
                    Supprimer
                </button>
            </div>
        </div>
    </div>
{/if}