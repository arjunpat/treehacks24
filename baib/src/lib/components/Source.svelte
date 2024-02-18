<script lang="ts">
	import MessageIcon from '~icons/mdi/chat';
	import EmailIcon from '~icons/mdi/email';
	import PhotoIcon from '~icons/mdi/insert-photo';
	import { onMount } from 'svelte';
	import { fade, slide } from 'svelte/transition';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import AnimatedCheck from './AnimatedCheck.svelte';
	import type { SourceType } from '$lib/types';

	// Props
	export let message = '';
	export let type: SourceType;
	export let delay = 0;

	let visible = false;
	let loading = true;

	let showCheckmark = false;
	$: if (!loading) {
		// Show checkmark after we stop loading
		showCheckmark = true;
		setTimeout(() => (showCheckmark = false), 1000);
	}

	onMount(() => {
		setTimeout(() => (visible = true), delay);
		setTimeout(() => (loading = false), 1000 + delay);
	});
</script>

{#if visible}
	<div transition:slide class="card flex items-center p-4 gap-2">
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
					{#if type === 'message'}
						<MessageIcon />
					{:else if type === 'email'}
						<EmailIcon />
					{:else if type === 'photo'}
						<PhotoIcon />
					{/if}
				</span>
			{/if}
		</div>
		{#if !loading && !showCheckmark}
			<div transition:slide={{ delay: 100 }} class="text-sm">"{message}"</div>
		{/if}
	</div>
{/if}
