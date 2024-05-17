<template>
<div class="finish">
    <navbar-component page="Finish" @check-remaining="CheckRemaining" />
    <div class="container">
        <base-card v-if="ExamNotFinished">
            <h3>Are you sure that you have finished and want to quit the exam?</h3>
            <menu>
                <div class="btn-group">
                    <button class="btn btn-primary btn-outline" @click="BacktoExam">Back to the Exam</button>
                    <button class="btn btn-danger btn-outline" @click="Quit">Finish the Exam</button>
                </div>

            </menu>
        </base-card>
        <base-card v-else>
            <h3> Your exam is finished </h3>
            <div v-if="score != null">
                <h1 class="d-inline">Your score is: </h1>
                <h1 class="d-inline badge-primary float-right" style="width:50%; text-align:center;">{{ score }} %</h1>
            </div>

        </base-card>
    </div>

</div>

    
</template>
<script>
import NavbarComponent from "../components/UI/Navbar.vue";
import BaseCard from "../components/UI/BaseCard.vue";
import { apiService, patchAxios } from "../common/api.service";
import { useCookies } from "vue3-cookies";

export default {

    setup() {
        const { cookies } = useCookies();
        return { cookies };
    },

    components: { BaseCard, NavbarComponent },
    name: "FinishePage",

    data() {
        return {
            SessionId: '',
            ExamNotFinished: true,
            score: null,
        };
    },

    methods: {
        BacktoExam() {
            this.$router.push({
                    name: "Exam",
                    params: { SessionId: this.SessionId },
                });
        },

        Quit() {
            let data = {'is_finished': true};
            let endpoint = "api/results/" + this.SessionId + "/";
            patchAxios(endpoint, data).then( response => {
                console.log(response);
                this.getResult()
            })
            this.ExamNotFinished = false                
                    

        },

        CheckRemaining() {
            let endpoint = "api/results/" + this.SessionId + "/";
            apiService(endpoint).then( data => {
                if ( data['exam_remaining']<=0 ) {
                    this.Quit();
                }
            }).catch(e => {
            console.log(e);})
            

        },

        getResult() {
            let endpoint = "api/results/" + this.SessionId + "/";
            apiService(endpoint).then( data => {
                if (data['show_score']) {
                    this.score = data['score'];
                    this.cookies.remove('Answers_'+this.SessionId);

                }
            }).catch(e => {
            console.log(e);})
        }

    },

    created() {
        this.SessionId = this.$route.params.SessionId;
        this.CheckRemaining();
    },
    
}
</script>
