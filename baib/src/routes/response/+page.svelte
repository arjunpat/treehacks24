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
	import showdown from 'showdown';

	// const WEBSOCKET_URL = 'wss://l6xbzhkc-8000.usw3.devtunnels.ms';
	const WEBSOCKET_URL = 'ws://localhost:8000';

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

		const citationsSet = new Set();
		const converter = new showdown.Converter();

		let left = data.answer;
		while (left.length > 0) {
			const newline = left.indexOf('\n');
			const start = left.indexOf('{{');
			const end = left.indexOf('}}', start);

			if (newline !== -1 && (start === -1 || newline < start)) {
				answer.push({ type: 'text', text: left.substring(0, newline) });
				left = left.substring(newline + 1);
				continue;
			}

			if (start === -1 || end === -1) break;

			let text = left.substring(0, start);
			const citationNum = parseInt(left.substring(start + 2, end));

			const messages = [];
			for (let i = -1; i <= 1; ++i) {
				if (!citationsSet.has(citationNum + i)) {
					citationsSet.add(citationNum + i);
					messages.push(citationNum + i);
				}
			}

			answer.push({ type: 'text', text: text });
			if (messages.length > 0) {
				answer.push({ type: 'message', messages });
			}

			left = left.substring(end + 2);
			if (left[0] === '.' || left[0] === ',') {
				left = left.substring(1);
			}
		}
		if (left.length > 0) {
			answer.push({ type: 'text', text: left });
		}

		for (let i = 0; i < answer.length; ++i) {
			if (answer[i].type === 'text') {
				answer[i].text = converter.makeHtml(answer[i].text!);
			}
		}
	}

	// Run generate api call
	let messageProgress: Progress = { done: false, text: '' };
	let emailProgress: Progress = { done: false, text: '' };
	let photoProgress: Progress = { done: false, text: '' };

	function initHardcoded() {
		setTimeout(() => {
			emailProgress.text = 'Searching emails...';
			setTimeout(() => {
				emailProgress.done = true;
			}, 5000);
		}, 200);
		setTimeout(() => {
			photoProgress.text = 'Searching photos...';
			setTimeout(() => {
				photoProgress.done = true;
			}, 9500);
		}, 400);
	}

	let socket: WebSocket;
	function init() {
		// 		parseAnswer({
		// 			answer: `Based on the text messages, it seems that Tony has a variety of interests that could inspire great gift ideas. Here are a few suggestions based on the conversations:

		// 1. **Skiing Trip or Gear**: Tony mentioned going skiing and seemed excited about it {{3587}} {{3588}} {{3590}} {{3591}}. A gift related to skiing, such as a trip to Tahoe, ski gear, or accessories, could be a fantastic choice.

		// 2. **Car-Related Items**: There were discussions about car incidents and driving {{779}} {{780}} {{781}} {{268}}. If Tony is into cars, perhaps something car-related, like accessories or a driving experience, could be a good idea.

		// 3. **Fun Foods**: Tony mentioned a "fun food gift" {{662}} {{663}} {{664}}. This suggests he might enjoy unique or gourmet food items. A basket of exotic snacks or a subscription to a gourmet food service could be delightful.

		// 4. **Beach and Surfing Gear**: Tony expressed enthusiasm for Pismo Beach and suggested surfing {{993}} {{994}} {{995}} {{996}}. Beach or surfing-related gifts, such as a surfboard, wetsuit, or beach gear, could be appreciated.

		// 5. **Party or Social Gathering Supplies**: There were mentions of parties and gatherings {{3584}} {{3586}} {{3589}} {{2910}} {{2912}}. Items that enhance social gatherings, like a high-quality portable speaker, party games, or barware, could be great gifts.

		// 6. **Tech or Gadgets**: Given the mention of meeting at the Roblox office {{3257}} {{3258}}, Tony might have an interest in tech or gaming. A new gadget, game, or accessory could be a hit.

		// Remember, the best gifts are often those that show you've paid attention to what the recipient loves and enjoys. These suggestions are based on the conversations you've had with Tony, so they should hopefully resonate with his interests!`,
		// 			citations: {
		// 				3584: { speaker: 'other', text: 'Invite them to our rager on the 20th' },
		// 				3586: { speaker: 'self', text: 'Haha good one' },
		// 				3587: { speaker: 'self', text: 'I kinda want to go skiing on the 19th' },
		// 				3588: { speaker: 'self', text: 'Tahoe just dumped snow and the weekends will be crowded' },
		// 				3589: { speaker: 'self', text: "Liked “That's hype”" },
		// 				3590: { speaker: 'other', text: 'Lets run it' },
		// 				3591: { speaker: 'other', text: 'Tahoe mad dumpy rn' },
		// 				3583: { speaker: 'other', text: "That's the 15th right" },
		// 				662: { speaker: 'other', text: 'Just a fun food gift' },
		// 				663: { speaker: 'other', text: 'U should try it' },
		// 				664: { speaker: 'other', text: 'I want to know what it tastes like' },
		// 				665: { speaker: 'self', text: 'Ok that is what I thought ' },
		// 				3256: { speaker: 'self', text: 'I think I had some minor food poisoning or something idk' },
		// 				3257: { speaker: 'self', text: 'I can go whenever u want to leave work ' },
		// 				3258: { speaker: 'self', text: 'And meet u at the Roblox office' },
		// 				3259: { speaker: 'other', text: "Lol I don't have my car tnr" },
		// 				267: { speaker: 'other', text: 'U GUYS CAN MAKE A GUEST APPEARANCE' },
		// 				268: { speaker: 'other', text: 'So yeah I have to drive to school' },
		// 				269: { speaker: 'self', text: "LOL that's very hype" },
		// 				778: { speaker: 'self', text: 'they have not been so great' },
		// 				779: { speaker: 'self', text: 'Izzy and I have faced two highly stressful car incidents' },
		// 				780: {
		// 					speaker: 'self',
		// 					text: 'One has resulted in a crash and pretty decent damage to my car'
		// 				},
		// 				781: {
		// 					speaker: 'self',
		// 					text: 'And the other included towing and a stressful journey to collect $378 from ATMs within 30 minutes'
		// 				},
		// 				782: { speaker: 'self', text: 'So like' },
		// 				2909: { speaker: 'self', text: 'But may be down to come for a bit sober' },
		// 				2910: { speaker: 'other', text: "Let's run it" },
		// 				2911: { speaker: 'other', text: 'Wait what time' },
		// 				2912: { speaker: 'other', text: 'Might be hanging out w Olivia' },
		// 				992: { speaker: 'self', text: 'Also we want to go atving' },
		// 				993: { speaker: 'other', text: 'Oh damn' },
		// 				994: { speaker: 'other', text: 'Pismo beach is pretty hype' },
		// 				995: { speaker: 'other', text: 'Wait I passed it when we came here' },
		// 				996: { speaker: 'other', text: 'U guys should go surfing' }
		// 			}
		// 		});
		// 		console.log(answer);
		// 		return;

		input = '';

		if ($query.length === 0) {
			goto('/');
			return;
		}

		showAnswer = false;
		messageProgress = { done: false, text: '' };

		emailProgress = { done: false, text: '' };
		photoProgress = { done: false, text: '' };
		initHardcoded();

		socket?.close();
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
					messageProgress.text = `Analyzing content from ${name}...`;
				} else if (data.progress.includes('query_text_messages_from_contact')) {
					const matches = [...data.progress.matchAll(insideQuoteRegex)];
					const keywords = matches[1][1];
					messageProgress.text = `Looking for content related to ${keywords}...`;
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
				<Source delay={200} type="email" progress={emailProgress} />
				<Source delay={400} type="photo" progress={photoProgress} />
			{/key}
		</div>
	</div>

	{#if showAnswer}
		<div transition:fade>
			<h4 class="h4 mb-2">Answer</h4>
			<ImageSection text={$query}></ImageSection>
			<AnswerSection {answer} bind:citations />
		</div>
	{/if}

	<div class="w-full fixed bottom-0 left-0 p-4">
		<PromptInput bind:input on:submit={submit}></PromptInput>
	</div>
</div>
