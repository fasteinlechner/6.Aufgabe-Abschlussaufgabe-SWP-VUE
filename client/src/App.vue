<template>
  <div id="app">
    <div class="cell cell-map">
      <MapContainer :geojson="geojson" v-on:select="selected = $event"></MapContainer>
    </div>
    <div class="cell1 cell-edit">
      <Edit @countryChange="onCountryChange($event)"></Edit>
    </div>
    <div class="cell1 cell-inspect">
      <Inspect v-if="country!= undefined" :country = "country"></Inspect>
    </div>
  </div>
</template>

<script>
  import MapContainer from './components/MapContainer.vue'
  import Edit from './components/Edit.vue'
  import Inspect from './components/Inspect.vue'
  import { Services, api_request_parameter } from "@/requests.js";

  export default {
    name: 'App',
    components: {
      Inspect,
      Edit,
      MapContainer
    },
    data: () => ({
      selected: undefined,
      country: undefined,
      values: undefined,
      geojson: {
        type: 'Feature',
        properties: {
          name: 'default object',
          quality: 'top'
        },
        geometry: {
          type: 'Point',
          coordinates: [16.373, 48.2083], 
            
        }
      }
    }),
    methods: {
      async onCountryChange(value) {
        if (value != this.country) {
          console.log(value);
          this.country = value;
          this.values = await api_request_parameter(Services.country_data,this.country);
          
          this.geojson.geometry.coordinates = [Number(this.values[0][3]), Number(this.values[0][2])];
          
        }
      },
    }
  }
</script>

<style>
  html, body {
    margin: 0;
  }
  #MyApp {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    height: 100vh;
    box-sizing: border-box;
    width: 100%;
  }

  #app {
    height: 100%;
    width: 100%;
    display: grid;
  }

  .cell {
    border-radius: 4px;
    background-color: lightgrey;
    height: 100%;
  }

  .cell1{
    border-radius: 4px;
    background-color: lightgrey;
    height: 100%;
    width: 100%;
  }

  .cell-map {
    grid-column-start: 1;
    grid-column-end: 4;
    grid-row-start: 1;
    grid-row-end: 3;
    width: 100%;
  }
  .cell-edit {
    grid-column: 4;
    grid-row: 1;
    width: 100%;
  }
  .cell-inspect {
    grid-column: 4;
    grid-row: 2;
    width: 100%;
  }
</style>