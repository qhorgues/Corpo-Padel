<script>
    import { goto } from '$app/navigation';
    import profile from "$lib/data/profile_test.json";
    
    let editedProfile = { ...profile };
    function handleSubmit() {
        console.log("Profil sauvegardé :", editedProfile);
        goto('/profile');
    }
    function handleCancel() {
        goto('/profile');
    }
</script>


        <div class="bg-white rounded-2xl shadow-xl p-8">
            <h1 class="text-3xl font-bold mb-6 text-center">Éditer le profil</h1>
               <!-- PDP -->
                <div class="flex justify-center mb-6">
                    <img class="size-32 shadow-xl rounded-md" alt="Photo de profil" src={editedProfile.filename} />
                </div>
                <!-- NOM -->
                <div>
                    <label for="nom" class="block font-semibold mb-2 text-gray-700">
                        Nom
                    </label>
                    <input 
                        id="nom"
                        type="text" 
                        bind:value={editedProfile.nom}
                        class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        required
                    />
                </div>

                <!-- PRENOM -->
                <div>
                    <label for="prenom" class="block font-semibold mb-2 text-gray-700">
                        Prénom
                    </label>
                    <input 
                        id="prenom"
                        type="text" 
                        bind:value={editedProfile.prenom}
                        class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        required
                    />
                </div>

                <!-- DATE DE NAISSANCE -->
                <div>
                    <label for="date_naissance" class="block font-semibold mb-2 text-gray-700">
                        Date de naissance
                    </label>
                    <input 
                        id="date_naissance"
                        type="date" 
                        bind:value={editedProfile.date_naissance}
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

                <!-- NUMERO DE LICENCE -->
                <div>
                    <label for="numero_licence" class="block font-semibold mb-2 text-gray-700">
                        Numéro de licence
                    </label>
                    <input 
                        id="numero_licence"
                        type="text" 
                        bind:value={editedProfile.numero_licence}
                        class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        required
                    />
                </div>

                <!-- BOUTTONS -->
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
                        class="flex-1 p-3 bg-gray-500 text-white rounded-lg font-semibold hover:bg-gray-600 transition-colors shadow-md">
                        Annuler
                    </button>
                </div>
</div>