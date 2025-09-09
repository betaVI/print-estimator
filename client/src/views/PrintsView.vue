<template>
    <div class="container">
        <div class="row">
            <div class="col-md-8">
            </div>
            <div class="col-md-2">
                <h3>Total Profit:</h3>
            </div>
            <div class="col-md-2">
                <h3>${{ getTotalProfit() }}</h3>
            </div>
        </div>
        <ListView title="Prints" :isloading="isloading" @onaddclick="$router.push({ name: 'print' })">
            <template #headers>
                <tr>
                    <th scope="col">Date</th>
                    <th scope="col">Print</th>
                    <th scope="col">Customer</th>
                    <th scope="col">Price</th>
                    <th scope="col">Profit</th>
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
                    <td>{{ displayProfit(print) }}</td>
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
    </div>
</template>

<script>
import { getCustomers, getEstimates, getPrints, deletePrint } from '@/estimater-api';

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
            let response = await getCustomers();
            this.customers = response.customers;
            if (!response.success){
                console.log('Customers error: ' + response.error);
            }

            response = await getEstimates();
            this.estimates = response.estimates;
            if (!response.success){
                console.log('Estimates error: ' + response.error);
            }

            response = await getPrints();
            if (response.success){
                this.prints = response.prints;
                this.prints.sort(function(c1,c2) {return c1.createon < c2.createon })
            }
            else
            {
                console.log('Prints error: ' + response.error);
            }

            this.isloading = false;
        },
        displayCustomer(customerid){
            let customer = this.customers.find(c=>c.id == customerid);
            if (customer == null){
                return '?? (??)';
            }
            return `${customer.name} (${customer.description})`;
        },
        displayEstimate(estimateid){
            let estimate = this.estimates.find(e=>e.id == estimateid);
            if (estimate == null){
                return '?? (??/??)';
            }
            return `${estimate.name} ($${estimate.totalcostlabor}/$${estimate.minimumprice})`;
        },
        displayProfit(print){
            let estimate = this.estimates.find(e=>e.id == print.estimateid);
            if (estimate == null){
                return '$?.??'
            }
            let profit = print.price - estimate.totalcostlabor
            return `$${profit.toFixed(2)}`
        },
        getTotalProfit(){
            let total = this.estimates.reduce((prev,current)=>prev+=current.totalcostlabor,0);
            return total.toFixed(2);
        },
        async deletePrint(id){
            if (confirm('This action is permanent. Are you sure you want to continue?')){
                this.isloading = true;
                let response = await deletePrint(id);
                if (!response.success){
                    console.log(response.error);
                }
                this.loadPage();
                this.isloading = false;
            }
        }
    },
    mounted(){
        this.loadPage();
    }
}
</script>