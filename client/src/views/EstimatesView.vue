<template>
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
</template>

<script>
import { sendRequest } from '@/utilities';

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
            try{
                let data = await sendRequest('/api/settings', 'GET');
                this.settings = data.settings;
            }catch(error){
                console.log(error);
            }
        },
        async getEstimates(){
            this.estimatesLoading = true;
            try{
                let data = await sendRequest('/api/estimates', 'GET');
                this.estimates = data.estimates;
            }
            catch(error){
                console.log(error);
            }
            this.estimatesLoading = false;
        },
        async deleteEstimate(id){
            this.estimatesLoading = true;
            try{
                let data = await sendRequest('/api/estimates/' + id,'DELETE');
                if (!data.success){
                    console.log(error);
                }
                this.getEstimates()
            }
            catch(error){
                console.log(error);
            }
            this.estimatesLoading = false;
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