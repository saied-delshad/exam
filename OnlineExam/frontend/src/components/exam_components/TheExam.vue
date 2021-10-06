<template>
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
            <base-button @click="PrevQ">Previous Question</base-button>
            <base-button @click="NextQ">Next Question</base-button>
        </div>
    </base-card>
</template>

<script>
import Question from "./Question.vue";
import { apiService } from "../../common/api.service";

export default {
    components: {
        Question,
    },
    data() {
        return {
            Questions: [],
            displayedQ: 0,
            SessionId: '',
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
        },

        getQuestions() {
            let endpoint = "api/" + this.SessionId + "/questions/";
            apiService(endpoint).then((data) => {
                const midvar = [];
                midvar.push(...data);
                this.Questions = JSON.parse(JSON.stringify(midvar));
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