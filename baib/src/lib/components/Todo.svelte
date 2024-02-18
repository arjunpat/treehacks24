<script lang="ts">
	import { fade, slide } from 'svelte/transition';

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
			todo.deadline.toDateString().split(' ')[0];
		return s;
	};
</script>

<li in:slide={{ duration: 200 }} out:fade={{ duration: 200 }} class="relative overflow-hidden">
	<div class={`absolute left-0 top-0 w-full h-full ${todo.completed ?'bg-gray-800/50' : ''} flex justify-end items-center transition-all`}>
		<div>
			<input
				on:change={() => completeTodo(todo.id)}
				checked={todo.completed}
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
			<div class={`${todo.completed ? 'line-through' : ''} text-sm`}>
				{todo.text}
			</div>
			<div class="text-gray-500 text-xs">
				{toDateString(todo.deadline)}
			</div>
		</div>
    <div class="w-10"></div>
	</div>
</li>

<style>
</style>
