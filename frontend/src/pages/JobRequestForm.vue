<template>
  <div class="max-w-xl mx-auto mt-6">
    <h2 class="text-2xl font-bold mb-4">
      Request Service from {{ providerName }}
    </h2>

    <form @submit.prevent="submitRequest" class="space-y-4 bg-white p-6 rounded shadow">
      <div>
        <label class="block text-sm font-medium text-gray-700">Title</label>
        <input
          type="text"
          v-model="form.title"
          required
          class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Description</label>
        <textarea
          v-model="form.description"
          rows="4"
          required
          class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary"
        ></textarea>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Model File (optional)</label>
        <input
          type="file"
          @change="onFileChange"
          accept=".stl,.obj,.zip"
          class="mt-1 block w-full text-gray-700"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Initial Message</label>
        <textarea
          v-model="form.initialMessage"
          rows="3"
          placeholder="Include any extra details or questions here"
          class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary"
        ></textarea>
      </div>

      <button
        type="submit"
        class="bg-primary text-white px-4 py-2 rounded hover:bg-primary-dark"
      >
        Send Request
      </button>
      <button
        type="button"
        @click="$router.back()"
        class="ml-2 text-gray-500 hover:text-gray-700"
      >
        Cancel
      </button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useMainStore } from "../store";

export default {
  props: ["providerId"],
  setup(props) {
    const store = useMainStore();
    const form = ref({
      title: "",
      description: "",
      initialMessage: "",
      modelFile: null,
    });
    const providerName = ref("");

    const fetchProviderName = async () => {
      try {
        const res = await axios.get(`/api/providers/${props.providerId}`);
        providerName.value = res.data.full_name;
      } catch (err) {
        console.error("Error fetching provider:", err);
      }
    };

    onMounted(fetchProviderName);

    const onFileChange = (event) => {
      form.value.modelFile = event.target.files[0] || null;
    };

    const submitRequest = async () => {
      try {
        let jobPayload = {
          customer_id: store.user.id,
          provider_id: parseInt(props.providerId),
          title: form.value.title,
          description: form.value.description,
          model_file_url: null,
        };

        const jobRes = await axios.post("/api/job_requests", jobPayload);
        const jobId = jobRes.data.job_id;

        if (form.value.initialMessage.trim() !== "") {
          await axios.post(`/api/job_requests/${jobId}/messages`, {
            sender_id: store.user.id,
            content: form.value.initialMessage.trim(),
          });
        }

        alert("Request sent! Redirecting to chat...");
        return (window.location.href = `/messages/${jobId}`);
      } catch (err) {
        console.error("Error submitting request:", err.response?.data || err);
        alert(err.response?.data?.error || "Failed to create job request.");
      }
    };

    return {
      store,
      form,
      onFileChange,
      submitRequest,
      providerName,
    };
  },
};
</script>

<style scoped>
</style>
