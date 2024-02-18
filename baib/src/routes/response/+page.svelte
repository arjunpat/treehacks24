<script lang="ts">
	import { goto } from '$app/navigation';
	import AnswerSection from '$lib/components/AnswerSection.svelte';
	import PromptInput from '$lib/components/PromptInput.svelte';
	import ImageSection from '$lib/components/ImageSection.svelte';
	import Source from '$lib/components/Source.svelte';
	import { query } from '$lib/stores';
	import type { AnswerContent, Progress } from '$lib/types';
	import { onDestroy, onMount } from 'svelte';
	import { fade } from 'svelte/transition';

	// const WEBSOCKET_URL = 'wss://l6xbzhkc-8000.usw3.devtunnels.ms';
	const WEBSOCKET_URL = 'ws://localhost:8000';

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

	let showAnswer = false;
	// onMount(() => {
	// 	setTimeout(() => {
	// 		showAnswer = true;
	// 	}, 3000);
	// });

	// Run generate api call
	let messageProgress: Progress = { done: false, text: '' };

	let socket: WebSocket;
	function init() {
		input = '';

		if ($query.length === 0) {
			goto('/');
			return;
		}

		showAnswer = false;
		messageProgress = { done: false, text: '' };

		socket = new WebSocket(`${WEBSOCKET_URL}/generate`);
		socket.onopen = (event) => {
			socket.send(JSON.stringify({ question: e.detail.text }));
		};
		socket.onmessage = (event) => {
			const data = JSON.parse(event.data);
			console.log('message: ', data);
			if (data.status === 'progress') {
				const insideQuoteRegex = /"(.+?)"/g;
				if (data.progress.includes('query_contacts_by_name')) {
					const matches = [...data.progress.matchAll(insideQuoteRegex)];
					const name = matches[0][1];
					messageProgress.text = `Analyzing texts from ${name}...`;
				} else if (data.progress.includes('query_text_messages_from_contact')) {
					const matches = [...data.progress.matchAll(insideQuoteRegex)];
					const keywords = matches[1][1];
					messageProgress.text = `Looking for texts related to ${keywords}...`;
				}
			} else if (data.status === 'success') {
				messageProgress.done = true;
				showAnswer = true;
			}
		};
	}
	onMount(() => {
		init();
	});

	onDestroy(() => {
		socket?.close();
	});

	let input = '';
	function submit(event: any) {
		query.set(event.detail.text);
		init();
	}
</script>

<div class="container h-full w-full mx-auto p-4 flex flex-col gap-4 mb-16">
	<div class="mb-4 flex gap-1 items-center flex-row">
		<h1 class="text-4xl"><a href="/">BAIB</a></h1>
	</div>

	<div>
		<div class="font-bold text-xs">HEY BAIB,</div>
		<div class="text-2xl">{$query}</div>
	</div>

	<div>
		<h4 class="h4 mb-2">Sources</h4>
		<div class="space-y-2">
			{#key $query}
				<Source type="message" progress={messageProgress} />
				<!-- <Source delay={200} type="email" message="Hi this is Tony" />
			<Source delay={400} type="photo" message="Here are some photos:" /> -->
			{/key}
		</div>
	</div>

	{#if showAnswer}
		<div transition:fade>
			<h4 class="h4 mb-2">Answer</h4>
			<ImageSection text={$query}></ImageSection>
			<AnswerSection {answer} />
		</div>
	{/if}

	<div class="w-full fixed bottom-0 left-0 p-4">
		<PromptInput bind:input on:submit={submit}></PromptInput>
	</div>
</div>
