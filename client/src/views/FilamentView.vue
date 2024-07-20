<template>
    <EditView :title="title" :isloading="isloading" :issubmitting="issubmitting" @onsubmit="saveFilament()">
        <template #default>
            <div class="row">
                <div class="col">
                    <div class="form-floating">
                        <input v-model="filament.name" placeholder="Name" class="form-control" id="name"/>
                        <label for="name">Name</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-floating">
                        <input v-model="filament.type" placeholder="Type" class="form-control" id="type"/>
                        <label for="type">Type</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-floating">
                        <input v-model="filament.color" placeholder="Color" class="form-control" id="color"/>
                        <label for="color">Color</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-check">
                        <input type="checkbox" v-model="filament.isactive" class="form-check-input" id="isactive"/>
                        <label class="form-check-label" for="isactive">Active</label>
                    </div>
                </div>
            </div>
            <hr class="hr"/>
            <div class="row mb-3">
                <div class="col">
                    <div class="form-floating">
                        <input v-model.number="filament.cost" placeholder="Cost" class="form-control" id="cost"/>
                        <label for="cost">Cost</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-floating">
                        <input v-model="filament.grams" placeholder="Grams" class="form-control" id="grams"/>
                        <label for="grams">Total Grams</label>
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
        return{
            title: 'Add Filament',
            isloading: false,
            issubmitting: false,
            alert: {
                show: false,
                success: true,
                message: 'Success'
            },
            filament:{
                name: null,
                isactive: true,
                type: null,
                color: null,
                cost: null,
                grams: null
            }
        }
    },
    methods:{
        async loadFilament(){
            this.title = 'Add Filament';
            if (this.id!=0){
                this.title = 'Edit Filament';
                this.isloading = true;
                try{
                    let data = await sendRequest('/api/filaments/' + this.id, 'GET');
                    this.filament = data.filament;
                }catch(error){
                    console.log(error);
                    this.showAlert(error, false);
                }
                this.isloading = false;
            }
        },
        async saveFilament(){
            this.issubmitting = true;
            if(this.id!=0){
                try{
                    let data = await sendRequest('/api/filaments/' + this.id, 'PATCH', this.filament)
                    if (data.success){
                        this.$router.push({ name: 'filaments' });
                    }
                    else{
                        this.showAlert(data.message, false);
                    }
                }
                catch(error){
                    console.log(error);
                    this.showAlert(error, false);
                }
            }
            else{
                try{
                    let data = await sendRequest('/api/filaments','POST', this.filament)
                    if (data.success){
                        this.$router.push({ name: 'filaments' });
                    }
                    else{
                        this.showAlert(data.message, false);
                    }
                }
                catch(error){
                    console.log(error);
                    this.showAlert(error, false);
                }
            }
            this.issubmitting = false;
        },
        showAlert(message, success=true){
            alert.show = true;
            alert.success = success;
            alert.message = message;
        }
    },
    mounted(){
        this.loadFilament();
    }
}
</script>