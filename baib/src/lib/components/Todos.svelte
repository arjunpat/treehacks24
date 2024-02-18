<script lang="ts">
  import Todo from '$lib/components/Todo.svelte';
  import { fade, scale, slide } from 'svelte/transition';
	import { onMount } from 'svelte';
  import { flip } from 'svelte/animate';

  let todos = [{text: "I'm a todo, you have to finish doing the form by the thing", id: '1', completed: false, deadline: new Date()}, {text: "I'm another todo", id: '2', completed: true, deadline: new Date()}, {text: "I'm another todo", id: '3', completed: true, deadline: new Date()}]

  $: todosAmount = todos.length
  $: incompleteTodos = todos.filter((todo) => !todo.completed).length
  $: completedTodos = todos.filter((todo) => todo.completed).length
  $: sortedTodos = todos.sort((a, b) => (a.completed ? 1 : -1) - (b.completed ? 1 : -1))

  function completeTodo(id: string): void {
    todos = todos.map((todo) => {
      if (todo.id === id) {
        todo.completed = !todo.completed
      }
      return todo
    })
  }

  let ready = false;

	onMount(() => {
		ready = true;
	});
</script>

<main>

  {#if ready}
  <div transition:fade>
  <h1 class="title mb-2">Todos</h1>

  <section class="todos rounded-lg overflow-hidden card">
    {#if todosAmount}
      <ul class="todo-list">
        {#each todos as todo (todo.id)}
        <div animate:flip={{ duration: 200 }}>
          <Todo {todo} {completeTodo}  />
        </div>
        {/each}
      </ul>
    {/if}
  </section>
</div>
  {/if}
</main>

<style>

</style>