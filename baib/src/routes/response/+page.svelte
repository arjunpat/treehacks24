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

	const WEBSOCKET_URL = 'wss://l6xbzhkc-8000.usw3.devtunnels.ms';
	// const WEBSOCKET_URL = 'ws://localhost:8000';

	let citations = {
		1: { speaker: 'other', text: 'Yo olivia and i are having our 2 year this weekend' },
		2: { speaker: 'other', text: 'hahah' },
		3: { speaker: 'self', text: 'niceeeee' }
	};
	let answer = [
		{
			type: 'text',
			text: `Based on the text messages, it appears Tony Xin has expressed romantic interest in at least one individual named Olivia. This is evidenced by a message where Tony mentions hanging out with Olivia because it is their "2 year", indicating a significant anniversary that suggests a romantic relationship.`
		},
		{
			type: 'message',
			messages: [1, 2, 3]
		}
	];

	let showAnswer = false;
	// onMount(() => {
	// 	setTimeout(() => {
	// 		showAnswer = true;
	// 	}, 3000);
	// });

	function parseAnswer(data: { answer: string; citations: any }) {
		answer = [];
		citations = data.citations;

		let left = data.answer;
		while (left.length > 0) {
			const start = left.indexOf('{{');
			const end = left.indexOf('}}', start);
			if (start === -1 || end === -1) break;

			const text = left.substring(0, start);
			const citationNum = parseInt(left.substring(start + 2, end));

			answer.push({ type: 'text', text: text });
			answer.push({ type: 'message', messages: [citationNum - 1, citationNum, citationNum + 1] });

			left = left.substring(end + 2);
		}
		if (left.length > 0) {
			answer.push({ type: 'text', text: left });
		}
	}

	// Run generate api call
	let messageProgress: Progress = { done: false, text: '' };

	let socket: WebSocket;
	function init() {
		// parseAnswer({
		// 	answer: `Tony Xin's birthday is on October 22nd. This information comes from a text message sent on October 22, 2021, at 08:22 AM, where the sender wishes Tony Xin a "big boy happy birthday" and mentions seeing him later that day {{1457}}. This message clearly indicates that October 22nd is the day Tony Xin celebrates his birthday.`,
		// 	citations: {
		// 		1456: { speaker: 'other', text: 'Have not done extra credit' },
		// 		1457: { speaker: 'self', text: 'TONY XIN big boy happy birthday see you later today ' },
		// 		1458: { speaker: 'other', text: 'THANK U ARJUN PAT' }
		// 	}
		// });
		// console.log(answer);
		// return;
		input = '';

		if ($query.length === 0) {
			goto('/');
			return;
		}

		showAnswer = false;
		messageProgress = { done: false, text: '' };

		socket = new WebSocket(`${WEBSOCKET_URL}/generate`);
		socket.onopen = (event) => {
			socket.send(JSON.stringify({ question: $query }));
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
				console.log('answer: ', data);
				messageProgress.done = true;
				showAnswer = true;
				parseAnswer(data);
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
			<AnswerSection {answer} {citations} />
		</div>
	{/if}

	<div class="w-full fixed bottom-0 left-0 p-4">
		<PromptInput bind:input on:submit={submit}></PromptInput>
	</div>
</div>
