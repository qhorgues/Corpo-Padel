<script>
    import "../app.css";
    import NavBar from "$lib/components/NavBar.svelte";
    import { authStore } from "$lib/store/auth";
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { page } from "$app/state";

    onMount(() => {
        authStore.checkAuth();

        if (page.url.pathname !== "/" && !$authStore.isAuthenticated) {
            goto('/login');
        }
        else if (page.url.pathname === "/login") {
            goto("/");
        }
    });
</script>

{#if $authStore.isAuthenticated}
    <NavBar />
{/if}

<slot />
