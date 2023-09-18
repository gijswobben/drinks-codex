<script>
	import '../app.css';
	import AppContent from '$lib/components/AppContent.svelte';
	import Header from '$lib/components/Header.svelte';
</script>

<Header />

<AppContent>
	<slot />
</AppContent>
