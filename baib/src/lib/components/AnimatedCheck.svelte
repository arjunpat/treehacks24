<!-- Checkmark that animates on mount -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { quintIn, quintOut } from 'svelte/easing';
	import { draw } from 'svelte/transition';

	export let delay = 0;
	let visible = false;

	onMount(() => {
		setTimeout(() => {
			visible = true;
		}, delay);
	});
</script>

<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24">
	{#if visible}
		<path
			transition:draw={{ easing: quintOut }}
			fill="none"
			stroke="currentColor"
			d="M 3.5 13.5 L 9 19 L 21 7"
			stroke-width="2"
		/>
	{/if}
</svg>
