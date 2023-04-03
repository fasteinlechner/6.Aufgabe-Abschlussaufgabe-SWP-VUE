<template>
  <DataTable v-if="values != undefined" class="table table-hover table-striped" width="100%" :data="values">
    <thead>
      <tr>
        <th v-for="c in columns" :key="c">{{ c }}</th>
      </tr>
    </thead>
    <tfoot></tfoot>
  </DataTable>
</template>
  
<script>
import DataTable from "datatables.net-vue3";
import DataTablesLib from "datatables.net-bs5";
import { Services, api_request_parameter } from "@/requests.js";
import Feature from 'ol/Feature'
DataTable.use(DataTablesLib)

export default {
  name: 'Inspect',
  components: {
    DataTable,
  },
  props: {
    feature: Feature,
    country: "",
  },
  computed: {
    props() {
      return this.feature
        ? this.feature.getKeys().filter(key => key !== this.feature.getGeometryName())
        : []
    }
  },
  data() {
    return {
      columns: [],
      values: undefined,
    };
  },
  methods: {
    async load_table() {
      if (this.country != "") {
        console.log(this.country);
        this.columns = ["Name", "Code", "Latitude", "Longitude", "Wikipedia Description"];
        this.values = await api_request_parameter(
          Services.country_data,
          this.country
        );
      }
    },
  },
  mounted(){
    this.load_table();
  }
}
</script>
  
<style scoped>
ul {
  list-style: none;
}
</style>