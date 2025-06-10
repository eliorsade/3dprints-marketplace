import { defineStore } from "pinia";
import axios from "axios";

export const useMainStore = defineStore("main", {
  state: () => ({
    user: null,
    token: null,
    providers: [],
  }),
  actions: {
    init() {
      // 1) Load saved user
      const savedUser = localStorage.getItem("user");
      if (savedUser) {
        this.user = JSON.parse(savedUser);
      }

      // 2) Load saved token (if any) and set axios header
      const savedToken = localStorage.getItem("token");
      if (savedToken) {
        this.token = savedToken;
        axios.defaults.headers.common["Authorization"] = `Bearer ${savedToken}`;
      }
    },

    async login(email, password) {
      // Don’t attach any stray invalid header before you call this.
      // We’ll rely on axios.post(...) directly, no extra headers needed:
      const res = await axios.post("/api/login", { email, password });

      // Save user object
      this.user = res.data;
      localStorage.setItem("user", JSON.stringify(res.data));

      // If your backend also returned a JWT in `res.data.token`, do:
      // this.token = res.data.token;
      // localStorage.setItem("token", res.data.token);
      // axios.defaults.headers.common["Authorization"] = `Bearer ${res.data.token}`;

      return res;
    },

    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem("user");
      localStorage.removeItem("token");
      delete axios.defaults.headers.common["Authorization"];
    },

    async fetchProviders() {
      const res = await axios.get("/api/providers");
      this.providers = res.data;
    },

    async register(data) {
      await axios.post("/api/register", data);
    },
  },
});
