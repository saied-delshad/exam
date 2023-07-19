<template>
  <base-card>
    <div v-if="givenAnswer != null" class="badge-success" >Answered</div>
    <div v-else-if="isMarked" class="badge-warning" >Marked</div>
    <div v-else class="badge-secondary">Not Answered</div>
    <form @submit.prevent="submitData">
      <div class="form-group">
        <div class="form-control">
          <h4 v-html=rectifiedQ(questionNo,question) align="justify" class="q-style"></h4>
        </div>
        <div v-for="(answer, ind) in answers" :key="ind" class="form-check">
          <input v-if="answer != null" :id="id + ind" :name="id+ ind" :value="ind" type="radio" class="form-check-input" v-model="yourAnswer" />
          <b>{{ choices[ind] }}. </b> <label :for="id + ind"  v-html=answer class="form-check-label"></label>
        </div>
        <div class="container-fluid container-btn">
          <button v-if="givenAnswer == null && ! isMarked" class="btn btn-warning" style="margin-left: 30%;" 
                                                                          type="submit" @click="markQuestion()">
            Mark Question <span class="fa fa-flag"></span></button>
          <button v-else-if="isMarked" class="btn btn-warning" style="margin-left: 30%;" type="submit" @click="markQuestion()">
            Un-Mark Question <span class="fa fa-close"></span></button>
          <button v-else class="btn btn-danger" style="margin-left: 30%;" type="submit" @click="clearAnswer()">
            Clear Answer <span class="fa fa-window-close"></span></button>
          <button class="btn btn-success float-right butt" @click="updateAnswer()">Next
            <span class="fa fa-share-square"></span>
          </button>
          <button v-if="questionNo>0" class="btn btn-info float-left butt" @click="previousQ()">
            <span class="fa fa-hand-point-left">
            </span> Previous</button>
        </div>
      </div>
    </form>
  </base-card>
</template>

<script>
export default {
  data() {
    return {
      inputIsInvalid: false,
      choices: ['A', 'B', 'C', 'D', 'E'],
      yourAnswer: this.givenAnswer
    };
  },
  props:['id', 'questionRefCode', 'questionNo', 'question', 'isMarked', 'answers', 'givenAnswer' ],

  emits: {
    'update-answer': function(id, yourAnswer) {
      if (yourAnswer >= 0) {
        return true;
      } else {
        return false;
      }
    },

    'mark-question': function(id) {
      if (id > 0) {
        return true;
      } else {
        return false;
      }

    },

    'previous-question': function(id) {
      if (id > 0) {
        return true;
      } else {
        return false;
      }

    },

    'clear-answer': function(id) {
      if (id > 0) {
        return true;
      } else {
        return false;
      }
    }
  },

  watch: {
    id() {
      this.yourAnswer = this.givenAnswer
    }
  },
  methods: {
    updateAnswer() {
      
      if (this.yourAnswer !== this.givenAnswer){
        this.$emit('update-answer', this.id, this.yourAnswer);
      }
      else {
        this.$emit('update-answer', this.id, null);
      }
    },

    markQuestion() {
      this.$emit('mark-question', this.id);
      
    },

    previousQ() {
      console.log('prev')
      this.$emit('previous-question', this.id);
      
    },

    clearAnswer() {
      this.yourAnswer = null;
      this.$emit('clear-answer', this.id);
    },

    rectifiedQ(questionNo, question) {
      const Num = questionNo + 1
      const q = question.replace(/(<p[^>]+?>|<p>|<\/p>)/img, "");
      return Num.toString() + '. ' + q

    }

  },
};
</script>

<style scoped>
label {
  font-weight: bold;
  margin-bottom: 0.5rem;
}

input {
  display: inline-block;
  font: inherit;
  padding: 0.15rem;
  border: 1px solid #ccc;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #3a0061;
  background-color: #f7ebff;
}

.form-control {
  margin: 1rem 0;
}

.q-style {
  color: black;

}
</style>