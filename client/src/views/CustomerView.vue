
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
import { upsertCustomer, getCustomer } from '@/estimater-api';

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
                let response = await getCustomer(this.id);
                if (response.success){
                    this.customer = response.customer;
                }
                else{
                    console.log(response.error);
                }
                this.isloading = false;
            }
        },
        async submit(){
            this.issubmitting = true;
            var response = await upsertCustomer(this.id, this.customer);
            if (response.success){
                this.$router.back();
            }
            else {
                console.log(response.error);
            }
            this.issubmitting = false;
        }
    },
    mounted(){
        this.getCustomer();
    }
}
</script>