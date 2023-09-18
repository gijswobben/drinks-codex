<script lang="ts">
	import { page } from '$app/stores';
	import logo from '$lib/assets/Ordina-logo.2f7ddcfe.svg';
</script>

<header
	class="sticky top-0 z-20 flex h-16 w-full items-center border-b border-solid border-light-gray bg-white drop-shadow md:h-20"
>
	<div
		class="mx-auto flex w-full items-center justify-between px-5 py-3 lg:px-7 xl:px-12 2xl:px-16"
	>
		<div class="flex items-center">
			<a href="/"><img src={logo} alt="Ordina-logo" height="52" width="168" /></a>
		</div>
		<div class="flex flex-row gap-4">
			{#if $page.data.session}
				<div>
					<img src={$page.data.session.user.profile_picture_url} width="32px" height="32px" />
				</div>
				<a href="/auth/signout" class=""> Sign out </a>
			{:else}
				<a href="/auth/signin" class=""> Sign in </a>
			{/if}
		</div>
	</div>
</header>
