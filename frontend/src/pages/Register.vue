<!-- frontend/src/pages/Register.vue -->
<template>
  <div class="max-w-md mx-auto mt-8">
    <h2 class="text-2xl font-bold mb-4">Register</h2>
    <form @submit.prevent="submitRegister" class="bg-white p-6 rounded shadow space-y-4">
      <!-- Full Name -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Full Name</label>
        <input
          v-model="form.full_name"
          type="text"
          required
          class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary"
        />
      </div>

      <!-- Email -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Email</label>
        <input
          v-model="form.email"
          type="email"
          required
          class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary"
        />
      </div>

      <!-- Password -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Password</label>
        <input
          v-model="form.password"
          type="password"
          required
          class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary"
        />
      </div>

      <!-- Role (customer or provider) -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Role</label>
        <select
          v-model="form.role"
          required
          class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary"
        >
          <option value="customer">Customer</option>
          <option value="provider">Provider</option>
        </select>
      </div>

      <!-- If “Provider” is selected, show extra fields -->
      <div v-if="form.role === 'provider'">
        <h3 class="text-lg font-semibold mt-4 mb-2">Provider Details</h3>

        <!-- Bio (optional) -->
        <div>
          <label class="block text-sm font-medium text-gray-700">Bio</label>
          <textarea
            v-model="form.bio"
            rows="3"
            class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary"
            placeholder="Tell customers about your 3D printing expertise"
          ></textarea>
        </div>

        <!-- Equipment Specs (optional) -->
        <div>
          <label class="block text-sm font-medium text-gray-700">Equipment Specs</label>
          <input
            v-model="form.equipment_specs"
            type="text"
            class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary"
            placeholder="e.g. Prusa i3 MK3S, Formlabs Form 3"
          />
        </div>

        <!-- Per Gram Price -->
        <div>
          <label class="block text-sm font-medium text-gray-700">Price per Gram ($)</label>
          <input
            v-model.number="form.per_gram"
            type="number"
            step="0.01"
            required
            class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary"
          />
        </div>

        <!-- Per Hour Price -->
        <div>
          <label class="block text-sm font-medium text-gray-700">Price per Hour ($)</label>
          <input
            v-model.number="form.per_hour"
            type="number"
            step="0.01"
            required
            class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary"
          />
        </div>

        <!-- Location (optional) -->
        <div>
          <label class="block text-sm font-medium text-gray-700">Location</label>
          <input
            v-model="form.location"
            type="text"
            class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary"
            placeholder="e.g. New York, NY"
          />
        </div>
      </div>

      <!-- Submit Button -->
      <div class="mt-6">
        <button
          type="submit"
          class="w-full bg-primary text-white px-4 py-2 rounded hover:bg-primary-dark"
        >
          Register
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import { ref } from "vue";
import { useRouter } from "vue-router";

export default {
  setup() {
    const router = useRouter();
    const form = ref({
      full_name: "",
      email: "",
      password: "",
      role: "customer",     // default to customer
      bio: "",
      equipment_specs: "",
      per_gram: null,       // numeric
      per_hour: null,       // numeric
      location: "",
    });

    const submitRegister = async () => {
      try {
        // Build the payload. If role is "provider", combine per_gram/per_hour into pricing_info.
        const payload = {
          full_name: form.value.full_name,
          email: form.value.email,
          password: form.value.password,
          role: form.value.role,
        };

        if (form.value.role === "provider") {
          // Add provider-specific fields
          payload.bio = form.value.bio;
          payload.equipment_specs = form.value.equipment_specs;
          payload.pricing_info = {
            per_gram: form.value.per_gram,
            per_hour: form.value.per_hour,
          };
          payload.location = form.value.location;
        }

        // Send to your backend
        await axios.post("/api/register", payload);

        alert("Registered successfully! Please log in.");
        router.push("/login");
      } catch (err) {
        console.error("Registration error:", err.response?.data || err);
        alert(err.response?.data?.error || "Registration failed.");
      }
    };

    return {
      form,
      submitRegister,
    };
  },
};
</script>

<style scoped>
/* Any additional styling you want */
</style>
