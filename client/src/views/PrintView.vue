<template>
    <EditView :title="title" :isloading="isloading" :issubmitting="issubmitting" @onsubmit="submit()">
        <template #default>
            <div class="row mb-3">
                <div class="col">
                    <div class="form-floating">
                        <select v-model="print.estimateid" class="form-select" id="estimate">
                            <option selected value="">Select an Estimate</option>
                            <option v-for="estimate in estimates" :value="estimate.id">{{ estimate.name }} (${{ estimate.totalcostlabor }}/${{ estimate.minimumprice }})</option>
                        </select>
                        <label for="estimate">Estimate</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-floating">
                        <select v-model="print.customerid" class="form-select">
                            <option selected value="">Select a Customer</option>
                            <option v-for="customer in customers" :value="customer.id">{{ customer.name }} ({{ customer.description }})</option>
                        </select>
                        <label for="customer">Customer</label>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col">
                    <div class="form-floating">
                        <input v-model.number="print.price" placeholder="Price" class="form-control" id="price"/>
                        <label for="price">Price</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-floating">
                        <input v-model="print.createon" placeholder="Date" type="date" class="form-control" id="date"/>
                        <label for="date">Date</label>
                    </div>
                </div>
            </div>
        </template>
    </EditView>
</template>

<script>
import { sendRequest } from '@/utilities';

export default{
    props:{
        id:{
            type: Number,
            default: 0
        }
    },
    data(){
        return {
            title: 'Add Print',
            isloading: false,
            issubmitting: false,
            customers:[],
            estimates:[],
            print:{
                customerid: "",
                estimateid: "",
                price: null,
            }
        }
    },
    methods: {
        async loadPage(){
            this.isloading = true;
            try{
                let data = await sendRequest('/api/estimates', 'GET');
                this.estimates = data.estimates;

                data = await sendRequest('/api/customers', 'GET');
                this.customers = data.customers;

                if (this.id!=0){
                    data = await sendRequest('/api/prints/' + this.id, 'GET');
                    this.print = data.print;
                }
            }catch(error){
                console.log(error);
            }
            this.isloading = false;
        },
        async submit(){
            this.issubmitting = true;
            try{
                if (this.id==0){
                    let data = await sendRequest('/api/prints', 'POST', this.print);
                    if (!data.success){
                        console.log(error);
                    }
                }
                else{
                    let data = await sendRequest('/api/prints/' + this.id, 'PATCH', this.print);
                    if (!data.success){
                        console.log(error)
                    }
                }
                this.$router.push({ name: 'prints' });
            }catch(error){
                console.log(error);
            }
            this.issubmitting = false;
        }
    },
    mounted(){
        this.loadPage();
    }
}
</script>