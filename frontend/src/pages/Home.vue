<!-- frontend/src/pages/Home.vue -->
<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <h1 class="text-3xl font-bold mb-6">Welcome to 3D Printing Marketplace</h1>

    <!-- Featured Works: show up to 3 random works from any provider with at least one image -->
    <section class="mb-12">
      <h2 class="text-2xl font-semibold mb-4">Featured Works</h2>

      <!-- While loading, display a spinner or message -->
      <div v-if="loading" class="text-gray-500">Loading featured works…</div>

      <!-- If not loading but no works found, display a “none available” message -->
      <div v-else-if="!loading && featuredWorks.length === 0" class="text-gray-500">
        No featured works to display right now.
      </div>

      <!-- Otherwise, render the grid of random works -->
      <div
        v-else
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
      >
        <div
          v-for="work in featuredWorks"
          :key="work.id"
          class="bg-white rounded-lg overflow-hidden shadow"
        >
          <img
            :src="work.image_url"
            :alt="work.title"
            class="w-full h-48 object-cover"
          />
          <div class="p-4">
            <h3 class="text-lg font-medium">{{ work.title }}</h3>
            <p class="text-sm text-gray-600">by {{ work.providerName }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Browse Providers (unchanged) -->
    <section>
      <BrowseProviders />
    </section>
  </div>
</template>

<script>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import BrowseProviders from './BrowseProviders.vue'

export default {
  components: { BrowseProviders },
  setup() {
    const featuredWorks = ref([])
    const loading = ref(true)

    // Simple Fisher–Yates shuffle
    function shuffleArray(arr) {
      for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1))
        ;[arr[i], arr[j]] = [arr[j], arr[i]]
      }
      return arr
    }

    const fetchRandomWorks = async () => {
      try {
        // 1) Fetch all providers (each provider includes a `works` array)
        const res = await axios.get('/api/providers')
        const providers = res.data

        // 2) Filter to only those providers who have at least one work
        const providersWithWorks = providers.filter(
          (p) => Array.isArray(p.works) && p.works.length > 0
        )

        // 3) Flatten all works into one array, attaching providerName to each
        let allWorks = []
        providersWithWorks.forEach((p) => {
          p.works.forEach((w) => {
            allWorks.push({
              id: w.id,
              image_url: w.image_url,
              title: w.title,
              providerName: p.full_name
            })
          })
        })

        // 4) Shuffle and take the first 3 (or fewer if less than 3 exist)
        const shuffled = shuffleArray(allWorks)
        featuredWorks.value = shuffled.slice(0, 3)
      } catch (err) {
        console.error('Error fetching providers/works:', err)
      } finally {
        loading.value = false
      }
    }

    onMounted(fetchRandomWorks)

    return {
      featuredWorks,
      loading
    }
  }
}
</script>

<style scoped>
/* (Optional) Add custom styling here if you like */
</style>
