<template>
  <nav class="bg-white shadow mb-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo + “Providers” link -->
        <div class="flex">
          <router-link
            to="/"
            class="flex-shrink-0 flex items-center text-xl font-bold text-primary"
          >
            3DPrint
          </router-link>
          <div class="hidden sm:-my-px sm:ml-6 sm:flex sm:space-x-8">
            <router-link
              to="/providers"
              class="border-transparent text-gray-500 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium hover:text-gray-700"
            >
              Providers
            </router-link>
            <!-- “My Jobs” link for providers -->
            <router-link
              v-if="store.user && store.user.role === 'provider'"
              to="/my-jobs"
              class="border-transparent text-gray-500 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium hover:text-gray-700"
            >
              My Jobs
            </router-link>
            <!-- “My Requests” link for customers -->
            <router-link
              v-if="store.user && store.user.role === 'customer'"
              to="/my-requests"
              class="border-transparent text-gray-500 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium hover:text-gray-700"
            >
              My Requests
            </router-link>
          </div>
        </div>

        <!-- Right-hand side: either Login/Register or Profile/Logout -->
        <div class="flex items-center space-x-4">
          <template v-if="!store.user">
            <router-link
              to="/login"
              class="text-gray-500 hover:text-gray-700 px-3 text-sm font-medium"
            >
              Login
            </router-link>
            <router-link
              to="/register"
              class="text-gray-500 hover:text-gray-700 px-3 text-sm font-medium"
            >
              Register
            </router-link>
          </template>

          <template v-else>
            <router-link
              to="/profile"
              class="text-gray-700 hover:text-gray-900 px-3 text-sm font-medium"
            >
              Hello, {{ store.user.full_name }}
            </router-link>
            <button
              @click="handleLogout"
              class="text-red-500 hover:text-red-700 px-3 text-sm font-medium"
            >
              Logout
            </button>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { useMainStore } from "../store"
import { useRouter } from "vue-router"

export default {
  setup() {
    const store = useMainStore()
    const router = useRouter()

    const handleLogout = () => {
      store.logout()
      router.push("/")
    }

    return {
      store,
      handleLogout,
    }
  },
}
</script>
