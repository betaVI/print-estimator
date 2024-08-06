<template>
    <EditView :title="title" :isloading="isloading" :issubmitting="issubmitting" @onsubmit="saveEstimate()">
        <div class="row">
            <div class="col">
                <div class="form-floating">
                    <input v-model="estimate.name" placeholder="Name" class="form-control" id="name"/>
                    <label for="name">Name</label>
                </div>
            </div>
        </div>
        <hr class="hr"/>
        <div class="row mb-3">
            <div class="col">
                <div class="form-floating">
                    <input v-model.number="printablehours" placeholder="Printable Hours" class="form-control" id="printablehours"/>
                    <label for="printablehours">Printable Hours</label>
                </div>
            </div>
            <div class="col">
                <div class="form-floating">
                    <input v-model="laborcost" placeholder="Labor Cost" class="form-control" id="laborcost"/>
                    <label for="laborcost">Labor Cost</label>
                </div>
            </div>
            <div class="col">
                <div class="form-floating">
                    <input v-model="kwhcost" placeholder="Kwh Cost" class="form-control" id="kwhcost"/>
                    <label for="kwhcost">Kwh Cost</label>
                </div>
            </div>
        </div>
        <div class="row mb-3">
            <div class="col">
                <div class="form-floating">
                    <input v-model="printlabor" placeholder="Print Labor" class="form-control" id="printlabor"/>
                    <label for="printlabor">Print Labor</label>
                </div>
            </div>
            <div class="col">
                <div class="form-floating">
                    <input v-model="colorchangelabor" placeholder="Color Change Labor" class="form-control" id="colorchangelabor"/>
                    <label for="colorchangelabor">Color Change Labor</label>
                </div>
            </div>
            <div class="col">
                <div class="form-floating">
                    <input v-model="postprocessinglabor" placeholder="Post Processing Labor" class="form-control" id="postprocessinglabor"/>
                    <label for="postprocessinglabor">Post Processing Labor</label>
                </div>
            </div>
        </div>
        <hr class="hr"/>
        <div class="row mb-3">
            <div class="col">
                <h3>Models</h3>
            </div>
            <div class="col">
                <button type="button" class="btn btn-outline-primary btn-sm float-end" :disabled="issubmitting" @click="estimate.models.push({ postprocessing: false })">
                    <i class="bi bi-plus" style="font-size: 1.2em;"></i>
                </button>
            </div>
        </div>
        <div class="row px-2">
            <table class="table">
                <thead>
                    <tr>
                        <th scope="col" class="col-2">Name</th>
                        <th scope="col" class="col-1">Qty</th>
                        <th scope="col" class="col-1">Grams</th>
                        <th scope="col">Post</th>
                        <th scope="col" class="col-2">Minutes</th>
                        <th scope="col">Filament</th>
                        <th scope="col">Cost</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(model, index) in estimate.models" :keys="index" class="align-middle">
                        <td>
                            <!-- <FileImport v-model="model.file" class="form-control form-control-sm"></FileImport> -->
                            <input v-model.trim="model.name" type="text" class="form-control form-control-sm"/>
                        </td>
                        <td>
                            <input v-model.number="model.quantity" type="text" class="form-control form-control-sm"/>
                        </td>
                        <td>
                            <input v-model.number="model.grams" type="text" class="form-control form-control-sm"/>
                        </td>
                        <td class="text-center">
                            <input v-model="model.postprocessing" type="checkbox" class="form-check-input"/>
                        </td>
                        <td>
                            <input v-model.number="model.minutes" type="text" class="form-control form-control-sm"/>
                        </td>
                        <td>
                            <select v-model="model.filamentid" class="form-select form-select-sm">
                                <option v-for="filament in filaments" :value="filament.id">{{ getFilamentName(filament.id) }}</option>
                            </select>
                        </td>
                        <td>{{ getModelCost(model) }}</td>
                        <td class="text-end">
                            <button :disabled="issubmitting" type="button" class="btn btn-outline-danger btn-sm" @click="estimate.models.splice(index,1)">
                                <i class="bi bi-trash"></i>
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
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
            title: 'Add Estimate',
            isloading: false,
            issubmitting: false,
            filaments:[],
            estimate:{
                name: null,
                models:[]
            },
            filamentcost: .02,
            kwhcost: .018,
            printablehours: 16,
            printlabor: .01,
            colorchangelabor: .03,
            postprocessinglabor: .05,
            laborcost: 30,
        }
    },
    methods:{
        async loadFilaments(){
            try{
                let data = await sendRequest('/api/filaments', 'GET');
                this.filaments = data.filaments.filter(f=>f.isactive);
            }catch(error){
                console.log(error);
            }
        },
        async loadEstimate(){
            this.title = 'Add Estimate';
            if (this.id !=0){
                this.title = 'Edit Estimate';
                this.isloading = true;
                try{
                    let data = await sendRequest('/api/estimates/' + this.id, 'GET');
                    this.estimate = data.estimate;
                    if (!this.estimate.models){
                        this.estimate.models = []
                    }
                }
                catch(error){
                    console.log(error);
                }
                this.isloading = false;
            }
        },
        async saveEstimate(){
            this.issubmitting = true;
            let endpoint = '/api/estimates';
            let method = 'POST'
            if (this.id != 0){
                endpoint += '/' + this.id;
                method = 'PATCH';
            }
            try{
                this.estimate.models = this.removeEmptyModels(this.estimate.models);
                let data = await sendRequest(endpoint, method, this.estimate);
                if (data.success){
                    this.$router.back();
                }
                else{
                    console.log(error);
                }
            }catch(error){
                console.log(error);
            }
            this.issubmitting = false;
        },
        getFilamentName(id){
            let filament = this.filaments.find(f=>f.id == id);
            return `${filament.name} ${filament.type} ${filament.color} ($${filament.cost})`;
        },
        getModelCost(model){
            if (model==null || model.filamentid == undefined){
                return "???";
            }
            let filament = this.filaments.find(f=>f.id == model.filamentid);
            if (filament == null){
                return "???";
            }
            let costpergram = filament.cost / filament.grams;
            return '$' + (costpergram * model.quantity * model.grams).toFixed(2);
        },
        removeEmptyModels(models){
            return models.filter(m => m.name && m.quantity && m.grams && m.minutes && m.filamentid);
        }
    },
    mounted(){
        this.loadFilaments();
        this.loadEstimate();
    }
}
</script>