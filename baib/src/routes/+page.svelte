<!-- YOU CAN DELETE EVERYTHING IN THIS PAGE -->

<script lang="ts">
	import { onMount } from 'svelte';
	import logo from '../assets/logo.png';
	import imLogo from '../assets/imessage.png';
	import gmailLogo from '../assets/gmail.png';
	import gPhotos from '../assets/gphotos.png';
	import { fade, scale } from 'svelte/transition';
	import PromptInput from '$lib/components/PromptInput.svelte';

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

	onMount(() => {
		revealText();
		ready = true;
		showHideCursor();
	});
</script>

<div class="container h-full mx-auto flex justify-center items-center p-5 w-full">
	<div class="w-full">
		<div class="flex gap-1 items-center flex-row">
			<h1 class="text-4xl">BAIB</h1>
		</div>

		<div class="container flex justify-center flex-col w-full items-center gap-2 mt-20">
			<h1 class="h1">Hey Arjun</h1>
			<div class="flex">
				<p>{question}</p>

				<div class="h-5 w-0.5">
					{#if showCursor}
						<div transition:fade class="bg-red-200 h-5 w-0.5 fading-div"></div>
					{/if}
				</div>
			</div>

			{#if ready}
				<img
					alt="logo"
					transition:scale
					class="rounded-[50%] h-32 mt-6 border-2 border-white"
					src={logo}
				/>
			{/if}

			<div class="w-full absolute bottom-0 p-5">
				{#if ready}
					<div class="w-full mt-24" transition:fade>
						<h1>Searches through</h1>
						<div class="card p-4 mt-1 flex items-center justify-between">
							<div class="flex gap-2 items-center">
								<img class="w-5 h-5" alt="imessage" src={imLogo} />
								<p>imessage</p>
							</div>
							<div><p class="text-gray-500">connected</p></div>
						</div>

						<div class="card p-4 mt-1 flex items-center justify-between">
							<div class="flex gap-2 items-center">
								<img class="w-5 h-4" alt="gmail" src={gmailLogo} />
								<p>gmail</p>
							</div>
							<div><p class="text-gray-500">connected</p></div>
						</div>

						<div class="card p-4 mt-1 flex items-center justify-between">
							<div class="flex gap-2 items-center">
								<img class="w-5 h-5" alt="googlephotos" src={gPhotos} />
								<p>google photos</p>
							</div>
							<div><p class="text-gray-500">connected</p></div>
						</div>
					</div>
				{/if}

				{#if ready}
					<PromptInput bind:input={input}></PromptInput>
				{/if}
			</div>
		</div>
	</div>
</div>
