<!-- YOU CAN DELETE EVERYTHING IN THIS PAGE -->

<script lang="ts">
	import { onMount } from 'svelte';
	import logo from "../assets/logo.png";

	let input = ""

	let questionFinal = 'What do you want help with today?';
	let question = '';

	function revealText() {
		const characters = questionFinal.split('');

		characters.forEach((char, index) => {
			setTimeout(() => {
				question = characters.slice(0, index + 1).join('');
			}, 50 * index);
		});
	}

	onMount(() => {
		revealText();
	});
</script>

<div class="container h-full mx-auto flex justify-center items-center p-5 w-full">
	<div class="w-full">
		<div class="flex gap-1 items-center flex-row">
			
		<h1 class="text-4xl">BAIB</h1></div>

		<div class="container flex justify-center flex-col w-full items-center gap-2 mt-20">
			<h1 class="h1">Hey Arjun</h1>
			<div class="flex">
				<p>{question}</p>
					<div class="bg-red-200 h-5 w-0.5 fading-div"></div>
			</div>


			<img class="rounded-[50%] h-32 mt-6 border-2 border-white" src={logo}/>

			<div class="mt-10">
				<input class="input rounded-lg" bind:value={input} placeholder="enter your name" />
				<button type="button" class="btn-icon variant-filled">send</button>



			</div>
		</div>
	</div>
</div>
