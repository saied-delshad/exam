<template>
  <base-card>
    <div v-if="givenAnswer != null" class="badge-success" >Answered</div>
    <div v-else class="badge-secondary">Not Answered</div>
    <form @submit.prevent="submitData">
      <div class="form-group">
        <div class="form-control">
          <h4 v-html=rectifiedQ(questionNo,question)></h4>
        </div>
        <div v-for="(answer, ind) in answers" :key="ind" class="form-check">
          <input v-if="answer != null" :id="id + ind" :name="id+ ind" :value="ind" type="radio" class="form-check-input" v-model="yourAnswer" />
          <label :for="id + ind"  v-html=answer class="form-check-label"></label>
        </div>
        <div class="container-fluid container-btn">
          <button class="btn btn-success" type="submit" @click="updateAnswer('')">
            Save answer <span class="fa fa-check-circle"></span></button>
          <button class="btn btn-success float-right butt" @click="updateAnswer('next')">Save and Next
            <span class="fa fa-share-square"></span>
          </button>
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
      yourAnswer: this.givenAnswer
    };
  },
  props:['id', 'questionRefCode', 'questionNo', 'question', 'answers', 'givenAnswer' ],

  emits: {
    'update-answer': function(id, yourAnswer) {
      if (yourAnswer >= 0) {
        return true;
      } else {
        console.log("empty answer!!")
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
    updateAnswer(arg) {
      
      if (this.yourAnswer !== this.givenAnswer){
        if (arg=='next') {
          this.$emit('update-answer', this.id, this.yourAnswer, arg);
        }
        else{
          this.$emit('update-answer', this.id, this.yourAnswer);
        }
      }
    },

    rectifiedQ(questionNo, question) {
      const Num = questionNo + 1
      const q = question.replace(/(<p[^>]+?>|<p>|<\/p>)/img, "");
      return '#' + Num.toString() + '. ' + q

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
</style>