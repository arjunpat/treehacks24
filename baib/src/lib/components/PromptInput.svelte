<!-- Checkmark that animates on mount -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import ArrowRightIcon from '~icons/mdi/arrow-right';

	export let input = '';

	let ready = false;

	onMount(() => {
		ready = true;
	});
</script>

{#if ready}
	<div class="mt-2 flex gap-1 w-full" transition:fade>
		<input class="input rounded-lg" bind:value={input} placeholder="ask anything :)" />
    <a href="/response">
		<button type="button" class="shrink-0 btn-icon variant-filled-surface"
			><ArrowRightIcon /></button
		></a>
	</div>
{/if}
