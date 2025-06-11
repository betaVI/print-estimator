<template>
    <div class="alert alert-dismissible" :class="success ? 'alert-success' : 'alert-danger'" v-if="isVisible">
        <span>{{ message }}</span>
        <button type="button" class="btn-close" aria-label="Close" @click="dismiss()"></button>
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
            isVisible: this.visible
        }
    },
    methods:{
        dismiss(){
            console.log('hello');
            this.isVisible = false;
            this.$emit('dismissed');
        }
    },
    watch:{
        visible: function(newval, oldval){
            this.isVisible = newval;
            console.log('alert '+ (newval?'visible':'hidden'))
        }
    }
}
</script>