<template>
    <ListView title="Prints" :isloading="isloading" @onaddclick="$router.push({ name: 'print' })">
        <template #headers>
            <tr>
                <th scope="col">Date</th>
                <th scope="col">Print</th>
                <th scope="col">Customer</th>
                <th scope="col">Price</th>
                <th></th>
            </tr>
        </template>
        <template #default>
            <tr v-if="prints.length==0" class="text-center">
                <td colspan="5">No Records to display</td>
            </tr>
            <tr v-else v-for="(print,index) in prints" :keys="index">
                <td>{{ print.createon }}</td>
                <td>{{ displayEstimate(print.estimateid) }}</td>
                <td>{{ displayCustomer(print.customerid) }}</td>
                <td>{{ '$' + print.price.toFixed(2) }}</td>
                <td class="text-end">
                    <button type="button" class="btn btn-outline-info btn-sm mx-sm-1" @click="$router.push({ name: 'print', params: { id: print.id }})">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button type="button" class="btn btn-outline-danger btn-sm" @click="deletePrint(print.id)">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>
        </template>
    </ListView>
</template>

<script>
import { sendRequest } from '@/utilities';

export default {
    data(){
        return {
            isloading: false,
            prints: [],
            customers: [],
            estimates: [],
        }
    },
    methods:{
        async loadPage(){
            this.isloading = true;
            try{
                let data = await sendRequest('/api/customers', 'GET');
                this.customers = data.customers;

                data = await sendRequest('/api/estimates', 'GET');
                this.estimates = data.estimates;

                data = await sendRequest('/api/prints', 'GET');
                this.prints = data.prints;
                this.prints.sort(function(c1,c2) {return c1.createon < c2.createon })
            }catch(error){
                console.log(error);
            }
            this.isloading = false;
        },
        displayCustomer(customerid){
            let customer = this.customers.find(c=>c.id == customerid);
            return `${customer.name} (${customer.description})`;
        },
        displayEstimate(estimateid){
            let estimate = this.estimates.find(e=>e.id == estimateid);
            return `${estimate.name} ($${estimate.totalcostlabor}/$${estimate.minimumprice})`;
        },
        async deletePrint(id){
            this.isloading = true;
            try{
                let data = await sendRequest('/api/prints/' + id, 'DELETE');
                if (!data.success){
                    console.log(error);
                }
                this.loadPage();
            }catch(error){
                console.log(error);
            }
            this.isloading = false;
        }
    },
    mounted(){
        this.loadPage();
    }
}
</script>