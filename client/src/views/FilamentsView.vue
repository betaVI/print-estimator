<template>
    <ListView title="Filaments" :isloading="isloading" @onaddclick="$router.push({name:'filament'})">
        <template #headers>
            <tr>
                <th scope="col">Vendor</th>
                <th scope="col">Color</th>
                <th scope="col">Name</th>
                <th scope="col">Material</th>
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
                <td>{{ filament.vendor.name }}</td>
                <td>
                    <div v-if="filament.color_hex" class="badge d-inline" :style="{ 'background-color': '#' + filament.color_hex }"></div>
                    <div v-else v-for="hex in filament.multi_color_hexes.split(',')" class="badge d-block w-25" :style="{ 'background-color': '#' + hex }"></div>
                </td>
                <td>{{ filament.name }}</td>
                <td>{{ filament.material }}</td>
                <td>{{ filament.price }}</td>
                <td>{{ filament.weight }}</td>
                <td>{{ (filament.price / filament.weight).toFixed(3) }}</td>
                <td class="text-end">
                    <button type="button" class="btn btn-outline-info btn-sm mx-sm-1" @click="$router.push({ name: 'filament', params: { id: filament.id }})">
                        <i class="bi bi-pencil"></i>
                    </button>
                </td>
            </tr>
        </template>
    </ListView>
</template>

<script>
import { getFilaments } from '@/spoolman-api';

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
            let response = await getFilaments();
            if (response.success){
                this.filaments = response.filaments;
            }else{
                console.log(response.error);
            }
            this.isloading = false;
        }
    },
    mounted(){
        this.getFilaments();
    }
}
</script>