<script>
    import { authStore } from "$lib/store/auth.js";
    import profile from "$lib/data/profile_test.json"; 
    import Page from "../+page.svelte";
    import { goto } from '$app/navigation';
</script>

<div class="min-h-screen flex items-center justify-center bg-linear-to-br from-blue-50 to-indigo-100">
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
                    <h1 class="text-2xl font-semibold text-gray-800">Profil utilisateur</h1>
                </div>    

                <div class="flex flex-col items-center gap-6 p-7 rounded-2xl">
                    <div>
                        <img 
                            class="size-48 shadow-xl rounded-full object-cover border-4 border-blue-100" 
                            alt="Photo de profil" 
                            src={profile.player.photo_url} 
                        />
                    </div>
                    <div class="w-full max-w-2xl space-y-3">
                        <p class="text-lg"><strong>Nom :</strong> {profile.player.last_name}</p>
                        <p class="text-lg"><strong>Prénom :</strong> {profile.player.first_name}</p>
                        <p class="text-lg"><strong>Date de naissance :</strong> {new Date(profile.player.birth_date).toLocaleDateString('fr-FR')}</p>
                        <p class="text-lg"><strong>Email :</strong> {profile.user.email}</p>
                        <p class="text-lg"><strong>Entreprise :</strong> {profile.player.company}</p>
                        <p class="text-lg"><strong>Numéro de licence :</strong> {profile.player.license_number}</p>
                        <p class="text-lg"><strong>Rôle :</strong> {profile.user.role}</p>
                        
                        <button 
                            on:click={() => goto('/profile/edit')}
                            class="mt-6 px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors shadow-md font-semibold"
                        >
                            Éditer les informations
                        </button>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</div>