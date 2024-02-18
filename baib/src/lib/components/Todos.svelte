<script lang="ts">
  import Todo from '$lib/components/Todo.svelte';

  let todos = [{text: "I'm a todo", id: '1', completed: false, deadline: new Date()}]

  $: todosAmount = todos.length
  $: incompleteTodos = todos.filter((todo) => !todo.completed).length
  $: completedTodos = todos.filter((todo) => todo.completed).length

  function completeTodo(id: string): void {
    todos = todos.map((todo) => {
      if (todo.id === id) {
        todo.completed = !todo.completed
      }
      return todo
    })
  }
</script>

<main>
  <h1 class="title">todos</h1>

  <section class="todos">

    {#if todosAmount}
      <ul class="todo-list">
        {#each todos as todo (todo.id)}
          <Todo {todo} {completeTodo} />
        {/each}
      </ul>
    {/if}
  </section>
</main>

<style>
  .title {
    font-size: var(--font-80);
    font-weight: inherit;
    text-align: center;
    color: var(--color-title);
  }

  .todos {
    --width: 500px;
    --todos-bg: hsl(0 0% 98%);
    --todos-text: hsl(220 20% 14%);

    width: var(--width);
    color: var(--todos-text);
    background-color: var(--todos-bg);
    border-radius: var(--radius-base);
    border: 1px solid var(--color-gray-90);
    box-shadow: 0 0 4px var(--shadow-1);
  }

  .todo-list {
    list-style: none;
  }

  .actions {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-8) var(--spacing-16);
    font-size: 0.9rem;
    border-top: 1px solid var(--color-gray-90);
  }

  .actions:before {
    content: '';
    height: 40px;
    position: absolute;
    right: 0;
    bottom: 0;
    left: 0;
    box-shadow: 0 1px 1px hsla(0, 0%, 0%, 0.2), 0 8px 0 -3px hsl(0, 0%, 96%),
      0 9px 1px -3px hsla(0, 0%, 0%, 0.2), 0 16px 0 -6px hsl(0, 0%, 96%),
      0 17px 2px -6px hsla(0, 0%, 0%, 0.2);
    z-index: -1;
  }
</style>