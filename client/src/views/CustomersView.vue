<template>
    <ListView title="Customers" :isloading="isloading" @onaddclick="$router.push({ name: 'customer' })">
        <template #headers>
            <tr>
                <th scope="col">Name</th>
                <th scope="col">Description</th>
                <th></th>
            </tr>
        </template>
        <template #default>
            <tr v-if="customers.length==0" class="text-center">
                <td colspan="3">No Records to display</td>
            </tr>
            <tr v-else v-for="(customer,index) in customers" :keys="index">
                <td>{{ customer.name }}</td>
                <td>{{ customer.description }}</td>
                <td class="text-end">
                    <button type="button" class="btn btn-outline-info btn-sm mx-sm-1" @click="$router.push({ name: 'customer', params: { id: customer.id }})">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button type="button" class="btn btn-outline-danger btn-sm" @click="deleteCustomer(customer.id)">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>
        </template>
    </ListView>
</template>

<script>
import { getCustomers, deleteCustomer } from '@/estimater-api';

export default {
    data(){
        return {
            isloading: false,
            customers: []
        }
    },
    methods:{
        async loadCustomers(){
            this.isloading = true;
            let response = await getCustomers();
            if (response.success){
                this.customers = response.customers;
            }
            else{
                console.log(response.error);
            }
            this.isloading = false;
        },
        async deleteCustomer(id){
            if (confirm('This action is permanent. Are you sure you want to continue?')){
                let response = await deleteCustomer(id);
                if (!data.success){
                    console.log(response.error);
                }
                this.loadCustomers();
            }
        }
    },
    mounted(){
        this.loadCustomers()
    }
}
</script>