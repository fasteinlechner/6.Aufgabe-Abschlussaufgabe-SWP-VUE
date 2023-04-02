<template>
    <h1>Medaillien pro Land</h1>
    <div class="col-sm">
        <DataTable class="table-hover " :data="CountryData">
            <thead>
                <tr>
                    <th v-for="c in ['Land', 'Team', 'Medailien']">{{ c }}</th>
                </tr>
            </thead>

        </DataTable>
    </div>
</template>
<style>
table {
    width: 100% !important;
}
</style>
<script>
import { VuePlotly } from 'vue3-plotly';
import DataTable from 'datatables.net-vue3'
import DataTablesLib from 'datatables.net-bs5';
import axios from 'axios';

DataTable.use(DataTablesLib);


export default {
    data() {
        return {
            CountryData: []

        }
    },
    methods: {
        async getCountryData() {
            await axios.get(`http://127.0.0.1:5000/medals_per_country`).then(result => this.CountryData= result.data)
        }
    },
    components: {
        VuePlotly,
        DataTable
    },
    mounted() {
        this.getCountryData()
    }
}

</script>

