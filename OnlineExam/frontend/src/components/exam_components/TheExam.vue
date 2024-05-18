<template>
    <div class="exam">
        <navbar-component page='Exam' :duration="examDur" @click-quit="clickQuit" />
        <div class="row">
        <base-card class="col col-md-auto">
            <div>
                <div v-if="Questions[displayedQ] !== undefined">
                    <question
                        :id="Questions[displayedQ]['id']"
                        :questionRefCode="Questions[displayedQ]['question_ref_code']"
                        :questionNo="displayedQ"
                        :question="Questions[displayedQ]['question_content']"
                        :isMarked="markedQuestions.includes(Questions[displayedQ]['question_ref_code'])"
                        :answers="answers()"
                        :givenAnswer="Questions[displayedQ].givenAnswer"
                        @update-answer="updateAnswer"
                        @mark-question="markQuestion"
                        @previous-question="prevQ"
                        @clear-answer="clearAnswer"
                    ></question>
                </div>
                <div class="container-fluid container-btn">
                    
                    <!-- <button v-if="displayedQ+1<Object.keys(Questions).length"
                     class="btn btn-info float-right butt" @click="NextQ">Next <span class="fa fa-hand-point-right">
                         </span>
                     </button> -->
                    <button v-if="displayedQ+1==Object.keys(Questions).length"
                     class="btn btn-danger float-right butt" @click="finishExam">Finish</button>
                </div>
            </div>
        </base-card>
        <!-- <div class="d-flex justify-content-center">
            <p>To navigate through the question click on:</p>
            <button @click="SwitchNav('open')" class="btn btn-sm btn-outline-info">Overview</button>
        </div> -->
        <div class="col col-md-auto t-container">
                <!-- <h3>Question List</h3>
                <p>Click on the box to go to the question</p> -->
            <question-navigator :Questions="Questions" :marked="markedQuestions" @go-to-question="goToQuestion"/>
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
        <div class="connection-status">
            <p>Connetion Status</p>
            <p> {{ isconnected[1] }}<span class="dot" :style="isconnected[0]"></span></p>
        </div>
        
    </div>
</template>

<script>
import Question from "./Question.vue";
import NavbarComponent from "../UI/Navbar.vue"
import { apiService, patchAxios } from "../../common/api.service";
import QuestionNavigator from './QuestionNavigator.vue';
import { useCookies } from "vue3-cookies";

