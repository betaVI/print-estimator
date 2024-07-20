<template>
    <div class="container">
        <div class="row">
            <h1 class="col-sm-11 float-start">{{ title }}</h1>
            <div class="col-sm-1 text-center float-end">
                <button class="btn btn-outline-success btn-sm float-end" @click="$emit('onaddclick')">Add</button>
            </div>
        </div>
        <div v-if="isloading" class="col-sm-12 text-center">
            <Spinner></Spinner>
        </div>
        <table v-else class="table table-hover">
            <thead>
                <slot name="headers">
                    <tr>
                        <th scope="col">Name</th>
                        <th scope="col">Age</th>
                        <th></th>
                    </tr>
                </slot>
            </thead>
            <tbody>
                <slot name="default">
                    <tr>
                        <td>Brian</td>
                        <td>39</td>
                    </tr>
                </slot>
            </tbody>
        </table>
    </div>
</template>

<script>
export default {
    props: {
        title: {
            type: String,
            default: 'Test Title'
        },
        isloading: {
            type: Boolean,
            default: true
        }
    }
}
</script>