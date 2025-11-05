<script>
    import "../app.css";
    import NavBar from "$lib/components/NavBar.svelte";
    import { authStore } from "$lib/store/auth";
    import { onMount } from "svelte";

    onMount(() => {
        authStore.checkAuth();
    });
</script>

{#if $authStore.isAuthenticated}
    <NavBar />
{/if}

<slot />
