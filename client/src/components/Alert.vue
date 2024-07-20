<template>
    <div class="alert" :class="success ? 'alert-success' : 'alert-danger'" v-if="isdisplayed">
        <span>{{ message }}</span>
        <button type="button" class="close" aria-label="Close" @click.prevent="dimiss">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>
</template>

<script>
export default{
    props: {
        visible: {
            type: Boolean,
            default: false
        },
        message: {
            type: String,
            default: 'Some test message'
        },
        success: {
            type: Boolean,
            default: true
        },
    },
    data(){
        return {
            isdisplayed: this.visible
        }
    },
    methods:{
        dismiss(){
            this.isdisplayed = false;
            this.$emit('dismissed')
        }
    }
}
</script>