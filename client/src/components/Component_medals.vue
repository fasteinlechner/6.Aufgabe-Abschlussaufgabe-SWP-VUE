<template>
    <h1>Medailienübersicht</h1>
    <div class="row" style="padding:20px">
        <div class="col-sm">
            <VuePlotly :layout="layout2" :data="medallsbySeason"></VuePlotly>
        </div>
    </div>
    <div class ="col-sm">
        <VuePlotly :layout="layout1" :data="medalls"></VuePlotly>
    </div>
    <div class="row" style="padding:20px">
        <div class="col-sm">
            <DataTable class="table-hover table-striped" width="100%" :data="medallsData">
                <thead>
                    <tr>
                        <th v-for="m in ['Medailien', 'Anzahl']">{{ m }}</th>
                    </tr>
                </thead>
            </DataTable>
        </div>
    </div>
    
  
       
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
            medalls: [{ x: [] }],
            medallsData: [],
            medallsbySex: [],
            medallsbySeason: [],
            layout1: { title: "Medailien der Nation" },
            layout2: { title: "Goldmedailien"}
        }
    },
    methods: {
        async getMedalls() {
            await axios.get(`http://127.0.0.1:5000/medals2/${this.currentNoc}`)
                .then(result => this.medalls = result.data)
        },
        async getMedallsData() {
            await axios.get(`http://127.0.0.1:5000/medals/${this.currentNoc}`)
                .then(result => this.medallsData = result.data)
        },
        async getMedallsbySex() {
            await axios.get(`http://127.0.0.1:5000/count_by_sex2`)
                .then(result => this.medallsbySex = result.data)
        },
        async getMedallsbySeason() {
            await axios.get(`http://127.0.0.1:5000//winner/${this.currentNoc}`)
                .then(result => this.medallsbySeason = result.data)
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
            this.getMedalls()

            this.getMedallsData()

            this.getMedallsbySex()

            this.getMedallsbySeason()
        }
    }, mounted() {
        this.getMedalls()

        this.getMedallsData()

        this.getMedallsbySex()

        this.getMedallsbySeason()
    }

}

</script>