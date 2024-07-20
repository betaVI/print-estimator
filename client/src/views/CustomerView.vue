
import Spinner from '@/components/Spinner.vue';
<template>
    <EditView :title="title" :isloading="isloading" :issubmitting="issubmitting" @onsubmit="submit()">
        <template #default>
            <div class="row">
                <div class="col">
                    <div class="form-floating">
                        <input v-model="customer.name" placeholder="Name" class="form-control" id="name"/>
                        <label for="name">Name</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-floating">
                        <input v-model="customer.description" placeholder="Description" class="form-control" id="description"/>
                        <label for="description">Description</label>
                    </div>
                </div>
            </div>
        </template>
    </EditView>
</template>

<script>
import { sendRequest } from '@/utilities';

export default {
    props:{
        id:{
            type: Number,
            default: 0
        }
    },
    data(){
        return {
            title: 'Add Customer',
            isloading: false,
            issubmitting: false,
            customer:{
                name: null,
                description: null,
            }
        }
    },
    methods:{
        async getCustomer(){
            this.title = 'Add Customer';
            if (this.id!=0){
                this.title = 'Edit Customer';
                this.isloading = true;
                try{
                    let data = await sendRequest('/api/customers/' + this.id, 'GET')
                    this.customer = data.customer;
                }
                catch(error){
                    console.log(error);
                }
                this.isloading = false;
            }
        },
        async submit(){
            this.issubmitting = true;
            let endpoint = '/api/customers'
            let method = 'POST'
            if (this.id != 0){
                endpoint += '/' + this.id;
                method = 'PATCH';
            }
            try{
                let data = await sendRequest(endpoint, method, this.customer);
                if (data.success){
                    this.$router.back();
                }
                else{
                    console.log(data.message)
                }
            }
            catch(error){
                console.log(error);
            }
            this.issubmitting = false;
        }
    },
    mounted(){
        this.getCustomer();
    }
}
</script>