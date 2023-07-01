<template>
<div class="d-flex justify-content-center ">
    <div class="q-nav">
        <table class="table table-bordered">
            <tr v-for="row in tableHeight(Questions)" :key="row">
                <td v-for="col in tableLength(Questions)" :key="col"
                @click="goToQuestion(cellNumber(row, col, Questions))" :class="classColor(row, col, Questions, marked)">
                        {{ cellNumber(row, col, Questions) }}
                </td>
            </tr>
        </table>
    </div>
</div>
    
</template>

<script>
export default {
   

    props: ['Questions', 'marked'],


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
        
        classColor(r, c, qs, marked) {
            const n = this.cellNumber(r, c, qs);
            if (isNaN(n)) {
                return 'n-answered'
            }
            if (marked.includes(qs[n-1]['question_ref_code'])) {
                return 'marked'
            }
            if (isNaN(qs[n-1]['givenAnswer']) | qs[n-1]['givenAnswer'] == null) {
                return 'n-answered'
            }
            else {
                return 'answered'
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
    max-width: 2em;
}
</style>

<style scoped>

header {
    background-color: #3a0061;
    color: white;
    width: 100%;
    padding: 1rem;
}

section {
    padding: 1rem;
}

table, tr, td {
  border: 1px solid black;
  border-collapse: collapse;
  padding: 0.5rem;
}
</style>
<style scoped>
table {
    overflow: hidden;
}
</style>
<style scoped>
tr {
    line-height: 2px;
}
</style>
<style scoped>
td {
    width: 2px;
    cursor: pointer;
}
</style>
<style>
.answered {
    background-color: greenyellow;
}

.n-answered {
    background-color: #bfbfbf;
}

.marked {
    background-color: #ffc107;
}
</style>