<script lang="ts">
	import MessageIcon from '~icons/mdi/chat';
	import { onMount } from 'svelte';
	import { fade, slide } from 'svelte/transition';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import AnimatedCheck from './AnimatedCheck.svelte';

	// Props
	export let message = '';

	let loading = true;

	let showCheckmark = false;
	$: if (!loading) {
		// Show checkmark after we stop loading
		showCheckmark = true;
		setTimeout(() => (showCheckmark = false), 1000);
	}

	onMount(() => {
		setTimeout(() => (loading = false), 1000);
	});
</script>

<div class="card flex items-center p-4 gap-2">
	<div class="shrink-0 w-5 h-6 flex items-center">
		{#if loading}
			<span transition:fade class="absolute">
				<ProgressRadial width="w-5" />
			</span>
		{:else if showCheckmark}
			<span transition:fade class="absolute">
				<AnimatedCheck delay={300} />
			</span>
		{:else}
			<span transition:fade class="absolute">
				<MessageIcon />
			</span>
		{/if}
	</div>
	{#if !loading && !showCheckmark}
		<div transition:slide={{ delay: 100 }} class="text-sm">"{message}"</div>
	{/if}
</div>
