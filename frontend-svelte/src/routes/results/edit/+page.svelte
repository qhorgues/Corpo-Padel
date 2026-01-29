<script lang="ts">
    import { goto } from '$app/navigation';
    import { profileService, type ProfileOutput, type ProfileInput } from "$lib/services/profile";
    import { onMount } from 'svelte';
    
    let profile: ProfileOutput | null = null;
    let loading = true;
    let saving = false;
    
    // Créer une copie éditable
    let editedProfile = {
        photo_url: '',
        first_name: '',
        last_name: '',
        birth_date: '',
        email: '',
        company: '',
        license_number: ''
    };

    onMount(async () => {
        await loadProfile();
    });

    async function loadProfile() {
        loading = true;
        try {
            const response = await profileService.getMyProfile();
            profile = response.data;
            
            // Date d'aujourd'hui par défaut si birth_date vide
            const today = new Date().toISOString().split('T')[0];
            
            // Initialiser les champs éditables
            editedProfile = {
                photo_url: profile.player.photo_url || '',
                first_name: profile.player.first_name,
                last_name: profile.player.last_name,
                birth_date: profile.player.birth_date || today,
                email: profile.user.email,
                company: profile.player.company,
                license_number: profile.player.license_number
            };
        } catch (error) {
            console.error("Erreur lors du chargement du profil:", error);
            alert("Erreur lors du chargement du profil");
        } finally {
            loading = false;
        }
    }

    async function handleSave() {
        saving = true;
        try {
            const profileInput: ProfileInput = {
                first_name: editedProfile.first_name,
                last_name: editedProfile.last_name,
                birth_date: editedProfile.birth_date,
                email: editedProfile.email,
                photo_url: editedProfile.photo_url || null
            };

            await profileService.updateMyProfile(profileInput);
            alert("Profil mis à jour avec succès");
            goto('/profile');
        } catch (error) {
            console.error("Erreur lors de la sauvegarde:", error);
            alert("Erreur lors de la sauvegarde du profil");
        } finally {
            saving = false;
        }
    }
    
    function handleCancel() {
        goto('/profile');
    }
</script>

<div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
    <div class="w-full max-w-2xl">
        {#if loading}
            <div class="bg-white rounded-2xl shadow-xl p-8">
                <p class="text-center text-gray-600">Chargement...</p>
            </div>
        {:else}
        <div class="bg-white rounded-2xl shadow-xl p-8">
            <h1 class="text-3xl font-bold mb-6 text-center text-gray-800">Éditer le profil</h1>
                <!-- PHOTO DE PROFIL -->
                <div>
                    <label for="photo_url" class="block font-semibold mb-2 text-gray-700">
                        URL de la photo de profil
                    </label>
                    <input 
                        id="photo_url"
                        type="url"
                        bind:value={editedProfile.photo_url}
                        class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="https://exemple.com/photo.jpg"
                    />
                </div>

                <!-- PRÉNOM -->
                <div>
                    <label for="first_name" class="block font-semibold mb-2 text-gray-700">
                        Prénom
                    </label>
                    <input 
                        id="first_name"
                        type="text" 
                        bind:value={editedProfile.first_name}
                        class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        required
                    />
                </div>

                <!-- NOM -->
                <div>
                    <label for="last_name" class="block font-semibold mb-2 text-gray-700">
                        Nom
                    </label>
                    <input 
                        id="last_name"
                        type="text"
                        bind:value={editedProfile.last_name} 
                        class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        required
                    />
                </div>

                <!-- DATE DE NAISSANCE -->
                <div>
                    <label for="birth_date" class="block font-semibold mb-2 text-gray-700">
                        Date de naissance
                    </label>
                    <input 
                        id="birth_date"
                        type="date" 
                        bind:value={editedProfile.birth_date}
                        class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        required
                    />
                </div>

                <!-- EMAIL -->
                <div>
                    <label for="email" class="block font-semibold mb-2 text-gray-700">
                        Email
                    </label>
                    <input 
                        id="email"
                        type="email" 
                        bind:value={editedProfile.email}
                        class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        required
                    />
                </div>

                <!-- ENTREPRISE (lecture seule) -->
                <div>
                    <label for="company" class="block font-semibold mb-2 text-gray-700">
                        Entreprise
                    </label>
                    <input 
                        id="company"
                        type="text" 
                        bind:value={editedProfile.company}
                        class="w-full p-3 border border-gray-300 rounded-lg bg-gray-100 cursor-not-allowed"
                        disabled
                    />
                    <p class="text-sm text-gray-500 mt-1">L'entreprise ne peut pas être modifiée</p>
                </div>

                <!-- NUMERO DE LICENCE (lecture seule) -->
                <div>
                    <label for="license_number" class="block font-semibold mb-2 text-gray-700">
                        Numéro de licence
                    </label>
                    <input 
                        id="license_number"
                        type="text" 
                        bind:value={editedProfile.license_number}
                        class="w-full p-3 border border-gray-300 rounded-lg bg-gray-100 cursor-not-allowed"
                        disabled
                    />
                    <p class="text-sm text-gray-500 mt-1">Le numéro de licence ne peut pas être modifié</p>
                </div>

                <!-- BOUTONS -->
                <div class="flex gap-4 pt-4">
                    <button 
                        type="button"
                        on:click={handleSave}
                        disabled={saving}
                        class="flex-1 p-3 bg-green-500 text-white rounded-lg font-semibold hover:bg-green-600 transition-colors shadow-md disabled:bg-gray-400 disabled:cursor-not-allowed"
                    >
                        {saving ? 'Sauvegarde...' : 'Sauvegarder'}
                    </button>
                    <button 
                        type="button"
                        on:click={handleCancel}
                        disabled={saving}
                        class="flex-1 p-3 bg-gray-500 text-white rounded-lg font-semibold hover:bg-gray-600 transition-colors shadow-md disabled:bg-gray-400 disabled:cursor-not-allowed"
                    >
                        Annuler
                    </button>
                </div>
        </div>
        {/if}
    </div>
</div>