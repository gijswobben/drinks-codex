<script lang="ts">
	import Protected from '$lib/guards/Protected.svelte';
	import { page } from '$app/stores';
</script>

<Protected>
	<h1>Protected page</h1>
	<p>This is a protected content. You can access this content because you are signed in.</p>
	<p>Session expiry: {$page.data.session?.expires}</p>
</Protected>
