<template>
    <div class="exam">
        <navbar-component page='Exam' @click-quit="clickQuit"/>
        <base-card>
            <div>
                <div v-if="Questions[displayedQ] !== undefined">
                    <question
                        :id="Questions[displayedQ]['id']"
                        :questionRefCode="Questions[displayedQ]['question_ref_code']"
                        :questionNo="displayedQ"
                        :question="Questions[displayedQ]['question_content']"
                        :answers="answers()"
                        :givenAnswer="Questions[displayedQ].givenAnswer"
                        @update-answer="updateAnswer"
                    ></question>
                </div>
                <div class="container-fluid container-btn">
                    <button v-if="displayedQ>0" class="btn btn-info float-left butt" @click="PrevQ">Previous Question</button>
                    <button v-if="displayedQ+1<Object.keys(Questions).length" class="btn btn-info float-right butt" @click="NextQ">Next Question</button>
                </div>
            </div>
        </base-card>
    </div>
    <base-dialog v-if="UserFinish" title="Quit the exam!">
        <template #default>
            <p> Are you sure? </p>
            <p> You will quit the exam and will not be able to continue </p>
        </template>
        <template #actions>
            <base-button @click="BackToExam" class="btn btn-sm btn-primary">Back to Exam </base-button>
            <base-button @click="Quit" class="btn btn-sm btn-danger">Quit the Exam</base-button>
        </template>
    </base-dialog>
</template>

<script>
import Question from "./Question.vue";
import NavbarComponent from "../UI/Navbar.vue"
import { apiService, patchAxios } from "../../common/api.service";
import BaseDialog from '../UI/BaseDialog.vue';

export default {
    components: {
        Question,
        NavbarComponent,
        BaseDialog,
    },
    data() {
        return {
            Questions: [],
            displayedQ: 0,
            SessionId: '',
            Answers: {},
            UserFinish: false
        };
    },
    provide() {
        return {
            examQuestions: this.Questions,
        };
    },

    methods: {

        answers() {
            const answers = [];
            for (var i = 1; i <= 4; i++) {
                const opt = this.Questions[this.displayedQ]['opt_'+i]
                if (opt !== '') {
                    answers.push(opt)
                }
            }
            return answers
        },

        PrevQ() {
            if (this.displayedQ > 0) {
                this.displayedQ--;
            }
        },

        NextQ() {
            const l = this.Questions.length;
            if (this.displayedQ < l - 1 && this.displayedQ >= 0) {
                this.displayedQ++;
            }
        },

        updateAnswer(Qid, newAnswer) {
            const identQ = this.Questions.find(
                (question) => question.id === Qid
            );
            identQ['givenAnswer'] = newAnswer;
            this.Answers[identQ.question_ref_code] = newAnswer;
            let data = {'answers':this.Answers}
            let endpoint = "api/results/" + this.SessionId + '/';
            patchAxios(endpoint, data).then( response => {
                console.log(response.data);}).catch(e => {
                    console.log(e);
                });
        },

        getQuestions() {
            let endpoint = "api/" + this.SessionId + "/questions/";
            apiService(endpoint).then((data) => {
                const midvar = [];
                midvar.push(...data);
                this.Questions = JSON.parse(JSON.stringify(midvar));
            });
        },

        clickQuit() {
            this.UserFinish = true;
        },

        BackToExam() {
            this.UserFinish = false;
        },

        Quit() {
            let data = {'is_finished': true};
            let endpoint = "api/results/" + this.SessionId + "/";
            patchAxios(endpoint, data).then( response => {
                console.log(response.data);}).catch(e => {
                    console.log(e);
                });
        },

        // removeResource(resId) {
        //   const resIndex = this.storedResources.findIndex(res => res.id === resId);
        //   this.storedResources.splice(resIndex, 1);
        // },
    },

    created() {
        this.SessionId = this.$route.params.SessionId;
    },

    mounted() {
        this.getQuestions();
    },
};
</script>

<style scoped>
.container-btn {
    height: 50px;
}

.butt {
    margin-top: 10px;
}
</style>