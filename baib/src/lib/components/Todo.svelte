<script lang="ts">
	import { fade, slide } from 'svelte/transition';
  import gmailLogo from '../../assets/gmail.png';

	type CompleteTodoType = (id: string) => void;
	type RemoveTodoType = (id: string) => void;
	type EditTodoType = (id: string, newTodo: string) => void;
	type DurationType = number;

	export let todo: any;
	export let completeTodo: CompleteTodoType;

	const toDateString = (date: Date) => {
		let s = '';
		const time = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

		s +=
			time.split(':')[0] +
			':' +
			time.split(':')[1] +
			' ' +
			date.toDateString().split(' ')[0];
		return s;
	};

  let completed = false;
</script>

<li in:slide={{ duration: 200 }} out:fade={{ duration: 200 }} class="relative overflow-hidden">
	<div class={`absolute left-0 top-0 w-full h-full ${completed ?'bg-gray-800/50' : ''} flex justify-end items-center transition-all`}>
		<div>
			<input
				on:change={() => completed = !completed}
				checked={completed}
				color="red"
				id="todo"
				class="checkbox mr-4"
				type="checkbox"
			/>
			<label aria-label="Check todo" class="todo-check" for="todo" />
		</div>
	</div>
	<div class="flex gap-2 justify-between p-4 rounded-none items-center h-full card bg-red-300">
		<div class="gap-1 flex flex-col">
			<div class={`${completed ? 'line-through' : ''} text-sm`}>
				{todo.name}
			</div>
      <div class={`${completed ? 'line-through' : ''} text-xs text-gray-300 mb-1`}>
				{@html todo.brief_description}
			</div>
			<div class="text-gray-500 text-xs flex gap-2 items-center">
        <img alt="icon" src={gmailLogo} class="h-3"/>
				{toDateString(new Date(todo.due_date))}
			</div>
		</div>
    <div class="w-10"></div>
	</div>
</li>

<style>
</style>
