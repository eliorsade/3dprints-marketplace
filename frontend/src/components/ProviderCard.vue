<template>
  <div class="bg-white rounded-xl shadow p-4 hover:shadow-lg transition">
    <!-- Show first work image if available -->
    <div v-if="provider.works && provider.works.length > 0" class="mb-3">
      <img
        :src="provider.works[0].image_url"
        alt="work image"
        class="w-full h-40 object-cover rounded-md"
      />
    </div>

    <h2 class="text-xl font-semibold">{{ provider.full_name }}</h2>
    <p class="text-gray-600">{{ provider.bio }}</p>
    <div class="mt-2 text-sm text-gray-500">
      <span>Equipment: {{ provider.equipment_specs }}</span>
    </div>
    <router-link :to="`/providers/${provider.id}`" class="mt-3 inline-block text-primary">
      View Profile →
    </router-link>
  </div>
</template>

<script>
export default {
  props: ['provider']
}
</script>

<style scoped>
/* (Optional) Add any extra per‐card styling here */
</style>
