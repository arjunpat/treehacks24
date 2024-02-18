<script lang="ts">
	import { fade } from 'svelte/transition';
	import skiingImage1 from '../../assets/dynamic-images/skiing1.jpeg';
	// import skiingImage2 from '../../assets/dynamic-images/skiing2.jpeg';

	export let text: string;
	let question_image = {
		skiing: [
			skiingImage1,
			'https://l6xbzhkc-8000.usw3.devtunnels.ms/static/IMG_0988.jpg',
			'https://l6xbzhkc-8000.usw3.devtunnels.ms/static/IMG_1977.jpg'
		],
		week: []
	};

	$: skiing = text.includes('skiing');
	$: week = text.includes('do this week');

	let images: string[];

	$: if (skiing) {
		images = question_image.skiing;
	} else if (week) {
		images = question_image.week;
	} else {
		images = [];
	}
</script>

{#if images.length > 0}
	<div class="p-4 gap-2 card mb-4" transition:fade>
		{#each images as image (image)}
			<img alt={image} src={image} class="w-32 rounded-lg" />
		{/each}
	</div>
{/if}
