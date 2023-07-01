<template>
    <span style="margin-right:10px;" :class="{'blinking' : finishing}"> {{ output }} </span>
    
</template>

<script>
export default {
    data() {
        return {
            remainingTime: 0,
            finishing: false,
        }
    },

    emits: {

        'remaining-time': function(remainingTime) {
            return remainingTime > 0
        }

    },

    props: ['exam_dur'],

    methods: {

        calcRemaining() {
            console.log(this.remainingTime)
            var vm = this;
            var x = setInterval(function() {
                vm.remainingTime = vm.remainingTime - 1000;

                if (vm.remainingTime <= 15000) {
                    console.log(vm.remainingTime)
                    vm.finishing = true
                }

                if (vm.remainingTime < 0) {
                    clearInterval(x);
                }

            }, 1000)
        }
    },

    computed: {
        output: function() {
            var h = Math.floor(this.remainingTime/(1000*60*60));
            var m = Math.floor((this.remainingTime % (1000 * 60 * 60)) / (1000 * 60));
            var s = Math.floor((this.remainingTime % (1000 * 60)) / (1000));
            if (this.remainingTime < 0) {
                
                return "FINISHED";
                
            }
            return h + " : " + m + " : " + s;

        },


    },


    mounted() {
        this.remainingTime = this.exam_dur;
        setTimeout(() => {  this.calcRemaining(); }, 1000);

    },
}
</script>

<style scoped>

.blinking {
    color:red;
    animation: blinker 1s linear infinite;
}

@keyframes blinker {
  50% {
    opacity: 0;
  }
}

</style>