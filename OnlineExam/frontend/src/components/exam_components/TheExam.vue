<template>
    <div class="exam">
        <navbar-component page='Exam' :duration="examDur" @click-quit="clickQuit" />
        <div class="row">
        <base-card class="col-xs-6">
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
                    <button v-if="displayedQ>0" class="btn btn-info float-left butt" @click="PrevQ">
                        <span class="fa fa-hand-point-left">
                         </span> Previous</button>
                    <button v-if="displayedQ+1<Object.keys(Questions).length"
                     class="btn btn-info float-right butt" @click="NextQ">Next <span class="fa fa-hand-point-right">
                         </span>
                     </button>
                    <button v-if="displayedQ+1==Object.keys(Questions).length"
                     class="btn btn-danger float-right butt" @click="finishExam">Finish</button>
                </div>
            </div>
        </base-card>
        <!-- <div class="d-flex justify-content-center">
            <p>To navigate through the question click on:</p>
            <button @click="SwitchNav('open')" class="btn btn-sm btn-outline-info">Overview</button>
        </div> -->
        <div class="col-xs-6 t-container">
                <!-- <h3>Question List</h3>
                <p>Click on the box to go to the question</p> -->
            <question-navigator :Questions="Questions" @go-to-question="goToQuestion"/>
                <!-- <button @click="SwitchNav('close')" class="btn btn-sm btn-primary">Close
                </button> -->
        
        </div>
        </div>
        <base-dialog v-if="UserFinish" title="Quit the exam!">
            <template #default>
                <p> Are you sure? </p>
                <p> You will quit the exam and will not be able to continue </p>
            </template>
            <template #actions>
                <div class="btn-group">
                    <button @click="BackToExam" class="btn btn-sm btn-success">Back to Exam </button>
                    <button @click="finishExam" class="btn btn-sm btn-danger">Quit the Exam</button>
                </div>
            </template>
        </base-dialog>
    </div>
</template>

<script>
import Question from "./Question.vue";
import NavbarComponent from "../UI/Navbar.vue"
import { apiService, patchAxios } from "../../common/api.service";
import QuestionNavigator from './QuestionNavigator.vue';

export default {
    components: {
        Question,
        QuestionNavigator,
        NavbarComponent,
    },
    data() {
        return {
            Questions: [],
            displayedQ: 0,
            SessionId: '',
            Answers: {},
            UserFinish: false,
            NavigateQ: false,
            examDur: 0
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

        updateAnswer(Qid, newAnswer, arg) {
            const identQ = this.Questions.find(
                (question) => question.id === Qid
            );
            identQ['givenAnswer'] = newAnswer;
            this.Answers[identQ.question_ref_code] = newAnswer;
            let data = {'answers':this.Answers};
            console.log(data);
            let endpoint = "api/results/" + this.SessionId + '/';
            patchAxios(endpoint, data).then( response => {
                console.log(response.data);}).catch(e => {
                    console.log(e);
                });
            if (arg=='next') {
                this.NextQ();
            }
        },

        goToQuestion(qnum) {
            this.displayedQ = qnum - 1;
            this.NavigateQ = false;

        },

        async getQuestions() {
            let endpoint = "api/" + this.SessionId + "/questions/";
            apiService(endpoint).then((data) => {
                console.log(data)
                const midvar = [];
                midvar.push(...data);
                this.Questions = JSON.parse(JSON.stringify(midvar));
                this.getAnswers()
            });
        },

        getAnswers() {
            let endpoint = 'api/results/' + this.SessionId +'/';
            apiService(endpoint).then((data) => {
                if (data['exam_duration']) {
                    this.examDur = data['exam_duration'];
                }
                if (data['answers'] != null && Object.keys(this.Questions).length >0 ){
                    this.Answers = data['answers'];
                    console.log(data)
                    for (var key of Object.keys(this.Answers)) {
                        const q = this.Questions.find(
                            (question) => question.question_ref_code === key
                        )
                        q['givenAnswer'] = this.Answers[key];

                    }
                }
            })
        },

        clickQuit() {
            this.UserFinish = true;
        },

        BackToExam() {
            this.UserFinish = false;
        },

        Quit() {
            this.finishExam();
        },

        finishExam() {
            this.$router.push({
                    name: "FinishPage",
                    params: { SessionId: this.SessionId },
                });
        }, 
        SwitchNav(action) {
            if (action == "open") {
                this.NavigateQ = true;
            } else {
                this.NavigateQ = false;
            }

        },

        startCallBack: function(x) {
            console.log(x);
        },
        endCallBack: function(x) {
            console.log(x);
        },

    },

    created() {
        
        this.SessionId = this.$route.params.SessionId;
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

.t-container {
    margin-top:20%;
}
</style>