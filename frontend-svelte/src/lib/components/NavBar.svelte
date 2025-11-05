<script>
    import { authStore } from "$lib/store/auth";
    import { goto } from "$app/navigation";

    async function handleLogout() {
        await authStore.logout();
        goto("/login");
    }
</script>

<nav class="bg-blue-600 text-white shadow-lg">
    <div class="container mx-auto px-4">
        <div class="flex justify-between items-center h-16">
            <!-- Logo -->
            <div class="flex items-center space-x-4">
                <a href="/" class="text-xl font-bold hover:text-blue-200">
                    🎾 Corpo Padel
                </a>
            </div>

            <!-- Menu principal -->
            <div class="hidden md:flex space-x-4">
                <a href="/" class="px-3 py-2 rounded hover:bg-blue-700"
                    >Accueil</a
                >
                <a href="/planning" class="px-3 py-2 rounded hover:bg-blue-700"
                    >Planning</a
                >
                <a href="/matches" class="px-3 py-2 rounded hover:bg-blue-700"
                    >Matchs</a
                >
                <a href="/results" class="px-3 py-2 rounded hover:bg-blue-700"
                    >Résultats</a
                >

                {#if $authStore.isAdmin}
                    <a
                        href="/admin"
                        class="px-3 py-2 rounded hover:bg-blue-700"
                    >
                        Administration
                    </a>
                {/if}
            </div>

            <!-- Menu utilisateur -->
            <div class="flex items-center space-x-4">
                <a href="/profile" class="px-3 py-2 rounded hover:bg-blue-700">
                    👤 {$authStore.user?.email}
                </a>
                <button
                    on:click={handleLogout}
                    class="px-4 py-2 bg-red-500 rounded hover:bg-red-600"
                >
                    Déconnexion
                </button>
            </div>
        </div>
    </div>
</nav>
