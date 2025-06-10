<!-- frontend/src/pages/ProviderProfile.vue -->
<template>
  <div class="max-w-3xl mx-auto mt-6">
    <!-- Provider’s Basic Info -->
    <h2 class="text-2xl font-bold mb-4">{{ provider.full_name }}</h2>
    <p class="mb-2"><strong>Bio:</strong> {{ provider.bio }}</p>
    <p class="mb-2"><strong>Equipment:</strong> {{ provider.equipment_specs }}</p>

    <!-- 👉 This was changed from showing raw JSON -->
    <p class="mb-2">
      <strong>Pricing:</strong>
      <span v-if="provider.pricing_info">
        ${{ provider.pricing_info.per_hour }} / hour • ${{ provider.pricing_info.per_gram }} / gram
      </span>
      <span v-else class="text-gray-500">(No pricing info)</span>
    </p>

    <p class="mb-2"><strong>Location:</strong> {{ provider.location }}</p>

    <!-- “Add Image” Button (visible if provider or admin) -->
    <div
      v-if="store.user && (store.user.id === provider.id || store.user.role === 'admin')"
      class="mt-6 mb-4"
    >
      <button
        @click="triggerFileSelect"
        class="bg-primary text-white px-4 py-2 rounded hover:bg-green-600"
      >
        Add Image
      </button>
      <input
        type="file"
        ref="fileInput"
        @change="uploadImage"
        accept="image/*"
        class="hidden"
      />
    </div>

    <!-- Gallery of Works -->
    <h3 class="text-xl font-semibold mt-6 mb-3">Gallery of Works</h3>
    <div
      v-if="provider.works && provider.works.length > 0"
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"
    >
      <div
        v-for="w in works"
        :key="w.id"
        class="bg-white p-2 rounded shadow relative group"
      >
        <img
          :src="w.image_url"
          alt="work"
          class="w-full h-32 object-cover rounded-md"
        />
        <p class="mt-2 text-sm text-gray-700">{{ w.title }}</p>

        <!-- Delete button (visible if provider or admin) -->
        <button
          v-if="store.user && (store.user.id === provider.id || store.user.role === 'admin')"
          @click="deleteWork(w.id)"
          class="absolute top-1 right-1 bg-red-600 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition"
          title="Delete Image"
        >
          ✕
        </button>
      </div>
    </div>
    <div v-else class="text-gray-600">
      <p>No works to display yet.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useMainStore } from "../store";
import { useRouter } from "vue-router";

export default {
  props: ["id"],
  setup(props) {
    const store = useMainStore();
    const router = useRouter();
    const provider = ref({
      id: null,
      full_name: "",
      bio: "",
      equipment_specs: "",
      pricing_info: null,      // pricing_info should be an object
      location: "",
      works: [],
    });
    const works = ref([]);
    const fileInput = ref(null);

    const fetchProvider = async () => {
      try {
        const res = await axios.get(`/api/providers/${props.id}`);
        provider.value = res.data;
        works.value = res.data.works || [];
      } catch (err) {
        console.error("Error fetching provider:", err);
      }
    };

    function triggerFileSelect() {
      fileInput.value.click();
    }

    async function uploadImage(event) {
      const file = event.target.files[0];
      if (!file) return;
      const formData = new FormData();
      formData.append("image", file);
      formData.append("user_id", store.user.id);

      try {
        const res = await axios.post(
          `/api/providers/${props.id}/works`,
          formData,
          { headers: { "Content-Type": "multipart/form-data" } }
        );
        works.value.push(res.data);
        fileInput.value.value = "";
      } catch (err) {
        console.error("Upload failed:", err.response?.data || err);
        alert(err.response?.data?.error || "Failed to upload image.");
      }
    }

    async function deleteWork(workId) {
      if (!confirm("Are you sure you want to delete this image?")) return;
      try {
        await axios.delete(
          `/api/providers/${props.id}/works/${workId}?user_id=${store.user.id}`
        );
        works.value = works.value.filter((w) => w.id !== workId);
      } catch (err) {
        console.error("Delete failed:", err.response?.data || err);
        alert(err.response?.data?.error || "Failed to delete image.");
      }
    }

    onMounted(fetchProvider);

    return {
      store,
      provider,
      works,
      fileInput,
      triggerFileSelect,
      uploadImage,
      deleteWork,
    };
  },
};
</script>

<style scoped>
button[title="Delete Image"] {
  font-size: 0.75rem;
  line-height: 1;
}
</style>
