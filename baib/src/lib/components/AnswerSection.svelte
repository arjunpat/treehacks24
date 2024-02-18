<script lang="ts">
	import type { AnswerContent } from '$lib/types';

	export let answer: any[] = [];
	export let citations: any = {};
</script>

<div class="space-y-4">
	{#each answer as a}
		{#if a.type === 'text'}
			<div class="text-sm">{a.text}</div>
		{:else if a.type === 'message'}
			<div class="card p-2 text-sm space-y-2 flex flex-col">
				{#each a.messages as id}
					{#if citations[id]?.speaker === 'other'}
						<div class="px-2 py-2 rounded-xl bg-[#3B3B3D] max-w-72 self-start">
							{citations[id]?.text}
						</div>
					{:else if citations[id]?.speaker === 'self'}
						<div class="px-2 py-2 rounded-xl bg-[#1A89FF] max-w-72 self-end">
							{citations[id]?.text}
						</div>
					{/if}
				{/each}
			</div>
		{/if}
	{/each}
</div>
