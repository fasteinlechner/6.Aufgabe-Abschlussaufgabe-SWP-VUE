<template>
  <section>
    <select v-model="info" @change="onOptionChange($event)">
      <option disabled value="" selected="selected">Please select one</option>
      <option v-for="c in infos" :value="c" :key="c">
        {{ c["country"] }}
      </option>
    </select>
  </section>
</template>
  
<script>
import { api_request, Services } from "@/requests.js";

export default {
  name: 'Edit',
  props: {
    geojson: Object,
  },
  data() {
    return {
      infos: null,
      info: "",
    };
  },
  methods: {
    async load_infos() {
      this.infos = await api_request(Services.countries)
      console.log(this.infos)
    },
    onOptionChange(event) {
      if (this.info["country"] != undefined) {
        this.$emit("countryChange", this.info["iso3"]);
      }
    },
  },
  mounted() {
    this.load_infos();
  },
  computed: {
    geojsonEdit: {
      set(value) {
        this.$emit('change', JSON.parse(value))
      },
      get() {
        return JSON.stringify(this.geojson, null, ' ')
      }
    }
  }
}
</script>
  
<style scoped>
textarea {
  width: 100%;
  height: 100%;
  resize: none;
}
</style>