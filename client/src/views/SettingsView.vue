<template>
    <form>
        <div class="container">
            <Alert :visible="alert.show" :success="alert.success" :message="alert.message" @dismissed="alert.show=false"></Alert>
            <div v-if="isloading" class="col-12-sm text-center">
                <Spinner></Spinner>
            </div>
            <div v-else>
                <div class="row mb-3">
                    <div class="col">
                        <button type="button" class="btn btn-outline-success float-end" v-if="!issubmitting" @click="saveSettings()">
                            <i class="bi bi-floppy"></i>
                        </button>
                        <button v-else disabled type="button" class="btn btn-outline-success float-end">
                            Sending...
                        </button>
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col">
                        <div class="form-floating">
                            <input v-model.number="settings.printablehours" placeholder="Printable Hours" class="form-control" id="printablehours"/>
                            <label for="printablehours">Printable Hours</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <input v-model.number="settings.laborcost" placeholder="Labor Cost" class="form-control" id="laborcost"/>
                            <label for="laborcost">Labor Cost</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <input v-model.number="settings.kwhcost" placeholder="Kwh Cost" class="form-control" id="kwhcost"/>
                            <label for="kwhcost">Kwh Cost</label>
                        </div>
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col">
                        <div class="form-floating">
                            <input v-model.number="settings.printlabor" placeholder="Print Labor" class="form-control" id="printlabor"/>
                            <label for="printlabor">Print Labor</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <input v-model.number="settings.colorchangelabor" placeholder="Color Change Labor" class="form-control" id="colorchangelabor"/>
                            <label for="colorchangelabor">Color Change Labor</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <input v-model.number="settings.postprocessinglabor" placeholder="Post Processing Labor" class="form-control" id="postprocessinglabor"/>
                            <label for="postprocessinglabor">Post Processing Labor</label>
                        </div>
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col">
                        <div class="form-floating">
                            <input v-model.number="settings.materialmarkup" placeholder="Material Markup" class="form-control" id="materialmarkup"/>
                            <label for="materialmarkup">Material Markup</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <input v-model.number="settings.electricmarkup" placeholder="Electric Markup" class="form-control" id="electricmarkup"/>
                            <label for="electricmarkup">Electric Markup</label>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </form>
</template>

<script>
import { getSettings, saveSettings } from '@/estimater-api';

export default{
    data(){
        return {
            isloading: false,
            issubmitting: false,
            alert:{
                show: false,
                message: '',
                success: true
            },
            settings: {
                printablehours: 16,
                laborcost: 30,
                kwhcost: .018,
                printlabor: .01,
                colorchangelabor: .03,
                postprocessinglabor: .05
            }
        }
    },
    methods:{
        async loadSettings(){
            this.isloading = true;
            let response = await getSettings();
            if (response.success){
                this.settings = response.settings;
            }
            else{
                console.log(response.error);
            }
            this.isloading = false;
        },
        async saveSettings(){
            this.issubmitting = true;
            let response = await saveSettings(this.settings);
            if (response.success){
                this.showAlert('Successfully updated settings', true);
            }
            else{
                this.showAlert(response.error);
            }
            this.issubmitting = false;
        },
        showAlert(message, success = false){
            this.alert.message = message;
            this.alert.success = success;
            this.alert.show = true;
        }
    },
    mounted(){
        this.loadSettings();
    }
}
</script>