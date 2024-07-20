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
import { sendRequest } from '@/utilities';

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
            try{
                let response = await sendRequest('/api/customers', 'GET');
                this.customers = response.customers;
            }
            catch(error){
                console.log(error)
            }
            this.isloading = false;
        },
        async deleteCustomer(id){
            try{
                let data = await sendRequest('/api/customers/'+ id, 'DELETE');
                if (!data.success){
                    console.log(error);
                }
                this.loadCustomers();
            }catch(error){
                console.log(error)
            }
        }
    },
    mounted(){
        this.loadCustomers()
    }
}
</script>