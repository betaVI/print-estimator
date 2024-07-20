
import Spinner from '@/components/Spinner.vue';
<template>
    <form>
        <div class="container">
            <div v-if="isloading" class="col-12-sm text-center">
                <Spinner></Spinner>
            </div>
            <div v-else>
                <div class="row mb-3">
                    <div class="col">
                        <button type="button" class="btn btn-outline-secondary" :disabled="issubmitting" @click="$router.back()">
                            <i class="bi bi-arrow-left"></i>
                        </button>
                    </div>
                    <h1 class="col">{{ title }}</h1>
                    <div class="col">
                        <button type="button" class="btn btn-outline-success float-end" v-if="!issubmitting" @click="$emit('onsubmit')">
                            <i class="bi bi-floppy"></i>
                        </button>
                        <button v-else disabled type="button" class="btn btn-outline-success float-end">
                            Sending...
                        </button>
                    </div>
                </div>
                <slot>
                    Enter form fields here
                </slot>
            </div>
        </div>
    </form>
</template>

<script>
export default {
    emits: [ 'onsubmit' ],
    props: {
        title: {
            type: String,
            default: 'Test Title'
        },
        isloading: {
            type: Boolean,
            default: true
        },
        issubmitting: {
            type: Boolean,
            default: true
        },
    }
}
</script>