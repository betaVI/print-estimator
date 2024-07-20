<template>
    <ListView title="Filaments" :isloading="isloading" @onaddclick="$router.push({name:'filament'})">
        <template #headers>
            <tr>
                <th scope="col">Name</th>
                <th scope="col">Active</th>
                <th scope="col">Type</th>
                <th scope="col">Color</th>
                <th scope="col">Cost</th>
                <th scope="col">Grams</th>
                <th scope="col">$/g</th>
                <th></th>
            </tr>
        </template>
        <template #default>
            <tr v-if="filaments.length==0" class="text-center">
                <td colspan="8">No Records to display</td>
            </tr>
            <tr v-for="(filament, index) in filaments" :keys="index">
                <td>{{ filament.name }}</td>
                <td><i class="bi bi-check-lg" v-if="filament.isactive"></i></td>
                <td>{{ filament.type }}</td>
                <td>{{ filament.color }}</td>
                <td>{{ filament.cost }}</td>
                <td>{{ filament.grams }}</td>
                <td>{{ (filament.cost / filament.grams).toFixed(3) }}</td>
                <td class="text-end">
                    <button type="button" class="btn btn-outline-info btn-sm mx-sm-1" @click="$router.push({ name: 'filament', params: { id: filament.id }})">Edit</button>
                    <button type="button" class="btn btn-outline-danger btn-sm" @click="deleteFilament(filament.id)">Delete</button>
                </td>
            </tr>
        </template>
    </ListView>
</template>

<script>
import { sendRequest } from '@/utilities'

export default{
    data(){
        return{
            isloading: false,
            filaments:[],
            filamentid: 0,
            filament:{
                name: null,
                cost: 19.99,
                grams: 1000
            }
        }
    },
    methods:{
        async getFilaments(){
            this.isloading = true;
            try{
                let data = await sendRequest('/api/filaments', 'GET');
                this.filaments = data.filaments;
            }catch(error){
                console.log(error);
            }
            this.isloading = false;
        },
        async deleteFilament(id){
            try{
                let data = await sendRequest('/api/filaments/' + id, 'DELETE')
                if (!data.success){
                    console.log(error);
                }
                this.getFilaments()
            }catch(error){
                console.log(error);
            }
        }
    },
    mounted(){
        this.getFilaments();
    }
}
</script>