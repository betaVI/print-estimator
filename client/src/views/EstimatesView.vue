<template>
    <div class="container">
        <ListView title="Estimates" :isloading="estimatesLoading" @onaddclick="$router.push({ name: 'estimate' })">
            <template #headers>
                <tr>
                    <th scope="col">Name</th>
                    <th scope="col">Prints</th>
                    <th scope="col">Total Grams</th>
                    <th scope="col">Total Print Time</th>
                    <th scope="col">Colors</th>
                    <th scope="col">Total Post</th>
                    <th scope="col">Cost</th>
                    <th scope="col">Min Price</th>
                    <th></th>
                </tr>
            </template>
            <template #default>
                <tr v-if="estimates.length == 0" class="text-center">
                    <td colspan="9">No Records to display</td>
                </tr>
                <tr v-else v-for="(estimate, index) in estimates" :keys="index">
                    <td>{{ estimate.name }}</td>
                    <td>{{ estimate.totalprints }}</td>
                    <td>{{ estimate.totalgrams }}</td>
                    <td>{{ formatPrintTime(estimate.totalprinttime) }}</td>
                    <td>{{ estimate.totalcolors }}</td>
                    <td>{{ estimate.totalpostprocessing }}</td>
                    <td>{{ '$' + estimate.totalcostlabor.toFixed(2) }}</td>
                    <td>{{ '$' + estimate.minimumprice.toFixed(2) }}</td>
                    <td class="text-end">
                        <button type="button" class="btn btn-outline-warning btn-sm" @click="$router.push({ name: 'estimate', params: { id: estimate.id }})">
                            <i class="bi bi-printer"></i>
                        </button>
                        <button type="button" class="btn btn-outline-info btn-sm mx-sm-1" @click="$router.push({ name: 'estimate', params: { id: estimate.id }})">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button type="button" class="btn btn-outline-danger btn-sm" @click="deleteEstimate(estimate.id)">
                            <i class="bi bi-trash"></i>
                        </button>
                    </td>
                </tr>
            </template>
        </ListView>
    </div>
</template>

<script>
import { getEstimates, deleteEstimate, getSettings } from '@/estimater-api';

export default{
    data(){
        return{
            settings: {},
            estimatesLoading: true,
            estimates: [],
        }
    },
    mounted(){
        this.getSettings();
        this.getEstimates();
    },
    methods: {
        async getSettings(){
            let response = await getSettings();
            if (response.success){
                this.settings = response.settings;
            }
            else{
                console.log('Settings failure: ' + response.error);
            }
        },
        async getEstimates(){
            this.estimatesLoading = true;
            let response = await getEstimates();
            if (response.success){
                this.estimates = response.estimates;
            }
            else{
                console.log('Estimates error: ' + response.error);
            }
            this.estimatesLoading = false;
        },
        async deleteEstimate(id){
            if (confirm('This action is permanent. Are you sure you want to continue?')){
                let response = await deleteEstimate(id);
                if (!response.success){
                    console.log(response.error);
                }
                this.getEstimates();
            }
        },
        formatPrintTime(totaltime){
            let hoursinday = 24;
            if (this.settings.printablehours>0){
                hoursinday = this.settings.printablehours;
            }
            let days = (totaltime / (60 * hoursinday)).toFixed(0);
            let hours = (totaltime / 60).toFixed(0);
            return `${days}d (${hours}h)`;
        },
        formatPrintTimeDays(totaltime){
            return days;
        }
    }
}
</script>