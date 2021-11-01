<template>
<div class="d-flex justify-content-center">
    <div class="q-nav row align-items-center">
        <table class="table table-bordered">
            <tr v-for="row in tableHeight(Questions)" :key="row">
                <td v-for="col in tableLength(Questions)" :key="col"
                @click="goToQuestion(cellNumber(row, col, Questions))" :class="classColor(row, col, Questions)">
                        {{ cellNumber(row, col, Questions) }}
                </td>
            </tr>
        </table>
    </div>
</div>
    
</template>

<script>
export default {
   

    props: ['Questions'],

    // emits: {
    // 'go-to-question'
    // }

    methods: {
        length(qs) {
            return qs.length
        },

        cellNumber(r, c, qs) {
            const n = c + (r-1)*this.tableLength(qs)
            if (n <= this.length(qs)) {
                return n
            }
            else {
                return '-'
            }
        },

        tableLength(qs) {
            const l = Math.floor(Math.sqrt(qs.length));
            if (l <= 1) {
                return 2
            }
            return l 
        },

        tableHeight(qs) {
            const h = Math.floor( this.length(qs) / this.tableLength(qs) ) 
            if (this.length(qs) % this.tableLength(qs) == 0) {
                return h;
            }
            else {
                return h + 1
            }
            },
        
        classColor(r, c, qs) {
            const n = this.cellNumber(r, c, qs);
            if (isNaN(n)) {
                return 'n-answered'
            }
            if (qs[n-1]['givenAnswer']) {
                return 'answered'
            }
            else {
                return 'n-answered'
            }
        },
        goToQuestion(num) {
            this.$emit('go-to-question', num);
        }
        },

    }
</script>

<style scoped>
.q-nav {
    min-height: 5em;
    max-width: 50%;
}

table, tr, td {
  border: 1px solid black;
  border-collapse: collapse;
}

table {
    overflow: hidden;
}

tr {
    line-height: 10px;
}

td {
    width: 5px;
    cursor: pointer;
}
.answered {
    background-color: greenyellow;
}
.n-answered {
    background-color: gray;
}
</style>