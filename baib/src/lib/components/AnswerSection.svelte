<script lang="ts">
	import type { AnswerContent } from '$lib/types';

	export let answer: AnswerContent[] = [];
</script>

<div class="space-y-4">
	{#each answer as a}
		{#if a.type === 'text'}
			<div class="text-sm">{a.content.text}</div>
		{:else if a.type === 'message'}
			<div class="card p-2 text-sm space-y-2 flex flex-col">
				{#each a.content.messages as message}
					{#if message.speaker === 'other'}
						<div class="px-2 py-2 rounded-xl bg-[#3B3B3D] max-w-72">
							{message.text}
						</div>
					{:else if message.speaker === 'self'}
						<div class="px-2 py-2 rounded-xl bg-[#1A89FF] max-w-72 self-end">
							{message.text}
						</div>
					{/if}
				{/each}
			</div>
		{/if}
	{/each}
</div>
