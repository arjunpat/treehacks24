<!-- Checkmark that animates on mount -->
<script lang="ts">
	import { createEventDispatcher, onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import ArrowRightIcon from '~icons/mdi/arrow-right';

	export let input = '';

	const dispatch = createEventDispatcher();

	let ready = false;

	onMount(() => {
		ready = true;
	});

	function submit() {
		dispatch('submit', {
			text: input
		});
	}
</script>

{#if ready}
	<form on:submit|preventDefault={submit} class="mt-2 flex gap-1 w-full" transition:fade>
		<input class="input rounded-lg" bind:value={input} placeholder="ask anything :)" />
		<button on:click={submit} type="button" class="shrink-0 btn-icon variant-filled-surface"
			><ArrowRightIcon /></button
		>
	</form>
{/if}
