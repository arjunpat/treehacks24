<script lang="ts">
  import Todo from '$lib/components/Todo.svelte';
  import { fade, scale, slide } from 'svelte/transition';
	import { onMount } from 'svelte';
  import { flip } from 'svelte/animate';
  import { action_items } from '$lib/stores';

  let todos = [{text: "I'm a todo, you have to finish doing the form by the thing", id: '1', completed: false, deadline: new Date()}, {text: "I'm another todo", id: '2', completed: true, deadline: new Date()}, {text: "I'm another todo", id: '3', completed: true, deadline: new Date()}]
  let completedMap = new Map();

  $: todosAmount = todos.length
  $: incompleteTodos = todos.filter((todo) => !todo.completed).length
  $: completedTodos = todos.filter((todo) => todo.completed).length
  $: sortedTodos = todos.sort((a, b) => (a.completed ? 1 : -1) - (b.completed ? 1 : -1))

  function completeTodo(todo: any): void {

    const actions = JSON.parse(JSON.stringify(action_items))
    console.log(actions)
      action_items.forEach((todo: any) => {
        if (todo.name === todo.name) {
          todo.completed = !todo.completed
        }
      })
  }

  let ready = false;
  let new_todos;

  let interval: any;

  const retrieveTodos = () => {
		fetch("https://l6xbzhkc-8000.usw3.devtunnels.ms/actions")
		.then(response => response.json())
		.then(data => {
      console.log($action_items)
      action_items.set(data["action_items"]);
		}).catch(error => {
			console.log(error);
      clearInterval(interval)
			return [];
		});
	}

	onMount(() => {
		ready = true;

    setInterval(retrieveTodos, 1000)
	});
</script>

<main>

  {#if ready}
  <div transition:fade>
  <h1 class="title mb-2">Todos</h1>

  <section class="todos rounded-lg overflow-hidden card">
    {#if todosAmount}
      <ul class="todo-list">
        {#each $action_items as todo (todo.name)}
        <div animate:flip={{ duration: 200 }}>
          <Todo {todo} {completeTodo} {completedMap} />
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