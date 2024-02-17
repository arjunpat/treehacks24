<script lang="ts">
	import MessageIcon from '~icons/mdi/chat';
	import CheckIcon from '~icons/mdi/check';
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { ProgressRadial } from '@skeletonlabs/skeleton';

	// Props
	export let message = '';

	let loading = true;

	let showCheckmark = false;
	$: if (!loading) {
		// Show checkmark after we stop loading
		showCheckmark = true;
		setTimeout(() => (showCheckmark = false), 500);
	}

	onMount(() => {
		setTimeout(() => (loading = false), 200);
	});
</script>

<div class="card flex items-center p-4 gap-2">
	<div class="w-5">
		{#if loading}
			<span transition:fade>
				<ProgressRadial width="w-5" />
			</span>
		{:else if showCheckmark}
			<span transition:fade>
				<CheckIcon />
			</span>
		{:else}
			<span transition:fade>
				<MessageIcon />
			</span>
		{/if}
	</div>
	<div>"{message}"</div>
</div>
