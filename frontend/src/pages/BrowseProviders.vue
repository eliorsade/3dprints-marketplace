<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Browse Providers</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <ProviderCard
        v-for="p in store.providers"
        :key="p.id"
        :provider="p"
      />
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useMainStore } from '../store'
import ProviderCard from '../components/ProviderCard.vue'

export default {
  components: {
    ProviderCard
  },
  setup() {
    const store = useMainStore()

    onMounted(() => {
      store.fetchProviders()
    })

    return {
      store
    }
  }
}
</script>
