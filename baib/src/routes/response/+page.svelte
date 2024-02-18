<script lang="ts">
	import Source from '$lib/components/Source.svelte';

	let question = "What is Tony's birthday?";
	let answer = "Tony's birthday is on October 10th";
</script>

<div class="container h-full mx-auto p-4 flex flex-col gap-4">
	<div>
		<div class="font-bold text-xs">HEY BAIB,</div>
		<div class="text-2xl">{question}</div>
	</div>

	<div>
		<h4 class="h4 mb-2">Sources</h4>
		<div class="space-y-2">
			<Source type="message" message="my birthday is on oct 10th LMAO" />
			<Source type="email" message="Hi this is Tony" />
			<Source type="photo" message="Here are some photos:" />
		</div>
	</div>

	<div>
		<h4 class="h4 mb-2">Answer</h4>
		<div>{answer}</div>
	</div>
</div>
