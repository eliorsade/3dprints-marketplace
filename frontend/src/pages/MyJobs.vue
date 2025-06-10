<template>
  <div class="max-w-3xl mx-auto mt-6">
    <h2 class="text-2xl font-bold mb-4">My Job Requests</h2>

    <div v-if="jobs.length === 0" class="text-gray-600">
      <p>No job requests at the moment.</p>
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="job in jobs"
        :key="job.id"
        class="bg-white p-4 rounded shadow flex justify-between items-center"
      >
        <div>
          <p class="font-medium">Title: {{ job.title }}</p>
          <p class="text-sm text-gray-600">
            Customer ID: {{ job.customer_id }} |
            Created: {{ formatDate(job.created_at) }} |
            Status: {{ job.status }}
          </p>
          <p class="mt-1 text-gray-700">{{ job.description }}</p>
        </div>
        <div>
          <router-link
            :to="{ name: 'MessageWindow', params: { jobId: job.id } }"
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
    const jobs = ref([]);

    const fetchMyJobs = async () => {
      try {
        const res = await axios.get(
          `/api/job_requests/provider/${store.user.id}`
        );
        jobs.value = res.data;
      } catch (err) {
        console.error("Error fetching my jobs:", err);
      }
    };

    function formatDate(iso) {
      return new Date(iso).toLocaleString();
    }

    onMounted(() => {
      if (store.user && store.user.role === "provider") {
        fetchMyJobs();
      }
    });

    return {
      jobs,
      formatDate,
    };
  },
};
</script>

<style scoped>
</style>

