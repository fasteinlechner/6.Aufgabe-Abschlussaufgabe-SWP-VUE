<template>
    <h1>Sportler von gewähltem Sportereignis</h1>
    <DataTable class="table-hover table-striped" width="100%" :data="athletes">
        <thead>
            <tr>
                <th v-for="m in ['Sportlername', 'Geschlecht', 'Alter', 'Höhe', 'Gewicht']">{{ m }}</th>
            </tr>
        </thead>
    </DataTable>
</template>

<script>
import { VuePlotly } from 'vue3-plotly';
import DataTable from 'datatables.net-vue3'
import DataTablesLib from 'datatables.net-bs5';
import axios from 'axios';

DataTable.use(DataTablesLib);

export default {
    data() {
        return {
            athletes: []
        }
    },
    methods: {
        async getAthletes(){
            await axios.get(`http://127.0.0.1:5000/get_Athletes/${this.currentNoc}/${this.currentEvent}`).then(result => this.athletes = result.data)
        }
    },
    components: {
        VuePlotly,
        DataTable
    },
    props: {
        currentEvent: {
            default: "None",
            required: true
        },
        currentNoc: {
            default: "AUT",
            required: true
        }
    }, watch: {
        currentNoc() {
            this.getAthletes()
        },
        currentEvent(){
            this.getAthletes()
        }
    }, mounted() {
        this.getAthletes()
    }
}

</script>