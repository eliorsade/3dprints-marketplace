<!-- frontend/src/pages/Login.vue -->
<template>
  <div class="max-w-md mx-auto mt-8">
    <h2 class="text-2xl font-bold mb-4">Login</h2>
    <form @submit.prevent="submitLogin" class="space-y-4 bg-white p-6 rounded shadow">
      <!-- Email Field -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Email</label>
        <input
          v-model="email"
          type="email"
          required
          placeholder="you@example.com"
          class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary"
        />
      </div>

      <!-- Password Field -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Password</label>
        <input
          v-model="password"
          type="password"
          required
          placeholder="••••••••"
          class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary"
        />
      </div>

      <!-- Submit Button -->
      <div>
        <button
          type="submit"
          class="w-full bg-primary text-white px-4 py-2 rounded hover:bg-primary-dark"
        >
          Login
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useMainStore } from "../store";

export default {
  setup() {
    const store = useMainStore();
    const router = useRouter();

    const email = ref("");
    const password = ref("");

    const submitLogin = async () => {
      try {
        // Call the store.action login(email, password)
        await store.login(email.value.trim(), password.value);

        // On success, redirect to home
        router.push("/");
      } catch (err) {
        // Show an alert with the server’s error message (or a generic one)
        const serverMsg = err.response?.data?.error;
        alert(serverMsg || "Login failed. Please try again.");
      }
    };

    return {
      email,
      password,
      submitLogin,
    };
  },
};
</script>

<style scoped>
/* You can adjust these classes to match your site’s theme */
</style>

