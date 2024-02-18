<!-- YOU CAN DELETE EVERYTHING IN THIS PAGE -->

<script lang="ts">
	import { onMount } from 'svelte';
	import logo from '../assets/logo.png';
	import imLogo from '../assets/imessage.png';
	import gmailLogo from '../assets/gmail.png';
	import gPhotos from '../assets/gphotos.png';
	import { fade, scale, slide } from 'svelte/transition';
	import PromptInput from '$lib/components/PromptInput.svelte';
	import Todos from '$lib/components/Todos.svelte';
	import { goto } from '$app/navigation';
	import { query } from '$lib/stores';

	let input = '';

	let questionFinal = 'What do you want help with today?';
	let question = '';

	let showCursor = false;

	function revealText() {
		const characters = questionFinal.split('');

		characters.forEach((char, index) => {
			setTimeout(() => {
				question = characters.slice(0, index + 1).join('');
			}, 50 * index);
		});
	}

	let ready = false;
	let interval;

	function showHideCursor() {
		setInterval(() => {
			showCursor = !showCursor;
		}, 500);
	}

	function submit(event: any) {
		query.set(event.detail.text);
		goto('/response');
	}

	onMount(() => {
		revealText();
		ready = true;
		showHideCursor();
	});
</script>

<div class="container h-full mx-auto flex justify-center items-center p-4 w-full">
	<div class="w-full flex flex-col">
		<div class="flex gap-1 items-center flex-row">
			<h1 class="text-4xl">B<span class="text-gray-300">AI</span>B</h1>
		</div>

		<div class="container flex justify-center flex-row w-full items-center gap-2 mt-10 mb-5">
			<div class="w-10">
				{#if ready}
					<img
						alt="logo"
						transition:scale
						class="rounded-[50%] h-10 border-2 border-white"
						src={logo}
					/>
				{/if}
			</div>

			{#if ready}
				<div class="flex flex-col w-80 p-1 rounded-lg" transition:slide>
					{#if ready}
						<h1 class="h2" transition:slide>Hey Arjun!</h1>
					{/if}
					<div class="flex">
						<div class="flex">
							{question}
							<div class="h-5 w-0.5">
								{#if showCursor}
									<div transition:fade class="bg-red-200 h-5 w-0.5 fading-div"></div>
								{/if}
							</div>
						</div>
					</div>
				</div>
			{/if}
		</div>
		<Todos></Todos>

		<div class="w-full p-4 absolute bottom-0 left-0">
			{#if ready}
				<div class="w-full mb-5 flex flex-col gap-2" transition:fade>
					<h1 class="">Searches through</h1>
					<div class="card p-4 flex items-center justify-between">
						<div class="flex gap-2 items-center">
							<img class="w-5 h-5" alt="imessage" src={imLogo} />
							<p>imessage</p>
						</div>
						<div><p class="text-gray-500">connected</p></div>
					</div>

					<div class="card p-4 flex items-center justify-between">
						<div class="flex gap-2 items-center">
							<img class="w-5 h-4" alt="gmail" src={gmailLogo} />
							<p>gmail</p>
						</div>
						<div><p class="text-gray-500">connected</p></div>
					</div>

					<div class="card p-4 flex items-center justify-between">
						<div class="flex gap-2 items-center">
							<img class="w-5 h-5" alt="googlephotos" src={gPhotos} />
							<p>google photos</p>
						</div>
						<div><p class="text-gray-500">connected</p></div>
					</div>
				</div>
			{/if}

			{#if ready}
				<PromptInput bind:input on:submit={submit}></PromptInput>
			{/if}
		</div>
	</div>
</div>
