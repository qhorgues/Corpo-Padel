<!-- ============================================
FICHIER : src/routes/HomePage.svelte
============================================ -->

<script lang="ts">
    import { authStore } from "$lib/store/auth.js";
    import { playersService, type PlayerOutput, type PlayerInput, Role } from "$lib/services/player";
    import { onMount } from "svelte";
    
    let showModal = false;
    let currentUser = null;
    let isEditMode = false;
    let players = [];
    let loading = true;
    
    // Charger les données depuis le backend
    onMount(async () => {
        await loadPlayers();
    });

    async function loadPlayers() {
        loading = true;
        try {
            const response = await playersService.getAllPlayers();
            players = response.data.players;
        } catch (error) {
            console.error("Erreur lors du chargement des joueurs:", error);
            alert("Erreur lors du chargement des joueurs");
        } finally {
            loading = false;
        }
    }
    
    // Validation states
    let validation = {
        first_name: { valid: false, error: "" },
        last_name: { valid: false, error: "" },
        company: { valid: false, error: "" },
        license_number: { valid: false, error: "" },
        email: { valid: false, error: "" }
    };
    
    // Regex patterns
    const patterns = {
        first_name: /^[a-zA-ZÀ-ÿ\s]{2,50}$/,
        last_name: /^[a-zA-ZÀ-ÿ\s]{2,50}$/,
        company: /^.{2,100}$/,
        license_number: /^.+$/,
        email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    };
    
    function validateField(field, value) {
        if (!value || value.trim() === "") {
            validation[field] = { valid: false, error: "Ce champ est obligatoire" };
            return;
        }
        
        const isValid = patterns[field].test(value);
        
        if (field === "first_name" || field === "last_name") {
            if (!isValid) {
                validation[field] = { valid: false, error: "Caractère non autorisé" };
            } else {
                validation[field] = { valid: true, error: "" };
            }
        } else {
            validation[field] = { valid: isValid, error: isValid ? "" : "Format invalide" };
        }
    }
    
    function handleInput(field, event) {
        let value = event.target.value;
        
        // Block input at max length
        if (field === "first_name" || field === "last_name") {
            if (value.length > 50) {
                value = value.substring(0, 50);
                event.target.value = value;
            }
        } else if (field === "company") {
            if (value.length > 100) {
                value = value.substring(0, 100);
                event.target.value = value;
            }
        }
        
        currentUser[field] = value;
        validateField(field, value);
    }
    
    function openCreateModal() {
        isEditMode = false;
        currentUser = {
            first_name: "",
            last_name: "",
            company: "",
            license_number: "",
            email: ""
        };
        validation = {
            first_name: { valid: false, error: "" },
            last_name: { valid: false, error: "" },
            company: { valid: false, error: "" },
            license_number: { valid: false, error: "" },
            email: { valid: false, error: "" }
        };
        showModal = true;
    }
    
    function openEditModal(joueur) {
        isEditMode = true;
        currentUser = { ...joueur };
        
        // Validate all fields on edit
        Object.keys(currentUser).forEach(field => {
            if (patterns[field]) {
                validateField(field, currentUser[field]);
            }
        });
        
        showModal = true;
    }
    
    function closeModal() {
        showModal = false;
        currentUser = null;
    }
    
    async function saveUser() {
        // Check all fields are valid
        const allValid = Object.values(validation).every(v => v.valid);
        if (!allValid) {
            alert("Veuillez corriger les erreurs avant de sauvegarder");
            return;
        }
        
        try {
            const playerInput: PlayerInput = {
                first_name: currentUser.first_name,
                last_name: currentUser.last_name,
                company: currentUser.company,
                license_number: currentUser.license_number,
                email: currentUser.email,
                password: "TempPassword123!", // Mot de passe temporaire
                role: Role.JOUEUR
            };

            if (isEditMode) {
                await playersService.updatePlayer(currentUser.id, playerInput);
            } else {
                await playersService.createPlayer(playerInput);
            }

            await loadPlayers();
            closeModal();
        } catch (error) {
            console.error("Erreur lors de la sauvegarde:", error);
            alert("Erreur lors de la sauvegarde de l'utilisateur");
        }
    }
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
        <div class="h-full bg-white shadow-xl overflow-y-auto overflow-x-hidden">
            <div class="flex justify-between items-center p-6 bg-gray-50 border-b sticky top-0">
                <h2 class="text-2xl font-bold text-gray-800">Liste des joueurs</h2>
                <button 
                    on:click={openCreateModal}
                    class="px-6 py-2 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition-colors"
                >
                    Créer utilisateur
                </button>
            </div>
            
            <!-- En-têtes -->
            <div class="grid grid-cols-[1fr_1fr_1.5fr_1fr_2fr_auto] gap-6 px-8 py-3 bg-gray-100 border-b font-semibold text-gray-700 text-sm sticky top-[73px]">
                <div>Prénom</div>
                <div>Nom</div>
                <div>Entreprise</div>
                <div>Licence</div>
                <div>Email</div>
                <div>Actions</div>
            </div>
            
            <!-- Lignes de données -->
            {#if loading}
                <div class="px-8 py-12 text-center text-gray-500">
                    Chargement...
                </div>
            {:else if players.length === 0}
                <div class="px-8 py-12 text-center text-gray-500">
                    Aucun joueur trouvé
                </div>
            {:else}
                {#each players as joueur, index}
                <div class="grid grid-cols-[1fr_1fr_1.5fr_1fr_2fr_auto] gap-6 px-8 py-4 border-b hover:bg-blue-50 transition-colors {index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}">
                    <div class="text-gray-900">{joueur.first_name}</div>
                    <div class="text-gray-900">{joueur.last_name}</div>
                    <div class="text-gray-600">{joueur.company}</div>
                    <div class="text-gray-600">{joueur.license_number}</div>
                    <div class="text-blue-600 text-sm">{joueur.email || 'N/A'}</div>
                    <div>
                        <button 
                            on:click={() => openEditModal(joueur)}
                            class="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-semibold hover:bg-blue-700 transition-colors"
                        >
                            Modifier
                        </button>
                    </div>
                </div>
            {/each}
            {/if}
        </div>
    </div>
    
    <!-- Modal de création/modification -->
    {#if showModal}
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" on:click={closeModal}>
        <div class="bg-white rounded-lg shadow-xl p-8 max-w-2xl w-full mx-4" on:click|stopPropagation>
            <h3 class="text-2xl font-bold text-gray-800 mb-6">
                {isEditMode ? "Modifier l'utilisateur" : "Créer un utilisateur"}
            </h3>
            
            <form on:submit|preventDefault={saveUser} class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Prénom</label>
                        <p class="text-xs text-gray-500 mb-2">2-50 caractères, lettres et espaces uniquement</p>
                        <input 
                            type="text" 
                            value={currentUser.first_name}
                            on:input={(e) => handleInput('first_name', e)}
                            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent {validation.first_name.valid ? 'border-green-500' : validation.first_name.error ? 'border-red-500' : 'border-gray-300'}"
                            required
                        />
                        {#if validation.first_name.error}
                            <p class="text-xs text-red-500 mt-1">{validation.first_name.error}</p>
                        {:else if validation.first_name.valid}
                            <p class="text-xs text-green-500 mt-1">✓ Valide</p>
                        {/if}
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Nom</label>
                        <p class="text-xs text-gray-500 mb-2">2-50 caractères, lettres et espaces uniquement</p>
                        <input 
                            type="text" 
                            value={currentUser.last_name}
                            on:input={(e) => handleInput('last_name', e)}
                            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent {validation.last_name.valid ? 'border-green-500' : validation.last_name.error ? 'border-red-500' : 'border-gray-300'}"
                            required
                        />
                        {#if validation.last_name.error}
                            <p class="text-xs text-red-500 mt-1">{validation.last_name.error}</p>
                        {:else if validation.last_name.valid}
                            <p class="text-xs text-green-500 mt-1">✓ Valide</p>
                        {/if}
                    </div>
                </div>
                
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Entreprise</label>
                    <p class="text-xs text-gray-500 mb-2">2-100 caractères</p>
                    <input 
                        type="text" 
                        value={currentUser.company}
                        on:input={(e) => handleInput('company', e)}
                        class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent {validation.company.valid ? 'border-green-500' : validation.company.error ? 'border-red-500' : 'border-gray-300'}"
                        required
                    />
                    {#if validation.company.error}
                        <p class="text-xs text-red-500 mt-1">{validation.company.error}</p>
                    {:else if validation.company.valid}
                        <p class="text-xs text-green-500 mt-1">✓ Valide</p>
                    {/if}
                </div>
                
                {#if !isEditMode}
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Numéro de licence</label>
                    <p class="text-xs text-gray-500 mb-2">Champ obligatoire</p>
                    <input 
                        type="text" 
                        value={currentUser.license_number}
                        on:input={(e) => handleInput('license_number', e)}
                        class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent {validation.license_number.valid ? 'border-green-500' : validation.license_number.error ? 'border-red-500' : 'border-gray-300'}"
                        required
                    />
                    {#if validation.license_number.error}
                        <p class="text-xs text-red-500 mt-1">{validation.license_number.error}</p>
                    {:else if validation.license_number.valid}
                        <p class="text-xs text-green-500 mt-1">✓ Valide</p>
                    {/if}
                </div>
                
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                    <p class="text-xs text-gray-500 mb-2">Format: exemple@domaine.com</p>
                    <input 
                        type="email" 
                        value={currentUser.email}
                        on:input={(e) => handleInput('email', e)}
                        class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent {validation.email.valid ? 'border-green-500' : validation.email.error ? 'border-red-500' : 'border-gray-300'}"
                        required
                    />
                    {#if validation.email.error}
                        <p class="text-xs text-red-500 mt-1">{validation.email.error}</p>
                    {:else if validation.email.valid}
                        <p class="text-xs text-green-500 mt-1">✓ Valide</p>
                    {/if}
                </div>
                {:else}
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Numéro de licence</label>
                    <p class="text-xs text-gray-500 mb-2">Non modifiable</p>
                    <input 
                        type="text" 
                        value={currentUser.license_number}
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-100 cursor-not-allowed"
                        disabled
                        readonly
                    />
                </div>
                
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                    <p class="text-xs text-gray-500 mb-2">Non modifiable</p>
                    <input 
                        type="email" 
                        value={currentUser.email}
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-100 cursor-not-allowed"
                        disabled
                        readonly
                    />
                </div>
                {/if}
                
                <div class="flex justify-end gap-4 mt-6">
                    <button 
                        type="button"
                        on:click={closeModal}
                        class="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-400 transition-colors"
                    >
                        Annuler
                    </button>
                    <button 
                        type="submit"
                        class="px-6 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                    >
                        {isEditMode ? "Modifier" : "Créer"}
                    </button>
                </div>
            </form>
        </div>
    </div>
    {/if}
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

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<!-- svelte-ignore a11y-label-has-associated-control -->
