<template>
  <div class="max-w-3xl mx-auto mt-8">
    <h2 class="text-2xl font-bold mb-4">My Profile</h2>

    <!-- If not logged in -->
    <div v-if="!store.user">
      <p>
        Please
        <router-link to="/login" class="text-primary">log in</router-link>
        first.
      </p>
    </div>

    <!-- If logged in -->
    <div v-else class="bg-white p-6 rounded shadow">
      <!-- Basic User Info -->
      <p class="mb-2"><strong>Name:</strong> {{ store.user.full_name }}</p>
      <p class="mb-2"><strong>Email:</strong> {{ store.user.email }}</p>
      <p class="mb-2"><strong>Role:</strong> {{ store.user.role }}</p>

      <!-- If the user is a provider, show provider fields -->
      <div v-if="store.user.role === 'provider'">
        <hr class="my-4" />
        <h3 class="text-xl font-semibold mb-3">Provider Details</h3>

        <!-- Loading indicator while we fetch the provider profile -->
        <div v-if="loadingProvider" class="text-gray-600">
          <p>Loading provider details…</p>
        </div>

        <!-- Show provider data once loaded -->
        <div v-else-if="providerProfile">
          <p class="mb-2"><strong>Bio:</strong> {{ providerProfile.bio }}</p>
          <p class="mb-2">
            <strong>Equipment:</strong> {{ providerProfile.equipment_specs }}
          </p>
          <p class="mb-2">
            <strong>Pricing:</strong> {{ providerProfile.pricing_info }}
          </p>
          <p class="mb-2"><strong>Location:</strong> {{ providerProfile.location }}</p>
        </div>

        <!-- If fetch failed for some reason -->
        <div v-else class="text-red-500">
          <p>Failed to load provider details.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useMainStore } from "../store";

export default {
  setup() {
    const store = useMainStore();
    const providerProfile = ref(null);
    const loadingProvider = ref(false);

    // Only fetch provider data if the logged‐in user is a provider
    const fetchProviderProfile = async () => {
      if (!store.user || store.user.role !== "provider") {
        return;
      }
      loadingProvider.value = true;
      try {
        // GET /api/providers/<userId> returns { id, full_name, bio, equipment_specs, pricing_info, location, works: [...] }
        const res = await axios.get(`/api/providers/${store.user.id}`);
        providerProfile.value = res.data;
      } catch (err) {
        console.error("Error fetching provider profile:", err);
        providerProfile.value = null;
      } finally {
        loadingProvider.value = false;
      }
    };

    onMounted(fetchProviderProfile);

    return {
      store,
      providerProfile,
      loadingProvider,
    };
  },
};
</script>

<style scoped>
/* Optional: any extra styling here */
</style>
