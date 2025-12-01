<template>
  <div class="card">
    <div class="card-body">
      <div class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th v-for="column in columns" :key="column.key">
                {{ column.label }}
              </th>
            </tr>
          </thead>
          <tbody>
            <slot name="body" :data="data"></slot>
            <tr v-if="!data || data.length === 0">
              <td :colspan="columns.length" class="text-center text-muted">
                {{ emptyMessage }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DataTable',
  props: {
    columns: { type: Array, required: true },
    data: { type: Array, default: () => [] },
    emptyMessage: { type: String, default: 'No data found' }
  }
}
</script>
