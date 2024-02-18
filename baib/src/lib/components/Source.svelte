<script lang="ts">
	import MessageIcon from '~icons/mdi/chat';
	import EmailIcon from '~icons/mdi/email';
	import PhotoIcon from '~icons/mdi/insert-photo';
	import { onMount } from 'svelte';
	import { fade, fly, slide } from 'svelte/transition';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import AnimatedCheck from './AnimatedCheck.svelte';
	import type { Progress, SourceType } from '$lib/types';

	// Props
	export let type: SourceType;
	export let delay = 0;
	export let progress: Progress = { done: false, text: '' };

	let typeString = '';
	$: {
		switch (type) {
			case 'message':
				typeString = 'messages';
				break;
			case 'email':
				typeString = 'emails';
				break;
			case 'photo':
				typeString = 'photos';
				break;
		}
	}

	let visible = false;
	let loading = true;

	let showCheckmark = false;

	$: progress, onProgressChanged();
	function onProgressChanged() {
		if (progress.done) {
			loading = false;
		}
	}

	$: if (!loading) {
		showCheckmark = true;
		setTimeout(() => (showCheckmark = false), 1000);
	}

	onMount(() => {
		setTimeout(() => (visible = true), delay);
		// setTimeout(() => (loading = false), 1000 + delay);
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
		{#if loading}
			<div class="grid">
				{#key progress.text}
					<div
						in:slide={{ delay: 300 }}
						out:slide
						class="text-sm col-start-1 col-end-2 row-start-1 row-end-2"
					>
						{progress.text}
					</div>
				{/key}
			</div>
		{:else}
			<div transition:slide class="text-sm">Done parsing {typeString}</div>
		{/if}
	</div>
{/if}
