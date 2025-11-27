<script>
    import { goto } from '$app/navigation';
    import profile from "$lib/data/match_test.json";
    
    // Créer une copie éditable
    let editedProfile = {
        photo_url: profile.player.photo_url,
        first_name: profile.player.first_name,
        last_name: profile.player.last_name,
        birth_date: profile.player.birth_date,
        email: profile.user.email,
        company: profile.player.company,
        license_number: profile.player.license_number
    };
    function handleCancel() {
        goto('/profile');
    }
</script>

<div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
    <div class="w-full max-w-2xl">
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
                        type="submit"
                        class="flex-1 p-3 bg-green-500 text-white rounded-lg font-semibold hover:bg-green-600 transition-colors shadow-md"
                    >
                        Sauvegarder
                    </button>
                    <button 
                        type="button"
                        on:click={handleCancel}
                        class="flex-1 p-3 bg-gray-500 text-white rounded-lg font-semibold hover:bg-gray-600 transition-colors shadow-md"
                    >
                        Annuler
                    </button>
                </div>
        </div>
    </div>
</div>