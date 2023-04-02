<template>
  <div id="app">
    <div class="cell cell-map">
      <MapContainer :geojson="geojson" v-on:select="selected = $event"></MapContainer>
    </div>
    <div class="cell cell-edit">
      <Edit @countryChange="onCountryChange($event)"></Edit>
    </div>
    <div class="cell cell-inspect">
      <Inspect :country = "country"></Inspect>
    </div>
  </div>
</template>

<script>
  import MapContainer from './components/MapContainer.vue'
  import Edit from './components/Edit.vue'
  import Inspect from './components/Inspect.vue'

  export default {
    name: 'App',
    components: {
      Inspect,
      Edit,
      MapContainer
    },
    data: () => ({
      selected: undefined,
      country: "",
      geojson: {
        type: 'Feature',
        properties: {
          name: 'default object',
          quality: 'top'
        },
        geometry: {
          type: 'Polygon',
          coordinates: [
            [
              [
                -27.0703125,
                43.58039085560784
              ],
              [
                -28.125,
                23.563987128451217
              ],
              [
                -10.8984375,
                32.84267363195431
              ],
              [
                -27.0703125,
                43.58039085560784
              ]
            ]
          ]
        }
      }
    }),
    methods: {
      onCountryChange(value) {
        console.log(value);
        this.country = value;
        console.log(this.country);
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
  .cell-map {
    grid-column: 1;
    grid-row-start: 1;
    grid-row-end: 3;
  }
  .cell-edit {
    grid-column: 2;
    grid-row: 1;
  }
  .cell-inspect {
    grid-column: 2;
    grid-row: 2;
  }
</style>