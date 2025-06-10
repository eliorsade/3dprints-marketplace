<template>
  <div class="max-w-3xl mx-auto mt-6">
    <h2 class="text-2xl font-bold mb-4">Conversation with {{ providerName }}</h2>

    <!-- Messages List -->
    <div class="space-y-2 mb-4 max-h-96 overflow-y-auto bg-white p-4 rounded shadow">
      <div
        v-for="msg in messages"
        :key="msg.id"
        class="p-2 rounded flex"
        :class="{
          'bg-blue-100 justify-end': msg.sender_id === store.user.id,
          'bg-gray-100 justify-start': msg.sender_id !== store.user.id
        }"
      >
        <div>
          <p class="text-sm">{{ msg.content }}</p>
          <p class="text-xs text-gray-500 mt-1">{{ formatDate(msg.created_at) }}</p>
        </div>
      </div>
    </div>

    <!-- Input for new message -->
    <div class="flex space-x-2 mb-6">
      <input
        v-model="newMessage"
        @keyup.enter="sendMessage"
        type="text"
        placeholder="Type your message..."
        class="flex-grow border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary px-3 py-1"
      />
      <button
        @click="sendMessage"
        class="bg-primary text-white px-4 py-2 rounded hover:bg-primary-dark"
      >
        Send
      </button>
    </div>

    <!-- Back button -->
    <button
      @click="$router.back()"
      class="text-gray-500 hover:text-gray-700"
    >
      ← Back
    </button>
  </div>
</template>

<script>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useMainStore } from "../store";

export default {
  props: ["jobId"],
  setup(props) {
    const store = useMainStore();
    const messages = ref([]);
    const newMessage = ref("");
    const providerName = ref("");

    const fetchJobAndMessages = async () => {
      try {
        const jobRes = await axios.get(`/api/job_requests/${props.jobId}`);
        const job = jobRes.data;
        const profRes = await axios.get(`/api/providers/${job.provider_id}`);
        providerName.value = profRes.data.full_name;

        const msgRes = await axios.get(`/api/job_requests/${props.jobId}/messages`);
        messages.value = msgRes.data;
      } catch (err) {
        console.error("Error fetching job or messages:", err);
      }
    };

    const sendMessage = async () => {
      if (!newMessage.value.trim()) return;
      try {
        const payload = {
          sender_id: store.user.id,
          content: newMessage.value.trim(),
        };
        await axios.post(`/api/job_requests/${props.jobId}/messages`, payload);
        messages.value.push({
          id: Date.now(),
          sender_id: store.user.id,
          content: newMessage.value.trim(),
          created_at: new Date().toISOString(),
        });
        newMessage.value = "";
      } catch (err) {
        console.error("Send message failed:", err);
        alert("Failed to send message.");
      }
    };

    function formatDate(iso) {
      return new Date(iso).toLocaleString();
    }

    onMounted(fetchJobAndMessages);

    return {
      store,
      messages,
      newMessage,
      providerName,
      sendMessage,
      formatDate,
    };
  },
};
</script>

<style scoped>
.bg-blue-100 {
  background-color: #ebf8ff;
}
.bg-gray-100 {
  background-color: #f7fafc;
}
.justify-end {
  justify-content: flex-end;
}
.justify-start {
  justify-content: flex-start;
}
</style>

