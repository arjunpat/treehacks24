<script lang="ts">
	import AnswerSection from '$lib/components/AnswerSection.svelte';
	import PromptInput from '$lib/components/PromptInput.svelte';
	import Source from '$lib/components/Source.svelte';
	import type { AnswerContent } from '$lib/types';
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';

	let question = "What is Tony's birthday?";
	let answer: AnswerContent[] = [
		{
			type: 'text',
			content: {
				text: `Based on the text messages, it appears Tony Xin has expressed romantic interest in at least one individual named Olivia. This is evidenced by a message where Tony mentions hanging out with Olivia because it is their "2 year", indicating a significant anniversary that suggests a romantic relationship.`
			}
		},
		{
			type: 'message',
			content: {
				citationId: '1',
				messages: [
					{ speaker: 'other', text: 'Yo Olivia and I are having our 2 year this weekend' },
					{ speaker: 'self', text: 'niceeee' }
				]
			}
		},
		{
			type: 'text',
			content: {
				text: `Additionally, there's another instance where Tony mentions that Olivia is staying over, which could imply a close personal relationship.`
			}
		},
		{
			type: 'message',
			content: {
				citationId: '2',
				messages: [
					{ speaker: 'other', text: 'Olivia is staying over imma need the room to myself >:)' },
					{
						speaker: 'self',
						text: 'hahhaha sounds good ksdfkasjdfkajds fkjsdf kajdf jadkf jasdkf jaskdfj aksdfjaksdjf aksdjfa ksdjf kadjf aksdj fkj'
					}
				]
			}
		}
	];

	let input = '';

	let showAnswer = true;
	onMount(() => {
		setTimeout(() => {
			showAnswer = true;
		}, 3000);
	});
</script>

<div class="container h-full w-full mx-auto p-4 flex flex-col gap-4">
	<div class="mb-4 flex gap-1 items-center flex-row">
		<h1 class="text-4xl"><a href="/">BAIB</a></h1>
	</div>

	<div>
		<div class="font-bold text-xs">HEY BAIB,</div>
		<div class="text-2xl">{question}</div>
	</div>

	<div>
		<h4 class="h4 mb-2">Sources</h4>
		<div class="space-y-2">
			<Source type="message" message="my birthday is on oct 10th LMAO" />
			<Source delay={200} type="email" message="Hi this is Tony" />
			<Source delay={400} type="photo" message="Here are some photos:" />
		</div>
	</div>

	{#if showAnswer}
		<div transition:fade>
			<h4 class="h4 mb-2">Answer</h4>
			<AnswerSection {answer} />
		</div>
	{/if}

	<!-- <div class="w-full absolute bottom-0 left-0 p-4">
		<PromptInput bind:input></PromptInput>
	</div> -->
</div>
