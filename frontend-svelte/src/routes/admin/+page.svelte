<!-- ============================================
FICHIER : src/routes/HomePage.svelte
============================================ -->

<script>
    import { authStore } from "$lib/store/auth.js";
    import admin from "$lib/data/admin_test.json"; 
    
    let showModal = false;
    let currentUser = null;
    let isEditMode = false;
    
    function openCreateModal() {
        isEditMode = false;
        currentUser = {
            nom: "",
            prenom: "",
            entreprise: "",
            numero_licence: "",
            email: ""
        };
        showModal = true;
    }
    
    function openEditModal(joueur) {
        isEditMode = true;
        currentUser = { ...joueur };
        showModal = true;
    }
    
    function closeModal() {
        showModal = false;
        currentUser = null;
    }
    
    function saveUser() {
        // Logique de sauvegarde à implémenter
        console.log(isEditMode ? "Modification" : "Création", currentUser);
        closeModal();
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
                <div>Nom</div>
                <div>Prénom</div>
                <div>Entreprise</div>
                <div>Licence</div>
                <div>Email</div>
                
            </div>
            
            <!-- Lignes de données -->
            {#each admin.joueurs as joueur, index}
                <div class="grid grid-cols-[1fr_1fr_1.5fr_1fr_2fr_auto] gap-6 px-8 py-4 border-b hover:bg-blue-50 transition-colors {index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}">
                    <div class="text-gray-900">{joueur.nom}</div>
                    <div class="text-gray-900">{joueur.prenom}</div>
                    <div class="text-gray-600">{joueur.entreprise}</div>
                    <div class="text-gray-600">{joueur.numero_licence}</div>
                    <div class="text-blue-600 text-sm">{joueur.email}</div>
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
                        <label class="block text-sm font-medium text-gray-700 mb-2">Nom</label>
                        <input 
                            type="text" 
                            bind:value={currentUser.nom}
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            required
                        />
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Prénom</label>
                        <input 
                            type="text" 
                            bind:value={currentUser.prenom}
                            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            required
                        />
                    </div>
                </div>
                
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Entreprise</label>
                    <input 
                        type="text" 
                        bind:value={currentUser.entreprise}
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        required
                    />
                </div>
                
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Numéro de licence</label>
                    <input 
                        type="text" 
                        bind:value={currentUser.numero_licence}
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        required
                    />
                </div>
                
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
                    <input 
                        type="email" 
                        bind:value={currentUser.email}
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        required
                    />
                </div>
                
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
