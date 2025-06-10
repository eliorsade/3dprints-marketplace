<template>
  <div class="max-w-3xl mx-auto mt-6">
    <h2 class="text-2xl font-bold mb-4">My Requests</h2>

    <div v-if="requests.length === 0" class="text-gray-600">
      <p>You haven’t made any service requests yet.</p>
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="r in requests"
        :key="r.id"
        class="bg-white p-4 rounded shadow flex justify-between items-center"
      >
        <div>
          <p class="font-medium">Title: {{ r.title }}</p>
          <p class="text-sm text-gray-600">
            Provider ID: {{ r.provider_id }} |
            Created: {{ formatDate(r.created_at) }} |
            Status: {{ r.status }}
          </p>
          <p class="mt-1 text-gray-700">{{ r.description }}</p>
        </div>
        <div>
          <router-link
            :to="{ name: 'MessageWindow', params: { jobId: r.id } }"
            class="bg-primary text-white px-3 py-1 rounded hover:bg-primary-dark text-sm"
          >
            View Conversation
          </router-link>
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
    const requests = ref([]);

    const fetchMyRequests = async () => {
      try {
        const res = await axios.get(
          `/api/job_requests/customer/${store.user.id}`
        );
        requests.value = res.data;
      } catch (err) {
        console.error("Error fetching my requests:", err);
      }
    };

    function formatDate(iso) {
      return new Date(iso).toLocaleString();
    }

    onMounted(() => {
      if (store.user && store.user.role === "customer") {
        fetchMyRequests();
      }
    });

    return {
      requests,
      formatDate,
    };
  },
};
</script>

<style scoped>
</style>
