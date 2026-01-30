<!-- ============================================
FICHIER : src/routes/HomePage.svelte
============================================ -->

<script lang="ts">
    import { authStore } from "$lib/store/auth.js";
    import { playersService, type PlayerOutput, type PlayerInput, Role } from "$lib/services/player";
    import { onMount } from "svelte";
    
    // Types
    type UserForm = {
        id?: number;
        first_name: string;
        last_name: string;
        company: string;
        license_number: string;
        email: string;
    };

    type ValidationField = {
        valid: boolean;
        error: string;
    };

    type ValidationState = {
        first_name: ValidationField;
        last_name: ValidationField;
        company: ValidationField;
        license_number: ValidationField;
        email: ValidationField;
    };
    
    let showModal = false;
    let currentUser: UserForm | null = null;
    let isEditMode = false;
    let players: PlayerOutput[] = [];
    let loading = true;
    
    // Gestion des entreprises
    let companies: string[] = [];
    let showCompanyModal = false;
    let newCompanyName = "";
    
    // Gestion de la suppression
    let showDeleteModal = false;
    let userToDelete: PlayerOutput | null = null;
    
    // Charger les données depuis le backend
    onMount(async () => {
        await loadPlayers();
    });

    async function loadPlayers() {
        loading = true;
        try {
            const response = await playersService.getAllPlayers();
            players = response.data.players;
            // Extraire les entreprises uniques
            companies = [...new Set(players.map(p => p.company))].sort();
        } catch (error) {
            console.error("Erreur lors du chargement des joueurs:", error);
            alert("Erreur lors du chargement des joueurs");
        } finally {
            loading = false;
        }
    }
    
    // Validation states
    let validation: ValidationState = {
        first_name: { valid: false, error: "" },
        last_name: { valid: false, error: "" },
        company: { valid: false, error: "" },
        license_number: { valid: false, error: "" },
        email: { valid: false, error: "" }
    };
    
    // Regex patterns
    const patterns: Record<keyof ValidationState, RegExp> = {
        first_name: /^[a-zA-ZÀ-ÿ\s]{2,50}$/,
        last_name: /^[a-zA-ZÀ-ÿ\s]{2,50}$/,
        company: /^.{2,100}$/,
        license_number: /^L[0-9]{6}$/,
        email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    };
    
    function validateField(field: keyof ValidationState, value: string) {
        if (!value || value.trim() === "") {
            validation[field] = { valid: false, error: "Ce champ est obligatoire" };
            return;
        }
        
        const isValid = patterns[field].test(value);
        
        if (field === "license_number" && !isValid) {
            validation[field] = { valid: false, error: "Format: L suivi de 6 chiffres (ex: L123456)" };
        } else if (field === "first_name" || field === "last_name") {
            if (!isValid) {
                validation[field] = { valid: false, error: "Caractère non autorisé" };
            } else {
                validation[field] = { valid: true, error: "" };
            }
        } else {
            validation[field] = { valid: isValid, error: isValid ? "" : "Format invalide" };
        }
    }
    
    function handleInput(field: keyof ValidationState, event: Event) {
        if (!currentUser) return;
        
        const target = event.target as HTMLInputElement | HTMLSelectElement;
        let value = target.value;
        
        // Block input at max length
        if (field === "first_name" || field === "last_name") {
            if (value.length > 50) {
                value = value.substring(0, 50);
                target.value = value;
            }
        } else if (field === "company") {
            if (value.length > 100) {
                value = value.substring(0, 100);
                target.value = value;
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
    
    function openEditModal(joueur: PlayerOutput) {
        isEditMode = true;
        currentUser = { 
            id: joueur.id,
            first_name: joueur.first_name,
            last_name: joueur.last_name,
            company: joueur.company,
            license_number: joueur.license_number,
            email: joueur.email || "" // S'assurer que email n'est jamais undefined
        };
        
        // Validate all fields on edit
        const fieldsToValidate: (keyof ValidationState)[] = ['first_name', 'last_name', 'company', 'license_number', 'email'];
        fieldsToValidate.forEach(field => {
            if (currentUser && currentUser[field]) {
                validateField(field, currentUser[field] as string);
            }
        });
        
        showModal = true;
    }
    
    function closeModal() {
        showModal = false;
        currentUser = null;
    }
    
    async function saveUser() {
        if (!currentUser) return;
        
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

            if (isEditMode && currentUser.id) {
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
    
    async function deleteUser() {
        if (!userToDelete) return;
        
        try {
            await playersService.deletePlayer(userToDelete.id);
            await loadPlayers();
            showDeleteModal = false;
            userToDelete = null;
        } catch (error) {
            console.error("Erreur lors de la suppression:", error);
            alert("Erreur lors de la suppression de l'utilisateur");
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
                <div class="flex gap-3">
                    <a
                        href="/admin/teams-pools"
                        class="px-6 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                    >
                        🏆 Équipes & Poules
                    </a>
                    <button 
                        on:click={() => showCompanyModal = true}
                        class="px-6 py-2 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700 transition-colors"
                    >
                        Ajouter entreprise
                    </button>
                    <button 
                        on:click={openCreateModal}
                        class="px-6 py-2 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition-colors"
                    >
                        Créer utilisateur
                    </button>
                </div>
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
                    <div class="flex gap-2">
                        <button 
                            on:click={() => openEditModal(joueur)}
                            class="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-semibold hover:bg-blue-700 transition-colors"
                        >
                            Modifier
                        </button>
                        <button 
                            on:click={() => { userToDelete = joueur; showDeleteModal = true; }}
                            class="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-semibold hover:bg-red-700 transition-colors"
                        >
                            Supprimer
                        </button>
                    </div>
                </div>
            {/each}
            {/if}
        </div>
    </div>
    
    <!-- Modal de création/modification -->
    {#if showModal && currentUser}
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
                    <p class="text-xs text-gray-500 mb-2">Sélectionnez une entreprise</p>
                    <select 
                        bind:value={currentUser.company}
                        on:change={(e) => handleInput('company', e)}
                        class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent {validation.company.valid ? 'border-green-500' : validation.company.error ? 'border-red-500' : 'border-gray-300'}"
                        required
                    >
                        <option value="">-- Sélectionner une entreprise --</option>
                        {#each companies as company}
                            <option value={company}>{company}</option>
                        {/each}
                    </select>
                    {#if validation.company.error}
                        <p class="text-xs text-red-500 mt-1">{validation.company.error}</p>
                    {:else if validation.company.valid}
                        <p class="text-xs text-green-500 mt-1">✓ Valide</p>
                    {/if}
                </div>
                
                {#if !isEditMode}
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Numéro de licence</label>
                    <p class="text-xs text-gray-500 mb-2">Format: L suivi de 6 chiffres (ex: L123456)</p>
                    <input 
                        type="text" 
                        value={currentUser.license_number}
                        on:input={(e) => handleInput('license_number', e)}
                        placeholder="L123456"
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
    
    <!-- Modal de création d'entreprise -->
    {#if showCompanyModal}
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" on:click={() => showCompanyModal = false}>
        <div class="bg-white rounded-lg shadow-xl p-8 max-w-md w-full mx-4" on:click|stopPropagation>
            <h3 class="text-2xl font-bold text-gray-800 mb-6">Créer une entreprise</h3>
            
            <form on:submit|preventDefault={() => {
                if (newCompanyName.trim() && !companies.includes(newCompanyName.trim())) {
                    companies = [...companies, newCompanyName.trim()].sort();
                    newCompanyName = "";
                    showCompanyModal = false;
                }
            }}>
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Nom de l'entreprise</label>
                    <input 
                        type="text" 
                        bind:value={newCompanyName}
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Ex: TechCorp"
                        required
                    />
                </div>
                
                <div class="flex justify-end gap-4">
                    <button 
                        type="button"
                        on:click={() => { showCompanyModal = false; newCompanyName = ""; }}
                        class="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-400 transition-colors"
                    >
                        Annuler
                    </button>
                    <button 
                        type="submit"
                        class="px-6 py-2 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700 transition-colors"
                    >
                        Ajouter
                    </button>
                </div>
            </form>
        </div>
    </div>
    {/if}
    
    <!-- Modal de confirmation de suppression -->
    {#if showDeleteModal}
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" on:click={() => showDeleteModal = false}>
        <div class="bg-white rounded-lg shadow-xl p-8 max-w-md w-full mx-4" on:click|stopPropagation>
            <h3 class="text-2xl font-bold text-red-600 mb-4">Confirmer la suppression</h3>
            {#if userToDelete}
            <p class="text-gray-700 mb-6">
                Êtes-vous sûr de vouloir supprimer <strong>{userToDelete.first_name} {userToDelete.last_name}</strong> ?
                <br/><br/>
                Cette action est irréversible.
            </p>
            {/if}
            
            <div class="flex justify-end gap-4">
                <button 
                    type="button"
                    on:click={() => { showDeleteModal = false; userToDelete = null; }}
                    class="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-400 transition-colors"
                >
                    Annuler
                </button>
                <button 
                    type="button"
                    on:click={deleteUser}
                    class="px-6 py-2 bg-red-600 text-white rounded-lg font-semibold hover:bg-red-700 transition-colors"
                >
                    Supprimer
                </button>
            </div>
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