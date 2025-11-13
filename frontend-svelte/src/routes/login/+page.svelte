<!-- src/routes/login/+page.svelte -->
<script lang="ts">
    import { authStore } from "$lib/store/auth";
    import { goto } from "$app/navigation";
    import { writable } from "svelte/store";
    import { get } from "svelte/store";

    const email = writable("");
    const password = writable("");
    const loading = writable(false);
    const errorMessage = writable("");
    const attemptsRemaining = writable<number | null>(null);
    const minutesRemaining = writable<number | null>(null);

    const handleLogin = async () => {
        loading.set(true);
        errorMessage.set("");
        attemptsRemaining.set(null);
        minutesRemaining.set(null);

        const result = await authStore.login($email, $password)

        if (result.success && $authStore.isAuthenticated) {
            goto('/');
        } else {
            errorMessage.set(result.error || 'Erreur de connexion');
            attemptsRemaining.set(result.attemptsRemaining ?? null);
            minutesRemaining.set(result.minutesRemaining ?? null);
        }

        loading.set(false);
    };
</script>

<div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
    <div class="w-full max-w-md">
        <div class="bg-white rounded-lg shadow-2xl p-8">
            <!-- Header -->
            <div class="text-center mb-8">
                <div class="text-6xl mb-4">🎾</div>
                <h1 class="text-3xl font-bold text-gray-800">Corpo Padel</h1>
                <p class="text-gray-600 mt-2">Connectez-vous à votre compte</p>
            </div>

            <!-- Formulaire -->
            <form on:submit|preventDefault={handleLogin}>
                <!-- Email -->
                <div class="mb-4">
                    <label
                        for="email"
                        class="block text-sm font-medium text-gray-700 mb-2"
                    >
                        Email
                    </label>
                    <input
                        id="email"
                        type="email"
                        bind:value={$email}
                        required
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="votre@email.com"
                    />
                </div>

                <!-- Mot de passe -->
                <div class="mb-6">
                    <label
                        for="password"
                        class="block text-sm font-medium text-gray-700 mb-2"
                    >
                        Mot de passe
                    </label>
                    <input
                        id="password"
                        type="password"
                        bind:value={$password}
                        required
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="••••••••"
                    />
                </div>

                <!-- Message d'erreur -->
                {#if $errorMessage}
                    <div
                        class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg"
                    >
                        <p class="text-red-700 text-sm">{$errorMessage}</p>
                        {#if $attemptsRemaining !== null}
                            <p class="text-red-600 text-sm font-semibold mt-1">
                                Tentatives restantes : {$attemptsRemaining}
                            </p>
                        {/if}
                        {#if $minutesRemaining !== null}
                            <p class="text-red-600 text-sm font-semibold mt-1">
                                Compte bloqué pendant {$minutesRemaining} minutes
                            </p>
                        {/if}
                    </div>
                {/if}

                <!-- Bouton de connexion -->
                <button
                    type="submit"
                    class="w-full py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
                    disabled={$loading || $minutesRemaining !== null}
                >
                    {#if $loading}
                        Connexion...
                    {:else if $minutesRemaining !== null}
                        Compte bloqué
                    {:else}
                        Se connecter
                    {/if}
                </button>
            </form>

            <!-- Informations de test -->
            <div class="mt-6 p-4 bg-blue-50 rounded-lg">
                <p class="text-xs text-gray-600 text-center">
                    <strong>Compte de test :</strong><br />
                    admin@padel.com / Admin@2025!
                </p>
            </div>
        </div>
    </div>
</div>
