<template>
    <EditView :title="title" :isloading="isloading" :issubmitting="issubmitting" @onsubmit="submit()">
        <template #default>
            <div class="row mb-3">
                <div class="col">
                    <div class="form-floating">
                        <select v-model="print.estimateid" class="form-select" id="estimate" @change="displaySpoolSelection">
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
            <hr class="hr"/>
            <div class="row w-75 mx-auto mb-3" v-for="filament in spoolSelection">
                <div class="col text-end my-auto">
                    {{ filament.name }}
                </div>
                <div class="col">
                    <select class="form-select">
                        <option v-for="spool in spools.filter(s=>s.filament.id == filament.id)" :value="spool.id">#{{ spool.id }} {{ spool.filament.vendor.name }} {{ spool.filament.name }} {{ spool.filament.material }} ${{ spool.price / spool.initial_weight }} ({{ spool.remaining_weight.toFixed(0) }}g left)</option>
                    </select>
                </div>
            </div>
        </template>
    </EditView>
</template>

<script>
import { upsertPrint, getEstimates, getEstimate, getCustomers, getPrint } from '@/estimater-api';
import { getSpools, getFilaments } from '@/spoolman-api';

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
            filaments:[],
            spools:[],
            spoolSelection:[],
            print:{
                customerid: "",
                estimateid: "",
                price: null,
                spools:[]
            }
        }
    },
    methods: {
        async loadPage(){
            this.isloading = true;
            let response = await getEstimates();
            if (response.success){
                this.estimates = response.estimates;
            }

            response = await getCustomers();
            if (response.success){
                this.customers = response.customers;
            }

            response = await getSpools();
            if (response.success){
                this.spools = response.spools;
            }

            response = await getFilaments();
            if (response.success){
                this.filaments = response.filaments;
            }

            if (this.id != 0){
                response = await getPrint(this.id);
                if (response.success){
                    this.print = response.print;
                    this.displaySpoolSelection(null);
                }
                else{
                    console.log(response.error);
                }
            }
            this.isloading = false;
        },
        async submit(){
            this.issubmitting = true;
            let response = await upsertPrint(this.id, this.print);
            if (response.success){
                this.$router.push({ name: 'prints' });
            }
            else{
                console.log(response.error);
            }
            this.issubmitting = false;
        },
        async displaySpoolSelection(event){
            let response = await getEstimate(this.print.estimateid);
            if (!response.success){
                console.log(response.error);
                return;
            }

            let filamentsused = [...new Set(response.estimate.models.map(m=>m.filamentid))];
            this.spoolSelection = filamentsused.map(id=>{
                let filament = this.filaments.find(f=>f.id == id);
                return {
                    id: id,
                    name: `${filament.vendor.name} ${filament.material} ${filament.name}`
                }
            })
        }
    },
    mounted(){
        this.loadPage();
    }
}
</script>