export default {
    setup() {
        const { cookies } = useCookies();
        return { cookies };
    },


    components: {
        Question,
        QuestionNavigator,
        NavbarComponent,
    },
    data() {
        return {
            Questions: [],
            markedQuestions: [],
            displayedQ: 0,
            SessionId: '',
            Answers: {},
            UserFinish: false,
            NavigateQ: false,
            examDur: 0,
            remainingTime: null,
            questionsQue: {},
            isconnected: ['background-color: lightgreen;','Connected'],
            un_suc_attempts: 0,
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

        prevQ(Qid) {
            if (this.displayedQ > 0) {
                console.log(Qid)
                this.displayedQ--;
            }
        },

        NextQ() {
            const l = this.Questions.length;
            if (this.displayedQ < l - 1 && this.displayedQ >= 0) {
                this.displayedQ++;
            }
        },

        answersInCookies(Answers) {
            let data = {'answers':Answers, 'sesId':this.SessionId}
            this.cookies.set('Answers_'+this.SessionId, JSON.stringify(data))

        },

        updateAnswer(Qid, newAnswer) {
            const identQ = this.Questions.find(
                (question) => question.id === Qid
            );
            if (newAnswer != null) {
                identQ['givenAnswer'] = newAnswer;
                this.Answers[identQ.question_ref_code] = newAnswer;
                
                let data = {'answers':this.Answers, 'snapshot':this.questionsQue, 
                                'exam_remaining':parseInt(this.remainingTime/1000)};
                this.answersInCookies(this.Answers);
                let endpoint = "api/results/" + this.SessionId + '/';
                patchAxios(endpoint, data).then( response => {
                    if (response.data) {
                        console.log(response.data)
                    }
                    this.un_suc_attempts = 0;
                    this.isconnected = ['background-color: lightgreen;', 'Connected'];
                    console.log(this.un_suc_attempts);
                }).catch(e => {
                        console.log(e);
                        this.un_suc_attempts = this.un_suc_attempts+1;
                        if (this.un_suc_attempts > 3) {
                            this.isconnected=['background-color: red;', 'Disconnected'];
                        }
                        console.log(this.un_suc_attempts);
                    });
            }
            this.NextQ();
        },

        markQuestion(Qid) {
            const identQ = this.Questions.find(
                (question) => question.id === Qid
            );
            const index = this.markedQuestions.indexOf(identQ.question_ref_code)
            if (index > -1) {
                this.markedQuestions.splice(index, 1)

            }
            else {
                this.markedQuestions.push(identQ.question_ref_code)
            }

        },

        clearAnswer(Qid) {
            const id = this.Questions[this.displayedQ]['id'];
            if (id === Qid) {
                this.Questions[this.displayedQ].givenAnswer = null;
                this.Questions[this.displayedQ].givenAnswer = null;
                this.Answers[this.Questions[this.displayedQ].question_ref_code] = null;
                let data = {'answers':this.Answers, 'exam_remaining':parseInt(this.remainingTime/1000)};
                console.log(data);
                let endpoint = "api/results/" + this.SessionId + '/';
                patchAxios(endpoint, data).then( response => {
                    console.log(response.data);}).catch(e => {
                        console.log(e);
                    });
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
                if (this.Questions.length == 0) {
                    this.$router.push({
                        name: "Home",
                        params: {},
                    });
                }
                this.getAnswers()
            });
        },

        getAnswers() {
            let endpoint = 'api/results/' + this.SessionId +'/';
            apiService(endpoint).then((data) => {
                if (data['exam_duration']) {
                    this.examDur = data['exam_duration']*60000;
                    if (data['exam_remaining'] != null) {
                        this.examDur = data['exam_remaining']*1000;
                    }
                    this.remainingTime = this.examDur;
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
                this.Questions = this.shuffleQuestions(this.Questions);
                    
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
            this.cookies.remove('randomIndices');
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

        shuffleQuestions(qs) {
            let questions = qs;
            let loop = questions.length;
            let sorted_quests = [];
            let random_index = [];

            if (this.cookies.isKey('randomIndices')) {
                random_index = JSON.parse(this.cookies.get('randomIndices'));
                for (let i = 0; i < loop; i++) {

                    sorted_quests.push(questions[random_index[i]]);
                    let num = i+1;
                    this.questionsQue[num.toString()] = questions[random_index[i]].question_ref_code;
                    questions.splice(random_index[i], 1);
                }

            }
            else {
            
                for (let i = 0; i < loop; i++) {

                    let randomIndex = Math.floor(Math.random() * questions.length)
                    let num = i+1
                    sorted_quests.push(questions[randomIndex]);
                    this.questionsQue[num.toString()] = questions[randomIndex].question_ref_code ;
                    questions.splice(randomIndex, 1)
                    random_index.push(randomIndex)
                }

                this.cookies.set('randomIndices', JSON.stringify(random_index))
            }




            return sorted_quests

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
        console.log(this.cookies.isKey('randomIndices'));
        this.getQuestions()
        .then(setInterval(() => {
            if (this.remainingTime != null) {
                this.remainingTime = this.remainingTime - 1000;
                if (this.remainingTime <= 0) {

                    let data = {'answers':this.Answers, 'exam_remaining':0 };
                    console.log(data);
                    let endpoint = "api/results/" + this.SessionId + '/';
                    patchAxios(endpoint, data).then( response => {
                        console.log(response.data);
                        this.remainingTime = null;
                        }).catch(e => {
                        console.log(e);
                    });
                    this.cookies.remove('randomIndices');
                    this.$router.push({
                        name: "FinishPage",
                        params: { SessionId: this.SessionId }
                    });

                }
            }
            
        }, 1000))


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

.dot {
     height: 25px;
     width: 25px;
     border-radius: 50%;
     display: inline-block;
    margin-left: 40%;
}

.connection-status {
    border: solid 1px;
    position: fixed;
    bottom: 10px;
    right: 10px;
    padding:10px;
}

</style>