<template>
    <div class="modal fade">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <slot name="header">
                        <h3>Sample Header</h3>
                    </slot>
                </div>
                <div class="modal-body">
                    <slot>
                        Hello I am a modal
                    </slot>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" @click="$emit('cancelClick')" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" @click="$emit('confirmClick')">{{ confirmBtnContent }}</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default{
    props:{
        visible:{
            type: Boolean,
            default: false,
        },
        confirmBtnContent: {
            type: String,
            default: 'Save Changes'
        }
    },
    data(){
        return {
            isVisible: this.visible
        }
    },
    watch:{
        visible: function(newval, oldval){
            this.isVisible = newval;
            console.log('modal '+ (newval?'visible':'hidden'))
        }
    }
}
</script>